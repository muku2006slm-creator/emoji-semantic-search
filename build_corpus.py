import json
from collections import Counter

data = json.load(open("emoji_raw.json", encoding="utf-8"))

GROUP_NAMES = {
    0: "Smileys & Emotion", 1: "People & Body", 2: "Component",
    3: "Animals & Nature",  4: "Food & Drink",  5: "Travel & Places",
    6: "Activities",        7: "Objects",       8: "Symbols",
    9: "Flags",
}

DROP_GROUPS = {2, 9}          # skin-tone components, country flags

# ---------- filter ----------
kept = [
    e for e in data
    if "group" in e and e["group"] not in DROP_GROUPS
]
print(f"Before filter: {len(data)}")
print(f"After  filter: {len(kept)}")
print(f"Removed      : {len(data) - len(kept)}")

# ---------- build embedding text ----------
def build_text(e):
    label = e["label"]
    tags  = e.get("tags", [])
    # drop tags that are already words in the label — they add nothing
    label_words = set(label.lower().replace("-", " ").replace(":", " ").split())
    extra = [t for t in tags if t.lower() not in label_words]
    if extra:
        return f"{label}. {', '.join(extra)}"
    return label

for e in kept:
    e["text"] = build_text(e)
    e["n_extra"] = len(e["text"].split(", ")) - 1 if ". " in e["text"] else 0

# ---------- measure the gap ----------
bare = [e for e in kept if e["n_extra"] == 0]
weak = [e for e in kept if 1 <= e["n_extra"] <= 2]

print(f"\nBARE (no tags beyond the label): {len(bare)}")
print(f"WEAK (1-2 extra words)         : {len(weak)}")
print(f"OK   (3+ extra words)          : {len(kept) - len(bare) - len(weak)}")

print("\nBreakdown of BARE by group:")
for g, n in sorted(Counter(e["group"] for e in bare).items()):
    print(f"  {GROUP_NAMES[g]:<20} {n}")

print("\nSample BARE entries:")
for e in bare[:15]:
    print(f"  {e['emoji']}  {e['text']}")

print("\nSample built text (random healthy ones):")
import random; random.seed(7)
for e in random.sample([x for x in kept if x["n_extra"] >= 3], 8):
    print(f"  {e['emoji']}  {e['text']}")

# ---------- save ----------
with open("corpus.json", "w", encoding="utf-8") as f:
    json.dump(kept, f, ensure_ascii=False, indent=1)
print(f"\nSaved {len(kept)} entries to corpus.json")