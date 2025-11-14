# backend/app/services/interactions.py

from typing import List, Optional

from sqlalchemy.orm import Session

from app.db.models.interactions import Interaction
from app.schemas.interactions import InteractionCreate


def create_interaction(
    db: Session,
    interaction_in: InteractionCreate,
) -> Interaction:
    data = interaction_in.model_dump()
    interaction = Interaction(**data)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def get_interactions_for_session(
    db: Session,
    session_id: str,
    limit: int = 100,
) -> List[Interaction]:
    return (
        db.query(Interaction)
        .filter(Interaction.session_id == session_id)
        .order_by(Interaction.created_at.asc())
        .limit(limit)
        .all()
    )


def get_interaction(
    db: Session,
    interaction_id: int,
) -> Optional[Interaction]:
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()
