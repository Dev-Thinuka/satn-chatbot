# backend/app/api/v1/chat.py
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.llm import generate_neryx_answer

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


# --- Schemas ---


class AgentSummary(BaseModel):
    id: Optional[int] = None
    uuid: Optional[str] = None
    name: Optional[str] = None
    contact: Dict[str, Any] = Field(default_factory=dict)


class PropertyResult(BaseModel):
    id: Optional[int] = None
    uuid: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    price_from: Optional[float] = None
    location: Optional[str] = None
    features: Dict[str, Any] = Field(default_factory=dict)
    beds: Optional[int] = None
    baths: Optional[int] = None
    car_spaces: Optional[int] = None
    est_completion: Optional[str] = None
    video_url: Optional[str] = None
    virtual_tour_url: Optional[str] = None
    brochure: Optional[str] = None
    floor_plan: Optional[str] = None
    price_list: Optional[str] = None
    agent: Optional[AgentSummary] = None


class ChatRequest(BaseModel):
    text: str = Field(..., description="User's chat message")
    lang: str = Field(
        "en",
        description="Language code: 'en' (English), 'si' (Sinhala), 'ta' (Tamil)",
    )
    limit: int = Field(
        10,
        description="Max number of property results to return (for future RAG integration).",
    )


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Assistant's reply text")
    filters_used: Dict[str, Any] = Field(
        default_factory=dict,
        description="Any filters inferred from the query (future use).",
    )
    results: List[PropertyResult] = Field(
        default_factory=list,
        description="List of property results (future RAG integration).",
    )


# --- Endpoint ---


@router.post(
    "",
    response_model=ChatResponse,
    summary="Chat",
    description="Main chatbot endpoint. Currently uses OpenAI for NLP answers.",
)
def chat_endpoint(
    payload: ChatRequest,
    db: Session = Depends(get_db),  # kept for future logging / RAG, unused for now
) -> ChatResponse:
    """
    Chat with Neryx, backed by OpenAI.

    For now:
    - Uses OpenAI Responses API to generate a high-quality textual answer.
    - Does NOT yet query live property listings (results[] is empty).
    - Respects the 'lang' field for multilingual output.
    """

    # Normalize lang
    lang_str = payload.lang.lower().strip()
    if lang_str not in {"en", "si", "ta"}:
        lang_str = "en"
    lang: Literal["en", "si", "ta"] = lang_str  # type: ignore

    try:
        answer = generate_neryx_answer(payload.text, lang=lang)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream NLP error: {exc}",
        ) from exc

    return ChatResponse(
        answer=answer,
        filters_used={},
        results=[],
    )
