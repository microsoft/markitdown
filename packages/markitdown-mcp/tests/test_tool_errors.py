import asyncio
from unittest.mock import Mock

import pytest
from markitdown import FileConversionException, UnsupportedFormatException
from mcp.server.mcpserver.exceptions import ToolError, UnexpectedToolError
from requests.exceptions import HTTPError, Timeout

from markitdown_mcp import __main__ as server


@pytest.mark.parametrize(
    "error",
    [
        FileConversionException("The PDF could not be decoded."),
        UnsupportedFormatException("No converter supports this format."),
        PermissionError("Permission denied: sample.pdf"),
        HTTPError(
            "404 Client Error: Not Found for url: https://example.com/sample.pdf"
        ),
        Timeout("The request to https://example.com/sample.pdf timed out."),
    ],
)
def test_expected_failure_details_reach_the_sdk(monkeypatch, error):
    converter = Mock()
    converter.convert_uri.side_effect = error
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    with pytest.raises(ToolError) as raised:
        asyncio.run(
            server.mcp.call_tool(
                "convert_to_markdown", {"uri": "https://example.com/sample.pdf"}
            )
        )

    assert not isinstance(raised.value, UnexpectedToolError)
    assert str(error) in str(raised.value)


def test_unexpected_failure_details_remain_private(monkeypatch):
    converter = Mock()
    converter.convert_uri.side_effect = RuntimeError("internal implementation detail")
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    with pytest.raises(UnexpectedToolError) as raised:
        asyncio.run(
            server.mcp.call_tool("convert_to_markdown", {"uri": "file:///sample.pdf"})
        )

    assert "internal implementation detail" not in str(raised.value)
