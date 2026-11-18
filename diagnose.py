import json, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus_enriched.json", encoding="utf-8"))
E = np.load("embeddings_enriched.npy")
model = SentenceTransformer("all-MiniLM-L6-v2")

by_emoji = {e["emoji"]: i for i, e in enumerate(corpus)}

def words(i):
    return len(corpus[i]["text"].replace(".", " ").replace(",", " ").split())

def probe(query, watch):
    qv = model.encode(query, normalize_embeddings=True)
    s = E @ qv
    order = np.argsort(-s)
    print(f"\n=== {query!r}   top score {s[order[0]]:.3f}")
    for e in watch:
        i = by_emoji.get(e)
        if i is None:
            print(f"   {e}  NOT IN CORPUS")
            continue
        r = int(np.where(order == i)[0][0]) + 1
        print(f"   {e}  rank {r:>5}  score {s[i]:.3f}  words {words(i):>2}  | {corpus[i]['text'][:70]}")

probe("greed",  ["🤑", "💰", "💲", "🪙", "😈"])
probe("greedy", ["🤑", "💰", "💲", "🪙", "😈"])
probe("sad",    ["😢", "😭", "😞", "😔", "😕", "☹️", "🙁"])

# --- does text length predict rank for a one-word query? ---
print("\n=== length bias test: query 'sad'")
qv = model.encode("sad", normalize_embeddings=True)
s = E @ qv
top50 = np.argsort(-s)[:50]
lens = np.array([words(i) for i in top50])
ranks = np.arange(1, 51)
print(f"  mean words in top 10 : {lens[:10].mean():.1f}")
print(f"  mean words in 41-50  : {lens[40:].mean():.1f}")
print(f"  corr(rank, length)   : {np.corrcoef(ranks, lens)[0,1]:+.3f}")
print("  (positive corr = shorter texts rank higher)")

# same test for a longer query, as a control
print("\n=== control: query 'feeling completely overwhelmed and exhausted'")
qv2 = model.encode("feeling completely overwhelmed and exhausted", normalize_embeddings=True)
s2 = E @ qv2
top50b = np.argsort(-s2)[:50]
lens2 = np.array([words(i) for i in top50b])
print(f"  mean words in top 10 : {lens2[:10].mean():.1f}")
print(f"  mean words in 41-50  : {lens2[40:].mean():.1f}")
print(f"  corr(rank, length)   : {np.corrcoef(ranks, lens2)[0,1]:+.3f}")