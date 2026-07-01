"""
pipeline.run_query_pipeline(question, selected_tables)
→ PipelineResult

Schema and glossary are pulled from static_schema — no DB schema fetch needed.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import pandas as pd

from config import settings
from core.llm import generate_sql
from core.validator import validate_sql, clean_sql
from core.schema import schema_to_ddl
from core import static_schema
from core import db


@dataclass
class PipelineResult:
    question:          str
    sql:               str | None          = None
    dataframe:         pd.DataFrame | None = None
    error:             str | None          = None
    attempts:          int                 = 0
    validation_errors: list[str]           = field(default_factory=list)


def run_query_pipeline(
    question: str,
    selected_tables: list[str],
    extra_glossary: str = "",
) -> PipelineResult:
    """
    Parameters
    ----------
    question         Natural language question from the analyst.
    selected_tables  Tables chosen in the UI (subset of static_schema.SCHEMA).
    extra_glossary   Any additional glossary text the analyst typed in the UI.
    """
    result = PipelineResult(question=question)

    # Build DDL with inline alias comments from metadata
    inline_comments: dict[str, str] = {}
    for tbl in selected_tables:
        inline_comments.update(static_schema.get_inline_comments(tbl))

    ddl_context = schema_to_ddl(
        static_schema.SCHEMA,
        tables=selected_tables,
        inline_comments=inline_comments,
        qualifier_fn=static_schema.get_qualifier,
    )

    # Auto-generated glossary from metadata + any analyst additions.
    # Scope it to the selected tables so the model can't reference tables that
    # aren't in the provided DDL / allowlist.
    auto_glossary = static_schema.build_glossary_block(selected_tables)
    glossary = auto_glossary
    if extra_glossary.strip():
        glossary += f"\n\n-- ANALYST ADDITIONS --\n{extra_glossary.strip()}"

    allowed_tables    = set(selected_tables)
    qualified_tables  = [static_schema.get_qualified_table(t) for t in selected_tables]
    previous_sql      = ""
    previous_error    = ""

    for attempt in range(1, settings.MAX_RETRIES + 2):
        result.attempts = attempt

        sql, gen_error = generate_sql(
            question=question,
            ddl_context=ddl_context,
            glossary=glossary,
            allowed_tables=qualified_tables,
            previous_sql=previous_sql,
            previous_error=previous_error,
        )

        if gen_error:
            result.error = gen_error
            return result

        is_valid, val_error = validate_sql(sql, allowed_tables=allowed_tables)

        if not is_valid:
            result.validation_errors.append(f"Attempt {attempt}: {val_error}")
            previous_sql, previous_error = sql, val_error
            continue

        clean = clean_sql(sql)
        result.sql = clean

        df, exec_error = db.run_query(clean)

        if exec_error:
            if attempt <= settings.MAX_RETRIES:
                result.validation_errors.append(f"Attempt {attempt} (DB): {exec_error}")
                previous_sql, previous_error = clean, exec_error
                continue
            result.error = f"Database error after {attempt} attempts: {exec_error}"
            return result

        result.dataframe = df
        return result

    result.error = (
        f"Could not generate a valid query after {settings.MAX_RETRIES + 1} attempts. "
        f"Tip: make sure the table(s) your question is about are selected in the "
        f"sidebar (e.g. fingate_CbwtrBank for transactions).\n"
        + "\n".join(result.validation_errors)
    )
    return result