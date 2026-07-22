"""Outbox model placeholder.

Purpose:
    Reserve persistence models for outbox events.

TODO:
    Define outbox database models when event relay implementation begins.
"""
"""
Transactional Outbox model.

Purpose:
Stores events that must be reliably published to RabbitMQ.

The Outbox Relay reads unpublished events and sends them
to the message broker.
"""

from uuid import uuid4
from datetime import datetime, UTC

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from backend.database.base import Base


class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    job_id = Column(
        String,
        ForeignKey("jobs.id"),
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    payload = Column(
        Text,
        nullable=False
    )

    published = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    published_at = Column(
        DateTime,
        nullable=True
    )

    job = relationship(
        "Job",
        back_populates="outbox_events"
    )