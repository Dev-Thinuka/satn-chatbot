from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Any, Dict, Optional

from sqlalchemy import Integer, String, Text, Numeric, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Property(Base):
    __tablename__ = "properties"

    # Core columns (existing)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()")
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Optional[Decimal]] = mapped_column(Numeric(14, 2), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    features: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True
    )

    # New attributes (typed so Pylance & FastAPI know them)
    price_from: Mapped[Optional[Decimal]] = mapped_column(Numeric(14, 2), nullable=True)
    beds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    baths: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    car_spaces: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    est_completion: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    video_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    virtual_tour_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    brochure_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    floor_plan_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price_list_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
