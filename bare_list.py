import json

corpus = json.load(open("corpus.json", encoding="utf-8"))

GROUPS = {0: "Smileys", 1: "People", 3: "Animals", 4: "Food", 6: "Activities"}

def extra_tags(e):
    label_words = set(e["label"].lower().replace("-", " ").replace(":", " ").split())
    return [t for t in e.get("tags", []) if t.lower() not in label_words]

bare = [
    e for e in corpus
    if e["group"] in GROUPS and len(extra_tags(e)) <= 1
]

print(f"Tier-1 bare entries: {len(bare)}\n")
for e in bare:
    print(f'  "{e["hexcode"]}": "",   # {e["emoji"]}  {e["label"]}  {extra_tags(e)}')