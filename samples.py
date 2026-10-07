import json, random

data = json.load(open("emoji_raw.json", encoding="utf-8"))
random.seed(42)

def show(title, entries, n=12):
    print(f"\n{'='*60}\n{title}\n{'='*60}")
    for e in random.sample(entries, min(n, len(entries))):
        print(f"  {e['emoji']}  {e['label']:<32} {e.get('tags', [])}")

# the thin ones
thin = [e for e in data if "group" in e and len(e.get("tags", [])) <= 2]
show(f"THIN: 2 or fewer tags ({len(thin)} total)", thin)

# the rich ones
rich = [e for e in data if "group" in e and len(e.get("tags", [])) >= 10]
show(f"RICH: 10+ tags ({len(rich)} total)", rich)

# specifically emotional emoji — the ones our tool is really for
emotive = [e for e in data if e.get("group") == 0]
show(f"GROUP 0 — Smileys & Emotion ({len(emotive)} total)", emotive)

# how often do tags just repeat the label?
redundant = 0
for e in data:
    if "group" not in e: continue
    tags = set(t.lower() for t in e.get("tags", []))
    words = set(e["label"].lower().replace("-", " ").split())
    if tags and tags.issubset(words):
        redundant += 1
print(f"\n{'='*60}")
print(f"Entries where tags add NOTHING beyond the label: {redundant}")