"""Result schema placeholder.

Purpose:
    Reserve validation schemas for screening results.

TODO:
    Define result schemas when API contracts are designed.
"""
"""
Pydantic schemas for Result.
"""

from datetime import datetime
from pydantic import BaseModel


class ResultResponse(BaseModel):
    id: str
    job_id: str
    score: float
    summary: str
    recommendations: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True