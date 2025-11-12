from __future__ import annotations

from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...db.models.properties import Property

router = APIRouter()


def _to_float(val: Optional[Decimal]) -> Optional[float]:
    return float(val) if val is not None else None


@router.get("/properties")
def list_properties(
    q: Optional[str] = Query(None, description="Free text: title/location"),
    location: Optional[str] = Query(None, description="City/area contains"),
    min_beds: Optional[int] = Query(None, ge=0),
    min_baths: Optional[int] = Query(None, ge=0),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    property_type: Optional[str] = Query(None, alias="type", description='features->>"type"'),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Property)

    if q:
        like = f"%{q}%"
        query = query.filter((Property.title.ilike(like)) | (Property.location.ilike(like)))

    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))

    if min_beds is not None:
        query = query.filter(Property.beds >= min_beds)
    if min_baths is not None:
        query = query.filter(Property.baths >= min_baths)

    # Prefer price_from; fallback to price for ordering/filtering
    price_expr = func.coalesce(Property.price_from, Property.price)
    if min_price is not None:
        query = query.filter(price_expr >= min_price)
    if max_price is not None:
        query = query.filter(price_expr <= max_price)

    if property_type:
        query = query.filter((Property.features["type"].astext).ilike(property_type))

    rows = query.order_by(price_expr.nulls_last(), Property.title).limit(limit).all()

    def _row(r: Property) -> dict:
        return {
            "id": str(r.id),
            "title": r.title,
            "description": r.description,
            "price": _to_float(r.price),
            "price_from": _to_float(r.price_from),
            "location": r.location,
            "features": r.features or {},
            "beds": r.beds,
            "baths": r.baths,
            "car_spaces": r.car_spaces,
            "est_completion": r.est_completion,
            "video_url": r.video_url,
            "virtual_tour_url": r.virtual_tour_url,
            "brochure_url": r.brochure_url,
            "floor_plan_url": r.floor_plan_url,
            "price_list_url": r.price_list_url,
            "agent_id": str(r.agent_id) if r.agent_id is not None else None,
        }

    return [_row(r) for r in rows]
