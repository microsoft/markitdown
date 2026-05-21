"""Configuration for markitdown-glmocr."""

from dataclasses import dataclass, field
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
class GlmOcrConfig:
    """markitdown-glmocr configuration.
    
    Configuration priority (high to low):
    1. Constructor kwargs
    2. Environment variables
    3. .env file
    4. Built-in defaults
    """
    
    # API configuration
    api_key: str = ""  # Reads from ZHIPU_API_KEY by default
    
    # OCR configuration
    timeout: int = 1800
    enable_layout: bool = False
    
    # Processing strategy
    force_ai: bool = False
    
    # Scan detection mode for optimization
    scan_detection_mode: ScanDetectionMode = ScanDetectionMode.SAMPLING
    scan_sample_pages: int = 3  # Number of pages to sample in SAMPLING mode
    scan_text_threshold: int = 50  # Min text length to consider page as non-scanned