import json, sys, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus.json", encoding="utf-8"))
E = np.load("embeddings.npy")          # (1644, 384), unit-normalized
model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query, k=10):
    q = model.encode(query, normalize_embeddings=True)   # (384,)
    scores = E @ q                                       # (1644,)
    top = np.argsort(-scores)[:k]
    return [(corpus[i], float(scores[i])) for i in top]

if __name__ == "__main__":
    while True:
        q = input("\nquery> ").strip()
        if not q:
            break
        for e, s in search(q):
            print(f"  {s:.3f}  {e['emoji']}  {e['text'][:60]}")