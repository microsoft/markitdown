"""
Unit tests for how register_converters picks and wires the OCR backend.
"""

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_ocr._ocr_service import (  # noqa: E402
    AnthropicVisionOCRService,
    LLMVisionOCRService,
)
from markitdown_ocr._plugin import register_converters  # noqa: E402
from markitdown import MarkItDown  # noqa: E402


class _FakeOpenAIClient:
    class _Completions:
        def create(self, **kwargs: Any) -> Any:
            ...

    chat = type("Chat", (), {"completions": _Completions()})()


class _FakeAnthropicClient:
    class _Messages:
        def create(self, **kwargs: Any) -> Any:
            ...

    messages = _Messages()


def _ocr_services(**kwargs: Any) -> list[Any]:
    markitdown = MarkItDown()
    register_converters(markitdown, **kwargs)
    return [
        converter.converter.ocr_service
        for converter in markitdown._converters
        if hasattr(converter.converter, "ocr_service")
    ]


def test_no_client_leaves_ocr_disabled() -> None:
    services = _ocr_services()
    assert services
    assert all(service is None for service in services)


def test_llm_client_wires_the_openai_backend() -> None:
    services = _ocr_services(llm_client=_FakeOpenAIClient(), llm_model="gpt-4o")
    assert services
    assert all(isinstance(service, LLMVisionOCRService) for service in services)


def test_ocr_llm_client_wires_the_anthropic_backend() -> None:
    services = _ocr_services(
        ocr_llm_client=_FakeAnthropicClient(), ocr_llm_model="claude-opus-5"
    )
    assert services
    assert all(isinstance(service, AnthropicVisionOCRService) for service in services)


def test_ocr_llm_client_takes_precedence_over_llm_client() -> None:
    # OpenAI for MarkItDown's own image descriptions, Claude for OCR.
    services = _ocr_services(
        llm_client=_FakeOpenAIClient(),
        llm_model="gpt-4o",
        ocr_llm_client=_FakeAnthropicClient(),
        ocr_llm_model="claude-opus-5",
    )
    assert services
    assert all(isinstance(service, AnthropicVisionOCRService) for service in services)
    assert all(service.model == "claude-opus-5" for service in services)


def test_ocr_llm_prompt_overrides_llm_prompt() -> None:
    services = _ocr_services(
        llm_client=_FakeOpenAIClient(),
        llm_model="gpt-4o",
        llm_prompt="describe this image",
        ocr_llm_prompt="transcribe this image",
    )
    assert services
    assert all(
        service.default_prompt == "transcribe this image" for service in services
    )
