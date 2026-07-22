"""Application configuration for Guardian Pipeline."""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Holds process configuration read from environment variables."""

    def __init__(self) -> None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise RuntimeError(
                "DATABASE_URL is not set. Define it in your .env file, "
                "e.g. DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/guardian_pipeline"
            )
        self.DATABASE_URL: str = database_url


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
