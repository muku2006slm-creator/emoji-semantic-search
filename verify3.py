import json, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus_enriched.json", encoding="utf-8"))
E = np.load("embeddings_enriched.npy")
model = SentenceTransformer("all-MiniLM-L6-v2")
by_hex = {e["hexcode"]: i for i, e in enumerate(corpus)}

CHECKS = [
    ("greedy",              ["1F911", "1F4B0"]),
    ("greed",               ["1F911", "1F4B0"]),
    ("stranded and alone",  ["1F3DD"]),
    ("need a vacation",     ["1F3D6"]),
    ("a hard challenge",    ["1F3D4"]),
    ("saving money",        ["1F3E6", "1F4B0"]),
]

for q, targets in CHECKS:
    qv = model.encode(q, normalize_embeddings=True)
    s = E @ qv
    order = np.argsort(-s)
    print(f"\n{q!r}   top: ", end="")
    print("  ".join(f"{corpus[i]['emoji']} {s[i]:.2f}" for i in order[:6]))
    for hx in targets:
        i = by_hex[hx]
        r = int(np.where(order == i)[0][0]) + 1
        print(f"    {corpus[i]['emoji']}  rank {r}  score {s[i]:.3f}")