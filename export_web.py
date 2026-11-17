import json, os, numpy as np

OUT = "web/public/data"
os.makedirs(OUT, exist_ok=True)

corpus = json.load(open("corpus_enriched.json", encoding="utf-8"))
E = np.load("embeddings_enriched.npy")          # (1644, 384) float32, unit norm
n, d = E.shape

# ---------- quantize ----------
scale = float(np.abs(E).max())
Q = np.round(E / scale * 127).astype(np.int8)

# ---------- measure the damage ----------
E_hat = Q.astype(np.float32) * (scale / 127)
E_hat /= np.linalg.norm(E_hat, axis=1, keepdims=True)   # renormalize
per_row_cos = np.einsum("ij,ij->i", E, E_hat)

print(f"rows x dims      : {n} x {d}")
print(f"global scale     : {scale:.6f}")
print(f"int8 range used  : {Q.min()} .. {Q.max()}")
print()
print("fidelity after quantization (cosine vs original):")
print(f"  mean   {per_row_cos.mean():.6f}")
print(f"  min    {per_row_cos.min():.6f}")
print(f"  worst 5 rows: {[f'{v:.5f}' for v in np.sort(per_row_cos)[:5]]}")

# ---------- write ----------
Q.tofile(f"{OUT}/vectors_int8.bin")

meta = {"count": n, "dims": d, "scale": scale, "dtype": "int8",
        "model": "Xenova/all-MiniLM-L6-v2"}
json.dump(meta, open(f"{OUT}/meta.json", "w"), indent=1)

items = [{"e": x["emoji"], "n": x["label"], "t": x["text"]} for x in corpus]
json.dump(items, open(f"{OUT}/emoji.json", "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))

# also write float32 for the comparison test
E.tofile(f"{OUT}/vectors_f32.bin")

print()
for f in ["vectors_int8.bin", "vectors_f32.bin", "emoji.json", "meta.json"]:
    kb = os.path.getsize(f"{OUT}/{f}") / 1024
    print(f"  {f:<20} {kb:>8.1f} KB")