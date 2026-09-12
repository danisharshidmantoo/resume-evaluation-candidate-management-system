from app.services.embedding_service import embedding_service
from app.services.vector_store import ResumeVectorStore
from app.services import candidate_service

class CandidateRetrievalService:
    def __init__(self):
        self.embedding_service = embedding_service
        self.vector_store = ResumeVectorStore()

    def retrieve(self, job_description: str, top_k: int = 5):
        query_embedding = self.embedding_service.embed_query(
            job_description
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return results
    def rank_candidates(
        self,
        job_description: str,
        top_k: int = 20,
        chunks_per_candidate: int = 3,
    ):
        results = self.retrieve(
            job_description=job_description,
            top_k=top_k,
        )

        candidates = {}

        for metadata, distance in zip(
            results["metadatas"][0],
            results["distances"][0],
        ):
            candidate_id = metadata["candidate_id"]

            if candidate_id not in candidates:
                candidates[candidate_id] = []

            candidates[candidate_id].append(distance)

        ranked_candidates = []

        for candidate_id, distances in candidates.items():
            distances.sort()

            best_distances = distances[:chunks_per_candidate]

            average_distance = (
                sum(best_distances) / len(best_distances)
            )

            ranked_candidates.append(
                {
                    "candidate_id": candidate_id,
                    "distance": average_distance,
                    "matched_chunks": len(best_distances),
                }
            )

        ranked_candidates.sort(
            key=lambda candidate: candidate["distance"]
        )

        return ranked_candidates
    async def find_relevant_candidates(
        self,
        job_description: str,
        top_k: int = 20,
        chunks_per_candidate: int = 3,
    ):
        ranked_candidates = self.rank_candidates(
            job_description=job_description,
            top_k=top_k,
            chunks_per_candidate=chunks_per_candidate,
        )

        candidates = []

        for ranked_candidate in ranked_candidates:
            candidate = await candidate_service.get_candidate(
                ranked_candidate["candidate_id"]
            )

            if candidate:
                candidates.append(
                    {
                        "candidate_id": ranked_candidate["candidate_id"],
                        "name": candidate.name,
                        "distance": ranked_candidate["distance"],
                        "matched_chunks": ranked_candidate["matched_chunks"],
                    }
                )

        return candidates