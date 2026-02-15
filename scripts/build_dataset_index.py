import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("app/data/alpaca_dataset.json", "r") as f:
    data = json.load(f)

embeddings = []
for item in data:
    embeddings.append(model.encode(item["instruction"]))

embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "app/vector_store/dataset_index.faiss")
