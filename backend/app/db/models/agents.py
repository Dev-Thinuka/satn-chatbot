# app/db/models/agents.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base, TimestampMixin


class Agent(TimestampMixin, Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True, index=True)
    phone = Column(String(50), nullable=True)
    region = Column(String(100), nullable=True)  # AU / LK / UAE etc.

    # Use string for relationship targets to avoid circular import issues
    interactions = relationship("Interaction", back_populates="agent")
