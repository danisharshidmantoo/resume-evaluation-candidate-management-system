from datetime import datetime
from typing import Optional

from bson import ObjectId

from app.core.database import get_db
from app.models.schemas import Candidate


COLLECTION = "candidates"


async def save_candidate(
    name: str,
    resume_text: str,
) -> str:
    """Save a candidate's resume information to MongoDB."""

    db = get_db()

    doc = {
        "name": name,
        "resume_text": resume_text,
        "created_at": datetime.utcnow(),
    }

    result = await db[COLLECTION].insert_one(doc)

    return str(result.inserted_id)


async def get_candidate(
    candidate_id: str,
) -> Optional[Candidate]:
    """Fetch a candidate from MongoDB by ID."""

    db = get_db()

    try:
        oid = ObjectId(candidate_id)
    except Exception:
        return None

    doc = await db[COLLECTION].find_one({"_id": oid})

    if not doc:
        return None

    doc["id"] = str(doc.pop("_id"))

    return Candidate(**doc)