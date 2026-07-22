"""Pydantic schemas for Result."""

from datetime import datetime

from pydantic import BaseModel


class ResultResponse(BaseModel):
    """Response schema for screening results."""

    id: str
    job_id: str
    score: float
    summary: str
    recommendations: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
