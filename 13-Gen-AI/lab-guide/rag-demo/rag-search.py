"""
RAG Demo -- Search UPI runbooks and NPCI docs with AI
Run: python3 rag-search.py "What is the NPCI penalty for 1 hour downtime?"
"""

import os
import sys
import glob
import numpy as np

# --- Step 1: Load documents ---
def load_docs(docs_dir="docs"):
    """Load all markdown files and split into chunks."""
    chunks = []
    for filepath in glob.glob(os.path.join(docs_dir, "*.md")):
        filename = os.path.basename(filepath)
        with open(filepath, "r") as f:
            content = f.read()

        # Chunking: split by ### headings (finer granularity)
        # Fall back to ## if no ### found
        if "\n### " in content:
            sections = content.split("\n### ")
        else:
            sections = content.split("\n## ")

        for i, section in enumerate(sections):
            if i == 0:
                chunk_text = section.strip()
            else:
                chunk_text = "### " + section.strip()

            if len(chunk_text) > 30:  # Skip very short chunks
                chunks.append({
                    "text": chunk_text,
                    "source": filename,
                    "chunk_id": f"{filename}#chunk{i}"
                })

    return chunks


# --- Step 2: Create embeddings (simple TF-IDF based) ---
def create_embeddings(chunks):
    """Create simple word-frequency embeddings for each chunk."""
    # Build vocabulary from all chunks
    vocab = set()
    for chunk in chunks:
        words = chunk["text"].lower().split()
        vocab.update(words)

    vocab = sorted(vocab)
    word_to_idx = {w: i for i, w in enumerate(vocab)}

    # Create TF vectors
    vectors = []
    for chunk in chunks:
        vec = np.zeros(len(vocab))
        words = chunk["text"].lower().split()
        for w in words:
            if w in word_to_idx:
                vec[word_to_idx[w]] += 1
        # Normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        vectors.append(vec)

    return np.array(vectors), word_to_idx, vocab


# --- Step 3: Search ---
def search(query, chunks, vectors, word_to_idx, vocab, top_k=3):
    """Find the most relevant chunks for a query."""
    # Create query vector
    query_vec = np.zeros(len(vocab))
    for w in query.lower().split():
        if w in word_to_idx:
            query_vec[word_to_idx[w]] += 1
    norm = np.linalg.norm(query_vec)
    if norm > 0:
        query_vec = query_vec / norm

    # Cosine similarity
    scores = vectors @ query_vec
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if scores[idx] > 0:
            results.append({
                "chunk": chunks[idx],
                "score": scores[idx]
            })

    return results


# --- Step 4: Generate answer with context ---
def generate_answer(query, results):
    """Format the RAG response (without calling an LLM -- template based)."""
    if not results:
        return "No relevant documents found."

    context = "\n\n---\n\n".join([
        f"Source: {r['chunk']['source']} (relevance: {r['score']:.2f})\n{r['chunk']['text'][:500]}"
        for r in results
    ])

    return f"""
=== RAG SEARCH RESULTS ===

Query: "{query}"

Found {len(results)} relevant document(s):

{context}

===========================

To get an AI-generated answer, you would send this prompt to an LLM:

---
Answer the following question using ONLY the context provided.
If the answer is not in the context, say "Not found in documents."
Cite the source document.

Question: {query}

Context:
{context}
---
"""


# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 rag-search.py \"your question here\"")
        print()
        print("Example queries:")
        print('  python3 rag-search.py "What is the NPCI penalty for 1 hour downtime?"')
        print('  python3 rag-search.py "What is the SLA for P1 incidents?"')
        print('  python3 rag-search.py "How to diagnose payment 503 errors?"')
        print('  python3 rag-search.py "What is the refund timeline for failed transactions?"')
        print('  python3 rag-search.py "What is the daily transaction limit per VPA?"')
        sys.exit(0)

    query = " ".join(sys.argv[1:])

    print(f"\n[1] Loading documents from docs/...")
    docs_dir = os.path.join(os.path.dirname(__file__), "docs")
    chunks = load_docs(docs_dir)
    print(f"    Loaded {len(chunks)} chunks from {len(set(c['source'] for c in chunks))} documents")

    print(f"\n[2] Creating embeddings (TF-IDF vectors)...")
    vectors, word_to_idx, vocab = create_embeddings(chunks)
    print(f"    Vocabulary size: {len(vocab)} words")
    print(f"    Vector dimensions: {len(vocab)}")

    print(f"\n[3] Searching for: \"{query}\"")
    results = search(query, chunks, vectors, word_to_idx, vocab)

    print(generate_answer(query, results))
