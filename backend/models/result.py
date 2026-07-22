"""Result database model."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Result(Base):
    """Stores the AI screening result generated after processing a job."""

    __tablename__ = "results"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False, unique=True)
    score = Column(Float, nullable=False)
    summary = Column(Text, nullable=False)
    recommendations = Column(Text, nullable=True)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    job = relationship("Job", back_populates="result")
