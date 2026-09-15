"""
Unit tests for the OCR service backends and backend selection.

Both backends are exercised against fake clients: no network, no API key.
"""

import io
import sys
from pathlib import Path
from typing import Any

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_ocr._ocr_service import (  # noqa: E402
    AnthropicVisionOCRService,
    LLMVisionOCRService,
    create_ocr_service,
)
from markitdown import StreamInfo  # noqa: E402

# A 1x1 PNG, so Pillow can sniff a real format when stream_info is absent.
_PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

_EXPECTED = "EXTRACTED_TEXT"


# ---------------------------------------------------------------------------
# Fake clients
# ---------------------------------------------------------------------------


class _FakeOpenAIClient:
    """Minimal stand-in for openai.OpenAI."""

    def __init__(self) -> None:
        self.captured: dict[str, Any] = {}

        class _Completions:
            def create(inner, **kwargs: Any) -> Any:  # noqa: N805
                self.captured = kwargs
                message = type("Message", (), {"content": f"  {_EXPECTED}\n"})()
                choice = type("Choice", (), {"message": message})()
                return type("Response", (), {"choices": [choice]})()

        self.chat = type("Chat", (), {"completions": _Completions()})()


class _FakeAnthropicClient:
    """Minimal stand-in for anthropic.Anthropic."""

    def __init__(self, blocks: Any = None, stop_reason: str = "end_turn") -> None:
        self.captured: dict[str, Any] = {}
        if blocks is None:
            blocks = [type("Block", (), {"type": "text", "text": f" {_EXPECTED} "})()]

        class _Messages:
            def create(inner, **kwargs: Any) -> Any:  # noqa: N805
                self.captured = kwargs
                return type(
                    "Response", (), {"content": blocks, "stop_reason": stop_reason}
                )()

        self.messages = _Messages()


def _stream() -> io.BytesIO:
    return io.BytesIO(_PNG_BYTES)


# ---------------------------------------------------------------------------
# Backend selection
# ---------------------------------------------------------------------------


def test_openai_client_selects_openai_backend() -> None:
    service = create_ocr_service(_FakeOpenAIClient(), "gpt-4o")
    assert isinstance(service, LLMVisionOCRService)


def test_anthropic_client_selects_anthropic_backend() -> None:
    service = create_ocr_service(_FakeAnthropicClient(), "claude-opus-5")
    assert isinstance(service, AnthropicVisionOCRService)


def test_unrecognized_client_raises() -> None:
    with pytest.raises(ValueError, match="Unrecognized llm_client"):
        create_ocr_service(object(), "some-model")


# ---------------------------------------------------------------------------
# Anthropic backend
# ---------------------------------------------------------------------------


def test_anthropic_extracts_and_strips_text() -> None:
    service = AnthropicVisionOCRService(_FakeAnthropicClient(), "claude-opus-5")
    result = service.extract_text(_stream())
    assert result.text == _EXPECTED
    assert result.backend_used == "anthropic_vision"
    assert result.error is None


def test_anthropic_sends_a_base64_image_block() -> None:
    client = _FakeAnthropicClient()
    service = AnthropicVisionOCRService(client, "claude-opus-5")
    service.extract_text(_stream(), stream_info=StreamInfo(mimetype="image/png"))

    content = client.captured["messages"][0]["content"]
    image_block = next(b for b in content if b["type"] == "image")
    assert image_block["source"]["type"] == "base64"
    assert image_block["source"]["media_type"] == "image/png"
    assert image_block["source"]["data"]
    assert client.captured["model"] == "claude-opus-5"
    assert client.captured["max_tokens"] > 0


def test_anthropic_falls_back_for_unsupported_media_type() -> None:
    client = _FakeAnthropicClient()
    service = AnthropicVisionOCRService(client, "claude-opus-5")
    service.extract_text(_stream(), stream_info=StreamInfo(mimetype="image/bmp"))

    content = client.captured["messages"][0]["content"]
    image_block = next(b for b in content if b["type"] == "image")
    assert image_block["source"]["media_type"] == "image/png"


def test_anthropic_joins_multiple_text_blocks_and_skips_others() -> None:
    blocks = [
        type("Block", (), {"type": "thinking", "text": "IGNORED"})(),
        type("Block", (), {"type": "text", "text": "line one\n"})(),
        type("Block", (), {"type": "text", "text": "line two"})(),
    ]
    service = AnthropicVisionOCRService(
        _FakeAnthropicClient(blocks=blocks), "claude-opus-5"
    )
    assert service.extract_text(_stream()).text == "line one\nline two"


def test_anthropic_reports_refusal_as_an_error() -> None:
    client = _FakeAnthropicClient(blocks=[], stop_reason="refusal")
    service = AnthropicVisionOCRService(client, "claude-opus-5")
    result = service.extract_text(_stream())
    assert result.text == ""
    assert result.error == "Request was refused by the model"


def test_anthropic_custom_prompt_overrides_default() -> None:
    client = _FakeAnthropicClient()
    service = AnthropicVisionOCRService(client, "claude-opus-5")
    service.extract_text(_stream(), prompt="ONLY THE NUMBERS")

    content = client.captured["messages"][0]["content"]
    text_block = next(b for b in content if b["type"] == "text")
    assert text_block["text"] == "ONLY THE NUMBERS"


def test_anthropic_api_failure_is_returned_not_raised() -> None:
    class _FailingClient:
        class _Messages:
            def create(self, **kwargs: Any) -> Any:
                raise RuntimeError("boom")

        messages = _Messages()

    service = AnthropicVisionOCRService(_FailingClient(), "claude-opus-5")
    result = service.extract_text(_stream())
    assert result.text == ""
    assert "boom" in (result.error or "")


def test_anthropic_without_client_reports_error() -> None:
    service = AnthropicVisionOCRService(None, "claude-opus-5")
    result = service.extract_text(_stream())
    assert result.error == "Anthropic client not configured"


def test_anthropic_rewinds_the_stream() -> None:
    service = AnthropicVisionOCRService(_FakeAnthropicClient(), "claude-opus-5")
    stream = _stream()
    service.extract_text(stream)
    assert stream.tell() == 0


# ---------------------------------------------------------------------------
# OpenAI backend — unchanged behavior, guarded against regressions
# ---------------------------------------------------------------------------


def test_openai_extracts_and_strips_text() -> None:
    service = LLMVisionOCRService(_FakeOpenAIClient(), "gpt-4o")
    result = service.extract_text(_stream())
    assert result.text == _EXPECTED
    assert result.backend_used == "llm_vision"


def test_openai_sends_a_data_uri() -> None:
    client = _FakeOpenAIClient()
    service = LLMVisionOCRService(client, "gpt-4o")
    service.extract_text(_stream(), stream_info=StreamInfo(mimetype="image/png"))

    content = client.captured["messages"][0]["content"]
    image_part = next(p for p in content if p["type"] == "image_url")
    assert image_part["image_url"]["url"].startswith("data:image/png;base64,")
