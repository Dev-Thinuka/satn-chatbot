# app/db/models/interactions.py

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from .base import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    channel = Column(String(50), nullable=False, default="web_widget")  # web_widget, whatsapp, etc.
    language = Column(String(10), nullable=True)  # 'en', 'si', 'ta'
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship targets as strings to avoid forward-reference/type issues
    user = relationship("User", back_populates="interactions")
    agent = relationship("Agent", back_populates="interactions")
