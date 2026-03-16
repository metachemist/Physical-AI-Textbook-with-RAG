"""Sentence-transformers embedding wrapper. Model loaded once at startup."""

from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts and return a list of float vectors."""
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return [vec.tolist() for vec in embeddings]

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query string."""
        return self.embed_batch([text])[0]
