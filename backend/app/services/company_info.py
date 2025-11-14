# backend/app/services/company_info.py

from typing import Optional

from sqlalchemy.orm import Session

from app.db.models.company_info import CompanyInfo
from app.schemas.company_info import CompanyInfoCreate, CompanyInfoUpdate


def get_current_company_info(db: Session) -> Optional[CompanyInfo]:
    """
    Returns the latest company info record.
    Adjust logic as needed (e.g. always id=1).
    """
    return db.query(CompanyInfo).order_by(CompanyInfo.id.desc()).first()


def create_company_info(db: Session, info_in: CompanyInfoCreate) -> CompanyInfo:
    info = CompanyInfo(**info_in.model_dump())
    db.add(info)
    db.commit()
    db.refresh(info)
    return info


def update_company_info(
    db: Session,
    info_id: int,
    info_in: CompanyInfoUpdate,
) -> Optional[CompanyInfo]:
    info = db.query(CompanyInfo).filter(CompanyInfo.id == info_id).first()
    if not info:
        return None

    update_data = info_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(info, field, value)

    db.add(info)
    db.commit()
    db.refresh(info)
    return info
