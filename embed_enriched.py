import json, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus_enriched.json", encoding="utf-8"))
texts = [e["text"] for e in corpus]

model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode(texts, batch_size=64, show_progress_bar=True,
                   normalize_embeddings=True)

print("Shape:", emb.shape, "| norm:", np.linalg.norm(emb[0]))
np.save("embeddings_enriched.npy", emb.astype(np.float32))
print("Saved embeddings_enriched.npy")