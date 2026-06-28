import os
import json
from pathlib import Path
from dotenv import load_dotenv
import ollama
import chromadb
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "nomic-embed-text"
GEMINI_MODEL    = "gemini-2.5-flash"
CHUNK_SIZE      = 200   # tokens (approx words)
CHUNK_OVERLAP   = 40
TOP_K           = 3     # how many chunks to retrieve

# ─────────────────────────────────────────
# 1. CHUNKING
# Split text into overlapping chunks
# ─────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # overlap slides window back
    return chunks

# ─────────────────────────────────────────
# 2. EMBEDDING
# Convert text to vector using Ollama
# ─────────────────────────────────────────

def embed(text: str) -> list[float]:
    response = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
    return response["embedding"]

# ─────────────────────────────────────────
# 3. INDEXING
# Read docs folder, chunk, embed, store in ChromaDB
# ─────────────────────────────────────────

def index_documents(docs_folder: str, collection) -> int:
    docs_path = Path(docs_folder)
    total_chunks = 0

    for file_path in docs_path.glob("*.txt"):
        print(f"  📄 Indexing {file_path.name}...")
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_path.stem}_{i}"
            vector = embed(chunk)

            collection.upsert(
                ids=[chunk_id],
                embeddings=[vector],
                documents=[chunk],
                metadatas=[{"source": file_path.name, "chunk": i}]
            )
            total_chunks += 1

    return total_chunks

# ─────────────────────────────────────────
# 4. RETRIEVAL
# Embed the query, find most similar chunks
# ─────────────────────────────────────────

def retrieve(query: str, collection, top_k: int = TOP_K) -> list[dict]:
    query_vector = embed(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text":     results["documents"][0][i],
            "source":   results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

# ─────────────────────────────────────────
# 5. GENERATION
# Inject retrieved chunks into prompt and call Gemini
# ─────────────────────────────────────────

def answer(query: str, chunks: list[dict]) -> str:
    context = "\n\n---\n\n".join([
        f"Source: {c['source']}\n{c['text']}" for c in chunks
    ])

    prompt = f"""You are a helpful Android development assistant.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have information about that in my docs."

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return response.text

# ─────────────────────────────────────────
# 6. MAIN — wire it all together
# ─────────────────────────────────────────

def main():
    print("🚀 Setting up RAG system...\n")

    # Set up ChromaDB (local, persistent)
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection(
        name="android_docs",
        metadata={"hnsw:space": "cosine"}
    )

    # Index documents (skip if already indexed)
    existing = collection.count()
    if existing == 0:
        print("📚 Indexing documents...")
        total = index_documents("./docs", collection)
        print(f"✅ Indexed {total} chunks\n")
    else:
        print(f"✅ Using existing index ({existing} chunks)\n")

    # Chat loop
    print("💬 Chat with your Android docs!")
    print("Type 'quit' to exit, 'reindex' to rebuild the index\n")

    while True:
        query = input("You: ").strip()

        if not query:
            continue
        if query.lower() == "quit":
            print("Goodbye!")
            break
        if query.lower() == "reindex":
            chroma_client.delete_collection("android_docs")
            collection = chroma_client.get_or_create_collection(
                name="android_docs",
                metadata={"hnsw:space": "cosine"}
            )
            total = index_documents("./docs", collection)
            print(f"✅ Reindexed {total} chunks\n")
            continue

        # Retrieve relevant chunks
        chunks = retrieve(query, collection)

        # Show which sources were used
        sources = list(set(c["source"] for c in chunks))
        print(f"\n📎 Sources: {', '.join(sources)}")

        # Generate answer
        response = answer(query, chunks)
        print(f"\n🤖 {response}\n")

if __name__ == "__main__":
    main()