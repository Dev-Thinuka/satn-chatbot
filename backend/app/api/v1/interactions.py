# backend/app/api/v1/interactions.py

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.interactions import InteractionCreate, InteractionRead
from app.services import interactions as interactions_service

router = APIRouter(
    prefix="/interactions",
    tags=["interactions"],
)


@router.post(
    "",
    response_model=InteractionRead,
    summary="Log a chatbot interaction",
)
def log_interaction(
    payload: InteractionCreate,
    db: Session = Depends(get_db),
):
    """
    Endpoint to log each chat turn.
    Chat frontend can call this after sending/receiving messages.
    """
    interaction = interactions_service.create_interaction(db, payload)
    return interaction


@router.get(
    "/session/{session_id}",
    response_model=List[InteractionRead],
    summary="List interactions for a session",
)
def list_interactions_for_session(
    session_id: str,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return interactions_service.get_interactions_for_session(
        db, session_id=session_id, limit=limit
    )
