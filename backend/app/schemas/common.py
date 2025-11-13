from typing import Optional

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(100, ge=1, le=1000)


class MessageResponse(BaseModel):
    message: str


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    language: Optional[str] = None  # 'en', 'si', 'ta'


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    language: str
