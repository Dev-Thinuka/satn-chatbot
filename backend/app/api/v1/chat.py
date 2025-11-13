from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple
from sqlalchemy import text
from sqlalchemy.orm import Session

# Adjust this import to match your project. In many SATN setups this exists:
from app.db import get_db  # -> returns SQLAlchemy Session


router = APIRouter(prefix="/api/v1", tags=["chat"])


# -----------------------------
# Request / Response schema
# -----------------------------
class ChatRequest(BaseModel):
    text: str = Field(..., description="User's query, e.g., '2 bed apartment in Sydney under 800k'")
    lang: Optional[str] = Field(default="en")
    limit: int = Field(default=10, ge=1, le=50)


class AgentOut(BaseModel):
    id: Optional[str]            # short code: "0001"
    uuid: Optional[str]
    name: Optional[str]
    contact: Optional[dict]


class PropertyOut(BaseModel):
    id: str                      # short code: "0001"
    uuid: str
    title: str
    description: Optional[str]
    price: Optional[float]
    price_from: Optional[float]
    location: Optional[str]
    features: Optional[dict]
    beds: Optional[int]
    baths: Optional[int]
    car_spaces: Optional[int]
    est_completion: Optional[str]
    video_url: Optional[str]
    virtual_tour_url: Optional[str]
    brochure: Optional[str]
    floor_plan: Optional[str]
    price_list: Optional[str]
    agent: Optional[AgentOut]


class ChatResponse(BaseModel):
    answer: str
    filters_used: dict
    results: List[PropertyOut]


# -----------------------------
# Intent parsing (simple MVP)
# -----------------------------
import re

TYPES = {"apartment", "house", "townhouse", "land"}

def parse_intent(q: str) -> Tuple[dict, Optional[str]]:
    """
    Extracts filters:
      - beds/baths/parking: numbers like '2 bed', '2 beds', '2br', '2 bath', 'parking'
      - price caps: 'under 800k', 'below 1.2m', '<= 950000'
      - type: apartment/house/townhouse/land
      - location tokens: rest words -> joined into LIKE query
    Returns (filters, like_query)
    """
    s = q.lower()

    # price e.g. "under 800k", "below 1.2m", "under 950000"
    max_price = None
    m = re.search(r"(under|below|<=?)\s*([0-9]+(?:\.[0-9]+)?)([kKmM])?", s)
    if m:
        num = float(m.group(2))
        mag = m.group(3)
        if mag and mag.lower() == "k":
            num *= 1_000
        elif mag and mag.lower() == "m":
            num *= 1_000_000
        max_price = int(num)

    # beds / baths / parking
    beds = None
    baths = None
    parking = None

    mb = re.search(r"(\d+)\s*(bed|beds|br)\b", s)
    if mb: beds = int(mb.group(1))
    mbath = re.search(r"(\d+)\s*(bath|baths|ba)\b", s)
    if mbath: baths = int(mbath.group(1))
    if "parking" in s:
        mp = re.search(r"(\d+)\s*(car|parking|space|spaces)", s)
        parking = int(mp.group(1)) if mp else 1  # default to at least 1 if unspecified

    # type
    ptype = None
    for t in TYPES:
        if t in s:
            ptype = t
            break

    # location tokens: remove recognized numeric bits & keywords, keep the rest
    cleaned = re.sub(r"(under|below|<=?)\s*\d+(?:\.\d+)?[kKmM]?", " ", s)
    cleaned = re.sub(r"\b(\d+)\s*(bed|beds|br|bath|baths|ba|car|space|spaces)\b", " ", cleaned)
    for kw in list(TYPES) + ["parking", "in", "with", "and", "under", "below"]:
        cleaned = cleaned.replace(kw, " ")
    loc = " ".join([w for w in re.split(r"[^a-z0-9]+", cleaned) if w and not w.isdigit()])
    likeq = f"%{loc.strip()}%" if loc.strip() else None

    filters = {
        "beds": beds,
        "baths": baths,
        "parking": parking,
        "max_price": max_price,
        "ptype": ptype,
    }
    return filters, likeq


# -----------------------------
# DB query + shaping
# -----------------------------
def _row_to_property(row: Mapping[str, Any]) -> dict:
    return {
        "id": row.get("property_id"),                     # short code "0001"
        "uuid": str(row.get("property_uuid")),
        "title": row.get("title"),
        "description": row.get("description"),
        "price": float(row["price"]) if row.get("price") is not None else None,
        "price_from": float(row["price_from"]) if row.get("price_from") is not None else None,
        "location": row.get("location"),
        "features": row.get("features"),
        "beds": row.get("beds"),
        "baths": row.get("baths"),
        "car_spaces": row.get("car_spaces"),
        "est_completion": row.get("est_completion"),
        "video_url": row.get("video_url"),
        "virtual_tour_url": row.get("virtual_tour_url"),
        "brochure": row.get("brochure"),
        "floor_plan": row.get("floor_plan"),
        "price_list": row.get("price_list"),
        "agent": {
            "id": row.get("agent_id"),                   # short code "0001"
            "uuid": str(row.get("agent_uuid")) if row.get("agent_uuid") else None,
            "name": row.get("agent_name"),
            "contact": row.get("agent_contact"),
        } if row.get("agent_uuid") or row.get("agent_name") else None
    }


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    filters, likeq = parse_intent(req.text)

    bind: Dict[str, Any] = {
        "likeq": likeq,
        "max_price": filters.get("max_price"),
        "beds": filters.get("beds"),
        "baths": filters.get("baths"),
        "parking": filters.get("parking"),
        "ptype": filters.get("ptype"),
        "limit": req.limit,
    }

    sql = text("""
SELECT
  p.id                        AS property_uuid,
  lpad(p.code::text,4,'0')    AS property_id,
  p.title,
  p.description,
  p.price,
  p.price_from,
  p.location,
  p.features,
  p.beds, p.baths, p.car_spaces, p.est_completion,
  p.video_url, p.virtual_tour_url, p.brochure, p.floor_plan, p.price_list,
  a.id                        AS agent_uuid,
  lpad(a.code::text,4,'0')    AS agent_id,
  a.name                      AS agent_name,
  a.contact_info              AS agent_contact
FROM public.properties p
LEFT JOIN public.agents a ON a.id = p.agent_id
WHERE
  (:likeq IS NULL OR p.location ILIKE :likeq OR p.title ILIKE :likeq)
  AND (:max_price IS NULL OR p.price <= CAST(:max_price AS numeric))
  AND (:beds     IS NULL OR p.beds       >= CAST(:beds     AS integer))
  AND (:baths    IS NULL OR p.baths      >= CAST(:baths    AS integer))
  AND (:parking  IS NULL OR p.car_spaces >= CAST(:parking  AS integer))
  AND (:ptype    IS NULL OR lower(COALESCE(p.features->>'type','')) = lower(:ptype))
ORDER BY p.price ASC NULLS LAST
LIMIT :limit
""")

    try:
        rows: Sequence[Mapping[str, Any]] = db.execute(sql, bind).mappings().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

    results = [_row_to_property(r) for r in rows]

    # Simple natural-language answer (MVP)
    answer_bits = []
    if filters.get("beds"):      answer_bits.append(f"{filters['beds']}+ bed")
    if filters.get("baths"):     answer_bits.append(f"{filters['baths']}+ bath")
    if filters.get("parking"):   answer_bits.append(f"{filters['parking']}+ parking")
    if filters.get("max_price"): answer_bits.append(f"≤ {filters['max_price']:,}")
    if filters.get("ptype"):     answer_bits.append(filters['ptype'])
    if likeq:                    answer_bits.append(f"in {likeq.strip('%')}")
    answer = f"Found {len(results)} result(s)" + (": " + ", ".join(answer_bits) if answer_bits else "")

    resp = {
        "answer": answer,
        "filters_used": {k:v for k,v in filters.items() if v is not None} | ({"location_like": likeq} if likeq else {}),
        "results": results
    }
    return ChatResponse(**resp)
