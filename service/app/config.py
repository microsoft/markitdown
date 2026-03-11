"""Application configuration."""
import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
    )

    # Data directory for task storage
    data_dir: str = "/data"

    # Maximum upload size in bytes (500MB)
    max_upload_size: int = 500 * 1024 * 1024

    # Database file path
    db_path: str = "/data/task_db.sqlite"

    # OpenAI API token (note the intentional typo from PDR)
    openai_api_token: str = Field(default="", validation_alias="OPENAI_API_TOKEN")

    # OpenAI base URL override (for LLM gateway/proxy routing)
    openai_base_url: str | None = None

    # Vision model to use for image descriptions
    openai_vision_model: str = "gpt-4o-mini"

    # Worker settings
    max_concurrent_tasks: int = 2

    # Image description settings
    max_concurrent_descriptions: int = 5  # Max parallel OpenAI API calls
    description_max_retries: int = 3
    description_retry_delay: float = 1.0  # Base delay in seconds (exponential backoff)

    # Webhook settings
    webhook_timeout: float = 10.0
    webhook_max_retries: int = 3
    webhook_retry_delay: float = 5.0

    # Cleanup settings
    cleanup_interval_minutes: int = 15
    retention_hours: int = 24

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000


_settings: Settings | None = None


def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset settings singleton (for testing)."""
    global _settings
    _settings = None
