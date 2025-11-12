from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TIMESTAMP
from sqlalchemy import text
from ..base import Base

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    query_text = Column(VARCHAR, nullable=True)
    response_text = Column(VARCHAR, nullable=True)
    lang = Column(VARCHAR(8), nullable=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
