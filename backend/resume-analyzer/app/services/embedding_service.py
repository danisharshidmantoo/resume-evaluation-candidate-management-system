from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: list[str]):
        return self.model.encode(
            documents,
            show_progress_bar=True,
        )

    def embed_query(self, query: str):
        return self.model.encode([query])


embedding_service = EmbeddingService()