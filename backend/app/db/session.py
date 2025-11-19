# backend/app/db/session.py

import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

POSTGRES_USER = os.getenv("POSTGRES_USER", "satn_admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "SatnDb2025")
POSTGRES_DB = os.getenv("POSTGRES_DB", "satn_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

print("SQLALCHEMY_DATABASE_URL:", SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that yields a SQLAlchemy Session.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
