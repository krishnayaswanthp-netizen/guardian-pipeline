"""Model registration for SQLAlchemy metadata."""

from backend.models.job import Job
from backend.models.outbox import Outbox
from backend.models.result import Result
from backend.models.resume import Resume

__all__ = ["Job", "Outbox", "Result", "Resume"]
