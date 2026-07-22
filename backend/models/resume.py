"""Resume database model."""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Resume(Base):
    """Represents a resume uploaded by the user."""

    __tablename__ = "resumes"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    uploaded_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    jobs = relationship(
        "Job",
        back_populates="resume",
        cascade="all, delete-orphan",
    )
