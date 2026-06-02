"""Configuration for markitdown-paddleocr."""

import os
from dataclasses import dataclass
from enum import Enum


class ScanDetectionMode(str, Enum):
    """扫描检测模式。

    - PAGE_BY_PAGE: 逐页分析，当前默认行为
    - FIRST_PAGE_HINT: 首页是扫描件则全文档使用OCR
    - SAMPLING: 抽样前N页，多数是扫描件则全部OCR
    """

    PAGE_BY_PAGE = "page_by_page"
    FIRST_PAGE_HINT = "first_page_hint"
    SAMPLING = "sampling"


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
    model: str = "PaddleOCR-VL-1.6"

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

    # Scan detection mode for optimization
    scan_detection_mode: ScanDetectionMode = ScanDetectionMode.SAMPLING
    scan_sample_pages: int = 3  # Number of pages to sample in SAMPLING mode
    scan_text_threshold: int = 50  # Min text length to consider page as non-scanned

    @classmethod
    def from_env(cls, **overrides) -> "PaddleOcrConfig":
        """Create config from environment variables with optional overrides."""
        defaults = {
            "token": os.environ.get("BAIDU_PADDLE_TOKEN", ""),
            "model": os.environ.get("PADDLE_OCR_MODEL", "PaddleOCR-VL-1.6"),
        }
        defaults.update(overrides)
        return cls(**defaults)
