"""
ingest.py — Milestone 3: Ingestion and Chunking
Loads all .txt files from documents/, splits them into chunks,
generates embeddings with sentence-transformers, and stores them in ChromaDB.

Run: python ingest.py
"""

import os
import re
import chromadb
from sentence_transformers import SentenceTransformer

# ── Config ────────────────────────────────────────────────────────────────────
DOCUMENTS_DIR = "documents"
CHROMA_DIR    = "chroma_db"
COLLECTION    = "baruch_guide"
CHUNK_SIZE    = 500       # characters per chunk
CHUNK_OVERLAP = 50        # characters of overlap between chunks
EMBED_MODEL   = "all-MiniLM-L6-v2"
# ─────────────────────────────────────────────────────────────────────────────


def load_documents(directory: str) -> list[dict]:
    """Load all .txt files from the documents folder."""
    docs = []
    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".txt") or filename == ".gitkeep":
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({"filename": filename, "text": text})
        print(f"  Loaded: {filename} ({len(text):,} chars)")
    return docs


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into overlapping chunks by character count."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        # Try to break at a sentence or paragraph boundary
        if end < len(text):
            # Look for last newline or period within the chunk
            boundary = max(chunk.rfind("\n"), chunk.rfind(". "))
            if boundary > chunk_size // 2:
                end = start + boundary + 1
                chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
    return [c for c in chunks if len(c) > 50]  # skip tiny leftover chunks


def main():
    print("=== Baruch Guide Ingestion Pipeline ===\n")

    # 1. Load documents
    print("Step 1: Loading documents...")
    docs = load_documents(DOCUMENTS_DIR)
    print(f"  → {len(docs)} documents loaded\n")

    # 2. Chunk documents
    print("Step 2: Chunking documents...")
    all_chunks = []
    all_ids    = []
    all_metas  = []

    for doc in docs:
        chunks = chunk_text(doc["text"], CHUNK_SIZE, CHUNK_OVERLAP)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['filename']}__chunk{i}"
            all_chunks.append(chunk)
            all_ids.append(chunk_id)
            all_metas.append({"source": doc["filename"], "chunk_index": i})
        print(f"  {doc['filename']}: {len(chunks)} chunks")

    print(f"\n  → Total chunks: {len(all_chunks)}\n")

    # 3. Generate embeddings
    print(f"Step 3: Loading embedding model ({EMBED_MODEL})...")
    print("  (This may take a minute the first time — downloading the model)\n")
    model = SentenceTransformer(EMBED_MODEL)

    print("  Generating embeddings...")
    embeddings = model.encode(all_chunks, show_progress_bar=True).tolist()
    print(f"\n  → {len(embeddings)} embeddings generated\n")

    # 4. Store in ChromaDB
    print(f"Step 4: Storing in ChromaDB (folder: {CHROMA_DIR})...")
    client     = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete existing collection if re-running
    try:
        client.delete_collection(COLLECTION)
        print("  (Cleared existing collection)")
    except Exception:
        pass

    collection = client.create_collection(COLLECTION)
    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=all_ids,
        metadatas=all_metas,
    )
    print(f"  → Stored {collection.count()} chunks in collection '{COLLECTION}'\n")

    print("=== Ingestion complete! ===")
    print(f"Your vector store is saved in ./{CHROMA_DIR}/")
    print("Run query.py next to test retrieval.")


if __name__ == "__main__":
    main()
