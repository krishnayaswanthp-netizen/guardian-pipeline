"""Result model placeholder.

Purpose:
    Reserve persistence models for screening results.

TODO:
    Define result database models when persistence implementation begins.
"""
"""
Result database model.

Purpose:
Stores the AI screening result generated after processing a job.
"""

from uuid import uuid4
from datetime import datetime, UTC

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Result(Base):
    __tablename__ = "results"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    job_id = Column(
        String,
        ForeignKey("jobs.id"),
        nullable=False,
        unique=True
    )

    score = Column(
        Float,
        nullable=False
    )

    summary = Column(
        Text,
        nullable=False
    )

    recommendations = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    job = relationship(
        "Job",
        back_populates="result"
    )