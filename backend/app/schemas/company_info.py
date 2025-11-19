from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class CompanyInfoBase(BaseModel):
    legal_name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class CompanyInfoRead(CompanyInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
