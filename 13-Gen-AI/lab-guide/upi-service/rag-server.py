"""
RAG Server with ChromaDB -- Real vector database for semantic search
Runs as a lightweight HTTP API alongside the Node.js UPI service.

Start: python3 rag-server.py
Port:  5100
"""

import os
import glob
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import chromadb

# --- Config ---
DOCS_DIR = os.path.join(os.path.dirname(__file__), "rag-docs")
PORT = 5100
DB_PATH = os.path.join(os.path.dirname(__file__), "chroma-data")

# --- Initialize ChromaDB ---
print("[RAG] Initializing ChromaDB...")
client = chromadb.PersistentClient(path=DB_PATH)

# Create or get collection (uses ChromaDB's built-in embedding model)
collection = client.get_or_create_collection(
    name="upi_docs",
    metadata={"hnsw:space": "cosine"}  # Use cosine similarity
)

# --- Ingest documents ---
def ingest_docs():
    """Load markdown files, chunk by headings, store in ChromaDB."""
    existing = collection.count()
    if existing > 0:
        print(f"[RAG] Collection already has {existing} chunks. Skipping ingest.")
        print(f"[RAG] (Delete {DB_PATH} to re-ingest)")
        return existing

    print(f"[RAG] Ingesting documents from {DOCS_DIR}...")
    docs = []
    metas = []
    ids = []

    for filepath in sorted(glob.glob(os.path.join(DOCS_DIR, "*.md"))):
        filename = os.path.basename(filepath)
        with open(filepath, "r") as f:
            content = f.read()

        # Chunk by ### headings (finer), fallback to ##
        splitter = "\n### " if "\n### " in content else "\n## "
        sections = content.split(splitter)

        for i, section in enumerate(sections):
            text = section.strip() if i == 0 else (splitter.strip() + " " + section.strip())
            if len(text) < 30:
                continue

            chunk_id = f"{filename}__chunk_{i}"
            docs.append(text)
            metas.append({"source": filename, "chunk_index": i})
            ids.append(chunk_id)

    if docs:
        collection.add(documents=docs, metadatas=metas, ids=ids)
        print(f"[RAG] Ingested {len(docs)} chunks from {len(set(m['source'] for m in metas))} documents")

    return len(docs)


# --- Search ---
def search(query, top_k=3):
    """Search ChromaDB for relevant chunks."""
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
    )

    formatted = []
    if results and results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            formatted.append({
                "text": doc[:600],
                "source": results["metadatas"][0][i]["source"],
                "score": round(1 - results["distances"][0][i], 3),  # Convert distance to similarity
                "chunk_id": results["ids"][0][i],
            })

    return formatted


# --- HTTP Server ---
class RAGHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/rag/search":
            params = parse_qs(parsed.query)
            query = params.get("q", [""])[0]

            if not query:
                self._json(400, {"error": "q parameter required"})
                return

            results = search(query)
            self._json(200, {
                "query": query,
                "results": results,
                "total_chunks": collection.count(),
                "engine": "ChromaDB",
                "embedding_model": "all-MiniLM-L6-v2 (default)",
            })

        elif parsed.path == "/api/rag/status":
            self._json(200, {
                "status": "ok",
                "engine": "ChromaDB",
                "total_chunks": collection.count(),
                "embedding_model": "all-MiniLM-L6-v2 (default)",
            })

        else:
            self._json(404, {"error": "Not found"})

    def _json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        # Quieter logging
        pass


if __name__ == "__main__":
    total = ingest_docs()
    print(f"[RAG] ChromaDB ready with {collection.count()} chunks")
    print(f"[RAG] Server starting on http://localhost:{PORT}")
    print(f"[RAG] Test: curl 'http://localhost:{PORT}/api/rag/search?q=NPCI+penalty'")

    server = HTTPServer(("0.0.0.0", PORT), RAGHandler)
    server.serve_forever()
