from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


class SemanticRetriever:
    """
    Lightweight semantic search over case chunks.
    Uses sentence-transformers + FAISS.
    """

    def __init__(self, chunks):

        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

        # Convert YAML chunk structure safely
        if isinstance(chunks, dict):

            if "chunks" in chunks:
                chunk_list = chunks["chunks"]
            else:
                chunk_list = list(chunks.values())

        else:
            chunk_list = chunks

        self.chunk_dict = {c["id"]: c for c in chunk_list}

        self.chunk_ids = list(self.chunk_dict.keys())

        texts = [self.chunk_dict[cid]["text"] for cid in self.chunk_ids]

        embeddings = self.model.encode(texts, convert_to_numpy=True)

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)

        self.index.add(embeddings)

    def search(self, query, top_k=5):

        q_embedding = self.model.encode([query], convert_to_numpy=True)

        distances, indices = self.index.search(q_embedding, top_k)

        results = []

        for idx in indices[0]:

            if idx < len(self.chunk_ids):

                cid = self.chunk_ids[idx]

                results.append(cid)

        return results