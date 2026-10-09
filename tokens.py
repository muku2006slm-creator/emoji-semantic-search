from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
tok = model.tokenizer

WORDS = [
    "ily", "sassy", "sus", "143",
    "information", "love", "happy",
    "unhappy", "not happy",
    "pizza", "cringe", "slay", "yeet",
]

print(f"{'word':<14} {'n':<4} pieces")
print("-" * 60)
for w in WORDS:
    ids = tok.encode(w, add_special_tokens=False)
    pieces = tok.convert_ids_to_tokens(ids)
    print(f"{w:<14} {len(pieces):<4} {pieces}")

# is 'ily' actually close to 'information' in vector space?
print("\nCosine similarity between query words:")
pairs = [
    ("ily", "information"),
    ("ily", "love"),
    ("ily", "i love you"),
    ("sassy", "sarcastic"),
    ("sassy", "zodiac"),
    ("happy", "unhappy"),
    ("happy", "not happy"),
]
for a, b in pairs:
    va = model.encode(a, normalize_embeddings=True)
    vb = model.encode(b, normalize_embeddings=True)
    print(f"  {a:<12} vs {b:<14} {float(va @ vb):.3f}")