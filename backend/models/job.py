"""Job model placeholder.

Purpose:
    Reserve persistence models for job records.

TODO:
    Define job database models when persistence implementation begins.
"""
"""
Job database model.

Purpose:
Represents a processing job created after a resume upload.

A Job flows through the event-driven pipeline and is processed
asynchronously by background workers.
"""

from uuid import uuid4
from datetime import datetime, UTC

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    resume_id = Column(
        String,
        ForeignKey("resumes.id"),
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="Pending"
    )

    retry_count = Column(
        Integer,
        nullable=False,
        default=0
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False
    )

    resume = relationship(
        "Resume",
        back_populates="jobs"
    )

    result = relationship(
        "Result",
        back_populates="job",
        uselist=False,
        cascade="all, delete-orphan"
    )

    outbox_events = relationship(
        "Outbox",
        back_populates="job",
        cascade="all, delete-orphan"
    )