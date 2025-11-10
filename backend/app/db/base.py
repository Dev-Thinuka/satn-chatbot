"""
Declarative Base for SQLAlchemy ORM models.
This isolates Base to prevent circular imports.
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()
                