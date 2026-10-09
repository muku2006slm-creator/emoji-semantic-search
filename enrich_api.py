import json, os, time, unicodedata
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TARGETS = list(__import__("enrich_manual").MANUAL.keys())

corpus = json.load(open("corpus.json", encoding="utf-8"))
by_hex = {e["hexcode"]: e for e in corpus}

PROMPT = """For the emoji {emoji} ("{label}"), list 6-8 comma-separated keywords \
describing how people actually USE it — connotations, feelings, slang meanings, \
situations. Do not repeat words from the name. Use common English words only. \
Output only the comma-separated list, nothing else."""

def clean(s):
    # normalize fancy unicode punctuation the model sometimes emits
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    return s.strip().rstrip(".")

out = {}
for i, hx in enumerate(TARGETS, 1):
    e = by_hex[hx]
    r = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": PROMPT.format(emoji=e["emoji"], label=e["label"])}],
        temperature=0.7,
        max_tokens=250,
        reasoning_effort="low",
    )
    text = clean(r.choices[0].message.content or "")
    out[hx] = text
    status = text[:60] if text else "*** EMPTY ***"
    print(f"{i:3d}/{len(TARGETS)}  {e['emoji']}  {status}")
    time.sleep(0.3)

json.dump(out, open("enrich_api.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

empty = sum(1 for v in out.values() if not v)
print(f"\nSaved enrich_api.json  ({len(out)} entries, {empty} empty)")