from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base

# doc_type: 'price_list' | 'brochure' | 'floor_plan' | 'floor_plan_gdrive' | 'pos' | 'video' (if file) | etc.
class ListingDocument(Base):
    __tablename__ = "listing_documents"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), index=True, nullable=False)

    doc_type = Column(String, nullable=False)
    remote_url = Column(String)             # WP media/file URL (or Google Drive URL)
    filename = Column(String)
    mime_type = Column(String)

    # Local cache (Option 2a)
    local_path = Column(String)
    downloaded_at = Column(DateTime)

    listing = relationship("Listing", back_populates="documents")
