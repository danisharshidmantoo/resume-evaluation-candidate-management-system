from app.services.embedding_service import EmbeddingService
from app.services.resume_chunker import ResumeChunker
from app.services.vector_store import ResumeVectorStore


class ResumeIngestionService:
    def __init__(self):
        self.chunker = ResumeChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = ResumeVectorStore()

    def ingest_resume(
        self,
        candidate_id: str,
        resume_text: str,
    ):
        chunks = self.chunker.split_resume(resume_text)

        embeddings = self.embedding_service.embed_documents(
            chunks
        )

        self.vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            candidate_id=candidate_id,
        )

        return {
            "candidate_id": candidate_id,
            "chunks": len(chunks),
        }