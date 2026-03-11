"""Tests for LLM gateway compatibility (configurable base_url and model)."""
import importlib
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from app.config import Settings, reset_settings


class TestOpenAIBaseUrl:
    """Test configurable OpenAI base URL."""

    def test_openai_base_url_default(self):
        """When OPENAI_BASE_URL is not set, setting is None (SDK default)."""
        env = {"OPENAI_API_TOKEN": "sk-test"}
        with patch.dict(os.environ, env, clear=True):
            reset_settings()
            settings = Settings()
            assert settings.openai_base_url is None

    def test_openai_base_url_configured(self):
        """When OPENAI_BASE_URL is set, setting holds that value."""
        env = {
            "OPENAI_API_TOKEN": "sk-test",
            "OPENAI_BASE_URL": "http://llm-gateway:8100/v1",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_settings()
            settings = Settings()
            assert settings.openai_base_url == "http://llm-gateway:8100/v1"


class TestVisionModel:
    """Test configurable vision model."""

    def test_vision_model_default(self):
        """When OPENAI_VISION_MODEL is not set, defaults to gpt-4o-mini."""
        env = {"OPENAI_API_TOKEN": "sk-test"}
        with patch.dict(os.environ, env, clear=True):
            reset_settings()
            settings = Settings()
            assert settings.openai_vision_model == "gpt-4o-mini"

    def test_vision_model_configured(self):
        """When OPENAI_VISION_MODEL is set, that model is used."""
        env = {
            "OPENAI_API_TOKEN": "sk-test",
            "OPENAI_VISION_MODEL": "anthropic/claude-opus-4-6",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_settings()
            settings = Settings()
            assert settings.openai_vision_model == "anthropic/claude-opus-4-6"


@pytest.fixture
def image_describer_module():
    """Import image_describer module, mocking out heavy dependencies."""
    # Mock markitdown so the converters package can be imported
    markitdown_mock = MagicMock()
    with patch.dict(sys.modules, {
        "markitdown": markitdown_mock,
        "pdfplumber": MagicMock(),
    }):
        # Force re-import to pick up mocks
        for mod_name in list(sys.modules):
            if mod_name.startswith("app.converters"):
                del sys.modules[mod_name]

        import app.converters.image_describer as mod
        yield mod

        # Clean up to avoid polluting other tests
        for mod_name in list(sys.modules):
            if mod_name.startswith("app.converters"):
                del sys.modules[mod_name]


class TestClientConstructionWithBaseUrl:
    """Test that AsyncOpenAI client is constructed with base_url when configured."""

    @pytest.mark.asyncio
    async def test_client_receives_base_url_when_configured(self, image_describer_module):
        """When base_url is configured, AsyncOpenAI is constructed with it."""
        env = {
            "OPENAI_API_TOKEN": "sk-test",
            "OPENAI_BASE_URL": "http://llm-gateway:8100/v1",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_settings()

            with patch.object(image_describer_module, "AsyncOpenAI") as mock_cls:
                mock_client = MagicMock()
                mock_cls.return_value = mock_client

                from app.converters.pdf_extractor import ImageRef

                ref = ImageRef(
                    image_id="p1-i1",
                    page=1,
                    index=1,
                    filename="test.png",
                    context_before="",
                    context_after="",
                )

                with patch.object(image_describer_module, "_describe_single_image") as mock_desc:
                    mock_desc.return_value = MagicMock(
                        ref=ref, description="test", error=None
                    )
                    await image_describer_module.describe_images(
                        "![p1-i1](images/test.png)", [ref], Path("/tmp")
                    )

                mock_cls.assert_called_once_with(
                    api_key="sk-test",
                    base_url="http://llm-gateway:8100/v1",
                )

    @pytest.mark.asyncio
    async def test_client_no_base_url_when_not_configured(self, image_describer_module):
        """When base_url is not configured, AsyncOpenAI is called without it."""
        env = {"OPENAI_API_TOKEN": "sk-test"}
        with patch.dict(os.environ, env, clear=True):
            reset_settings()

            with patch.object(image_describer_module, "AsyncOpenAI") as mock_cls:
                mock_client = MagicMock()
                mock_cls.return_value = mock_client

                from app.converters.pdf_extractor import ImageRef

                ref = ImageRef(
                    image_id="p1-i1",
                    page=1,
                    index=1,
                    filename="test.png",
                    context_before="",
                    context_after="",
                )

                with patch.object(image_describer_module, "_describe_single_image") as mock_desc:
                    mock_desc.return_value = MagicMock(
                        ref=ref, description="test", error=None
                    )
                    await image_describer_module.describe_images(
                        "![p1-i1](images/test.png)", [ref], Path("/tmp")
                    )

                mock_cls.assert_called_once_with(api_key="sk-test")


class TestModelUsedInAPICall:
    """Test that the configured model is passed to the API call."""

    @pytest.mark.asyncio
    async def test_configured_model_used_in_api_call(self, image_describer_module):
        """When OPENAI_VISION_MODEL is set, that model is passed to create()."""
        env = {
            "OPENAI_API_TOKEN": "sk-test",
            "OPENAI_VISION_MODEL": "anthropic/claude-opus-4-6",
        }
        with patch.dict(os.environ, env, clear=True):
            reset_settings()

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "A test image"

            mock_create = AsyncMock(return_value=mock_response)
            mock_client = MagicMock()
            mock_client.chat.completions.create = mock_create

            with tempfile.TemporaryDirectory() as tmpdir:
                img_path = Path(tmpdir) / "test.png"
                img_path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

                from app.converters.pdf_extractor import ImageRef

                ref = ImageRef(
                    image_id="p1-i1",
                    page=1,
                    index=1,
                    filename="test.png",
                    context_before="before",
                    context_after="after",
                )

                await image_describer_module._get_image_description(
                    mock_client, ref, Path(tmpdir)
                )

            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args.kwargs
            assert call_kwargs["model"] == "anthropic/claude-opus-4-6"

    @pytest.mark.asyncio
    async def test_default_model_used_when_not_configured(self, image_describer_module):
        """When OPENAI_VISION_MODEL is not set, gpt-4o-mini is used."""
        env = {"OPENAI_API_TOKEN": "sk-test"}
        with patch.dict(os.environ, env, clear=True):
            reset_settings()

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "A test image"

            mock_create = AsyncMock(return_value=mock_response)
            mock_client = MagicMock()
            mock_client.chat.completions.create = mock_create

            with tempfile.TemporaryDirectory() as tmpdir:
                img_path = Path(tmpdir) / "test.png"
                img_path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

                from app.converters.pdf_extractor import ImageRef

                ref = ImageRef(
                    image_id="p1-i1",
                    page=1,
                    index=1,
                    filename="test.png",
                    context_before="before",
                    context_after="after",
                )

                await image_describer_module._get_image_description(
                    mock_client, ref, Path(tmpdir)
                )

            mock_create.assert_called_once()
            call_kwargs = mock_create.call_args.kwargs
            assert call_kwargs["model"] == "gpt-4o-mini"
