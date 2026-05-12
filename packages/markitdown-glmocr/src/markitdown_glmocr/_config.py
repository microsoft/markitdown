"""Configuration for markitdown-glmocr."""

from dataclasses import dataclass, field


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