"""MiniCPM-OCR service selection, request shape, and output normalization."""

import io
from pathlib import Path
from types import SimpleNamespace

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown_ocr._ocr_service import (
    LLMVisionOCRService,
    MiniCPMOCRService,
    create_ocr_service,
)
from markitdown_ocr._plugin import register_converters

_INFO = StreamInfo(mimetype="image/png", extension=".png")


class _Completions:
    def __init__(self, content: str | None) -> None:
        self.content = content
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=self.content))]
        )


class _Client:
    def __init__(self, content: str | None) -> None:
        self.completions = _Completions(content)
        self.chat = SimpleNamespace(completions=self.completions)


class _FailingClient:
    def __init__(self) -> None:
        self.completions = SimpleNamespace(create=self._fail)
        self.chat = SimpleNamespace(completions=self.completions)

    @staticmethod
    def _fail(**kwargs):
        raise RuntimeError("service unavailable")


def _extract(service: LLMVisionOCRService, prompt: str | None = None):
    return service.extract_text(io.BytesIO(b"image"), prompt=prompt, stream_info=_INFO)


@pytest.mark.parametrize(
    "model",
    [
        "minicpm-ocr",
        "minicpm-ocr:latest",
        "openbmb/MiniCPM-OCR-1.0",
        "MINICPM_OCR",
    ],
)
def test_minicpm_model_names_select_minicpm_service(model: str) -> None:
    assert isinstance(create_ocr_service(None, model), MiniCPMOCRService)


@pytest.mark.parametrize(
    "model",
    ["gpt-4o", "minicpm5-1b", "MiniCPM-OCR-Jev"],
)
def test_other_model_names_keep_the_generic_service(model: str) -> None:
    assert type(create_ocr_service(None, model)) is LLMVisionOCRService


def test_minicpm_request_uses_markdown_prompt_and_image_first() -> None:
    client = _Client("recognized")
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == "recognized"
    assert result.backend_used == "minicpm_ocr"
    request = client.completions.calls[0]
    assert request["model"] == "minicpm-ocr"
    assert request["temperature"] == 0.01
    assert request["top_p"] == 0.001

    content = request["messages"][0]["content"]
    assert content[0]["type"] == "image_url"
    assert content[0]["image_url"]["url"].startswith("data:image/png;base64,")
    assert content[1]["type"] == "text"
    assert "Convert this page to Markdown" in content[1]["text"]
    assert "tables as Markdown tables" in content[1]["text"]


def test_custom_prompt_overrides_the_minicpm_default() -> None:
    client = _Client("recognized")
    service = MiniCPMOCRService(
        client, "minicpm-ocr", default_prompt="Table Recognition:"
    )

    _extract(service)
    _extract(service, prompt="Seal Recognition:")

    assert client.completions.calls[0]["messages"][0]["content"][1]["text"] == (
        "Table Recognition:"
    )
    assert client.completions.calls[1]["messages"][0]["content"][1]["text"] == (
        "Seal Recognition:"
    )


def test_generic_service_keeps_text_first_and_default_sampling() -> None:
    client = _Client("recognized")
    result = _extract(create_ocr_service(client, "gpt-4o"))

    assert result.backend_used == "llm_vision"
    request = client.completions.calls[0]
    assert "temperature" not in request
    assert "top_p" not in request
    content = request["messages"][0]["content"]
    assert content[0]["type"] == "text"
    assert content[1]["type"] == "image_url"


def test_otsl_is_converted_to_a_markdown_table() -> None:
    client = _Client(
        "<otsl><fcel>Region<fcel>Sales<lcel><fcel>Growth %<nl>"
        "<ucel><fcel>2025<fcel>2026<ucel><nl>"
        "<fcel>North<fcel>120<fcel>150<fcel>25.0<nl></otsl>"
    )
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == (
        "| Region | Sales |  | Growth % |\n"
        "| --- | --- | --- | --- |\n"
        "|  | 2025 | 2026 |  |\n"
        "| North | 120 | 150 | 25.0 |"
    )


def test_fenced_otsl_is_unwrapped_before_conversion() -> None:
    client = _Client("```html\n<otsl><fcel>A<fcel>B<nl><fcel>1<fcel>2<nl></otsl>\n```")
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == "| A | B |\n| --- | --- |\n| 1 | 2 |"
    assert "```" not in result.text
    assert "<otsl>" not in result.text


def test_fenced_otsl_with_surrounding_prose_keeps_the_prose() -> None:
    client = _Client(
        "Before the table.\n\n"
        "```html\n<otsl><fcel>A<fcel>B<nl></otsl>\n```\n\n"
        "After the table."
    )
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == (
        "Before the table.\n\n| A | B |\n| --- | --- |\n\nAfter the table."
    )
    assert "```" not in result.text
    assert "<otsl>" not in result.text


def test_multiple_otsl_blocks_in_one_fence_do_not_leak_tags() -> None:
    client = _Client(
        "```html\n" "<otsl><fcel>A<nl></otsl>\n" "<otsl><fcel>B<nl></otsl>\n" "```"
    )
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == "| A |\n| --- |\n\n| B |\n| --- |"
    assert "<otsl>" not in result.text
    assert "</otsl>" not in result.text
    assert "```" not in result.text


def test_leading_thinking_block_is_removed() -> None:
    client = _Client("<think>internal reasoning</think>\n\n# Document title")
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == "# Document title"


def test_empty_otsl_table_disappears() -> None:
    client = _Client("<otsl><nl></otsl>")
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == ""


def test_unclosed_otsl_does_not_swallow_following_prose() -> None:
    client = _Client("Intro\n<otsl><fcel>A<fcel>B<nl>\nConclusion paragraph")
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == "Intro\n<otsl><fcel>A<fcel>B<nl>\nConclusion paragraph"


def test_non_otsl_fences_are_preserved() -> None:
    text_client = _Client("```text\nplain text\n```")
    code_client = _Client("```python\nprint(1)\n```")
    html_client = _Client("```html\n<div>literal</div>\n```")

    assert _extract(MiniCPMOCRService(text_client, "minicpm-ocr")).text == (
        "```text\nplain text\n```"
    )
    assert _extract(MiniCPMOCRService(code_client, "minicpm-ocr")).text == (
        "```python\nprint(1)\n```"
    )
    assert _extract(MiniCPMOCRService(html_client, "minicpm-ocr")).text == (
        "```html\n<div>literal</div>\n```"
    )


def test_generic_service_leaves_otsl_text_untouched() -> None:
    text = "<otsl><fcel>A<fcel>B<nl><fcel>1<fcel>2<nl></otsl>"
    client = _Client(text)
    result = _extract(create_ocr_service(client, "gpt-4o"))

    assert result.backend_used == "llm_vision"
    assert result.text == text


def test_factory_tolerates_a_missing_model_name() -> None:
    service = create_ocr_service(None, None)  # type: ignore[arg-type]

    assert type(service) is LLMVisionOCRService


def test_pipes_inside_otsl_cells_are_escaped() -> None:
    client = _Client("<otsl><fcel>a|b<fcel>c<nl></otsl>")
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == "| a\\|b | c |\n| --- | --- |"


def test_backslashes_before_pipes_keep_cell_boundaries() -> None:
    escaped_pipe = "\\" * 3 + "|"
    client = _Client("<otsl><fcel>\\|x\\|<fcel>c<nl></otsl>")
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == (f"| {escaped_pipe}x{escaped_pipe} | c |\n| --- | --- |")

    double_backslash_pipe = "\\" * 5 + "|"
    client = _Client("<otsl><fcel>\\\\|x<fcel>c<nl></otsl>")
    result = _extract(MiniCPMOCRService(client, "minicpm-ocr"))

    assert result.text == (f"| {double_backslash_pipe}x | c |\n| --- | --- |")


def test_missing_client_and_request_errors_keep_the_minicpm_backend() -> None:
    missing = _extract(MiniCPMOCRService(None, "minicpm-ocr"))
    assert missing.text == ""
    assert missing.error == "LLM client not configured"
    assert missing.backend_used == "minicpm_ocr"

    failed = _extract(MiniCPMOCRService(_FailingClient(), "minicpm-ocr"))
    assert failed.text == ""
    assert failed.error == "service unavailable"
    assert failed.backend_used == "minicpm_ocr"


def test_plugin_registration_selects_the_matching_service() -> None:
    minicpm = MarkItDown(enable_builtins=False)
    register_converters(minicpm, llm_client=_Client("x"), llm_model="minicpm-ocr")
    minicpm_services = [
        registration.converter.ocr_service for registration in minicpm._converters
    ]
    assert len(minicpm_services) == 4
    assert all(isinstance(service, MiniCPMOCRService) for service in minicpm_services)

    generic = MarkItDown(enable_builtins=False)
    register_converters(generic, llm_client=_Client("x"), llm_model="gpt-4o")
    generic_services = [
        registration.converter.ocr_service for registration in generic._converters
    ]
    assert len(generic_services) == 4
    assert all(type(service) is LLMVisionOCRService for service in generic_services)


def test_scanned_pdf_uses_the_minicpm_conversion() -> None:
    client = _Client("<otsl><fcel>A<fcel>B<nl><fcel>1<fcel>2<nl></otsl>")
    markitdown = MarkItDown(enable_builtins=False)
    register_converters(markitdown, llm_client=client, llm_model="minicpm-ocr")

    path = Path(__file__).parent / "ocr_test_data" / "pdf_scanned_minimal.pdf"
    result = markitdown.convert(str(path)).text_content

    assert "| A | B |" in result
    assert "| 1 | 2 |" in result
    assert "<otsl>" not in result
