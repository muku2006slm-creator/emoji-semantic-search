import json, re, unicodedata
from enrich_manual import MANUAL
from enrich_manual2 import MANUAL2

corpus = json.load(open("corpus.json", encoding="utf-8"))

ALL = {**MANUAL, **MANUAL2}
print(f"Enrichment entries: {len(MANUAL)} + {len(MANUAL2)} = {len(ALL)}")

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\u2010-\u2015]", "-", s)
    s = re.sub(r"[\u2018\u2019\u201c\u201d]", "", s)
    return s.lower().strip().rstrip(".")

applied, missing = 0, []
for e in corpus:
    hx = e["hexcode"]
    if hx in ALL:
        e["text"] = f'{e["label"]}. {norm(ALL[hx])}'
        e["enriched"] = True
        applied += 1

for hx in ALL:
    if not any(e["hexcode"] == hx for e in corpus):
        missing.append(hx)

print(f"Applied: {applied}")
if missing:
    print(f"WARNING - hexcodes not found in corpus: {missing}")

json.dump(corpus, open("corpus_enriched.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"Saved corpus_enriched.json ({len(corpus)} entries, {applied} enriched)")

print("\nSamples:")
for e in corpus:
    if e.get("enriched"):
        print(f"  {e['emoji']}  {e['text'][:75]}")