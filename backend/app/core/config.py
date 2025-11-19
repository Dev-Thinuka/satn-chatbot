# backend/app/core/config.py
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- OpenAI ---
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4.1-mini"

    # --- Email / Lead Capture ---
    SENDGRID_API_KEY: Optional[str] = None
    SALES_ALERT_TO: str = "sales@sathomson.com.au"
    WELCOME_EMAIL_FROM: str = "assistant@sathomson.com.au"
    SALES_FROM: str = "no-reply@sathomson.com.au"

    # --- General ---
    ENV: str = "dev"
    PROJECT_NAME: str = "SA Thomson Chatbot Backend"
    API_V1_PREFIX: str = "/api/v1"

    # --- Database ---
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433   # your container maps 5433 -> 5432
    POSTGRES_USER: str = "satn_admin"
    POSTGRES_PASSWORD: str = "Thinuka!@#123"
    POSTGRES_DB: str = "satn_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    # --- CORS ---
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5500",
        "https://sathomson.com.au",
    ]

    # --- Auth ---
    SECRET_KEY: str = "Thinuka!@#123"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # Load .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Build DB URL ---
    @property
    def database_url(self) -> str:
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI

        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()


def get_settings():
    return settings
