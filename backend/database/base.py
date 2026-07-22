"""Database base placeholder.

Purpose:
    Reserve shared database metadata configuration.

TODO:
    Add database base definitions when persistence implementation begins.
"""
"""Declarative base for ORM models.

Purpose:
    Provide the single SQLAlchemy declarative base that all models
    (Job, Outbox, Result, Resume, etc.) will inherit from in later phases.

    This module intentionally defines nothing else. Keeping the base
    isolated from the engine/session avoids circular imports: models can
    import Base from here without pulling in connection or session setup.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()