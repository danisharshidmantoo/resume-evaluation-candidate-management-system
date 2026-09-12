import asyncio

from app.core.database import connect_db, close_db, get_db
from app.services.resume_chunker import ResumeChunker


async def main():
    await connect_db()

    db = get_db()

    candidate = await db["candidates"].find_one(
        {"name": "Danish Arshid"}
    )

    if not candidate:
        print("Candidate not found.")
        await close_db()
        return

    chunker = ResumeChunker()

    chunks = chunker.split_resume(candidate["resume_text"])

    print("Number of chunks:", len(chunks))

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk)
        print("Length:", len(chunk))

    await close_db()


if __name__ == "__main__":
    asyncio.run(main())