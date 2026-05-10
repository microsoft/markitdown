"""Configuration management for glm-ocr provider."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ImportError:
        tomllib = None  # type: ignore[assignment]


@dataclass
class GlmOcrConfig:
    """glm-ocr provider configuration for markitdown-ocr.

    Config sources (priority high to low):
    1. kwargs parameters (passed at registration time)
    2. Environment variables
    3. Config file (pyproject.toml [tool.markitdown-ocr.glmocr] section)
    4. Default values
    """

    api_key: str = ""
    model: str = "glm-ocr"
    timeout: int = 120

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "GlmOcrConfig":
        """Load configuration from multiple sources."""
        config = cls()
        config._load_from_file(config_path)
        config._load_from_env()
        return config

    def _load_from_file(self, config_path: Optional[str] = None) -> None:
        """Load from config file (pyproject.toml)."""
        if tomllib is None:
            return

        search_paths: list[Path] = []

        if config_path:
            search_paths.append(Path(config_path))

        # Current directory pyproject.toml
        search_paths.append(Path("pyproject.toml"))

        # User config directory
        search_paths.append(
            Path.home() / ".config" / "markitdown-ocr" / "config.toml"
        )

        for path in search_paths:
            if path.exists():
                try:
                    with open(path, "rb") as f:
                        data = tomllib.load(f)

                    # Read [tool.markitdown-ocr.glmocr] section
                    if "tool" in data and "markitdown-ocr" in data["tool"]:
                        section = data["tool"]["markitdown-ocr"]
                        glmocr_section = section.get("glmocr", {})
                        self._apply_config(glmocr_section)

                    break  # Use first found config file
                except Exception:
                    pass

    def _apply_config(self, data: dict) -> None:
        """Apply config values from a dict."""
        if "api_key" in data:
            self.api_key = data["api_key"]
        if "model" in data:
            self.model = data["model"]
        if "timeout" in data:
            self.timeout = int(data["timeout"])

    def _load_from_env(self) -> None:
        """Load from environment variables (highest priority)."""
        if os.environ.get("GLMOCR_API_KEY"):
            self.api_key = os.environ["GLMOCR_API_KEY"]
        if os.environ.get("GLMOCR_MODEL"):
            self.model = os.environ["GLMOCR_MODEL"]
        if os.environ.get("GLMOCR_TIMEOUT"):
            try:
                self.timeout = int(os.environ["GLMOCR_TIMEOUT"])
            except ValueError:
                pass
