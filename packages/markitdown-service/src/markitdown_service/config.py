"""Configuration read from the environment. The service refuses to start on a bad value."""

import os
from dataclasses import dataclass
from typing import Mapping, Optional

# What the portal may upload. Anything else is refused before it reaches the converters.
EXTENSIONS = (".pdf", ".docx", ".pptx", ".xlsx", ".xls")

MIN_TOKEN_LENGTH = 32


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Config:
    token: str
    host: str = "0.0.0.0"
    port: int = 8000
    max_upload_bytes: int = 25 * 1024 * 1024
    timeout_seconds: int = 90
    max_concurrent: int = 2
    # Address-space cap for the conversion subprocess (0 = no cap).
    worker_memory_mb: int = 2048


def _int(env: Mapping[str, str], name: str, default: int, minimum: int) -> int:
    raw = env.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ConfigError(f"{name} must be an integer (got {raw!r})") from None
    if value < minimum:
        raise ConfigError(f"{name} must be >= {minimum} (got {value})")
    return value


def load_config(env: Optional[Mapping[str, str]] = None) -> Config:
    env = os.environ if env is None else env
    token = env.get("MARKITDOWN_ADMIN_TOKEN", "")
    if len(token) < MIN_TOKEN_LENGTH:
        raise ConfigError(
            f"MARKITDOWN_ADMIN_TOKEN must be set to a secret of {MIN_TOKEN_LENGTH}+ characters "
            "(the same value the admin portal uses)"
        )
    return Config(
        token=token,
        host=env.get("HOST", "0.0.0.0"),
        port=_int(env, "PORT", 8000, 1),
        max_upload_bytes=_int(env, "MARKITDOWN_MAX_UPLOAD_MB", 25, 1) * 1024 * 1024,
        timeout_seconds=_int(env, "MARKITDOWN_TIMEOUT_S", 90, 1),
        max_concurrent=_int(env, "MARKITDOWN_MAX_CONCURRENT", 2, 1),
        worker_memory_mb=_int(env, "MARKITDOWN_MAX_MEMORY_MB", 2048, 0),
    )
