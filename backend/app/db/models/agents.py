from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, JSONB, VARCHAR
from sqlalchemy import text
from ..base import Base

class Agent(Base):
    __tablename__ = "agents"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(VARCHAR, nullable=False)
    contact_info = Column(JSONB, nullable=True)
    role = Column(VARCHAR, nullable=True)
