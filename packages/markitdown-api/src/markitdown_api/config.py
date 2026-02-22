"""API configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API server settings."""

    host: str = "127.0.0.1"
    port: int = 8000
    workers: int = 1
    enable_plugins: bool = False
    rate_limit: int = 60  # requests per minute
    max_file_size: int = 10 * 1024 * 1024  # 10MB

    class Config:
        """Pydantic config."""

        env_prefix = "MARKITDOWN_API_"