"""
Lightweight SQL validation using sqlglot (no DB round-trip needed).
Returns (is_valid: bool, error: str | None).
"""

from __future__ import annotations
import re
import sqlglot
import sqlglot.expressions as exp


# Keywords that must never appear in analyst queries.
# Includes T-SQL write/DDL verbs plus DuckDB-specific statements that could
# read/write the filesystem or load extensions (ATTACH, COPY, INSTALL, …).
_BLOCKED_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
    "TRUNCATE", "CREATE", "EXEC", "EXECUTE", "GRANT",
    "REVOKE", "MERGE", "BULK",
    "ATTACH", "DETACH", "COPY", "INSTALL", "LOAD",
    "PRAGMA", "CALL", "EXPORT", "IMPORT",
}


def validate_sql(
    sql: str,
    allowed_tables: set[str] | None = None,
) -> tuple[bool, str | None]:
    """
    Parameters
    ----------
    sql            Raw SQL string from the model.
    allowed_tables Set of table names the query is allowed to reference.
                   None → skip table allowlist check.

    Returns
    -------
    (True, None)          → safe to run
    (False, error_msg)    → blocked; error_msg explains why
    """
    if not sql or not sql.strip():
        return False, "Model returned an empty response."

    sql = sql.strip()

    # ── 1. Strip markdown fences the model might wrap around the SQL ──────────
    sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)
    sql = sql.strip()

    # ── 2. Keyword blocklist (fast, pre-parse) ────────────────────────────────
    tokens = set(re.findall(r"\b[A-Z_]+\b", sql.upper()))
    blocked = tokens & _BLOCKED_KEYWORDS
    if blocked:
        return False, f"Query contains disallowed keyword(s): {', '.join(sorted(blocked))}."

    # ── 3. Parse with sqlglot (T-SQL dialect) ────────────────────────────────
    # Catch the SqlglotError base class — covers ParseError *and* TokenError
    # (e.g. an unbalanced quote from stray prose), so a malformed model output
    # becomes a clean rejection the retry loop can handle instead of a crash.
    try:
        statements = sqlglot.parse(sql, dialect="tsql")
    except sqlglot.errors.SqlglotError as exc:
        first_line = str(exc).strip().splitlines()[0] if str(exc).strip() else "could not tokenize SQL"
        return False, f"SQL syntax error: {first_line}"

    if not statements:
        return False, "Could not parse any SQL statement."

    if len(statements) > 1:
        return False, "Only single-statement queries are allowed."

    parsed = statements[0]

    # ── 4. Must be a SELECT ───────────────────────────────────────────────────
    if not isinstance(parsed, exp.Select):
        kind = type(parsed).__name__
        return False, f"Only SELECT statements are allowed (got {kind})."

    # ── 5. Table allowlist ────────────────────────────────────────────────────
    if allowed_tables is not None:
        # CTE names (WITH foo AS …) appear as table references but are virtual,
        # so exclude them from the allowlist check.
        cte_names = {
            c.alias_or_name.upper()
            for c in parsed.find_all(exp.CTE)
            if c.alias_or_name
        }
        referenced = {
            t.name.upper()
            for t in parsed.find_all(exp.Table)
            if t.name
        }
        disallowed = referenced - {t.upper() for t in allowed_tables} - cte_names
        if disallowed:
            return False, (
                f"Query references table(s) not in the provided schema: "
                f"{', '.join(sorted(disallowed))}. "
                f"Use ONLY these tables: {', '.join(sorted(allowed_tables))}."
            )

    return True, None


def clean_sql(sql: str) -> str:
    """Strip markdown fences and normalise whitespace — use before execution."""
    sql = re.sub(r"^```(?:sql)?\s*", "", sql.strip(), flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)
    return sql.strip()
