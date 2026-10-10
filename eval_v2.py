import json, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus.json", encoding="utf-8"))
E = {
    "base": np.load("embeddings.npy"),
    "v1":   np.load("embeddings_enriched_v1.npy"),
    "v2":   np.load("embeddings_enriched.npy"),
}
model = SentenceTransformer("all-MiniLM-L6-v2")
idx = {e["hexcode"]: i for i, e in enumerate(corpus)}
by_hex = {e["hexcode"]: e for e in corpus}

QUERIES = [
    ("that looks delicious",         "1F924"),
    ("creepy and not serious",       "1F921"),
    ("someone betrayed me",          "1F400"),
    ("abandoned and forgotten",      "1F578"),
    ("love is over",                 "1F940"),
    ("rude gesture",                 "1F595"),
    ("say cheese",                   "1F9C0"),
    ("eating healthy",               "1F957"),
    ("good luck message",            "1F960"),
    ("flirty and suggestive",        "1F351"),
    ("western cowboy vibes",         "1F920"),
    ("show support for a cause",     "1F397"),
    ("waiting around doing nothing", "1F9CD"),
    ("getting married",              "1F470"),
    ("wheelchair accessibility",     "1F9D1-200D-1F9BC"),
    ("studying for exams",           "1F9D1-200D-1F393"),
    ("refreshing on a hot day",      "1F349"),
    ("salty mediterranean snack",    "1FAD2"),
    ("warm comfort food",            "1F35B"),
    ("drink before bed",             "1F95B"),
    ("concert entry",                "1F39F"),
    ("throwing a frisbee",           "1F94F"),
    ("award for winning",            "1F3F5"),
    ("gentle forest animal",         "1F98C"),
]

print(f"{'query':<30} {'base':>6} {'v1':>5} {'v2':>5}  target")
print("-" * 60)
hits = {k: 0 for k in E}
ranks = {k: [] for k in E}
for q, target in QUERIES:
    qv = model.encode(q, normalize_embeddings=True)
    r = {}
    for name, M in E.items():
        order = np.argsort(-(M @ qv))
        r[name] = int(np.where(order == idx[target])[0][0]) + 1
        ranks[name].append(r[name])
        if r[name] <= 10:
            hits[name] += 1
    mark = "  <<<" if r["v2"] != r["v1"] else ""
    print(f"{q:<30} {r['base']:>6} {r['v1']:>5} {r['v2']:>5}  "
          f"{by_hex[target]['emoji']}{mark}")

print("-" * 60)
print(f"{'in top 10':<30} {hits['base']:>6} {hits['v1']:>5} {hits['v2']:>5}  / {len(QUERIES)}")
print(f"{'mean rank':<30} {np.mean(ranks['base']):>6.1f} "
      f"{np.mean(ranks['v1']):>5.1f} {np.mean(ranks['v2']):>5.1f}")
print(f"{'median rank':<30} {np.median(ranks['base']):>6.1f} "
      f"{np.median(ranks['v1']):>5.1f} {np.median(ranks['v2']):>5.1f}")