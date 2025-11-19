from __future__ import annotations

import os
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

# Routers
from .api.v1.chat import router as chat_router

# If you have a PDF router, keep it; otherwise this try/except is harmless.
try:
    from .api.v1.pdf import router as pdf_router  # type: ignore
except Exception:
    pdf_router = None  # type: ignore

# If you already centralize DB session in another module, keep it.
# We reuse the chat router's get_db to avoid duplication here.
from .api.v1.chat import get_db  # reuse MVP get_db/engine

app = FastAPI(title="SATN Chatbot API", version="0.1.0")

# CORS for local dev and widget
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health
@app.get("/api/v1/healthz")
def healthz():
    return {"status": "ok"}

# DB check (you were getting 404—this adds it)
@app.get("/api/v1/dbcheck")
def dbcheck(db: Session = Depends(get_db)):
    val = db.execute(text("SELECT 1")).scalar_one()
    return {"db": "ok", "result": int(val)}

# Mount routers
app.include_router(chat_router)
if pdf_router:
    app.include_router(pdf_router)  # keeps your existing PDF endpoint

# Root
@app.get("/")
def root():
    return {"service": "SATN Chatbot API"}
