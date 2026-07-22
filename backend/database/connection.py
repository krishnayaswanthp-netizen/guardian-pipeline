"""Database connection placeholder.

Purpose:
    Reserve database connection configuration.

TODO:
    Add connection setup when persistence implementation begins.
"""
"""Database engine setup.

Purpose:
    Create the single SQLAlchemy Engine used by the whole backend, from
    the DATABASE_URL provided by backend.core.config.

    This module owns exactly one responsibility: turning a connection
    string into a configured Engine. Session management lives in
    session.py, not here, so the engine can be reused (e.g. by Alembic
    migrations) without pulling in session/dependency code.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from backend.core.config import get_settings

settings = get_settings()

engine: Engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # detects stale/dropped connections before use
    future=True,
)