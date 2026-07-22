"""Job status retrieval service."""

from typing import Optional

from sqlalchemy.orm import Session

from backend.models.job import Job


class JobService:
    """Retrieves Job records by ID."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_job_by_id(self, job_id: str) -> Optional[Job]:
        """Return the Job with the given ID, or None if it does not exist."""
        return self.db.query(Job).filter(Job.id == job_id).first()
