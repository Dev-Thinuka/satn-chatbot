# backend/app/api/v1/leads.py

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.leads import LeadCreate, LeadRead
from app.services.lead_service import create_lead as create_lead_service

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", response_model=LeadRead, status_code=201)
def create_lead(
    payload: LeadCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Capture a lead from the chat widget or website:

    - Validates incoming data using `LeadCreate`.
    - Persists the lead into the `leads` table.
    - Triggers sales + user welcome emails via lead_service.
    - Returns the created lead as `LeadRead`.
    """
    lead = create_lead_service(db, payload)
    return lead
