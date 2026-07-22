"""Job schema placeholder.

Purpose:
    Reserve validation schemas for job payloads.

TODO:
    Define job schemas when API contracts are designed.
"""
"""
Pydantic schemas for Job.
"""

from datetime import datetime
from pydantic import BaseModel


class JobResponse(BaseModel):
    id: str
    resume_id: str
    status: str
    retry_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True