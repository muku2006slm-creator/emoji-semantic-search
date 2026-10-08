import json, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus.json", encoding="utf-8"))

E_mini  = np.load("embeddings.npy")
E_mpnet = np.load("embeddings_mpnet.npy")

m_mini  = SentenceTransformer("all-MiniLM-L6-v2")
m_mpnet = SentenceTransformer("all-mpnet-base-v2")

def top(model, E, query, k=5):
    q = model.encode(query, normalize_embeddings=True)
    s = E @ q
    idx = np.argsort(-s)[:k]
    return [(corpus[i]["emoji"], float(s[i])) for i in idx]

QUERIES = [
    "happy", "not happy", "unhappy",
    "my job is exhausting",
    "ily", "sassy",
    "quiet happiness",
    "the feeling of being hungry late at night",
    "my landlord",
]

for q in QUERIES:
    a = top(m_mini, E_mini, q)
    b = top(m_mpnet, E_mpnet, q)
    print(f"\n{'='*58}\n{q}\n{'='*58}")
    print("  MiniLM:  " + "  ".join(f"{e} {s:.2f}" for e, s in a))
    print("  mpnet :  " + "  ".join(f"{e} {s:.2f}" for e, s in b))