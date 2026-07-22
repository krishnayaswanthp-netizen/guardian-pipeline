"""Resume model placeholder.

Purpose:
    Reserve persistence models for resume records.

TODO:
    Define resume database models when persistence implementation begins.
"""
"""
Resume database model.

Purpose:
Represents a resume uploaded by the user.

A Resume only stores information about the uploaded file.
Processing status and AI results are stored separately.
"""

from uuid import uuid4
from datetime import datetime, UTC
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(
        String,
        primary_key=True,
        default=lambda: datetime.now(UTC)
    )

    filename = Column(
        String,
        nullable=False
    )

    storage_path = Column(
        String,
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    jobs = relationship(
        "Job",
        back_populates="resume",
        cascade="all, delete-orphan"
    )