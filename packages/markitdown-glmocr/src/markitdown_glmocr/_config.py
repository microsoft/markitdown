"""Configuration management for markitdown-glmocr."""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib


@dataclass
class GlmOcrConfig:
    """markitdown-glmocr configuration."""
    
    # API 配置
    api_key: str = ""
    
    # OCR 配置
    model: str = "glm-ocr"
    dpi: int = 150
    timeout: int = 120
    
    # 处理策略
    force_ai: bool = False
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "GlmOcrConfig":
        """
        Load configuration from multiple sources (priority high to low):
        1. Environment variables
        2. Config file (pyproject.toml or markitdown-glmocr.toml)
        3. Default values
        """
        config = cls()
        
        # 1. Load from config file
        config._load_from_file(config_path)
        
        # 2. Environment variables override
        config._load_from_env()
        
        return config
    
    def _load_from_file(self, config_path: Optional[str] = None):
        """Load from config file."""
        search_paths = []
        
        if config_path:
            search_paths.append(Path(config_path))
        
        # Current directory
        search_paths.append(Path("pyproject.toml"))
        search_paths.append(Path("markitdown-glmocr.toml"))
        
        # User config directory
        search_paths.append(Path.home() / ".config" / "markitdown-glmocr" / "config.toml")
        
        for path in search_paths:
            if path.exists():
                try:
                    with open(path, "rb") as f:
                        data = tomllib.load(f)
                    
                    # Read [tool.markitdown-glmocr] section
                    if "tool" in data and "markitdown-glmocr" in data["tool"]:
                        self._apply_config(data["tool"]["markitdown-glmocr"])
                    elif "markitdown-glmocr" in data:
                        self._apply_config(data["markitdown-glmocr"])
                    
                    break
                except Exception:
                    pass
    
    def _apply_config(self, data: dict):
        """Apply config from dict."""
        if "api_key" in data:
            self.api_key = data["api_key"]
        if "model" in data:
            self.model = data["model"]
        if "dpi" in data:
            self.dpi = data["dpi"]
        if "timeout" in data:
            self.timeout = data["timeout"]
        if "force_ai" in data:
            self.force_ai = data["force_ai"]
    
    def _load_from_env(self):
        """Load from environment variables (highest priority)."""
        if os.environ.get("GLMOCR_API_KEY"):
            self.api_key = os.environ["GLMOCR_API_KEY"]
        if os.environ.get("GLMOCR_MODEL"):
            self.model = os.environ["GLMOCR_MODEL"]
        if os.environ.get("GLMOCR_DPI"):
            self.dpi = int(os.environ["GLMOCR_DPI"])
        if os.environ.get("GLMOCR_TIMEOUT"):
            self.timeout = int(os.environ["GLMOCR_TIMEOUT"])
        if os.environ.get("GLMOCR_FORCE_AI"):
            self.force_ai = os.environ["GLMOCR_FORCE_AI"].lower() in ("true", "1", "yes")