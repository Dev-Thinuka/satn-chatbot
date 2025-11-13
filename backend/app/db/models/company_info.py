# app/db/models/company_info.py

from sqlalchemy import Column, Integer, String, Text

from .base import Base, TimestampMixin


class CompanyInfo(TimestampMixin, Base):
    __tablename__ = "company_info"

    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String(255), nullable=False)
    short_name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    website_url = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
