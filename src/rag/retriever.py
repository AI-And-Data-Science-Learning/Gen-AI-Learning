"""Retrieval logic for RAG: embed a query and fetch nearest documents."""

from src.rag.vector_store import VectorStore


class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        """Return the top_k most relevant chunks for a query."""
        # TODO: embed query and call vector_store.search
        return []
