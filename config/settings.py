import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ───────────────────────────────────────────────────────────────────────
# No live database. Each table is loaded from a spreadsheet in DATA_DIR/excel
# and queried locally with DuckDB.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR     = Path(os.getenv("DATA_DIR", str(PROJECT_ROOT / "data")))
EXCEL_DIR    = Path(os.getenv("EXCEL_DIR", str(DATA_DIR / "excel")))

# ── Ollama ────────────────────────────────────────────────────────────────────
OLLAMA_BASE_URL    = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL       = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")

# ── Safety ────────────────────────────────────────────────────────────────────
MAX_ROWS           = int(os.getenv("MAX_ROWS", "500"))
SQL_TIMEOUT        = int(os.getenv("SQL_TIMEOUT_SECONDS", "30"))
MAX_RETRIES        = 2
