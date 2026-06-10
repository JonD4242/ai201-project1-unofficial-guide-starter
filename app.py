"""
app.py — Milestone 5: Query Interface
A Gradio web UI for the Baruch Unofficial Guide RAG system.

Run: python app.py
Then open http://localhost:7860 in your browser.
"""

import os
import chromadb
import gradio as gr
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

# ── Config ────────────────────────────────────────────────────────────────────
CHROMA_DIR  = "chroma_db"
COLLECTION  = "baruch_guide"
EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL   = "llama-3.3-70b-versatile"
TOP_K       = 5
# ─────────────────────────────────────────────────────────────────────────────

load_dotenv()

SYSTEM_PROMPT = """You are the Unofficial Baruch College Student Guide — a helpful assistant that answers questions about Baruch College using only the provided source documents.

Rules:
- Answer using ONLY the information in the context below. Do not use outside knowledge.
- If the context does not contain enough information to answer, say: "I don't have enough information about that in my sources."
- Always cite your source(s) at the end of your answer using the filename(s) provided.
- Be concise and practical — students need clear, actionable answers.
"""

# Load models once at startup
print("Loading embedding model...")
embed_model = SentenceTransformer(EMBED_MODEL)

print("Connecting to ChromaDB...")
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection    = chroma_client.get_collection(COLLECTION)

print("Connecting to Groq...")
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
print(f"Ready — {collection.count()} chunks loaded.\n")


def build_context(results: dict) -> str:
    parts = []
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        parts.append(f"[Source {i+1}: {meta['source']}]\n{doc}")
    return "\n\n---\n\n".join(parts)


def chat(question: str, history: list) -> str:
    if not question.strip():
        return "Please enter a question."

    # Retrieve relevant chunks
    query_embedding = embed_model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=TOP_K,
        include=["documents", "metadatas"],
    )
    context = build_context(results)

    # Call Groq
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    response = groq_client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()


# ── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(title="Baruch Unofficial Guide") as demo:
    gr.Markdown(
        """
        # 📚 The Unofficial Baruch College Student Guide
        Ask anything about registration, financial aid, professors, clubs, and more.
        Answers are grounded in real Baruch sources.
        """
    )
    chatbot = gr.ChatInterface(
        fn=chat,
        examples=[
            "How do I register for classes at Baruch?",
            "What financial aid is available at Baruch?",
            "How do I find and join student clubs?",
            "What should I know about professor ratings?",
            "What happens if a class I want is full?",
        ],
        cache_examples=False,
    )

if __name__ == "__main__":
    demo.launch()
