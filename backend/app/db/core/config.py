from app.core.config import settings

SQL_ECHO: bool = settings.ENV == "dev"
POOL_PRE_PING: bool = True
