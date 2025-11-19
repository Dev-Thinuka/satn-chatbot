# backend/app/db/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# DO NOT import models here.
# Models automatically register themselves when imported by SQLAlchemy.
