import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

KNOWLEDGE_PATH = "app/data/knowledge_chunks.json"
RAG_INDEX_PATH = "app/vector_store/rag_index.faiss"

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_rag_index():

    if not os.path.exists(KNOWLEDGE_PATH):
        print(" knowledge_chunks.json not found.")
        return

    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
        knowledge_chunks = json.load(f)

    embeddings = []

    for chunk in knowledge_chunks:
        embeddings.append(model.encode(chunk))

    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("app/vector_store", exist_ok=True)

    faiss.write_index(index, RAG_INDEX_PATH)

    print(" RAG index built successfully!")
    print(f" Saved to {RAG_INDEX_PATH}")
    print(f" Total knowledge chunks indexed: {len(knowledge_chunks)}")


if __name__ == "__main__":
    build_rag_index()
