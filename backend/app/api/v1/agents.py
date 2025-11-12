from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ...db.session import get_db
from ...db.models.agents import Agent

router = APIRouter()

@router.get("/agents")
def list_agents(db: Session = Depends(get_db)):
    try:
        rows = db.execute(select(Agent).order_by(Agent.name)).scalars().all()
        return [
            {"id": str(r.id), "name": r.name, "role": r.role, "contact_info": r.contact_info or {}}
            for r in rows
        ]
    except Exception as e:
        # Surface the cause during dev; in prod, log and return generic error
        raise HTTPException(status_code=500, detail=f"/agents failed: {type(e).__name__}: {e}")
