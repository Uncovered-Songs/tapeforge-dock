from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration, loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    app_name: str = "TapeForge Dock API"
    environment: str = "development"
    debug: bool = True

    # API
    api_v1_prefix: str = "/api/v1"

    # Database — SQLAlchemy/SQLModel URL. Defaults to a local SQLite file.
    database_url: str = "sqlite:///./data/dock.db"

    # CORS — origins allowed to call the API (the Dock Vue dev server by default).
    cors_origins: list[str] = ["http://localhost:5174", "http://127.0.0.1:5174"]

    # Crew assistant (Claude API). Reads ANTHROPIC_API_KEY from the environment;
    # when unset, the /crew/chat endpoint returns 503.
    anthropic_api_key: str | None = None
    crew_model: str = "claude-sonnet-4-6"


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor so the .env is parsed only once."""
    return Settings()


settings = get_settings()
