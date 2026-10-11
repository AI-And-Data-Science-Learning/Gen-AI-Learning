"""Centralized configuration, loaded from environment variables (.env)."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    ANTHROPIC_API_KEY: str | None = os.environ.get("ANTHROPIC_API_KEY")
    OPENAI_API_KEY: str | None = os.environ.get("OPENAI_API_KEY")
    DEFAULT_MODEL: str = os.environ.get("DEFAULT_MODEL", "claude-sonnet-4-6")
    VECTOR_STORE_PATH: str = os.environ.get("VECTOR_STORE_PATH", "embeddings")
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")


settings = Settings()
