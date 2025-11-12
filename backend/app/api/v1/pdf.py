# app/api/v1/pdf.py
from __future__ import annotations

from fastapi import APIRouter, Response
from ...schemas.interactions import PDFSummaryRequest      # <-- three dots
from ...services.pdfs import make_chat_transcript_pdf

router = APIRouter()

@router.post("/pdf/summary", response_class=Response)
def generate_pdf(req: PDFSummaryRequest):
    """
    Returns a PDF (application/pdf) of the provided chat transcript + optional properties.
    Body: { name, email, messages: [{role,text,ts?}], properties?: [...] }
    """
    pdf_bytes = make_chat_transcript_pdf(
        name=req.name,
        email=req.email,
        messages=[msg.dict() for msg in req.messages],
        properties=req.properties or [],
    )
    headers = {"Content-Disposition": 'attachment; filename="satn-chat-summary.pdf"'}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
