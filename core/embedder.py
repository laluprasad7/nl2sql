"""
core/embedder.py
────────────────
Builds a persistent Chroma vector index from the static schema metadata
(COLUMN_META in static_schema.py) and exposes a single query function:

    suggest_tables(question, top_k) -> list[str]

Each document in the index represents one column, with its text being:
    "{alias}. {description}. tags: {tags}"

At query time, we embed the analyst's question, retrieve the top-k column
matches, deduplicate by table, and return a ranked table list.

Index rebuild policy:
    The index fingerprint (SHA256 of all COLUMN_META keys+values) is stored
    alongside the Chroma DB. On startup the fingerprint is compared; rebuild
    only happens when the schema has changed.

Embedding model: all-MiniLM-L6-v2 (sentence-transformers)
    - 384-dim, ~22 MB on disk after first download
    - Runs on CPU in ~5–10ms per query — no GPU needed
    - Downloaded once from HuggingFace on first run
"""

from __future__ import annotations

import hashlib
import json
import os
import logging
from pathlib import Path
from typing import TYPE_CHECKING

import warnings
warnings.filterwarnings("ignore", message=".*torchvision.*")
import chromadb

os.environ["TOKENIZERS_PARALLELISM"] = "false"  
os.environ["CHROMA_TELEMETRY"] = "false"

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

log = logging.getLogger(__name__)

# Paths 
_BASE_DIR    = Path(__file__).resolve().parent.parent   # project root
CHROMA_DIR   = _BASE_DIR / "data" / "chroma_index"
FINGERPRINT_FILE = CHROMA_DIR / "schema_fingerprint.json"
COLLECTION_NAME  = "schema_columns"

# Module-level singletons (loaded once per process) 
_chroma_client:     chromadb.PersistentClient | None = None
_collection:        chromadb.Collection       | None = None
_embed_model:       SentenceTransformer       | None = None


####################
#  Embedding model
####################

def _get_embed_model() -> "SentenceTransformer":
    """Load all-MiniLM-L6-v2 once and cache it in the module global."""
    global _embed_model
    if _embed_model is None:
        from sentence_transformers import SentenceTransformer
        log.info("Loading embedding model all-MiniLM-L6-v2 …")
        _embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        log.info("Embedding model ready (dim=384).")
    return _embed_model


def _embed(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings → list of 384-float vectors."""
    model = _get_embed_model()
    return model.encode(texts, show_progress_bar=False).tolist()


#############################################################
#  Schema fingerprint — detects when COLUMN_META has changed
#############################################################

def _compute_fingerprint(column_meta: dict) -> str:
    """SHA256 of the sorted COLUMN_META dict — stable across Python restarts."""
    payload = json.dumps(column_meta, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()


def _read_stored_fingerprint() -> str | None:
    if FINGERPRINT_FILE.exists():
        return json.loads(FINGERPRINT_FILE.read_text())["fingerprint"]
    return None


def _write_fingerprint(fp: str) -> None:
    FINGERPRINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    FINGERPRINT_FILE.write_text(json.dumps({"fingerprint": fp}))


######################
#  Index construction
######################

def _build_documents(column_meta: dict) -> tuple[list[str], list[str], list[dict]]:
    """
    Convert COLUMN_META into three parallel lists:
      ids       — "table.column"
      documents — searchable text blobs
      metadatas — {table, column, alias} dicts stored in Chroma
    """
    ids, docs, metas = [], [], []
    for key, meta in column_meta.items():
        table, col = key.split(".", 1)
        tags_str   = ", ".join(meta.get("tags", []))
        doc_text   = (
            f"{meta['alias']}. "
            f"{meta['description']} "
            f"tags: {tags_str}"
        )
        ids.append(key)
        docs.append(doc_text)
        metas.append({"table": table, "column": col, "alias": meta["alias"]})
    return ids, docs, metas


def _build_index(column_meta: dict, client: chromadb.PersistentClient) -> chromadb.Collection:
    """(Re)build the Chroma collection from scratch."""
    log.info("Building schema embedding index … (%d columns)", len(column_meta))

    # Drop existing collection if present
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids, docs, metas = _build_documents(column_meta)

    # Embed in batches of 64 to keep memory manageable
    batch_size = 64
    all_embeddings: list[list[float]] = []
    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        all_embeddings.extend(_embed(batch))
        log.info("  Embedded %d / %d columns", min(i + batch_size, len(docs)), len(docs))

    collection.add(
        ids=ids,
        documents=docs,
        embeddings=all_embeddings,
        metadatas=metas,
    )
    log.info("Index built: %d column vectors stored.", len(ids))
    return collection


##############################################
#  Startup — called once when the app starts
##############################################

def initialise(column_meta: dict | None = None) -> str:
    """
    Ensure the Chroma index is ready. Rebuilds only if COLUMN_META changed.

    Parameters
    ----------
    column_meta   Pass static_schema.COLUMN_META (or None to import automatically).

    Returns
    -------
    "built"   — index was (re)built this run
    "cached"  — existing index reused (schema unchanged)
    """
    global _chroma_client, _collection

    if column_meta is None:
        from core.static_schema import COLUMN_META
        column_meta = COLUMN_META

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    current_fp = _compute_fingerprint(column_meta)
    stored_fp  = _read_stored_fingerprint()

    if current_fp == stored_fp:
        # Schema unchanged — reuse existing collection
        try:
            _collection = _chroma_client.get_collection(COLLECTION_NAME)
            _get_embed_model()
            log.info(
                "Schema index loaded from disk (%d vectors).",
                _collection.count(),
            )
            return "cached"
        except Exception:
            log.warning("Collection not found on disk despite matching fingerprint; rebuilding.")

    # Schema changed (or first run) — rebuild
    _collection = _build_index(column_meta, _chroma_client)
    _write_fingerprint(current_fp)
    return "built"


#################################################
#  Query — the function the app calls at runtime
#################################################

def suggest_tables(
    question: str,
    top_k_columns: int = 40,
    max_tables: int = 6,
) -> list[str]:
    """
    Given a plain-English question, return a ranked list of table names
    whose columns are most semantically relevant.

    Parameters
    ----------
    question      The analyst's natural language question.
    top_k_columns How many column matches to retrieve from Chroma.
                  More = broader coverage; fewer = tighter focus.
    max_tables    Cap on how many distinct tables to return.

    Returns
    -------
    List of table names, ranked by aggregate relevance score,
    best match first. At most `max_tables` entries.

    Raises
    ------
    RuntimeError if initialise() has not been called yet.
    """
    if _collection is None:
        initialise()

    # Embed the question
    q_vec = _embed([question])

    # Retrieve top-k column matches
    results = _collection.query(
        query_embeddings=q_vec,
        n_results=min(top_k_columns, _collection.count()),
        include=["metadatas", "distances"],
    )

    if not results["metadatas"] or not results["metadatas"][0]:
        return []

    # Aggregate by table: sum (1 - cosine_distance) as relevance score
    # cosine distance in [0, 2]; similarity = 1 - distance ≈ [−1, 1]
    table_scores: dict[str, float] = {}
    for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
        table      = meta["table"]
        similarity = 1.0 - dist          # higher = more relevant
        table_scores[table] = table_scores.get(table, 0.0) + similarity

    # Sort descending by score, cap at max_tables
    ranked = sorted(table_scores.items(), key=lambda x: x[1], reverse=True)
    return [t for t, _ in ranked[:max_tables]]


def suggest_tables_with_scores(
    question: str,
    top_k_columns: int = 40,
    max_tables: int = 6,
) -> list[tuple[str, float]]:
    """
    Same as suggest_tables() but returns (table_name, score) tuples.
    Useful for displaying confidence in the UI.
    """
    if _collection is None:
        initialise()  # self-heal after a hot reload (see suggest_tables)

    q_vec   = _embed([question])
    results = _collection.query(
        query_embeddings=q_vec,
        n_results=min(top_k_columns, _collection.count()),
        include=["metadatas", "distances"],
    )

    if not results["metadatas"] or not results["metadatas"][0]:
        return []

    table_scores: dict[str, float] = {}
    for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
        table = meta["table"]
        table_scores[table] = table_scores.get(table, 0.0) + (1.0 - dist)

    ranked = sorted(table_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:max_tables]


def index_stats() -> dict:
    """Return basic stats about the current index — for display in the UI."""
    if _collection is None:
        return {"status": "not initialised"}
    return {
        "status":  "ready",
        "vectors": _collection.count(),
        "path":    str(CHROMA_DIR),
    }
