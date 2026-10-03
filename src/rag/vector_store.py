"""Vector store wrapper for storing and searching embeddings."""


class VectorStore:
    """Minimal interface for a vector database (Chroma, FAISS, Pinecone, etc.)."""

    def __init__(self, persist_directory: str = "embeddings"):
        self.persist_directory = persist_directory

    def add(self, texts: list[str], metadatas: list[dict] | None = None):
        """Embed and store a batch of text chunks."""
        # TODO: implement embedding + storage
        raise NotImplementedError

    def search(self, query: str, top_k: int = 5) -> list[str]:
        """Return the top_k most similar stored chunks."""
        # TODO: implement similarity search
        raise NotImplementedError
