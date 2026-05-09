"""Configuration management for nova-pdf."""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib


@dataclass
class NovaPdfConfig:
    """nova-pdf configuration."""
    
    # API 配置
    zhipu_api_key: str = ""
    
    # OCR 配置
    model: str = "glm-ocr"
    dpi: int = 150
    timeout: int = 120
    
    # 处理策略
    force_ai: bool = False
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "NovaPdfConfig":
        """
        Load configuration from multiple sources (priority high to low):
        1. Environment variables
        2. Config file (pyproject.toml or nova-pdf.toml)
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
        search_paths.append(Path("nova-pdf.toml"))
        
        # User config directory
        search_paths.append(Path.home() / ".config" / "nova-pdf" / "config.toml")
        
        for path in search_paths:
            if path.exists():
                try:
                    with open(path, "rb") as f:
                        data = tomllib.load(f)
                    
                    # Read [tool.nova-pdf] section
                    if "tool" in data and "nova-pdf" in data["tool"]:
                        self._apply_config(data["tool"]["nova-pdf"])
                    elif "nova-pdf" in data:
                        self._apply_config(data["nova-pdf"])
                    
                    break
                except Exception:
                    pass
    
    def _apply_config(self, data: dict):
        """Apply config from dict."""
        if "api_key" in data:
            self.zhipu_api_key = data["api_key"]
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
        if os.environ.get("NOVA_ZHIPU_API_KEY"):
            self.zhipu_api_key = os.environ["NOVA_ZHIPU_API_KEY"]
        if os.environ.get("NOVA_MODEL"):
            self.model = os.environ["NOVA_MODEL"]
        if os.environ.get("NOVA_DPI"):
            self.dpi = int(os.environ["NOVA_DPI"])
        if os.environ.get("NOVA_TIMEOUT"):
            self.timeout = int(os.environ["NOVA_TIMEOUT"])
        if os.environ.get("NOVA_FORCE_AI"):
            self.force_ai = os.environ["NOVA_FORCE_AI"].lower() in ("true", "1", "yes")
