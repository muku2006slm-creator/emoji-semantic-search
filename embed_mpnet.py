import json, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus.json", encoding="utf-8"))
texts = [e["text"] for e in corpus]

print(f"Embedding {len(texts)} texts with mpnet...")

model = SentenceTransformer("all-mpnet-base-v2")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True,
    normalize_embeddings=True,
)

print("Shape:", embeddings.shape)
print("Norm check:", np.linalg.norm(embeddings[0]))

np.save("embeddings_mpnet.npy", embeddings.astype(np.float32))
print("Saved embeddings_mpnet.npy")