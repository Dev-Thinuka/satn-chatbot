import logging

from app.core.config import settings

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"


def setup_sqlalchemy_logging() -> None:
    """
    Basic SQLAlchemy engine logging.
    Call this once at startup if you want verbose SQL logs in dev.
    """
    level = logging.DEBUG if settings.ENV == "dev" else logging.INFO
    logging.basicConfig(format=LOG_FORMAT, level=level)
    logging.getLogger("sqlalchemy.engine").setLevel(level)
