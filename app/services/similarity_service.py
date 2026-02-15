import faiss
import numpy as np
import json
import os
from app.utils.embedding import get_embedding
from app.config import DATASET_PATH, DATASET_INDEX_PATH


# For L2 distance:
# Smaller distance = better match
# Recommended threshold: 0.5 to 1.2 (depends on embeddings)
L2_DISTANCE_THRESHOLD = 1.0


class SimilarityService:
    def __init__(self):
        if not os.path.exists(DATASET_INDEX_PATH):
            raise FileNotFoundError("FAISS dataset index not found. Please build it first.")

        self.index = faiss.read_index(DATASET_INDEX_PATH)

        if not os.path.exists(DATASET_PATH):
            raise FileNotFoundError("Dataset file not found.")

        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)

    def search(self, query: str):
        try:
            # Get embedding
            query_embedding = get_embedding(query)

            query_vector = np.array([query_embedding]).astype("float32")

            # Search top 1 match
            distances, indices = self.index.search(query_vector, 1)

            distance = distances[0][0]
            idx = indices[0][0]

            print(f"[Similarity Debug] Distance: {distance}")

            # For L2 distance → smaller is better
            if distance <= L2_DISTANCE_THRESHOLD and idx >= 0:
                print("DATASET MATCH USED")
                return self.dataset[idx]["output"]

            print("No strong dataset match")
            return None

        except Exception as e:
            print("Similarity search error:", str(e))
            return None
