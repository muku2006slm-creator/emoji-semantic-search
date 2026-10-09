import json, numpy as np, re, unicodedata
from sentence_transformers import SentenceTransformer
from enrich_manual import MANUAL

corpus = json.load(open("corpus.json", encoding="utf-8"))
api = json.load(open("enrich_api.json", encoding="utf-8"))
by_hex = {e["hexcode"]: e for e in corpus}

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\u2010-\u2015]", "-", s)
    s = re.sub(r"[\u2018\u2019\u201c\u201d]", "", s)
    s = re.sub(r",(?=\S)", ", ", s)
    return s.lower().strip().rstrip(".")

model = SentenceTransformer("all-MiniLM-L6-v2")
base = np.load("embeddings.npy")
texts = [e["text"] for e in corpus]
idx = {e["hexcode"]: i for i, e in enumerate(corpus)}

def build(extra):
    t = list(texts)
    for hx, add in extra.items():
        t[idx[hx]] = f"{by_hex[hx]['label']}. {norm(add)}"
    return model.encode(t, batch_size=64, normalize_embeddings=True,
                        show_progress_bar=False)

print("Embedding three variants...")
E = {"base": base, "manual": build(MANUAL), "api": build(api)}

QUERIES = [
    ("that looks delicious",       "1F924"),
    ("creepy and not serious",     "1F921"),
    ("someone betrayed me",        "1F400"),
    ("abandoned and forgotten",    "1F578"),
    ("love is over",               "1F940"),
    ("rude gesture",               "1F595"),
    ("say cheese",                 "1F9C0"),
    ("eating healthy",             "1F957"),
    ("good luck message",          "1F960"),
    ("flirty and suggestive",      "1F351"),
    ("western cowboy vibes",       "1F920"),
    ("show support for a cause",   "1F397"),
]

print(f"\n{'query':<28} {'base':>6} {'manual':>8} {'api':>6}   target")
print("-" * 64)
score = {"base": 0, "manual": 0, "api": 0}
for q, target in QUERIES:
    qv = model.encode(q, normalize_embeddings=True)
    row = {}
    for name, M in E.items():
        order = np.argsort(-(M @ qv))
        rank = int(np.where(order == idx[target])[0][0]) + 1
        row[name] = rank
        if rank <= 10: score[name] += 1
    print(f"{q:<28} {row['base']:>6} {row['manual']:>8} {row['api']:>6}   "
          f"{by_hex[target]['emoji']}")

print("-" * 64)
print(f"{'in top 10':<28} {score['base']:>6} {score['manual']:>8} {score['api']:>6}  / {len(QUERIES)}")