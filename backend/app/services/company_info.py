from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.company_info import CompanyInfo


def get_current_company_info(db: Session) -> Optional[CompanyInfo]:
    """
    Returns the latest CompanyInfo record.
    Adjust if you want to select by a specific id or flag instead.
    """
    return db.query(CompanyInfo).order_by(CompanyInfo.id.desc()).first()
