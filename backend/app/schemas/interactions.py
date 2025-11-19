# backend/app/schemas/interactions.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InteractionBase(BaseModel):
    session_id: str
    channel: str = "web_widget"   # web_widget, whatsapp, etc.
    language: Optional[str] = None  # 'en', 'si', 'ta'
    user_message: str
    bot_response: Optional[str] = None


class InteractionCreate(InteractionBase):
    user_id: Optional[int] = None
    agent_id: Optional[int] = None


class InteractionRead(InteractionBase):
    id: int
    created_at: datetime
    user_id: Optional[int] = None
    agent_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
