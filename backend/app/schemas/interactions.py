# app/schemas/interactions.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: str
    lang: Optional[str] = None  # "en", "si", "ta"

class ChatResponse(BaseModel):
    reply: str
    user_id: str
    interaction_id: str
    properties: Optional[List[Dict]] = None  # lightweight cards for UI

# --- PDF Summary ---
class MessageItem(BaseModel):
    role: str  # "user" | "assistant"
    text: str
    ts: Optional[str] = None

class PDFSummaryRequest(BaseModel):
    name: str
    email: EmailStr
    messages: List[MessageItem]
    properties: Optional[List[Dict]] = None
