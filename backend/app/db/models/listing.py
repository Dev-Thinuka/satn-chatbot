"""
Listing model for SA Thomson Nerys real estate chatbot.
Represents WordPress property listings stored locally.

"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, JSON, Numeric
)
from sqlalchemy.orm import relationship
from app.db.session import Base, engine
Base.metadata.create_all(bind=engine)


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    wp_id = Column(Integer, unique=True, nullable=False)
    slug = Column(String, index=True)
    status = Column(String)
    title = Column(String, nullable=False)

    # Existing description/permalink/region info
    description_html = Column(Text)
    description_text = Column(Text)
    permalink = Column(String)
    region = Column(String)
    categories = Column(JSON)             # list of strings
    featured_image_url = Column(String)   # kept for backward compatibility
    gallery_image_urls = Column(JSON)     # kept for backward compatibility
    wp_created = Column(DateTime)
    wp_modified = Column(DateTime)

    # NEW – common, structured attributes (appear in your WP UI)
    listing_type = Column(String)         # Apartments | Townhomes | House and Land | Commercial
    location = Column(String)             # simple text (suburb/area)
    price_from = Column(Numeric(asdecimal=False))   # e.g., 705000 -> 705000.0
    beds = Column(Integer)
    baths = Column(Integer)
    car_spaces = Column(Integer)
    completed_percent = Column(Integer)   # 0..100
    est_completion = Column(String)       # free text like "Q4 2026"
    address = Column(String)
    video_url = Column(String)
    virtual_tour_url = Column(String)
    last_modified_note = Column(String)   # “Last Modified (optional)” free text

    # Flexible bag for category-specific attributes (zoning, land size, packages, etc.)
    attributes = Column(JSON)             # JSON dict
    image_url = Column(String, nullable=True)
    # NEW relationships
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")
    documents = relationship("ListingDocument", back_populates="listing", cascade="all, delete-orphan")
