"""Database engine setup."""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from backend.core.config import get_settings

settings = get_settings()

engine: Engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)
