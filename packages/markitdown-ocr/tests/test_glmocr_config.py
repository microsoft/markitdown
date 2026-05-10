"""Tests for GlmOcrConfig."""

import os
import tempfile
from pathlib import Path

import pytest

from markitdown_ocr._glmocr_config import GlmOcrConfig


class TestGlmOcrConfigDefaults:
    """Tests for default configuration values."""

    def test_defaults(self):
        config = GlmOcrConfig()
        assert config.api_key == ""
        assert config.model == "glm-ocr"
        assert config.timeout == 120


class TestGlmOcrConfigEnvOverride:
    """Tests for environment variable overrides."""

    def test_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("GLMOCR_API_KEY", "test-key-from-env")
        config = GlmOcrConfig.load()
        assert config.api_key == "test-key-from-env"

    def test_model_from_env(self, monkeypatch):
        monkeypatch.setenv("GLMOCR_MODEL", "custom-model")
        config = GlmOcrConfig.load()
        assert config.model == "custom-model"

    def test_timeout_from_env(self, monkeypatch):
        monkeypatch.setenv("GLMOCR_TIMEOUT", "60")
        config = GlmOcrConfig.load()
        assert config.timeout == 60

    def test_all_env_vars(self, monkeypatch):
        monkeypatch.setenv("GLMOCR_API_KEY", "key-123")
        monkeypatch.setenv("GLMOCR_MODEL", "glm-ocr-v2")
        monkeypatch.setenv("GLMOCR_TIMEOUT", "30")
        config = GlmOcrConfig.load()
        assert config.api_key == "key-123"
        assert config.model == "glm-ocr-v2"
        assert config.timeout == 30

    def test_invalid_timeout_ignored(self, monkeypatch):
        monkeypatch.setenv("GLMOCR_TIMEOUT", "not-a-number")
        config = GlmOcrConfig.load()
        assert config.timeout == 120  # default preserved


class TestGlmOcrConfigFile:
    """Tests for config file loading."""

    def test_load_from_pyproject_toml(self, monkeypatch, tmp_path):
        # Clear env vars to ensure file is used
        monkeypatch.delenv("GLMOCR_API_KEY", raising=False)
        monkeypatch.delenv("GLMOCR_MODEL", raising=False)
        monkeypatch.delenv("GLMOCR_TIMEOUT", raising=False)

        # Create a pyproject.toml
        toml_content = """
[tool.markitdown-ocr.glmocr]
api_key = "file-key-123"
model = "glm-ocr-file"
timeout = 90
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        config = GlmOcrConfig.load(config_path=str(toml_file))
        assert config.api_key == "file-key-123"
        assert config.model == "glm-ocr-file"
        assert config.timeout == 90

    def test_env_overrides_file(self, monkeypatch, tmp_path):
        """Environment variables should override file config."""
        monkeypatch.setenv("GLMOCR_API_KEY", "env-key")

        toml_content = """
[tool.markitdown-ocr.glmocr]
api_key = "file-key"
"""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text(toml_content)

        config = GlmOcrConfig.load(config_path=str(toml_file))
        assert config.api_key == "env-key"

    def test_missing_config_file(self):
        """Should return defaults when config file doesn't exist."""
        config = GlmOcrConfig.load(config_path="/nonexistent/path.toml")
        assert config.api_key == ""
        assert config.model == "glm-ocr"
        assert config.timeout == 120

    def test_malformed_config_file(self, tmp_path):
        """Should return defaults when config file is malformed."""
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text("this is not valid toml {{{")

        config = GlmOcrConfig.load(config_path=str(toml_file))
        assert config.model == "glm-ocr"  # default preserved
