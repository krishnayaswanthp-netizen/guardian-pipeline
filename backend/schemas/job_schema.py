"""Pydantic schemas for Job."""

from datetime import datetime

from pydantic import BaseModel


class JobResponse(BaseModel):
    """Response schema for job records."""

    id: str
    resume_id: str
    status: str
    retry_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
