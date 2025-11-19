# backend/app/schemas/chat.py
from typing import List, Optional
from pydantic import BaseModel


class ChatHistoryItem(BaseModel):
  role: str  # "user" or "assistant"
  content: str


class ChatRequest(BaseModel):
  text: str
  lang: str = "en"
  limit: int = 5
  name: Optional[str] = None
  email: Optional[str] = None
  phone: Optional[str] = None
  history: List[ChatHistoryItem] = []


class PropertyFeatures(BaseModel):
  beds: Optional[int] = None
  baths: Optional[int] = None
  parking: Optional[int] = None
  size_sqm: Optional[int] = None
  image_url: Optional[str] = None
  type: Optional[str] = None


class PropertyOut(BaseModel):
  id: str
  title: str
  description: Optional[str] = None
  price: Optional[float] = None
  location: Optional[str] = None
  features: Optional[PropertyFeatures] = None

  class Config:
    orm_mode = True


class ChatResponse(BaseModel):
  answer: str
  results: List[PropertyOut] = []
  quick_replies: List[str] = []
