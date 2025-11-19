# backend/app/services/intent.py
from __future__ import annotations
import re
from typing import Dict, Optional

_NUM_RE = re.compile(r"(?<!\d)(\d+(\.\d+)?)(\s*[kKmM])?(?!\d)")
_BEDS_RE = re.compile(r"\b(\d+)\s*(beds?|br|bedrooms?)\b", re.I)
_BATHS_RE = re.compile(r"\b(\d+)\s*(baths?|ba|bathrooms?)\b", re.I)
_PARK_RE = re.compile(r"\b(\d+)\s*(car\s*spaces?|parking|parks?)\b", re.I)
_TYPE_WORDS = {
    "apartment": {"apartment", "apt", "flat", "condo", "studio"},
    "house": {"house", "home"},
    "villa": {"villa"},
    "land": {"land", "plot"},
    "office": {"office", "commercial"},
    "townhouse": {"townhouse", "town-home", "town home"},
}

def _parse_money_token(tok: str) -> Optional[float]:
    """
    Convert tokens like '800', '800k', '1.2m' to a float price in the same currency units as DB (assumed to be AUD/LKR/AED amounts; we just keep number).
    """
    m = _NUM_RE.fullmatch(tok.strip())
    if not m:
        return None
    val = float(m.group(1))
    suf = (m.group(3) or "").strip().lower()
    if suf == "k":
        val *= 1_000
    elif suf == "m":
        val *= 1_000_000
    return val

def parse_filters(text: str) -> Dict:
    """
    Extract a minimal set of structured filters from free text.

    Returns:
        {
          'beds': int|None, 'baths': int|None, 'parking': int|None,
          'type': str|None,
          'max_price': float|None, 'min_price': float|None,
          'location_q': str|None,
          'terms': str,
        }
    """
    t = (text or "").strip()
    out: Dict[str, Optional[object]] = {
        "beds": None, "baths": None, "parking": None,
        "type": None, "max_price": None, "min_price": None,
        "location_q": None, "terms": t
    }
    if not t:
        return out

    # Beds / baths / car spaces
    m = _BEDS_RE.search(t)
    if m: out["beds"] = int(m.group(1))

    m = _BATHS_RE.search(t)
    if m: out["baths"] = int(m.group(1))

    m = _PARK_RE.search(t)
    if m: out["parking"] = int(m.group(1))

    # Simple price language
    lower = t.lower()
    # between X and Y
    btw = re.search(r"between\s+([0-9\.]+\s*[kKmM]?)\s+and\s+([0-9\.]+\s*[kKmM]?)", lower)
    if btw:
        p1 = _parse_money_token(btw.group(1))
        p2 = _parse_money_token(btw.group(2))
        if p1 is not None and p2 is not None:
            out["min_price"], out["max_price"] = min(p1, p2), max(p1, p2)
    else:
        # under / below
        under = re.search(r"(under|below|<=?)\s*([0-9\.]+\s*[kKmM]?)", lower)
        if under:
            p = _parse_money_token(under.group(2))
            if p is not None: out["max_price"] = p
        # over / above
        over = re.search(r"(over|above|>=?)\s*([0-9\.]+\s*[kKmM]?)", lower)
        if over:
            p = _parse_money_token(over.group(2))
            if p is not None: out["min_price"] = p
        # plain “<number> budget” style
        budget = re.search(r"(budget|around|approx)\s*([0-9\.]+\s*[kKmM]?)", lower)
        if budget and out["max_price"] is None:
            p = _parse_money_token(budget.group(2))
            if p is not None: out["max_price"] = p

    # Property type
    words = {w.strip(".,;:!()[]{}").lower() for w in t.split()}
    for typ, synonyms in _TYPE_WORDS.items():
        if words & synonyms:
            out["type"] = typ
            break

    # Naive location hint = everything left that isn't type/keyword
    # We’ll just re-use the whole query for ILIKE unless it’s super short.
    out["location_q"] = t if len(t) >= 3 else None
    return out

def filters_to_english(f: Dict) -> str:
    parts = []
    if f.get("type"): parts.append(f.get("type"))
    if f.get("beds"): parts.append(f'{int(f["beds"])}+ bed')
    if f.get("baths"): parts.append(f'{int(f["baths"])}+ bath')
    if f.get("parking"): parts.append(f'{int(f["parking"])}+ parking')
    if f.get("min_price") and f.get("max_price"):
        parts.append(f'{int(f["min_price"]):,}–{int(f["max_price"]):,}')
    elif f.get("max_price"):
        parts.append(f'≤ {int(f["max_price"]):,}')
    elif f.get("min_price"):
        parts.append(f'≥ {int(f["min_price"]):,}')
    if f.get("location_q"):
        parts.append(f'in “{f["location_q"]}”')
    return ", ".join(parts) or "your criteria"
