# backend/app/services/lead_service.py

from typing import Optional, cast

from sqlalchemy.orm import Session

from app.db.models.leads import Lead
from app.schemas.leads import LeadCreate
from app.services.email_service import send_welcome_email


def create_lead(db: Session, data: LeadCreate) -> Lead:
    """
    Create a new lead in the database and trigger notification emails.

    Called from /api/v1/leads endpoint. It:
    - Inserts a row into the `leads` table.
    - Sends a welcome email to the user via SendGrid template.
    """

    # Persist to DB – NOTE: no `name` field, only first_name / last_name
    lead = Lead(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        source=data.source or "chatbot",
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    # ---- Make Pylance happy with explicit casting ----
    # At runtime these are strings, but the type checker sees Column[str].
    email_val: str = cast(str, lead.email)
    first_name_val: Optional[str] = cast(Optional[str], lead.first_name)
    last_name_val: Optional[str] = cast(Optional[str], lead.last_name)

    # ---- Fire-and-forget welcome email; never crash the API on email failure ----
    try:
        send_welcome_email(
            to_email=email_val,
            first_name=first_name_val,
            last_name=last_name_val,
        )
    except Exception:
        # TODO: replace with proper logging, e.g.:
        # logger.exception("Failed to send welcome email for lead %s", lead.id)
        pass

    return lead
