# backend/app/services/interactions.py
from __future__ import annotations

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.db.models.interactions import Interaction


def log_interaction(
    db: Session,
    *,
    session_id: str,
    user_message: str,
    bot_response: str,
    user_id: Optional[int] = None,
    language: str = "en",
    metadata: Optional[Dict[str, Any]] = None,
) -> Interaction:
    """
    Persist a single chatbot interaction to the database.
    """
    interaction = Interaction(
        session_id=session_id,
        user_id=user_id,
        user_message=user_message,
        bot_response=bot_response,
        language=language,
        metadata=metadata or {},
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction


def list_interactions_for_session(
    db: Session,
    session_id: str,
) -> List[Interaction]:
    """
    Return all interactions for a given session, ordered oldest → newest.
    """
    return (
        db.query(Interaction)
        .filter(Interaction.session_id == session_id)
        .order_by(Interaction.created_at.asc())
        .all()
    )
