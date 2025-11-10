"""
ETL (Extract, Transform, Load) service — sync listings from WordPress to PostgreSQL.
Enhanced for encoding fixes, slug normalization, and clean text handling.
"""

import os
import re
import html
import time
import requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from typing import Optional, Dict, Any, List

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.models.listing import Listing

# Ensure database tables exist
Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

WP_API_URL = os.getenv("WP_API_URL")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

PER_PAGE = 50
TIMEOUT = 30


# -------------------------------
# Utility Functions
# -------------------------------

def clean_encoding(text: Optional[str]) -> str:
    """Fix encoding issues like â€“, â€™, etc. and normalize UTF-8."""
    if not text:
        return ""
    try:
        # Attempt to correct mis-decoded UTF-8 text
        text = text.encode("latin1").decode("utf-8")
    except Exception:
        pass
    return text


def strip_html(raw_html: Optional[str]) -> str:
    """Convert HTML content to plain text."""
    if not raw_html:
        return ""
    raw_html = html.unescape(raw_html)
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_slug(slug: Optional[str], wp_id: int) -> str:
    """Ensure slug is usable (non-numeric, non-empty)."""
    if not slug or slug.isdigit():
        return f"listing-{wp_id}"
    return slug.strip()


def safe_get(obj: Dict, path: List[str], default=None):
    """Safely navigate nested dicts."""
    for key in path:
        if not isinstance(obj, dict) or key not in obj:
            return default
        obj = obj[key]
    return obj


# -------------------------------
# Database Setup
# -------------------------------

def init_db():
    """Ensure listings table exists before sync."""
    Base.metadata.create_all(bind=engine)


# -------------------------------
# Transformation Logic
# -------------------------------

def transform(item: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize fields from WordPress JSON."""
    title = clean_encoding(strip_html(item.get("title", {}).get("rendered")))
    content_html = clean_encoding(item.get("content", {}).get("rendered", ""))

    embedded = item.get("_embedded", {})
    featured = embedded.get("wp:featuredmedia", [])
    attachments = embedded.get("wp:attachment", [])
    terms = embedded.get("wp:term", [])

    featured_image = featured[0]["source_url"] if featured else None
    gallery = [a.get("source_url") for a in attachments if a.get("source_url")]

    regions = []
    categories = []
    for group in terms:
        for t in group:
            if t.get("taxonomy") == "hp_listing_region":
                regions.append(clean_encoding(t["name"]))
            elif t.get("taxonomy") == "hp_listing_category":
                categories.append(clean_encoding(t["name"]))

    slug = normalize_slug(item.get("slug"), item.get("id"))

    return {
        "wp_id": item["id"],
        "slug": slug,
        "status": item.get("status"),
        "title": title,
        "description_html": content_html,
        "description_text": clean_encoding(strip_html(content_html)),
        "permalink": item.get("link"),
        "region": regions[0] if regions else None,
        "categories": categories or None,
        "featured_image_url": featured_image,
        "gallery_image_urls": gallery or None,
        "wp_created": item.get("date"),
        "wp_modified": item.get("modified"),
    }


# -------------------------------
# Database Upsert Logic
# -------------------------------

def upsert_listings(records: List[Dict[str, Any]]):
    """Insert or update listings based on wp_id."""
    db = SessionLocal()
    try:
        for record in records:
            existing = db.execute(
                select(Listing).where(Listing.wp_id == record["wp_id"])
            ).scalar_one_or_none()

            if existing:
                for k, v in record.items():
                    setattr(existing, k, v)
            else:
                db.add(Listing(**record))

        db.commit()
        print(f"✅ Upserted {len(records)} records.")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"❌ Database error: {e}")
    finally:
        db.close()


# -------------------------------
# WordPress Fetching
# -------------------------------

def fetch_page(page: int) -> List[Dict[str, Any]]:
    """Fetch one paginated page from WP API."""
    params = {"per_page": PER_PAGE, "page": page, "_embed": "true", "status": "publish"}
    resp = requests.get(
        WP_API_URL, auth=(WP_USER, WP_APP_PASSWORD), params=params, timeout=TIMEOUT
    )
    resp.encoding = "utf-8"  # Ensure correct decoding
    resp.raise_for_status()
    return resp.json(), int(resp.headers.get("X-WP-TotalPages", 1))


# -------------------------------
# Sync Runner
# -------------------------------

def run_full_sync():
    """Run full ETL synchronization from WP → PostgreSQL."""
    print("🚀 Starting WordPress → PostgreSQL sync...")
    init_db()

    first_page, total_pages = fetch_page(1)
    upsert_listings([transform(item) for item in first_page])

    if total_pages > 1:
        for page in range(2, total_pages + 1):
            time.sleep(0.3)
            print(f"📦 Fetching page {page}/{total_pages}...")
            items, _ = fetch_page(page)
            upsert_listings([transform(item) for item in items])

    print("🎉 Sync complete.")
