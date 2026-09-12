import chromadb


class ResumeVectorStore:
    def __init__(
        self,
        persist_directory: str = "data/chroma",
        collection_name: str = "candidate_resumes",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunks: list[str],
        embeddings,
        candidate_id: str,
    ):
        ids = [
            f"{candidate_id}_chunk_{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {
                "candidate_id": candidate_id,
                "chunk_index": index,
            }
            for index in range(len(chunks))
        ]

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding,
        top_k: int = 5,
    ):
        return self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )