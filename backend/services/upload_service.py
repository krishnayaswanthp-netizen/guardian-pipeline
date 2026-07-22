"""Upload service placeholder.

Purpose:
    Reserve service logic for resume upload processing.

TODO:
    Add upload orchestration when service implementation begins.
"""
"""
Resume upload orchestration service.

Purpose:
    Coordinate the full resume upload flow:
    - Save the uploaded PDF to disk.
    - Create Resume, Job, and Outbox records.
    - Perform everything in a single database transaction.
"""

import uuid
from pathlib import Path
from typing import BinaryIO

from sqlalchemy.orm import Session

from backend.models.job import Job
from backend.models.outbox import Outbox
from backend.models.resume import Resume

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"


class UploadService:
    """Handles the complete resume upload workflow."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def save_resume_file(self, filename: str, file: BinaryIO) -> str:
        """
        Save the uploaded PDF inside backend/uploads/
        and return its storage path.
        """
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        extension = Path(filename).suffix or ".pdf"
        stored_filename = f"{uuid.uuid4()}{extension}"
        destination = UPLOAD_DIR / stored_filename

        with open(destination, "wb") as out_file:
            out_file.write(file.read())

        return str(destination)

    def create_resume(
        self,
        original_filename: str,
        storage_path: str,
    ) -> Resume:
        """
        Create a Resume record.
        """
        resume = Resume(
            filename=original_filename,
            storage_path=storage_path,
        )

        self.db.add(resume)
        self.db.flush()

        return resume

    def create_job(
        self,
        resume_id: str,
    ) -> Job:
        """
        Create a Job record with status='Pending'.
        """
        job = Job(
            resume_id=resume_id,
            status="Pending",
        )

        self.db.add(job)
        self.db.flush()

        return job

    def create_outbox_event(
        self,
        job_id: str,
    ) -> Outbox:
        """
        Create an unpublished Outbox event.
        """
        outbox_event = Outbox(
            job_id=job_id,
            event_type="job_created",
            payload=f'{{"job_id":"{job_id}"}}',
            published=False,
        )

        self.db.add(outbox_event)
        self.db.flush()

        return outbox_event

    def upload_resume(
        self,
        filename: str,
        file: BinaryIO,
    ) -> Job:
        """
        Execute the complete upload workflow
        inside a single database transaction.
        """
        try:
            storage_path = self.save_resume_file(filename, file)

            resume = self.create_resume(
                filename,
                storage_path,
            )

            job = self.create_job(resume.id)

            self.create_outbox_event(job.id)

            self.db.commit()

            self.db.refresh(job)

            return job

        except Exception:
            self.db.rollback()
            raise