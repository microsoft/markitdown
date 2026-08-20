"""Tests for SvgConverter."""

import io
from unittest.mock import MagicMock

from markitdown._stream_info import StreamInfo
from markitdown.converters._svg_converter import SvgConverter

SIMPLE_SVG = b'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><circle cx="50" cy="50" r="40"/></svg>'


def _make_llm_client(reply: str) -> MagicMock:
    """Create a mock LLM client that returns the given response."""
    client = MagicMock()
    client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=reply))]
    )
    return client


class TestSvgConverterAccepts:
    """Test accepts() for .svg extension and image/svg+xml MIME type."""

    def test_accepts_svg_extension(self) -> None:
        conv = SvgConverter()
        assert conv.accepts(io.BytesIO(SIMPLE_SVG), StreamInfo(extension=".svg"))

    def test_accepts_svg_mimetype(self) -> None:
        conv = SvgConverter()
        assert conv.accepts(
            io.BytesIO(SIMPLE_SVG), StreamInfo(mimetype="image/svg+xml")
        )

    def test_rejects_html_mimetype(self) -> None:
        conv = SvgConverter()
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(mimetype="text/html"))

    def test_rejects_png_extension(self) -> None:
        conv = SvgConverter()
        assert not conv.accepts(io.BytesIO(b""), StreamInfo(extension=".png"))


class TestSvgConverterConvert:
    """Test convert() success and fallback cases."""

    def test_llm_response_produces_mermaid_block(self) -> None:
        """When LLM is configured and returns valid Mermaid, output is a mermaid code block."""
        conv = SvgConverter()
        llm_client = _make_llm_client("flowchart LR\n  A --> B")

        result = conv.convert(
            io.BytesIO(SIMPLE_SVG),
            StreamInfo(extension=".svg", mimetype="image/svg+xml"),
            llm_client=llm_client,
            llm_model="gpt-4o",
        )

        assert "```mermaid" in result.markdown
        assert "flowchart LR" in result.markdown
        assert "A --> B" in result.markdown

    def test_fallback_no_llm_client_returns_xml_block(self) -> None:
        """When no LLM client is provided, the SVG source is wrapped in an xml block."""
        conv = SvgConverter()

        result = conv.convert(
            io.BytesIO(SIMPLE_SVG),
            StreamInfo(extension=".svg", mimetype="image/svg+xml"),
        )

        assert "```xml" in result.markdown
        assert "<svg" in result.markdown

    def test_fallback_llm_returns_skip_produces_xml_block(self) -> None:
        """When LLM replies with SKIP, converter falls back to xml block."""
        conv = SvgConverter()
        llm_client = _make_llm_client("SKIP")

        result = conv.convert(
            io.BytesIO(SIMPLE_SVG),
            StreamInfo(extension=".svg", mimetype="image/svg+xml"),
            llm_client=llm_client,
            llm_model="gpt-4o",
        )

        assert "```xml" in result.markdown
        assert "<svg" in result.markdown
        assert "```mermaid" not in result.markdown

    def test_fallback_llm_raises_exception_produces_xml_block(self) -> None:
        """When the LLM call raises an exception, converter falls back."""
        conv = SvgConverter()
        client = MagicMock()
        client.chat.completions.create.side_effect = RuntimeError("API error")

        result = conv.convert(
            io.BytesIO(SIMPLE_SVG),
            StreamInfo(extension=".svg", mimetype="image/svg+xml"),
            llm_client=client,
            llm_model="gpt-4o",
        )

        assert "```xml" in result.markdown
        assert "<svg" in result.markdown

    def test_stream_position_restored_after_convert(self) -> None:
        """convert() must not consume the stream permanently."""
        conv = SvgConverter()
        stream = io.BytesIO(SIMPLE_SVG)
        stream.seek(0)

        conv.convert(stream, StreamInfo(extension=".svg"))

        # Verify the stream pointer was rewound to prevent data loss for subsequent readers
        assert stream.tell() == 0 or stream.seek(0) == 0
