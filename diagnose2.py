import json, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus_enriched.json", encoding="utf-8"))
raw = json.load(open("emoji_raw.json", encoding="utf-8"))
model = SentenceTransformer("all-MiniLM-L6-v2")
tok = model.tokenizer

# ---------- 1. tokenization ----------
print("tokens")
for w in ["greed", "greedy", "money", "algorithm", "sad", "selfish"]:
    print(f"  {w:<10} {tok.convert_ids_to_tokens(tok.encode(w, add_special_tokens=False))}")

print("\nword-level cosine")
pairs = [("greed","greedy"), ("greedy","algorithm"), ("greedy","money"),
         ("greed","money"), ("greedy","selfish"), ("greed","selfish")]
for a,b in pairs:
    va = model.encode(a, normalize_embeddings=True)
    vb = model.encode(b, normalize_embeddings=True)
    print(f"  {a:<8} vs {b:<10} {float(va@vb):+.3f}")

# ---------- 2. where is the money bag ----------
print("\nmoney bag (1F4B0)")
hit = [e for e in raw if e.get("hexcode") == "1F4B0"]
print(f"  in emoji_raw : {bool(hit)}", hit[0] if hit else "")
hit2 = [e for e in corpus if e["hexcode"] == "1F4B0"]
print(f"  in corpus    : {bool(hit2)}", hit2[0]["text"] if hit2 else "")

# ---------- 3. corrected bare-entry count ----------
def norm(s):
    return s.lower().replace("-", " ").replace(":", " ").replace("’", "'")

def extra(e):
    lw = set(norm(e["label"]).split())
    out = []
    for t in e.get("tags", []):
        parts = set(norm(t).split())
        if not parts.issubset(lw):          # keep only if it adds a new word
            out.append(t)
    return out

GROUPS = {0: "Smileys", 1: "People", 3: "Animals", 4: "Food",
          6: "Activities", 7: "Objects", 8: "Symbols", 5: "Travel"}

already = {e["hexcode"] for e in corpus if e.get("enriched")}
missed = [e for e in corpus
          if e["group"] in GROUPS and len(extra(e)) <= 1
          and e["hexcode"] not in already]

print(f"\nalready enriched      : {len(already)}")
print(f"newly found as bare   : {len(missed)}")
from collections import Counter
for g, n in sorted(Counter(e["group"] for e in missed).items()):
    print(f"  {GROUPS[g]:<12} {n}")
print("\nsample:")
for e in missed[:25]:
    print(f"  {e['emoji']}  {e['label']:<34} {extra(e)}")