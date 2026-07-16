# Data drop folder

The app has **no live database connection**. Instead, each table is loaded from a
local spreadsheet in this folder and queried with DuckDB.

## Naming convention (important)

Put **one file per table**, named **exactly** after the table name, with a
`.xlsx` (preferred) or `.csv` extension:

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

- The filename (without extension) **must match a table name** in
  `core/static_schema.py` (the `SCHEMA` dict keys). Case is ignored.
- Data goes in the **first sheet** of each workbook.
- Column headers in row 1 should match the column names in `SCHEMA` for that
  table (including the known typos, e.g. `trasactionTime`, `job id `).
- Files whose name doesn't match a known table are ignored (a warning is shown).

## How it's loaded

At startup the app builds an **in-memory DuckDB** with two schemas
(`FINCORE_BRIDGE`, `FIUMetaHub`) and loads each spreadsheet into the schema its
table belongs to (see `TABLE_QUALIFIERS`). So a generated query like

```sql
SELECT TOP 10 senderName FROM [FINCORE_BRIDGE].[fingate_CbwtrBank]
```

is transpiled to DuckDB and runs against `FINCORE_BRIDGE.fingate_CbwtrBank`.

Updating a file? Just replace it here and restart the app (or click
**Reload data** in the sidebar).
