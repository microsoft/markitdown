import asyncio
import errno
import os
from unittest.mock import Mock

import httpx2 as httpx
import pytest
import requests
from markitdown import (
    DocumentConverter,
    FileConversionException,
    MarkItDown,
    MarkItDownException,
    UnsupportedFormatException,
)
from mcp.server.mcpserver.exceptions import ToolError, UnexpectedToolError
from requests.exceptions import ConnectionError, HTTPError, Timeout

from markitdown_mcp import __main__ as server


def call_convert(uri: str = "https://example.com/sample.pdf"):
    return asyncio.run(server.mcp.call_tool("convert_to_markdown", {"uri": uri}))


def original_cause(exc):
    """The first non-ToolError in the __cause__ chain.

    Sanitized detail is withheld from the client but retained on the chain. The
    SDK re-wraps the tool's ToolError in one of its own, so walk past every
    ToolError rather than assuming a fixed depth.
    """
    while isinstance(exc, ToolError):
        exc = exc.__cause__
    return exc


@pytest.mark.parametrize(
    "error",
    [
        UnsupportedFormatException("No converter supports this format."),
        ValueError(
            "Unsupported URI scheme: gopher. Supported schemes are: "
            "file:, data:, http:, https:"
        ),
    ],
)
def test_client_input_failures_reach_the_sdk(monkeypatch, error):
    """Diagnoses that only restate the client's own input are returned verbatim."""
    converter = Mock()
    converter.convert_uri.side_effect = error
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    with pytest.raises(ToolError) as raised:
        call_convert()

    assert not isinstance(raised.value, UnexpectedToolError)
    assert str(error) in str(raised.value)


def test_http_status_is_returned_without_transport_details(monkeypatch):
    response = requests.Response()
    response.status_code = 404
    error = HTTPError(
        "404 Client Error: Not Found for url: https://internal.corp/sample.pdf",
        response=response,
    )
    converter = Mock()
    converter.convert_uri.side_effect = error
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    with pytest.raises(ToolError) as raised:
        call_convert()

    assert not isinstance(raised.value, UnexpectedToolError)
    assert "HTTP status 404" in str(raised.value)
    assert "internal.corp" not in str(raised.value)
    assert original_cause(raised.value) is error


@pytest.mark.parametrize(
    "error",
    [
        # requests exceptions subclass OSError, and their messages describe the
        # server's own network position rather than the client's request.
        ConnectionError(
            "HTTPSConnectionPool(host='10.0.0.5', port=443): Max retries exceeded "
            "(Caused by ProxyError('Unable to connect to proxy', "
            "NameResolutionError(\"Failed to resolve 'proxy.internal.corp'\")))"
        ),
        Timeout(
            "HTTPSConnectionPool(host='10.0.0.5', port=443): Read timed out. "
            "(proxy.internal.corp)"
        ),
    ],
)
def test_network_failure_details_remain_private(monkeypatch, error):
    converter = Mock()
    converter.convert_uri.side_effect = error
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    with pytest.raises(ToolError) as raised:
        call_convert()

    message = str(raised.value)
    assert not isinstance(raised.value, UnexpectedToolError)
    assert "Could not fetch the resource" in message
    assert "10.0.0.5" not in message
    assert "proxy.internal.corp" not in message
    assert "proxy.internal.corp" in str(original_cause(raised.value))


def test_local_read_failure_reports_errno_without_the_path(monkeypatch):
    error = PermissionError(
        errno.EACCES, os.strerror(errno.EACCES), "/srv/private/sample.pdf"
    )
    converter = Mock()
    converter.convert_uri.side_effect = error
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    with pytest.raises(ToolError) as raised:
        call_convert("file:///srv/private/sample.pdf")

    message = str(raised.value)
    assert not isinstance(raised.value, UnexpectedToolError)
    assert os.strerror(errno.EACCES) in message
    assert "/srv/private/sample.pdf" not in message
    assert "/srv/private/sample.pdf" in str(original_cause(raised.value))


@pytest.mark.parametrize("error_type", [RuntimeError, MarkItDownException])
def test_unexpected_failure_details_remain_private(monkeypatch, error_type):
    converter = Mock()
    converter.convert_uri.side_effect = error_type("internal implementation detail")
    monkeypatch.setattr(server, "MarkItDown", Mock(return_value=converter))

    with pytest.raises(UnexpectedToolError) as raised:
        call_convert("file:///sample.pdf")

    assert "internal implementation detail" not in str(raised.value)


def crashing_markitdown(error_type, private_detail):
    """A MarkItDown whose sole converter raises, to exercise the real
    convert_uri/_convert pipeline that aggregates converter exceptions into
    FileConversionException."""

    class CrashingConverter(DocumentConverter):
        def accepts(self, file_stream, stream_info, **kwargs):
            return True

        def convert(self, file_stream, stream_info, **kwargs):
            raise error_type(private_detail)

    converter = MarkItDown(enable_builtins=False, enable_plugins=False)
    converter.register_converter(CrashingConverter())
    return converter


@pytest.mark.parametrize("error_type", [RuntimeError, ValueError, OSError])
def test_wrapped_converter_crash_retains_the_cause(monkeypatch, error_type):
    private_detail = "private converter implementation detail"
    # Replace only construction, so the real pipeline does the aggregation.
    monkeypatch.setattr(
        server,
        "MarkItDown",
        Mock(return_value=crashing_markitdown(error_type, private_detail)),
    )

    with pytest.raises(ToolError) as raised:
        call_convert("data:text/plain,example")

    assert "File conversion failed" in str(raised.value)
    assert private_detail not in str(raised.value)

    cause = original_cause(raised.value)
    assert isinstance(cause, FileConversionException)
    assert cause.attempts
    for attempt in cause.attempts:
        assert isinstance(attempt.exc_info[1], error_type)
        assert str(attempt.exc_info[1]) == private_detail
        assert attempt.exc_info[2] is not None


@pytest.mark.parametrize("error_type", [RuntimeError, ValueError, OSError])
def test_wrapped_converter_crash_remains_private_over_http(monkeypatch, error_type):
    private_detail = "private converter implementation detail"
    monkeypatch.setattr(
        server,
        "MarkItDown",
        Mock(return_value=crashing_markitdown(error_type, private_detail)),
    )

    async def call_tool():
        app = server.create_starlette_app(server.mcp)
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url="http://127.0.0.1:3001",
                headers={"accept": "application/json, text/event-stream"},
            ) as client:
                return await client.post(
                    "/mcp",
                    json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {
                            "name": "convert_to_markdown",
                            "arguments": {"uri": "data:text/plain,example"},
                        },
                    },
                )

    response = asyncio.run(asyncio.wait_for(call_tool(), timeout=15))

    assert response.status_code == 200
    result = response.json()["result"]
    assert result["isError"] is True
    assert "File conversion failed" in result["content"][0]["text"]
    assert private_detail not in response.text
    assert error_type.__name__ not in response.text
    assert "CrashingConverter" not in response.text
