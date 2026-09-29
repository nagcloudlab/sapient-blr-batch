"""
=============================================================
  LEARN EMBEDDINGS — Hands-on Demo for Beginners
=============================================================
  Run: python3 learn_embeddings.py

  This demo builds embeddings from SCRATCH so you can see
  exactly what's happening. No magic, no black boxes.
=============================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

print("=" * 60)
print("  STEP 1: Why do we need embeddings?")
print("=" * 60)
print("""
Problem: Computers only understand numbers, not words.

Naive approach — assign each word an ID:
  "cat"    → 1
  "dog"    → 2
  "queen"  → 3
  "king"   → 4
  "banana" → 5

But ID 1 (cat) and ID 2 (dog) seem just as far apart
as ID 1 (cat) and ID 5 (banana).

The IDs tell us NOTHING about meaning!
""")
input("Press Enter to continue...\n")

# ─────────────────────────────────────────────────────────
print("=" * 60)
print("  STEP 2: What IS an embedding?")
print("=" * 60)
print("""
An embedding = a list of numbers (a vector) where
SIMILAR things have SIMILAR numbers.

Let's create simple 4-dimensional embeddings by hand:
  Each dimension = a concept score
""")

# Hand-crafted embeddings to demonstrate the concept
words = ["king", "queen", "man", "woman", "prince", "princess",
         "apple", "banana", "orange", "cat", "dog"]

#                          royalty  gender   food   animal
embeddings_manual = {
    "king":      np.array([ 0.9,    0.8,    0.0,   0.0]),
    "queen":     np.array([ 0.9,   -0.8,    0.0,   0.0]),
    "man":       np.array([ 0.1,    0.8,    0.1,   0.0]),
    "woman":     np.array([ 0.1,   -0.8,    0.1,   0.0]),
    "prince":    np.array([ 0.7,    0.7,    0.0,   0.0]),
    "princess":  np.array([ 0.7,   -0.7,    0.0,   0.0]),
    "apple":     np.array([-0.1,    0.0,    0.9,   0.0]),
    "banana":    np.array([-0.1,    0.0,    0.85,  0.0]),
    "orange":    np.array([-0.1,    0.0,    0.88,  0.0]),
    "cat":       np.array([ 0.0,    0.0,    0.0,   0.9]),
    "dog":       np.array([ 0.0,    0.0,    0.0,   0.85]),
}

print("  Word       | royalty | gender |  food  | animal")
print("  " + "-" * 50)
for word in words:
    v = embeddings_manual[word]
    print(f"  {word:10s} | {v[0]:6.2f} | {v[1]:6.2f} | {v[2]:5.2f} | {v[3]:6.2f}")

input("\nPress Enter to continue...\n")

# ─────────────────────────────────────────────────────────
print("=" * 60)
print("  STEP 3: Measuring similarity (cosine similarity)")
print("=" * 60)
print("""
To check if two words are related, we measure the ANGLE
between their vectors:
  - 1.0  = identical direction (same meaning)
  - 0.0  = unrelated
  - -1.0 = opposite meaning
""")

pairs = [
    ("king", "queen"),
    ("king", "man"),
    ("cat", "dog"),
    ("king", "banana"),
    ("apple", "banana"),
    ("cat", "queen"),
]

print("  Word Pair             | Similarity")
print("  " + "-" * 40)
for w1, w2 in pairs:
    v1 = embeddings_manual[w1].reshape(1, -1)
    v2 = embeddings_manual[w2].reshape(1, -1)
    sim = cosine_similarity(v1, v2)[0][0]
    bar = "#" * int(abs(sim) * 20)
    print(f"  {w1:8s} ↔ {w2:8s}  |  {sim:+.3f}  {bar}")

input("\nPress Enter to continue...\n")

# ─────────────────────────────────────────────────────────
print("=" * 60)
print("  STEP 4: Vector arithmetic — math on meaning!")
print("=" * 60)
print("""
The famous example:
  king - man + woman = ???

Let's compute it:
""")

result = embeddings_manual["king"] - embeddings_manual["man"] + embeddings_manual["woman"]
print(f"  king   = {embeddings_manual['king']}")
print(f"  man    = {embeddings_manual['man']}")
print(f"  woman  = {embeddings_manual['woman']}")
print(f"")
print(f"  king - man + woman = {result}")
print()

# Find the closest word to the result
best_word = None
best_sim = -1
for word, vec in embeddings_manual.items():
    if word in ("king", "man", "woman"):
        continue
    sim = cosine_similarity(result.reshape(1, -1), vec.reshape(1, -1))[0][0]
    if sim > best_sim:
        best_sim = sim
        best_word = word

print(f"  Closest word to result: '{best_word}' (similarity: {best_sim:.3f})")
print(f"  king - man + woman ≈ {best_word}!")

input("\nPress Enter to continue...\n")

# ─────────────────────────────────────────────────────────
print("=" * 60)
print("  STEP 5: How real embeddings are LEARNED (mini demo)")
print("=" * 60)
print("""
In real models, embeddings start RANDOM and get updated
during training. Words in similar contexts get pulled
closer together.

Let's simulate this with a tiny training loop:
""")

# Simple training simulation
np.random.seed(42)
vocab = ["cat", "dog", "fish", "car", "bus", "truck"]

# Start with random embeddings (2D for easy visualization)
learned = {word: np.random.randn(2) for word in vocab}

print("BEFORE training (random):")
for word in vocab:
    print(f"  {word:6s} → [{learned[word][0]:+.2f}, {learned[word][1]:+.2f}]")

# Training: push similar words closer together
similar_pairs = [("cat", "dog"), ("cat", "fish"), ("dog", "fish"),
                 ("car", "bus"), ("car", "truck"), ("bus", "truck")]
learning_rate = 0.1

for epoch in range(100):
    for w1, w2 in similar_pairs:
        # Pull vectors closer together
        diff = learned[w2] - learned[w1]
        learned[w1] += learning_rate * diff * 0.1
        learned[w2] -= learning_rate * diff * 0.1

print("\nAFTER training (100 epochs of pulling similar words closer):")
for word in vocab:
    print(f"  {word:6s} → [{learned[word][0]:+.2f}, {learned[word][1]:+.2f}]")

print("\nSimilarities AFTER training:")
test_pairs = [("cat", "dog"), ("car", "bus"), ("cat", "car")]
for w1, w2 in test_pairs:
    sim = cosine_similarity(learned[w1].reshape(1,-1), learned[w2].reshape(1,-1))[0][0]
    print(f"  {w1:5s} ↔ {w2:5s} = {sim:.3f}")

input("\nPress Enter to see the visualization...\n")

# ─────────────────────────────────────────────────────────
print("=" * 60)
print("  STEP 6: Visualizing embeddings (2D plot)")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Our hand-crafted embeddings (use first 2 dims: royalty & gender)
ax1 = axes[0]
ax1.set_title("Hand-Crafted Embeddings\n(royalty vs gender dimensions)", fontsize=13)
colors = {"king": "blue", "queen": "red", "man": "blue", "woman": "red",
          "prince": "blue", "princess": "red",
          "apple": "green", "banana": "green", "orange": "green",
          "cat": "purple", "dog": "purple"}

for word, vec in embeddings_manual.items():
    ax1.scatter(vec[0], vec[1], c=colors[word], s=100, zorder=5)
    ax1.annotate(word, (vec[0], vec[1]), textcoords="offset points",
                xytext=(8, 8), fontsize=11, fontweight='bold')
ax1.set_xlabel("← not royal          royal →", fontsize=11)
ax1.set_ylabel("← female            male →", fontsize=11)
ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
ax1.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
ax1.grid(True, alpha=0.2)

# Plot 2: Learned embeddings
ax2 = axes[1]
ax2.set_title("Learned Embeddings After Training\n(similar words cluster together)", fontsize=13)
colors2 = {"cat": "purple", "dog": "purple", "fish": "purple",
           "car": "orange", "bus": "orange", "truck": "orange"}

for word, vec in learned.items():
    ax2.scatter(vec[0], vec[1], c=colors2[word], s=100, zorder=5)
    ax2.annotate(word, (vec[0], vec[1]), textcoords="offset points",
                xytext=(8, 8), fontsize=11, fontweight='bold')

# Draw circles around clusters
from matplotlib.patches import Circle
ax2.set_xlabel("Dimension 1", fontsize=11)
ax2.set_ylabel("Dimension 2", fontsize=11)
ax2.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig("embeddings_visualization.png", dpi=150, bbox_inches='tight')
print("\nPlot saved to: embeddings_visualization.png")

# Show the plot if a display is available (skip on headless servers)
try:
    plt.show()
except Exception:
    print("  (No display available -- open embeddings_visualization.png to view)")

# ─────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 7: Semantic Search — a real use case")
print("=" * 60)
print("""
Embeddings power semantic search. Instead of matching exact
keywords, you match MEANING.
""")

# Simulate a tiny document search using our embeddings
documents = {
    "doc1": {"text": "The king ruled the kingdom", "words": ["king"]},
    "doc2": {"text": "She adopted a cute cat",    "words": ["cat"]},
    "doc3": {"text": "The queen wore a crown",    "words": ["queen"]},
    "doc4": {"text": "I ate a banana for lunch",  "words": ["banana"]},
    "doc5": {"text": "The dog fetched the ball",   "words": ["dog"]},
}

query_word = "prince"
print(f'  Search query: "{query_word}"')
print(f'  (No document contains the word "prince"!)\n')

results = []
query_vec = embeddings_manual[query_word].reshape(1, -1)
for doc_id, doc in documents.items():
    doc_vec = embeddings_manual[doc["words"][0]].reshape(1, -1)
    sim = cosine_similarity(query_vec, doc_vec)[0][0]
    results.append((sim, doc_id, doc["text"]))

results.sort(reverse=True)
print("  Results ranked by embedding similarity:")
for sim, doc_id, text in results:
    bar = "#" * int(max(0, sim) * 20)
    print(f"    {sim:+.3f}  {bar:20s}  {text}")

print("""
  Even though no document contains "prince", the search
  found "king" and "queen" documents because their embeddings
  are CLOSE to "prince" in vector space!
""")

print("=" * 60)
print("  SUMMARY")
print("=" * 60)
print("""
  1. Embeddings = words represented as lists of numbers
  2. Similar words → similar numbers → close in space
  3. They're LEARNED from data (start random, get refined)
  4. You can do math on them (king - man + woman ≈ queen)
  5. They power: search, recommendations, LLMs, and more

  In a real LLM like GPT/Claude:
  - Vocabulary: ~100,000 tokens
  - Dimensions:  4,096 - 12,288 (not 4 like our demo!)
  - The embedding table alone = ~400 million parameters
""")
