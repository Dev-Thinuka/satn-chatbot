from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import get_settings

engine = create_engine(get_settings().database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
