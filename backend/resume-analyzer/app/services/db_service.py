from datetime import datetime
from typing import List, Optional
from bson import ObjectId

from app.core.database import get_db
from app.models.schemas import AnalysisResult, AnalysisListItem

COLLECTION = "analyses"


def _serialize(doc: dict) -> dict:
    """Convert MongoDB _id to string id."""
    if doc and "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


async def save_analysis(result: AnalysisResult, user_id: Optional[str] = None) -> str:
    """Persist analysis result to MongoDB. Returns inserted document ID."""
    db = get_db()
    doc = result.model_dump(exclude={"id"})
    doc["created_at"] = datetime.utcnow()
    if user_id:
        doc["user_id"] = user_id

    inserted = await db[COLLECTION].insert_one(doc)
    return str(inserted.inserted_id)


async def get_analysis(analysis_id: str) -> Optional[AnalysisResult]:
    """Fetch a single analysis by ID."""
    db = get_db()
    try:
        oid = ObjectId(analysis_id)
    except Exception:
        return None

    doc = await db[COLLECTION].find_one({"_id": oid})
    if not doc:
        return None

    return AnalysisResult(**_serialize(doc))


async def list_analyses(
    user_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> List[AnalysisListItem]:
    """List analyses, optionally filtered by user_id."""
    db = get_db()
    query = {"user_id": user_id} if user_id else {}
    projection = {
        "candidateName": 1,
        "overallScore": 1,
        "verdict": 1,
        "created_at": 1,
    }
    cursor = (
        db[COLLECTION]
        .find(query, projection)
        .sort("created_at", -1)
        .skip(skip)
        .limit(limit)
    )
    items = []
    async for doc in cursor:
        _serialize(doc)
        items.append(AnalysisListItem(**doc))
    return items


async def delete_analysis(analysis_id: str) -> bool:
    """Delete an analysis by ID. Returns True if deleted."""
    db = get_db()
    try:
        oid = ObjectId(analysis_id)
    except Exception:
        return False
    result = await db[COLLECTION].delete_one({"_id": oid})
    return result.deleted_count > 0
