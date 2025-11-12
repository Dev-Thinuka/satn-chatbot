from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...db.session import get_db

router = APIRouter()

@router.get("/dbcheck")
def dbcheck(db: Session = Depends(get_db)):
    """
    Runs a trivial SQL to ensure connectivity and that seed tables exist.
    Returns row counts for quick sanity checks.
    """
    try:
        counts = {}
        for tbl in ("agents", "properties", "users", "interactions"):
            res = db.execute(text(f"SELECT COUNT(*) FROM {tbl}")).scalar_one()
            counts[tbl] = int(res)
        return {"ok": True, "counts": counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB check failed: {type(e).__name__}: {e}")
