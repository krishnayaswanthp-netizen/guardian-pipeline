"""Upload API for resume submissions."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.database.session import get_db
from backend.services.upload_service import UploadService

router = APIRouter(tags=["Upload"])


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Upload a resume PDF and create a processing job."""
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    service = UploadService(db)
    job = service.upload_resume(
        filename=file.filename,
        file=file.file,
    )

    return {
        "message": "Resume uploaded successfully.",
        "resume_id": job.resume_id,
        "job_id": job.id,
        "status": job.status,
    }
