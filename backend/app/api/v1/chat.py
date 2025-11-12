# app/api/v1/chat.py
from __future__ import annotations
from typing import List, Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy import cast, Integer, Float
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...db.models.users import User
from ...db.models.interactions import Interaction
from ...db.models.properties import Property
from ...services.i18n import detect_lang, translate_to_en, translate_from_en
from ...services.mailer import send_sales_alert
from ...services.nlp import parse_intent
from ...schemas.interactions import ChatRequest, ChatResponse

router = APIRouter()

def _get_or_create_user(db: Session, name: str, email: str, phone: str | None) -> User:
    u = db.query(User).filter(User.email == email).first()
    if u:
        changed = False
        if phone and u.phone != phone: u.phone = phone; changed = True
        if name and u.name != name:   u.name = name;   changed = True
        if changed: db.commit(); db.refresh(u)
        return u
    u = User(name=name, email=email, phone=phone)
    db.add(u); db.commit(); db.refresh(u)
    send_sales_alert(name, email, phone)  # FR-10: first-time lead alert
    return u

def _search_properties(db: Session, slots) -> List[Dict[str, Any]]:
    """Builds a SQLAlchemy query over features JSON and columns."""
    q = db.query(Property)

    # keyword fallback
    if slots.location:
        ilike = f"%{slots.location}%"
        q = q.filter(Property.location.ilike(ilike))
    else:
        # try broader keyword match
        if slots.q:
            ilike = f"%{slots.q}%"
            q = q.filter((Property.title.ilike(ilike)) | (Property.location.ilike(ilike)))

    # JSONB feature filters
    beds_expr  = cast(Property.features["beds"].astext, Integer)
    baths_expr = cast(Property.features["baths"].astext, Integer)
    typ_expr   = Property.features["type"].astext

    if slots.beds_min is not None:
        q = q.filter(beds_expr >= slots.beds_min)
    if slots.baths_min is not None:
        q = q.filter(baths_expr >= slots.baths_min)
    if slots.ptype:
        q = q.filter(typ_expr.ilike(f"%{slots.ptype}%"))

    if slots.price_min is not None:
        q = q.filter(Property.price >= float(slots.price_min))
    if slots.price_max is not None and slots.price_max > 0:
        q = q.filter(Property.price <= float(slots.price_max))

    rows = q.order_by(Property.price.asc().nulls_last()).limit(12).all()
    return [
        {
            "id": str(r.id),
            "title": r.title,
            "description": r.description,
            "price": float(r.price) if r.price is not None else None,
            "location": r.location,
            "features": r.features or {},
            "agent_id": str(r.agent_id) if r.agent_id else None,
            # thumbnail optional later via ETL/media
        }
        for r in rows
    ]

def _compose_reply(slots, count: int) -> str:
    parts = []
    if count:
        parts.append(f"Found {count} option{'s' if count!=1 else ''}")
        if slots.location: parts.append(f"in {slots.location}")
        if slots.beds_min: parts.append(f"with ≥{slots.beds_min} bed(s)")
        if slots.price_max: parts.append(f"under {int(slots.price_max):,}")
        if slots.price_min and not slots.price_max: parts.append(f"from {int(slots.price_min):,}")
        return " ".join(parts) + ". Showing the top results."
    else:
        hint = []
        if not slots.location: hint.append("add a location")
        if not slots.beds_min: hint.append("set beds")
        if not (slots.price_min or slots.price_max): hint.append("include a budget")
        if hint:
            return f"Sorry, I couldn't find matching properties. Try to {', '.join(hint)}."
        return "Sorry, I couldn't find matching properties. Try adjusting your filters."

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # User & language
    user = _get_or_create_user(db, req.name, req.email, req.phone)
    user_lang = req.lang or detect_lang(req.message)

    # Translate -> EN (stub keeps text for now)
    text_en = translate_to_en(req.message, user_lang)

    # Parse slots and query DB
    slots = parse_intent(text_en)
    results = _search_properties(db, slots)
    reply_en = _compose_reply(slots, len(results))

    # Back-translate (stub)
    reply = translate_from_en(reply_en, user_lang)

    # Log interaction (FR-8)
    inter = Interaction(user_id=user.id, query_text=req.message, response_text=reply, lang=user_lang)
    db.add(inter); db.commit(); db.refresh(inter)

    # Trim results for widget (6)
    return ChatResponse(
        reply=reply,
        user_id=str(user.id),
        interaction_id=str(inter.id),
        properties=results[:6],
    )
