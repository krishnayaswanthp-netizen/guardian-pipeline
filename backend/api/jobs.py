"""Job status API."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}")
def get_job_status(job_id: str, db: Session = Depends(get_db)) -> dict[str, str | None]:
    """Return status details for a single job, or 404 if it does not exist."""
    job_service = JobService(db)
    job = job_service.get_job_by_id(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": str(job.id),
        "status": job.status,
        "resume_id": str(job.resume_id),
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
    }
