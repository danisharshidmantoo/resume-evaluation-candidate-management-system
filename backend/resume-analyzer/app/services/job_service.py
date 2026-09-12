from datetime import datetime
from typing import Optional

from bson import ObjectId

from app.core.database import get_db
from app.models.schemas import Job


COLLECTION = "jobs"


async def save_job(title: str, job_description: str) -> str:
    db = get_db()

    doc = {
        "title": title,
        "job_description": job_description,
        "created_at": datetime.utcnow(),
    }

    result = await db[COLLECTION].insert_one(doc)

    return str(result.inserted_id)


async def get_job(job_id: str) -> Optional[Job]:
    db = get_db()

    try:
        oid = ObjectId(job_id)
    except Exception:
        return None

    doc = await db[COLLECTION].find_one({"_id": oid})

    if not doc:
        return None

    doc["id"] = str(doc.pop("_id"))

    return Job(**doc)