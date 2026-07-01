"""
Converts the static schema dict into CREATE TABLE DDL stubs for the LLM prompt.
"""

from __future__ import annotations


def schema_to_ddl(
    schema: dict[str, list[dict]],
    tables: list[str] | None = None,
    inline_comments: dict[str, str] | None = None,
    schema_qualifier: str | None = None,           # kept for compat; ignored when qualifier_fn set
    qualifier_fn=None,                             # callable: table_name → qualifier string
) -> str:
    """
    Parameters
    ----------
    schema            Raw schema dict {table: [col_defs]}.
    tables            Subset of tables to render. None → all.
    inline_comments   {table.column: "alias"} rendered as SQL inline comments.
    schema_qualifier  Single qualifier string (legacy, used if qualifier_fn is None).
    qualifier_fn      Callable(table_name) → qualifier string (takes precedence).
    """
    inline_comments = inline_comments or {}
    target_tables = tables if tables is not None else list(schema.keys())

    blocks: list[str] = []
    for tbl in target_tables:
        cols = schema.get(tbl)
        if not cols:
            continue

        if qualifier_fn is not None:
            q = qualifier_fn(tbl)
            qualified = f"[{q}].[{tbl}]"
        elif schema_qualifier:
            qualified = f"[{schema_qualifier}].[{tbl}]"
        else:
            qualified = f"[{tbl}]"

        lines: list[str] = []
        for col in cols:
            name     = col["column"]
            dtype    = col["type"]
            nullable = "NULL" if col["nullable"] == "YES" else "NOT NULL"
            comment  = inline_comments.get(f"{tbl}.{name}", "")
            suffix   = f"  -- {comment}" if comment else ""
            lines.append(f"    [{name}]{'':<2}{dtype:<15} {nullable}{suffix}")

        body = ",\n".join(lines)
        blocks.append(f"CREATE TABLE {qualified} (\n{body}\n);")

    return "\n\n".join(blocks)


def schema_summary(schema: dict[str, list[dict]]) -> str:
    rows = []
    for tbl, cols in schema.items():
        col_names = ", ".join(c["column"] for c in cols[:8])
        ellipsis  = f", … +{len(cols) - 8} more" if len(cols) > 8 else ""
        rows.append(f"  {tbl} ({len(cols)} cols): {col_names}{ellipsis}")
    return "\n".join(rows)