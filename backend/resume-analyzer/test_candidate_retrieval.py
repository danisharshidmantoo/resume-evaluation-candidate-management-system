import asyncio

from app.core.database import connect_db
from app.services.candidate_retrieval import CandidateRetrievalService


job_description = """
We are looking for a Machine Learning Engineer with experience in
Python, TensorFlow, computer vision, machine learning model development,
data preprocessing, model evaluation, and deployment. Experience with
OpenCV, NumPy, Pandas, and Scikit-learn is preferred.
"""


async def main():
    await connect_db()

    service = CandidateRetrievalService()

    candidates = await service.find_relevant_candidates(
        job_description=job_description,
        top_k=20,
        chunks_per_candidate=3,
    )

    print("\n=== Relevant Candidates ===")

    for rank, candidate in enumerate(candidates, start=1):
        print(
            f"{rank}. "
            f"{candidate['name']} | "
            f"candidate_id={candidate['candidate_id']} | "
            f"distance={candidate['distance']:.4f} | "
            f"matched_chunks={candidate['matched_chunks']}"
        )


if __name__ == "__main__":
    asyncio.run(main())