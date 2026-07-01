# CBWT Query Studio — NL2SQL Tool

Ask questions in plain English and get answers from your cross-border wire
transaction (CBWT) data. A local LLM writes the SQL, it's validated and executed
against your spreadsheets with DuckDB, and results come back as a table.

- **No GPU required** — everything runs on CPU.
- **No live database required** — tables are read from Excel/CSV files on disk.
- **Runs fully offline after setup** — once the model and embeddings are
  downloaded, no internet or external service is needed.

---

## How it works

```
   Plain-English question
            │
            ▼
   ┌──────────────────┐   selected tables →  DDL + glossary + allowed-tables list
   │  Qwen 2.5 Coder  │   ───────────────────────────────────────────────────►
   │   (Ollama, CPU)  │   ◄─────────────────────  Microsoft T-SQL
   └──────────────────┘
            │
            ▼
   ┌──────────────────┐   SELECT-only? allowed tables? single statement?
   │   Validator      │   (sqlglot, T-SQL dialect + keyword blocklist)
   └──────────────────┘
            │  valid
            ▼
   ┌──────────────────┐   T-SQL ─► DuckDB (sqlglot transpile), LIMIT injected
   │  DuckDB engine   │   runs against tables loaded from data/excel
   └──────────────────┘
            │
            ▼
      Results table  (CSV download, numeric summary)
```

Extras:
- **Semantic table suggestions** — as you type, an embedding index (MiniLM +
  ChromaDB) suggests the most relevant tables for your question.
- **Retry loop** — if a query fails validation or execution, the exact error is
  fed back to the model for a corrected attempt.
- The model writes **Microsoft T-SQL** (Qwen-Coder is strong at it); every query
  is transpiled to DuckDB before running. This is intentional — see
  [Design notes](#design-notes).

---

## Requirements

| Requirement | Details |
|---|---|
| **OS** | Windows 10/11, macOS, or Linux |
| **Python** | 3.10 or newer (developed on 3.13) |
| **RAM** | 8 GB minimum; 16 GB recommended (the 7B model uses ~5–6 GB) |
| **Disk** | ~7 GB free: Ollama model ~4.7 GB, Python deps (incl. PyTorch CPU) ~1.5 GB, embedding model ~90 MB |
| **GPU** | Not required |
| **Internet** | Needed **once** during setup (to pull the Ollama model, install pip packages, and download the embedding model). Not needed afterward. |
| **Ollama** | Installed and running, with `qwen2.5-coder:7b` pulled |

Python packages (installed via `requirements.txt`):

```
streamlit              # web UI
duckdb                 # local SQL engine over spreadsheets
openpyxl               # read .xlsx files
sqlglot                # SQL validation + T-SQL→DuckDB transpilation
pandas                 # dataframes
requests               # talk to Ollama
python-dotenv          # load .env
chromadb               # vector store for table suggestions
sentence-transformers  # embedding model (pulls PyTorch CPU build)
```

---

## Setup on a fresh machine

### 1. Install Python 3.10+

- **Windows**: download from https://www.python.org/downloads/ and tick
  *"Add Python to PATH"* during install.
- **macOS**: `brew install python@3.12`
- **Linux (Debian/Ubuntu)**: `sudo apt install python3 python3-venv python3-pip`

Verify: `python --version` (or `python3 --version`).

### 2. Install Ollama and pull the model

Ollama runs the LLM locally.

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows — download the installer from https://ollama.com/download
```

Then pull the model and start the server:

```bash
ollama pull qwen2.5-coder:7b     # ~4.7 GB, one-time download
ollama serve                     # keep this running (a new terminal)
```

> On Windows the Ollama app usually starts `serve` automatically in the
> background after install — you can skip `ollama serve` if the app is running.

### 3. Get the project and install dependencies

```bash
# copy/clone the project, then:
cd nl2sql

# create an isolated environment
python -m venv .venv

# activate it
#   Windows (PowerShell):
.venv\Scripts\Activate.ps1
#   Windows (cmd):
.venv\Scripts\activate.bat
#   macOS / Linux:
source .venv/bin/activate

# install everything
pip install --upgrade pip
pip install -r requirements.txt
```

> The first install downloads PyTorch (CPU build) via `sentence-transformers`,
> which is the largest package (~200 MB). This is normal.

### 4. Add your data

The app has **no database connection** — it reads each table from a spreadsheet
in `data/excel/`. Put **one file per table**, named **exactly** after the table
(case-insensitive), `.xlsx` preferred (`.csv` also works):

```
data/excel/
    fingate_CbwtrBank.xlsx
    fingate_Gos.xlsx
    fingate_KycSummary.xlsx
    fingate_AccountPerson.xlsx
    fingate_AccountDetail.xlsx
    fingate_EntityDetail.xlsx
    finnet_Currency.xlsx
    finnet_Country.xlsx
```

Rules (also in `data/excel/README.md`):
- Filename (without extension) **must match a table name** in
  `core/static_schema.py`. Unknown files are ignored.
- Data lives in the **first sheet**; column headers in row 1 should match the
  column names in `SCHEMA` for that table.
- Each file is loaded into the correct DuckDB schema (`FINCORE_BRIDGE` /
  `FIUMetaHub`) automatically.

### 5. (Optional) Configure environment

Defaults work out of the box. To override, create a `.env` in the project root:

```ini
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:7b

# Safety
MAX_ROWS=500                # max rows returned per query
SQL_TIMEOUT_SECONDS=30

# Data location (optional)
# DATA_DIR=./data
# EXCEL_DIR=./data/excel
```

### 6. Run

```bash
streamlit run app.py
```

Open http://localhost:8501 in a browser.

> **First launch** downloads the embedding model `all-MiniLM-L6-v2` (~90 MB) and
> builds the table-suggestion index (~20–30 s). Later launches load it from disk
> in ~2 s. The index rebuilds automatically only when the schema metadata
> changes.

To expose it on a LAN: `streamlit run app.py --server.address 0.0.0.0`
(then browse to `http://<host-ip>:8501`).

---

## Usage

1. **Sidebar → Data** — confirm your tables loaded (e.g. "8/8 tables loaded").
   Click **🔄 Reload data** after adding or editing a spreadsheet.
2. **Sidebar → Check Ollama** — verify the model is reachable.
3. **Type your question.** Semantic **table suggestions** appear — click
   **✦ Use suggested** to apply them, or pick tables manually.
4. **Select the tables your question is about.** The model can only reference
   tables you've selected (e.g. select `fingate_CbwtrBank` for transaction
   questions).
5. *(Optional)* add mappings under **Extra glossary hints** — e.g.
   `customerType: 1=individual, 2=company` — for coded columns.
6. Click **▶ Run**. The generated SQL and results appear; download as CSV.

Every run is appended to `query_history.csv` in the project folder.

---

## Configuration reference

| Setting | Where | Default | Meaning |
|---|---|---|---|
| `OLLAMA_MODEL` | `.env` / `config/settings.py` | `qwen2.5-coder:7b` | Ollama model name |
| `OLLAMA_BASE_URL` | `.env` | `http://localhost:11434` | Ollama server URL |
| `MAX_ROWS` | `.env` | `500` | Row cap (injected as `LIMIT`) |
| `SQL_TIMEOUT_SECONDS` | `.env` | `30` | Reserved timeout knob |
| `MAX_RETRIES` | `config/settings.py` | `1` | Extra attempts after the first (total = `MAX_RETRIES + 1`) |
| `EXCEL_DIR` | `.env` | `./data/excel` | Where spreadsheets are read from |

---

## Project structure

```
nl2sql/
├── app.py                  # Streamlit UI (entry point)
├── requirements.txt
├── README.md
├── data/
│   ├── excel/              # ← your table spreadsheets go here
│   │   └── README.md       # naming rules
│   └── chroma_index/       # embedding index (auto-built; safe to delete)
├── config/
│   └── settings.py         # env-var loader (data paths, Ollama, safety)
└── core/
    ├── db.py               # DuckDB engine: load spreadsheets → transpile T-SQL → run
    ├── static_schema.py    # SCHEMA / TABLE_QUALIFIERS / COLUMN_META (the 8 tables)
    ├── schema.py           # schema dict → CREATE TABLE DDL for the prompt
    ├── embedder.py         # MiniLM + ChromaDB; suggest_tables()
    ├── llm.py              # Ollama client + prompt builder
    ├── validator.py        # sqlglot validation + keyword blocklist
    └── pipeline.py         # orchestrator: generate → validate → transpile → execute → retry
```

### The schema lives in code, not the database

`core/static_schema.py` is the single source of truth for table structure and
business meaning. It holds three dicts:

- **`SCHEMA`** — raw column definitions per table (name, type, nullable, length).
- **`TABLE_QUALIFIERS`** — maps each table to its SQL schema
  (`FINCORE_BRIDGE` or `FIUMetaHub`).
- **`COLUMN_META`** — plain-English alias, description, and domain tags per
  column. Drives both the LLM glossary and the embedding index.

Currently **8 tables / 218 columns** are defined.

### Adding a new table

1. Add its `SCHEMA` block, a `TABLE_QUALIFIERS` entry, and full `COLUMN_META`
   entries to `core/static_schema.py`.
2. Drop `<tableName>.xlsx` into `data/excel/`.
3. Restart the app (or click **Reload data**). The embedding index rebuilds
   automatically because the schema fingerprint changed.

---

## Safety model

- **No write path** — the engine is an in-memory DuckDB, read-only by design.
- **Keyword blocklist** — blocks `INSERT/UPDATE/DELETE/DROP/…` **and**
  DuckDB-specific statements (`ATTACH/COPY/INSTALL/LOAD/PRAGMA/…`) before
  execution.
- **SELECT-only + table allowlist** — sqlglot parse-time checks restrict each
  query to a single `SELECT` over the tables you selected.
- **Row cap** — `MAX_ROWS` (default 500) is injected as a `LIMIT` if absent.
- **Retry cap** — the model gets a bounded number of attempts, then a clean
  error is shown.

---

## Design notes

- **Why T-SQL then transpile?** Qwen-Coder is strongest at Microsoft T-SQL, and
  the prompt/glossary machinery was built around it. `core/db.py` transpiles each
  query to DuckDB with `sqlglot` at execution time (`TOP N`→`LIMIT N`,
  `[schema].[table]`→`"schema"."table"`, `GETDATE()`/`DATEADD`→DuckDB
  equivalents). So the "Microsoft SQL Server (T-SQL)" wording in `core/llm.py` is
  intentional, not stale.
- **Coded columns.** Many columns (e.g. `country`, `state`, `customerType`) are
  numeric codes, not text. Filtering them by a human word (`= 'company'`) fails
  unless a lookup table is loaded or you supply the codes via Extra glossary
  hints.
- **Known DDL quirks** (preserved as-is from the source DDLs): a typo
  `trasactionTime`, and columns with spaces in their names such as
  `rcd_upd d_update_date`, `job id `, `rcd_create date`. These are handled by
  the bracket/quote transpilation.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Sidebar shows "0 tables loaded" | Put spreadsheets in `data/excel/` named after each table, then click **Reload data** |
| `<table> — no file found` | Filename must match the table name exactly (e.g. `finnet_Country.xlsx`) |
| Cannot reach Ollama | Run `ollama serve` (or start the Ollama app); check `OLLAMA_BASE_URL` |
| Model not found | Run `ollama pull qwen2.5-coder:7b` |
| Query references a table "not in the provided schema" / placeholder name | Select the relevant table in the sidebar (e.g. `fingate_CbwtrBank` for transactions) |
| `Could not convert string '…' to INT64` | You filtered a coded numeric column by text — add code mappings via Extra glossary hints, or filter a text column |
| "Could not translate query to DuckDB" | A T-SQL construct didn't transpile; rephrase — the retry loop usually recovers |
| Wrong/empty results | Check the spreadsheet's column headers match `SCHEMA` for that table |
| First run is slow | One-time: embedding-model download + index build (~20–30 s) |
| `ScriptRunContext` warnings in the terminal | Harmless Streamlit warnings; ignore |

---

## Moving to another machine

Copy the whole project folder **except** `.venv/` (recreate it with step 3).
You can also skip `data/chroma_index/` — it rebuilds on first launch. On the new
machine you still need to install Ollama and pull the model (step 2). Everything
else is reproduced by `pip install -r requirements.txt` and dropping your
spreadsheets into `data/excel/`.
