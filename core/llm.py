"""
NL → SQL via Ollama (Qwen 2.5 Coder).

Two public functions:
  generate_sql(question, ddl_context, glossary, history) → (sql, error)
  check_ollama()                                          → (ok, message)
"""

from __future__ import annotations
import re
import json
import requests
from config import settings

# ── Prompt templates ──────────────────────────────────────────────────────────

_SYSTEM = """\
You are an expert Microsoft SQL Server (T-SQL) query writer for a \
cross-border wire transaction (CBWT) financial intelligence database.

STRICT RULES — follow every one, no exceptions:
1. Output ONLY the raw T-SQL SELECT query. No explanation, no markdown fences, \
no preamble, no comments unless asked.
2. Never use SELECT *. Always name columns explicitly.
3. Never write INSERT, UPDATE, DELETE, DROP, ALTER, EXEC, or TRUNCATE.
4. Use table aliases (e.g. t, txn, snd) to keep queries readable.
5. For date filtering use CAST(col AS DATE) comparisons or DATEADD/DATEDIFF \
— never string literals for dates.
6. When the user asks for "last month" use:
   MONTH(col) = MONTH(DATEADD(MONTH,-1,GETDATE()))
   AND YEAR(col)  = YEAR(DATEADD(MONTH,-1,GETDATE()))
7. Monetary amounts in this database are stored in minor units \
(divide by 100.0 to get the display value) UNLESS the column name \
ends in _USD or _AMT_DC, which are already in major units.
8. If the question is ambiguous, write the most reasonable interpretation.
9. Use ONLY the exact table names listed under ALLOWED TABLES. NEVER invent, \
guess, or use placeholder table names such as YOUR_TABLE, your_transaction_table, \
table_name, transactions, or any name not in that list.
10. If none of the ALLOWED TABLES can answer the question, reply with exactly: \
CANNOT_ANSWER (do not substitute a made-up table to force an answer).
"""

_SCHEMA_BLOCK = """\
-- DATABASE SCHEMA (only the tables relevant to this question) --
{ddl}
"""

_ALLOWED_BLOCK = """\
-- ALLOWED TABLES (use ONLY these exact names; inventing any other is an error) --
{tables}
"""

_GLOSSARY_BLOCK = """\
-- BUSINESS GLOSSARY (map plain-English terms → column/table names) --
{glossary}
"""

_QUESTION_BLOCK = """\
-- USER QUESTION --
{question}
"""

_RETRY_PREFIX = """\
The previous SQL you generated was rejected with this error:
  {error}

Fix ONLY what caused the error. Output the corrected T-SQL query only.

Previous attempt:
{previous_sql}

"""


# ── Ollama helpers ────────────────────────────────────────────────────────────

def check_ollama() -> tuple[bool, str]:
    """Return (True, model_name) if Ollama is reachable and the model is pulled."""
    try:
        r = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
        r.raise_for_status()
        models = [m["name"] for m in r.json().get("models", [])]
        target = settings.OLLAMA_MODEL
        # Accept partial match (e.g. "qwen2.5-coder:7b" matches "qwen2.5-coder:7b-instruct-q4_K_M")
        matched = next((m for m in models if m.startswith(target.split(":")[0])), None)
        if matched:
            return True, matched
        return False, (
            f"Model '{target}' not found. Available: {models}. "
            f"Run: ollama pull {target}"
        )
    except requests.exceptions.ConnectionError:
        return False, (
            f"Cannot reach Ollama at {settings.OLLAMA_BASE_URL}. "
            "Is Ollama running? Try: ollama serve"
        )
    except Exception as exc:
        return False, str(exc)


def _call_ollama(prompt: str) -> str:
    """Send a single prompt to Ollama and return the raw text response."""
    payload = {
        "model":  settings.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.0,   # deterministic for SQL
            "num_predict": 512,
        },
    }
    r = requests.post(
        f"{settings.OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=120,
    )
    r.raise_for_status()
    return r.json().get("response", "").strip()


# ── Main generation function ──────────────────────────────────────────────────

def generate_sql(
    question: str,
    ddl_context: str,
    glossary: str = "",
    allowed_tables: list[str] | None = None,
    previous_sql: str = "",
    previous_error: str = "",
) -> tuple[str | None, str | None]:
    """
    Generate T-SQL for *question* given the provided schema context.

    Parameters
    ----------
    allowed_tables  Exact (qualified) table names the model may reference.
                    Listed explicitly in the prompt to stop placeholder names.

    Returns
    -------
    (sql, None)       on success
    (None, error_msg) if model returns CANNOT_ANSWER or an error occurs
    """
    parts = [_SYSTEM]

    if ddl_context:
        parts.append(_SCHEMA_BLOCK.format(ddl=ddl_context))

    if allowed_tables:
        parts.append(_ALLOWED_BLOCK.format(
            tables="\n".join(f"  {t}" for t in allowed_tables)
        ))

    if glossary:
        parts.append(_GLOSSARY_BLOCK.format(glossary=glossary))

    if previous_sql and previous_error:
        parts.append(_RETRY_PREFIX.format(
            error=previous_error,
            previous_sql=previous_sql,
        ))

    parts.append(_QUESTION_BLOCK.format(question=question))

    full_prompt = "\n".join(parts)

    try:
        raw = _call_ollama(full_prompt)
    except Exception as exc:
        return None, f"Ollama request failed: {exc}"

    if not raw:
        return None, "Model returned an empty response."

    if "CANNOT_ANSWER" in raw.upper():
        return None, (
            "The model could not answer this question from the available schema. "
            "Try selecting more tables or rephrasing."
        )

    # Strip any accidental markdown fences
    sql = re.sub(r"^```(?:sql)?\s*", "", raw, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql).strip()

    # The model sometimes prepends a sentence of explanation despite the rules.
    # Stray prose (e.g. an apostrophe in "haven't") breaks the tokenizer, so trim
    # everything before the first line that starts with SELECT or WITH.
    m = re.search(r"(?im)^\s*(WITH|SELECT)\b", sql)
    if m:
        sql = sql[m.start():].strip()

    # Keep only the first statement if the model tacked on trailing text.
    if ";" in sql:
        sql = sql.split(";", 1)[0].strip()

    return sql, None
