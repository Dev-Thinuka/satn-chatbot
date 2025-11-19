# backend/app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.api.v1.chat import router as chat_router
from app.api.v1.agents import router as agents_router
from app.api.v1.company_info import router as company_info_router
from app.api.v1.interactions import router as interactions_router

# backend/app/main.py (only the relevant parts)
from fastapi import Depends
from app.services.lead_service import create_lead
from app.schemas.leads import LeadCreate
from app.db.session import get_db

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat, leads  # <-- import your routers package(s)

app = FastAPI(title="SA Thomson Nerys Chat API")

@app.post("/api/v1/leads")
def save_lead(payload: LeadCreate, db=Depends(get_db)):
    lead = create_lead(db, payload)
    return {"status": "ok", "lead_id": str(lead.id)}

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # tighten later
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1")
app.include_router(leads.router, prefix="/api/v1")

# ... existing healthz/dbcheck/etc ...

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # DEV ONLY – tighten for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Root & Health ---

    @app.get("/", tags=["root"])
    def root():
        return {"service": "SATN Chatbot API"}

    @app.get("/api/v1/healthz", tags=["health"])
    def healthz():
        return {"status": "ok"}

    @app.get("/api/v1/dbcheck", tags=["health"])
    def dbcheck(db: Session = Depends(get_db)):
        """
        For demo: never crash FastAPI; always return JSON status.
        """
        try:
            val = db.execute(text("SELECT 1")).scalar_one()
            return {
                "status": "ok",
                "db": True,
                "value": val,
                "url": settings.database_url,
            }
        except Exception as e:
            return {
                "status": "error",
                "db": False,
                "error": str(e),
                "url": settings.database_url,
            }

    # --- API Routers (Wave 1) ---

    app.include_router(chat_router, prefix=settings.API_V1_PREFIX)
    app.include_router(agents_router, prefix=settings.API_V1_PREFIX)
    app.include_router(company_info_router, prefix=settings.API_V1_PREFIX)
    app.include_router(interactions_router, prefix=settings.API_V1_PREFIX)
    app.include_router(leads.router, prefix="/api/v1", tags=["leads"])
    return app


app = create_app()
