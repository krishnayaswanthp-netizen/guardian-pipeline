"""Job database model."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Job(Base):
    """Represents a processing job created after a resume upload."""

    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False)
    status = Column(String, nullable=False, default="Pending")
    retry_count = Column(Integer, nullable=False, default=0)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    resume = relationship("Resume", back_populates="jobs")
    result = relationship(
        "Result",
        back_populates="job",
        uselist=False,
        cascade="all, delete-orphan",
    )
    outbox_events = relationship(
        "Outbox",
        back_populates="job",
        cascade="all, delete-orphan",
    )
