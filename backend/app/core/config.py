from pydantic import BaseModel
from functools import lru_cache
import os

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "development")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://satn_admin:changeme@localhost:5432/satn_db")
    smtp_host: str | None = os.getenv("SMTP_HOST")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str | None = os.getenv("SMTP_USER")
    smtp_password: str | None = os.getenv("SMTP_PASSWORD")
    sales_alert_to: str = os.getenv("SALES_ALERT_TO", "sales@sathomson.com.au")
    from_email: str = os.getenv("FROM_EMAIL", "no-reply@sathomson.com.au")
    jwt_secret: str = os.getenv("JWT_SECRET", "change_me")
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")

@lru_cache
def get_settings() -> Settings:
    return Settings()
