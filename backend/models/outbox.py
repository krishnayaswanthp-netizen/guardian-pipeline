"""Transactional outbox database model."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Outbox(Base):
    """Stores events that must be reliably published later."""

    __tablename__ = "outbox"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    published_at = Column(DateTime, nullable=True)

    job = relationship("Job", back_populates="outbox_events")
