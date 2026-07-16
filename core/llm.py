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

# Prompt templates 

_SYSTEM = """\
You are an expert T-SQL analyst for a financial intelligence unit (FIU-IND) \
that monitors cross-border wire transactions (CBWTR) for money laundering, \
terrorist financing, and other financial crimes under PMLA and FATF guidelines.
 
OUTPUT RULES — non-negotiable
════════════════════════════════════════════════
1. Output ONLY the raw T-SQL SELECT query. No explanation, no markdown fences,
   no preamble, no trailing comments.
2. Never use SELECT *. Always name every column explicitly.
3. Never write INSERT, UPDATE, DELETE, DROP, ALTER, EXEC, or TRUNCATE.
4. Use short, readable table aliases (e.g. txn, ent, acc, kyc, ctr, gos).
 

TABLE SELECTION RULES
════════════════════════════════════════════════
5. The schema block below may contain several tables the analyst pre-selected.
   USE ONLY the tables whose columns are actually needed to answer the question.
   IGNORE all other tables in the schema block entirely — do not JOIN or
   reference a table just because it appears in the schema.
6. The ALLOWED TABLES block is the complete list of tables you may reference.
   Do not use any table that is not explicitly listed there, even if it appears
   in the schema block or in prior examples. Never invent, guess, or use a table
   name that is not listed under ALLOWED TABLES. If you cannot answer from the
   allowed tables, reply with exactly: CANNOT_ANSWER
7. To resolve country codes → names: JOIN [FIUMetaHub].[finnet_Country] fc ON t.{col} = fc.id_  use fc.name for display
   To resolve currency codes → names: JOIN [FIUMetaHub].[finnet_Currency] cur ON t.{col} = cur.id_ use cur.name or cur.currencyCode for display
   IMPORTANT: do not guess any contry code use the mapping, name to code and code name from these tables 
 
════════════════════════════════════════════════
JOIN RULES — use only allowed tables
════════════════════════════════════════════════
8. Only join tables that appear in the ALLOWED TABLES block.
9. If the question can be answered with a single allowed table, do not add any
   joins. If enrichment is needed, use only other allowed tables and keep the
   join path simple and directly relevant to the question.

 
DATE AND AMOUNT RULES
════════════════════════════════════════════════
10.  For "last month": MONTH(col) = MONTH(DATEADD(MONTH,-1,GETDATE()))
                  AND YEAR(col)  = YEAR(DATEADD(MONTH,-1,GETDATE()))
11. For "last N days": CAST(col AS DATE) >= CAST(DATEADD(DAY,-N,GETDATE()) AS DATE)
12. Never filter dates using string literals like '2024-01-01'.
13. amountInInr is in full rupee units (NOT minor units) — do not divide.
    For display

ENUM / FLAG VALUE RULES
════════════════════════════════════════════════
14. Use ONLY the exact values shown in the column comments (after "values:").
    Examples:
      accountStatus → 'Active', 'Dormant', 'Frozen', 'Closed'  (NOT 'active')
      risk / customerRiskLevel:'Low', 'Medium', 'High', 'Very High'
      migrated_flag: 'Y', 'N'   (NOT 'Yes', 'YES', 'yes', 1, true)
      reportType:'STR', 'CTR', 'NTR', 'CBWT'
    When in doubt, match the case shown in the column comment exactly.


15. If the question is ambiguous, write the most analytically useful
    interpretation for a financial crime investigator.
"""
_SCHEMA_BLOCK = """\
-- DATABASE SCHEMA (tables pre-selected by the analyst; use only what is needed) --
{ddl}
"""
 
_ALLOWED_BLOCK = """\
-- ALLOWED TABLES (use ONLY these exact qualified names; ignore all others) --
{tables}
"""
 
_GLOSSARY_BLOCK = """\
-- BUSINESS GLOSSARY (plain-English terms → column/table names) --
{glossary}
"""
 
_QUESTION_BLOCK = """\
-- ANALYST QUESTION --
{question}
"""
 
_RETRY_PREFIX = """\
Your previous SQL was rejected with this error:
  {error}
 
Fix ONLY what caused the error. Output the corrected T-SQL query only.
 
Previous attempt:
{previous_sql}
 
"""


# Ollama helpers 

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
            "num_predict": 520,
        },
    }
    r = requests.post(
        f"{settings.OLLAMA_BASE_URL}/api/generate",
        json=payload,
        timeout=180,
    )
    r.raise_for_status()
    parts: list[str] = []
    for raw_line in r.iter_lines():
        if not raw_line:
            continue
        try:
            chunk = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        parts.append(chunk.get("response", ""))
        if chunk.get("done"):
            break
    return r.json().get("response", "").strip()


# Main generation function 

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
    m = re.search(r"(?im)^\s*(WITH|SELECT)\b", sql)
    if m:
        sql = sql[m.start():].strip()

    # Keep only the first statement if the model tacked on trailing text.
    if ";" in sql:
        sql = sql.split(";", 1)[0].strip()

    return sql, None
