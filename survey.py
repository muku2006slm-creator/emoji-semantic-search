import json
from collections import Counter

data = json.load(open("emoji_raw.json", encoding="utf-8"))

print("Total:", len(data))

has_group = [e for e in data if "group" in e]
has_tags  = [e for e in data if e.get("tags")]
print("With 'group':", len(has_group))
print("With 'tags' :", len(has_tags))

print("\nGroup distribution:")
for g, n in sorted(Counter(e["group"] for e in has_group).items()):
    sample = next(e for e in has_group if e["group"] == g)
    print(f"  group {g:2d}: {n:4d}  e.g. {sample['emoji']} {sample['label']}")

print("\nTag count distribution:")
for n, c in sorted(Counter(len(e.get("tags", [])) for e in data).items()):
    print(f"  {n} tags: {c}")

print("\nSample of entries with no group:")
for e in [x for x in data if "group" not in x][:8]:
    print("  ", e["emoji"], "|", e["label"])