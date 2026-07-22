"""Resume schema placeholder.

Purpose:
    Reserve validation schemas for resume payloads.

TODO:
    Define resume schemas when API contracts are designed.
"""
"""
Pydantic schemas for Resume.
"""

from datetime import datetime
from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: str
    filename: str
    storage_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True