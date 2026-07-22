"""FastAPI application entry point for Guardian Pipeline."""

from fastapi import FastAPI

import backend.models
from backend.api.jobs import router as jobs_router
from backend.api.upload import router as upload_router
from backend.database.base import Base
from backend.database.connection import engine

app = FastAPI(title="Guardian Pipeline")


@app.on_event("startup")
def startup() -> None:
    """Create database tables when the application starts."""
    Base.metadata.create_all(bind=engine)


app.include_router(upload_router)
app.include_router(jobs_router)
