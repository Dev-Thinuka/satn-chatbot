# backend/app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import get_db
from app.api.v1.chat import router as chat_router
from app.api.v1.agents import router as agents_router
from app.api.v1.company_info import router as company_info_router
from app.api.v1.interactions import router as interactions_router


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

    return app


app = create_app()
