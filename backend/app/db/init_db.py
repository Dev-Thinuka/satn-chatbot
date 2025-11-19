# backend/app/db/init_db.py

from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    """
    Create all tables defined in SQLAlchemy models.

    This uses Base.metadata.create_all, so every model imported into
    app.db.base (e.g. leads, users, properties, etc.) will be created.
    """
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == "__main__":
    init_db()
