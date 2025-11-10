"""
Data cleanup utility — fix encoding, slugs, and HTML issues in existing listings.
Run manually when needed:  python -m app.services.fix_existing_listings
"""

import re
import html
from sqlalchemy import select
from app.db.session import SessionLocal
from app.db.models.listing import Listing


def clean_encoding(text: str) -> str:
    """Fix bad UTF-8 characters like â€“, â€™ etc."""
    if not text:
        return ""
    try:
        text = text.encode("latin1").decode("utf-8")
    except Exception:
        pass
    text = html.unescape(text)
    return text.strip()


def strip_html(raw_html: str) -> str:
    """Remove HTML tags for readability."""
    if not raw_html:
        return ""
    raw_html = html.unescape(raw_html)
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_slug(slug: str, wp_id: int) -> str:
    """Ensure slug is readable and unique."""
    if not slug or slug.isdigit():
        return f"listing-{wp_id}"
    return slug.strip()


def fix_listings():
    """Clean up existing listing records in the DB."""
    db = SessionLocal()
    try:
        listings = db.execute(select(Listing)).scalars().all()
        print(f"🧹 Found {len(listings)} listings to clean...")

        for listing in listings:
            # Fix slug
            listing.slug = normalize_slug(listing.slug, listing.wp_id)

            # Clean title and description fields
            listing.title = clean_encoding(listing.title)
            listing.description_html = clean_encoding(listing.description_html)
            listing.description_text = strip_html(listing.description_html)

            # Clean simple text fields
            if listing.region:
                listing.region = clean_encoding(listing.region)
            if listing.status:
                listing.status = clean_encoding(listing.status)

        db.commit()
        print("✅ Listings cleaned and updated successfully.")
    except Exception as e:
        db.rollback()
        print(f"❌ Error while cleaning listings: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🔧 Running database cleanup for existing listings...")
    fix_listings()
    print("🎉 Cleanup complete.")
