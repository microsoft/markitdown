"""Regression tests: the unauthenticated MCP tool must refuse internal targets.

The ``convert_to_markdown`` tool builds a default ``MarkItDown`` instance and
forwards the caller-supplied URI. These tests assert that the destination policy
added to ``convert_uri`` is actually inherited by the tool (a :class:`ToolError`
is raised and no request is issued), so the SSRF finding cannot be bypassed at
the MCP boundary.
"""

import asyncio
from unittest.mock import MagicMock

import pytest
from mcp.server.mcpserver.exceptions import ToolError

from markitdown import MarkItDown
from markitdown_mcp import __main__ as server


def call_convert(uri: str):
    return asyncio.run(server.mcp.call_tool("convert_to_markdown", {"uri": uri}))


@pytest.mark.parametrize(
    "uri",
    [
        "http://127.0.0.1/",
        "http://localhost/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://10.0.0.5/internal",
        "http://192.168.1.1/",
        "http://[::1]/",
    ],
)
def test_internal_targets_are_refused_by_the_tool(uri):
    """A caller reaching the MCP endpoint cannot pivot to internal addresses."""
    with pytest.raises(ToolError):
        call_convert(uri)


def test_tool_does_not_issue_request_to_internal_target(monkeypatch):
    """The destination must be rejected before any socket is opened."""
    session = MagicMock()
    monkeypatch.setattr(
        server, "MarkItDown", lambda **kw: MarkItDown(requests_session=session)
    )

    with pytest.raises(ToolError):
        call_convert("http://169.254.169.254/latest/meta-data/")

    session.get.assert_not_called()
