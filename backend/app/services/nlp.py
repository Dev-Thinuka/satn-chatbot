# app/services/nlp.py
"""
Lightweight NLP for property search:
- Language detection (langdetect)
- Rule-based intent + slot extraction (beds, baths, type, price, location, keyword)
- Optional LLM fallback later (plug at TODO)
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Optional

from langdetect import detect


ROOM_RX   = re.compile(r"\b(?P<num>\d+)\s*(bed|bedroom)s?\b", re.I)
BATH_RX   = re.compile(r"\b(?P<num>\d+)\s*(bath|bathroom)s?\b", re.I)
TYPE_RX   = re.compile(r"\b(apartment|apt|studio|unit|villa|house|townhouse|land|condo)\b", re.I)
BETWEEN_RX= re.compile(r"\b(between|from)\s*(?P<a>[\d\.,]+)\s*(k|m|million)?\s*(and|to)\s*(?P<b>[\d\.,]+)\s*(k|m|million)?", re.I)
UNDER_RX  = re.compile(r"\b(under|below|max|<=|less than)\s*(?P<val>[\d\.,]+)\s*(k|m|million)?", re.I)
OVER_RX   = re.compile(r"\b(over|above|min|>=|more than)\s*(?P<val>[\d\.,]+)\s*(k|m|million)?", re.I)
IN_RX     = re.compile(r"\b(in|at|around)\s+(?P<place>[a-zA-Z\s]{2,})\b", re.I)

KNOWN_PLACES = [
    "Sydney", "Parramatta", "Colombo", "Dubai",
    "NSW", "Queensland", "Melbourne", "Perth", "Adelaide",
    "Sri Lanka", "Colombo 07", "Colombo 03",
]

def _to_amount(s: str) -> float:
    raw = s.replace(",", "").strip().lower()
    mult = 1.0
    if raw.endswith("m") or "million" in raw:
        mult = 1_000_000.0
        raw = raw.replace("m", "").replace("million", "").strip()
    elif raw.endswith("k"):
        mult = 1_000.0
        raw = raw[:-1]
    try:
        return float(raw) * mult
    except Exception:
        return 0.0

@dataclass
class SearchIntent:
    q: Optional[str] = None
    location: Optional[str] = None
    beds_min: Optional[int] = None
    baths_min: Optional[int] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    ptype: Optional[str] = None
    lang: str = "en"

def detect_language(text: str) -> str:
    try:
        code = detect(text or "")
        if code.startswith("si"): return "si"
        if code.startswith("ta"): return "ta"
        return "en"
    except Exception:
        return "en"

def parse_intent(text: str) -> SearchIntent:
    t = text or ""
    lang = detect_language(t)
    intent = SearchIntent(lang=lang)

    # type
    m = TYPE_RX.search(t)
    if m:
        typ = m.group(1).lower()
        intent.ptype = {"apt": "apartment"}.get(typ, typ)

    # beds & baths
    m = ROOM_RX.search(t)
    if m:
        intent.beds_min = int(m.group("num"))
    m = BATH_RX.search(t)
    if m:
        intent.baths_min = int(m.group("num"))

    # price
    m = BETWEEN_RX.search(t)
    if m:
        intent.price_min = _to_amount(m.group("a"))
        intent.price_max = _to_amount(m.group("b"))
    m = UNDER_RX.search(t)
    if m:
        intent.price_max = _to_amount(m.group("val"))
    m = OVER_RX.search(t)
    if m:
        intent.price_min = _to_amount(m.group("val"))

    # location (prefer "in X", else match known)
    m = IN_RX.search(t)
    if m:
        intent.location = m.group("place").strip()
    else:
        for place in KNOWN_PLACES:
            if place.lower() in t.lower():
                intent.location = place
                break

    # fallback free-text
    intent.q = t.strip()
    return intent
