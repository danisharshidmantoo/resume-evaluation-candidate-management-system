from fastapi import APIRouter
from app.core.database import get_db

router = APIRouter()


@router.get("/health", summary="Health check")
async def health():
    db = get_db()
    db_ok = False
    if db is not None:
        try:
            await db.command("ping")
            db_ok = True
        except Exception:
            pass
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "disconnected",
    }
