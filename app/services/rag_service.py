import faiss
import numpy as np
import os
import json
from app.utils.embedding import get_embedding
from app.config import RAG_INDEX_PATH


KNOWLEDGE_PATH = "app/data/knowledge_chunks.json"


class RAGService:
    def __init__(self):
        if os.path.exists(RAG_INDEX_PATH):
            self.index = faiss.read_index(RAG_INDEX_PATH)
        else:
            self.index = None

        if os.path.exists(KNOWLEDGE_PATH):
            with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as f:
                self.knowledge_chunks = json.load(f)
        else:
            self.knowledge_chunks = []

    def retrieve(self, query):

        if self.index is None or not self.knowledge_chunks:
            return None

        query_vector = np.array([get_embedding(query)]).astype("float32")

        scores, indices = self.index.search(query_vector, 3)

        retrieved_texts = []

        for idx in indices[0]:
            if idx < len(self.knowledge_chunks):
                retrieved_texts.append(self.knowledge_chunks[idx])

        if not retrieved_texts:
            return None

        return "\n".join(retrieved_texts)
