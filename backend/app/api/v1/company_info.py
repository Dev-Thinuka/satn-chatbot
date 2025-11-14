# backend/app/api/v1/company_info.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.company_info import (
    CompanyInfoRead,
    CompanyInfoCreate,
    CompanyInfoUpdate,
)
from app.services import company_info as company_service

router = APIRouter(
    prefix="/company-info",
    tags=["company-info"],
)


@router.get("", response_model=CompanyInfoRead, summary="Get current company profile")
def get_company_info(
    db: Session = Depends(get_db),
):
    info = company_service.get_current_company_info(db)
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found",
        )
    return info


@router.post(
    "",
    response_model=CompanyInfoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create company profile",
)
def create_company_info(
    payload: CompanyInfoCreate,
    db: Session = Depends(get_db),
):
    info = company_service.create_company_info(db, payload)
    return info


@router.put(
    "/{info_id}",
    response_model=CompanyInfoRead,
    summary="Update company profile by ID",
)
def update_company_info(
    info_id: int,
    payload: CompanyInfoUpdate,
    db: Session = Depends(get_db),
):
    info = company_service.update_company_info(db, info_id, payload)
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found",
        )
    return info
