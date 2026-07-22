"""Database session placeholder.

Purpose:
    Reserve database session management.

TODO:
    Add session handling when persistence implementation begins.
"""
"""Database session management.

Purpose:
    Provide SessionLocal (a session factory bound to the shared engine)
    and get_db, a FastAPI-compatible dependency that yields one session
    per request and guarantees it is closed afterward.

Usage (in a future API route):
    from fastapi import Depends
    from backend.database.session import get_db

    @router.get("/jobs/{job_id}")
    def read_job(job_id: str, db: Session = Depends(get_db)):
        ...
"""

from typing import Generator

from sqlalchemy.orm import Session, sessionmaker

from backend.database.connection import engine

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after use.

    A generator dependency so FastAPI runs the code after `yield` as
    teardown, closing the session even if the request handler raises.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()