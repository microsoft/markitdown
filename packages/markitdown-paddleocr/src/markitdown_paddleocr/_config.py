"""Configuration for markitdown-paddleocr."""

import os
from dataclasses import dataclass


@dataclass
class PaddleOcrConfig:
    """markitdown-paddleocr configuration.

    Configuration priority (high to low):
    1. Constructor kwargs
    2. Environment variables
    3. Built-in defaults
    """

    # API configuration
    token: str = ""  # Reads from BAIDU_PADDLE_TOKEN by default

    # OCR model
    model: str = "PaddleOCR-VL-1.5"

    # API endpoint
    job_url: str = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"

    # Polling configuration
    poll_interval: float = 2.0  # seconds between polls
    poll_timeout: float = 300.0  # max seconds to wait for job completion

    # Optional OCR features
    use_doc_orientation_classify: bool = False
    use_doc_unwarping: bool = False
    use_chart_recognition: bool = False

    # Processing strategy
    force_ai: bool = False

    @classmethod
    def from_env(cls, **overrides) -> "PaddleOcrConfig":
        """Create config from environment variables with optional overrides."""
        defaults = {
            "token": os.environ.get("BAIDU_PADDLE_TOKEN", ""),
            "model": os.environ.get("PADDLE_OCR_MODEL", "PaddleOCR-VL-1.5"),
        }
        defaults.update(overrides)
        return cls(**defaults)
