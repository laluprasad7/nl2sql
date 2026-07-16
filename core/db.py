"""
Local query engine — DuckDB over spreadsheets (no live database).

Each table lives as a spreadsheet in settings.EXCEL_DIR, named after the table
(e.g. fingate_CbwtrBank.xlsx). At startup we build an in-memory DuckDB with two
schemas (FINCORE_BRIDGE, FIUMetaHub) and load every spreadsheet into the schema
its table belongs to (per static_schema.TABLE_QUALIFIERS).

The LLM still writes Microsoft T-SQL; run_query() transpiles it to DuckDB with
sqlglot before executing, so `SELECT TOP 10 ... FROM [FINCORE_BRIDGE].[t]`
becomes `SELECT ... FROM FINCORE_BRIDGE.t LIMIT 10`.

Public API:
    run_query(sql)   -> (DataFrame, None) | (None, error_message)
    load_report()    -> list of per-table load results (for the UI)
    reload()         -> rebuild the in-memory DB from disk
"""

from __future__ import annotations

import logging
from pathlib import Path

import duckdb
import pandas as pd
import sqlglot
import sqlglot.expressions as exp

from config import settings
from core import static_schema

log = logging.getLogger(__name__)

# Extensions we try when locating a table's file, in priority order.
_EXTENSIONS = (".xlsx", ".xlsm", ".xls", ".csv")

# Defense-in-depth: validator.py is the primary gate, but never let a
# non-SELECT statement reach the engine.
_BLOCKED_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE",
    "MERGE", "GRANT", "REVOKE", "ATTACH", "DETACH", "COPY", "INSTALL",
    "LOAD", "PRAGMA", "CALL", "EXPORT", "IMPORT", "SET",
}

# ── Module-level singletons (one in-memory DB per process) ──────────────────────
_CONN: duckdb.DuckDBPyConnection | None = None
_LOAD_REPORT: list[dict] | None = None


# ══════════════════════════════════════════════════════════════════════════════
#  Loading spreadsheets into DuckDB
# ══════════════════════════════════════════════════════════════════════════════

def _find_file(table: str) -> Path | None:
    """Locate the spreadsheet for *table* (case-insensitive name match)."""
    excel_dir: Path = settings.EXCEL_DIR
    if not excel_dir.exists():
        return None
    for ext in _EXTENSIONS:
        # exact-case first, then case-insensitive scan
        exact = excel_dir / f"{table}{ext}"
        if exact.exists():
            return exact
    lowered = {p.stem.lower() + p.suffix.lower(): p for p in excel_dir.iterdir() if p.is_file()}
    for ext in _EXTENSIONS:
        hit = lowered.get(f"{table.lower()}{ext}")
        if hit:
            return hit
    return None


def _read_file(path: Path) -> pd.DataFrame:
    """Read a spreadsheet/CSV into a DataFrame (first sheet for workbooks)."""
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    return pd.read_excel(path, sheet_name=0)


def _build_connection() -> tuple[duckdb.DuckDBPyConnection, list[dict]]:
    """Create an in-memory DuckDB, load every known table, return (conn, report)."""
    con = duckdb.connect(database=":memory:")

    schemas = {static_schema.get_qualifier(t) for t in static_schema.get_all_tables()}
    for sch in schemas:
        con.execute(f'CREATE SCHEMA IF NOT EXISTS "{sch}"')

    report: list[dict] = []
    for table in static_schema.get_all_tables():
        sch = static_schema.get_qualifier(table)
        path = _find_file(table)
        entry = {"table": table, "schema": sch, "file": None, "rows": 0, "error": None}

        if path is None:
            entry["error"] = "no file found"
            report.append(entry)
            log.warning("No spreadsheet found for table %s in %s", table, settings.EXCEL_DIR)
            continue

        entry["file"] = path.name
        try:
            df = _read_file(path)
            con.register("_load_tmp", df)
            con.execute(
                f'CREATE OR REPLACE TABLE "{sch}"."{table}" AS SELECT * FROM _load_tmp'
            )
            con.unregister("_load_tmp")
            entry["rows"] = len(df)
            log.info("Loaded %s.%s (%d rows) from %s", sch, table, len(df), path.name)
        except Exception as exc:  # noqa: BLE001 — surface any load failure per-table
            entry["error"] = str(exc)
            log.exception("Failed loading %s from %s", table, path)

        report.append(entry)

    # Let unqualified table references resolve against both schemas.
    search_path = ",".join(f"{s}" for s in schemas) + ",main"
    try:
        con.execute(f"SET search_path = '{search_path}'")
    except Exception:  # noqa: BLE001
        pass

    return con, report


def get_connection() -> duckdb.DuckDBPyConnection:
    """Return the process-wide DuckDB connection, building it on first use."""
    global _CONN, _LOAD_REPORT
    if _CONN is None:
        _CONN, _LOAD_REPORT = _build_connection()
    return _CONN


def reload() -> list[dict]:
    """Tear down and rebuild the in-memory DB from disk. Returns the load report."""
    global _CONN, _LOAD_REPORT
    if _CONN is not None:
        try:
            _CONN.close()
        except Exception:  # noqa: BLE001
            pass
    _CONN, _LOAD_REPORT = None, None
    get_connection()
    return _LOAD_REPORT or []


def load_report() -> list[dict]:
    """Per-table load results: [{table, schema, file, rows, error}, ...]."""
    get_connection()
    return _LOAD_REPORT or []


###################
#  Query execution
###################

def _ensure_limit(duck_sql: str) -> str:
    """Append LIMIT settings.MAX_ROWS to the outer query if none is present."""
    try:
        expr = sqlglot.parse_one(duck_sql, read="duckdb")
    except Exception:  # noqa: BLE001 — if we can't parse, run as-is
        return duck_sql
    if expr is None:
        return duck_sql
    if expr.args.get("limit") is None and isinstance(expr, (exp.Select, exp.Union, exp.Subquery)):
        expr = expr.limit(settings.MAX_ROWS)
        return expr.sql(dialect="duckdb")
    return duck_sql


def run_query(sql: str) -> tuple[pd.DataFrame | None, str | None]:
    """
    Transpile T-SQL → DuckDB and execute. Returns (DataFrame, None) on success
    or (None, error_message) on failure. Caps rows at settings.MAX_ROWS.
    """
    if not sql or not sql.strip():
        return None, "Empty query."

    # Defense-in-depth keyword guard (validator is the primary gate).
    tokens = set(sql.upper().replace("(", " ").replace(")", " ").split())
    blocked = tokens & _BLOCKED_KEYWORDS
    if blocked:
        return None, f"Blocked: statement contains disallowed keyword '{sorted(blocked)[0]}'."

    # T-SQL (what the model wrote) → DuckDB.
    try:
        transpiled = sqlglot.transpile(sql, read="tsql", write="duckdb")
    except Exception as exc:  # noqa: BLE001
        return None, f"Could not translate query to DuckDB: {exc}"
    if not transpiled:
        return None, "Query produced no executable statement after translation."

    duck_sql = _ensure_limit(transpiled[0])

    try:
        con = get_connection()
        df = con.execute(duck_sql).fetchdf()
        return df, None
    except Exception as exc:  # noqa: BLE001 — error text feeds the retry loop
        return None, str(exc)
