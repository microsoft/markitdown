import asyncio
import os
import stat
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from markitdown_mcp.__main__ import convert_to_markdown, mcp

URI = "file:///tmp/example.txt"
MARKDOWN = "# Example\n\nConverted text with unicode: cafe \N{HOT BEVERAGE}.\n"


def test_convert_to_markdown_returns_content_by_default(monkeypatch) -> None:
    monkeypatch.delenv("MARKITDOWN_ENABLE_PLUGINS", raising=False)
    conversion = MagicMock(markdown=MARKDOWN)

    with patch("markitdown_mcp.__main__.MarkItDown") as markitdown:
        markitdown.return_value.convert_uri.return_value = conversion
        result = asyncio.run(convert_to_markdown(URI))

    assert result == MARKDOWN
    markitdown.assert_called_once_with(enable_plugins=False)
    markitdown.return_value.convert_uri.assert_called_once_with(URI)


def test_convert_to_markdown_can_write_output_file(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("MARKITDOWN_ENABLE_PLUGINS", raising=False)
    conversion = MagicMock(markdown=MARKDOWN)
    output_path = tmp_path / "converted.md"

    with patch("markitdown_mcp.__main__.MarkItDown") as markitdown:
        markitdown.return_value.convert_uri.return_value = conversion
        result = asyncio.run(convert_to_markdown(URI, output_file=str(output_path)))

    assert result == str(output_path.resolve())
    assert output_path.read_bytes() == MARKDOWN.encode("utf-8")
    if os.name != "nt":
        assert stat.S_IMODE(output_path.stat().st_mode) == 0o600


def test_convert_to_markdown_does_not_overwrite(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("MARKITDOWN_ENABLE_PLUGINS", raising=False)
    output_path = tmp_path / "existing.md"
    output_path.write_bytes(b"existing")

    with patch("markitdown_mcp.__main__.MarkItDown") as markitdown:
        markitdown.return_value.convert_uri.return_value = MagicMock(markdown=MARKDOWN)
        with pytest.raises(FileExistsError):
            asyncio.run(convert_to_markdown(URI, output_file=str(output_path)))

    assert output_path.read_bytes() == b"existing"


def test_convert_to_markdown_removes_partial_file(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("MARKITDOWN_ENABLE_PLUGINS", raising=False)
    output_path = tmp_path / "partial.md"

    with (
        patch("markitdown_mcp.__main__.MarkItDown") as markitdown,
        patch("markitdown_mcp.__main__.os.fdopen", side_effect=OSError("write failed")),
    ):
        markitdown.return_value.convert_uri.return_value = MagicMock(markdown=MARKDOWN)
        with pytest.raises(OSError, match="write failed"):
            asyncio.run(convert_to_markdown(URI, output_file=str(output_path)))

    assert not output_path.exists()


def test_convert_to_markdown_preserves_plugin_setting(monkeypatch) -> None:
    monkeypatch.setenv("MARKITDOWN_ENABLE_PLUGINS", "true")
    conversion = MagicMock(markdown=MARKDOWN)

    with patch("markitdown_mcp.__main__.MarkItDown") as markitdown:
        markitdown.return_value.convert_uri.return_value = conversion
        result = asyncio.run(convert_to_markdown(URI))

    assert result == MARKDOWN
    markitdown.assert_called_once_with(enable_plugins=True)


def test_mcp_schema_and_tool_call(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("MARKITDOWN_ENABLE_PLUGINS", raising=False)
    tools = asyncio.run(mcp.list_tools())
    tool = next(tool for tool in tools if tool.name == "convert_to_markdown")
    output_schema = tool.inputSchema["properties"]["output_file"]
    assert output_schema == {
        "anyOf": [{"type": "string"}, {"type": "null"}],
        "default": None,
        "title": "Output File",
    }
    assert tool.inputSchema["required"] == ["uri"]

    output_path = tmp_path / "mcp-output.md"
    with patch("markitdown_mcp.__main__.MarkItDown") as markitdown:
        markitdown.return_value.convert_uri.return_value = MagicMock(markdown=MARKDOWN)
        result = asyncio.run(
            mcp.call_tool(
                "convert_to_markdown",
                {"uri": URI, "output_file": str(output_path)},
            )
        )

    assert len(result) == 1
    assert result[0].type == "text"
    assert result[0].text == str(output_path.resolve())
    assert output_path.read_bytes() == MARKDOWN.encode("utf-8")
