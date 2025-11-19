from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr


class LeadBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    source: Optional[str] = "chatbot"


class LeadCreate(LeadBase):
    pass


class LeadRead(LeadBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2
