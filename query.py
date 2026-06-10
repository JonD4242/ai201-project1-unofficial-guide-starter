"""
query.py — Milestone 4: Retrieval and Generation
Takes a question, retrieves the most relevant chunks from ChromaDB,
and sends them to Groq (llama-3.3-70b-versatile) to generate a grounded answer.

Run interactively: python query.py
Single query:      python query.py "How do I register for classes?"
"""

import os
import sys
import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

# ── Config ────────────────────────────────────────────────────────────────────
CHROMA_DIR  = "chroma_db"
COLLECTION  = "baruch_guide"
EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL   = "llama-3.3-70b-versatile"
TOP_K       = 5   # number of chunks to retrieve per query
# ─────────────────────────────────────────────────────────────────────────────

load_dotenv()

SYSTEM_PROMPT = """You are the Unofficial Baruch College Student Guide — a helpful assistant that answers questions about Baruch College using only the provided source documents.

Rules:
- Answer using ONLY the information in the context below. Do not use outside knowledge.
- If the context does not contain enough information to answer, say: "I don't have enough information about that in my sources."
- Always cite your source(s) at the end of your answer using the filename(s) provided.
- Be concise and practical — students need clear, actionable answers.
"""


def build_context(results: dict) -> str:
    """Format retrieved chunks into a context block for the LLM."""
    context_parts = []
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        context_parts.append(f"[Source {i+1}: {meta['source']}]\n{doc}")
    return "\n\n---\n\n".join(context_parts)


def answer(question: str, collection, embed_model, groq_client) -> str:
    # 1. Embed the question
    query_embedding = embed_model.encode([question]).tolist()

    # 2. Retrieve top-k chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    # 3. Build context
    context = build_context(results)

    # 4. Call Groq LLM
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}",
        },
    ]

    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()


def main():
    print("=== Baruch Unofficial Guide — RAG Query System ===\n")

    # Load models and DB
    print("Loading embedding model...")
    embed_model = SentenceTransformer(EMBED_MODEL)

    print("Connecting to ChromaDB...")
    client     = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(COLLECTION)
    print(f"  → {collection.count()} chunks loaded\n")

    print("Connecting to Groq...")
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    print("  → Ready\n")

    # Single query mode (passed as CLI arg)
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(f"Question: {question}\n")
        print("Answer:")
        print(answer(question, collection, embed_model, groq_client))
        return

    # Interactive mode
    print("Type your question and press Enter. Type 'quit' to exit.\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print("\nAnswer:")
        print(answer(question, collection, embed_model, groq_client))
        print()


if __name__ == "__main__":
    main()
