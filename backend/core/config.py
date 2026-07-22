"""Settings placeholder.

Purpose:
    Reserve application configuration settings.

TODO:
    Add configuration loading when backend implementation begins.
"""
"""Application configuration.

Purpose:
    Load environment-based configuration for the Guardian Pipeline backend.
    Currently exposes only what the Database Foundation phase (1.1) needs:
    the database connection string.

Usage:
    from backend.core.config import get_settings

    settings = get_settings()
    settings.DATABASE_URL
"""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Holds process configuration read from environment variables.

    Kept as a plain class (not a framework-specific settings base) so this
    module has no dependency beyond python-dotenv, which is already in
    requirements.txt.
    """

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
    """Return a cached Settings instance.

    lru_cache ensures the environment is read once per process rather than
    on every call, while still allowing modules to import and call this
    function independently.
    """
    return Settings()