from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.leads import LeadCreate
from app.db.session import get_db
from app.services.lead_service import create_lead as create_lead_service

router = APIRouter()


@router.post("/leads", response_model=dict)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    """
    Chatbot lead capture endpoint.

    - Saves the lead to the database.
    - Triggers sales alert + welcome email via lead_service.
    """
    lead = create_lead_service(db=db, data=payload)
    return {"lead_id": str(lead.id)}
