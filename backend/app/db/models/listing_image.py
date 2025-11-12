from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base

class ListingImage(Base):
    __tablename__ = "listing_images"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), index=True, nullable=False)

    # From WP
    remote_url = Column(String, nullable=False)
    alt_text = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    position = Column(Integer, default=0)     # gallery order
    is_featured = Column(Boolean, default=False)

    # Local cache (Option 2a)
    local_path = Column(String)               # e.g., /data/media/listings/<wp_id>/<filename>
    mime_type = Column(String)
    downloaded_at = Column(DateTime)

    listing = relationship("Listing", back_populates="images")
