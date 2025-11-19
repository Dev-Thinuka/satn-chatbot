import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    source = Column(String, nullable=True, default="chatbot")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
