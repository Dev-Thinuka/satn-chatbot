"""
Listing model for SA Thomson Nerys real estate chatbot.
Represents WordPress property listings stored locally.
"""

from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from app.db.base import Base

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    wp_id = Column(Integer, unique=True, nullable=False)
    slug = Column(String, index=True)
    status = Column(String, nullable=True)  # 👈 NEW LINE ADDED
    title = Column(String, nullable=False)
    description_html = Column(Text, nullable=True)
    description_text = Column(Text, nullable=True)
    permalink = Column(String, nullable=True)
    region = Column(String, nullable=True)
    categories = Column(JSON, nullable=True)
    featured_image_url = Column(String, nullable=True)
    gallery_image_urls = Column(JSON, nullable=True)
    wp_created = Column(DateTime, nullable=True)
    wp_modified = Column(DateTime, nullable=True)


    def __repr__(self):
        return f"<Listing(id={self.id}, wp_id={self.wp_id}, title='{self.title}')>"
