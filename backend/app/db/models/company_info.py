from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID, JSONB, VARCHAR
from sqlalchemy import text
from ..base import Base

class CompanyInfo(Base):
    __tablename__ = "company_info"
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    about = Column(VARCHAR, nullable=True)
    contact = Column(JSONB, nullable=True)
    branches = Column(JSONB, nullable=True)
