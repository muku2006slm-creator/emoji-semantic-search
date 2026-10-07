import json, numpy as np
from sentence_transformers import SentenceTransformer

corpus = json.load(open("corpus.json", encoding="utf-8"))
texts = [e["text"] for e in corpus]

print(f"Embedding {len(texts)} texts...")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    normalize_embeddings=True,     # unit length → cosine becomes dot product
)

print("Shape:", embeddings.shape)
print("Dtype:", embeddings.dtype)
print("Norm of first vector:", np.linalg.norm(embeddings[0]))

np.save("embeddings.npy", embeddings.astype(np.float32))
print("Saved embeddings.npy")