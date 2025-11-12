from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TIMESTAMP
from ..base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, unique=True, nullable=False)
    phone = Column(VARCHAR, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
