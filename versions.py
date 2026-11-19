import json
from collections import Counter

corpus = json.load(open("corpus_enriched.json", encoding="utf-8"))
c = Counter(e.get("version") for e in corpus)

total = len(corpus)
run = 0
print(f"{'unicode':>8} {'count':>6} {'cumulative':>11}")
for v in sorted(c, key=lambda x: (x is None, x)):
    run += c[v]
    print(f"{str(v):>8} {c[v]:>6} {run:>11}  ({100*run/total:.1f}%)")

print("\nnewest entries:")
for e in sorted(corpus, key=lambda x: -(x.get("version") or 0))[:15]:
    print(f"  {e['emoji']}  v{e.get('version')}  {e['label']}")