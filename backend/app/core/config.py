# app/core/config.py
from typing import List, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",             # <--- ADD THIS LINE
    )

    # General
    ENV: str = "dev"
    PROJECT_NAME: str = "SA Thomson Chatbot Backend"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "satn_admin"
    POSTGRES_PASSWORD: str = "Thinuka!@#123"
    POSTGRES_DB: str = "satn_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None  # override if you want full DSN

    # CORS – add/remove origins as needed
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://sathomson.com.au",
    ]

    # Auth / Security
    SECRET_KEY: str = "CHANGE_THIS_IN_ENV"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    @property
    def database_url(self) -> str:
        """
        Build the SQLAlchemy database URL.
        Uses SQLALCHEMY_DATABASE_URI if set, otherwise builds from parts.
        """
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI

        # Requires psycopg or psycopg to be installed
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
