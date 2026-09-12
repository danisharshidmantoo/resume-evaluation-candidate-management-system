import asyncio

from app.core.database import connect_db, close_db
from app.services.candidate_service import save_candidate, get_candidate


async def main():
    await connect_db()

    candidate_id = await save_candidate(
        name="Test Candidate",
        resume_text="Python developer with experience in FastAPI, MongoDB, and machine learning.",
    )

    print("Candidate ID:", candidate_id)

    candidate = await get_candidate(candidate_id)

    print("Candidate:", candidate)

    await close_db()


if __name__ == "__main__":
    asyncio.run(main())