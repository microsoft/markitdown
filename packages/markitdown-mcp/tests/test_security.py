# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

"""
Tests for MCP server security controls.

Covers issue #1905: Local file read via unsafe file:// URI resolution in
convert_to_markdown. Verifies that file:// URIs are blocked by default and
only permitted when MARKITDOWN_ALLOW_LOCAL_FILES is explicitly enabled.
"""

import asyncio
import pytest
from unittest.mock import MagicMock, patch

from markitdown_mcp.__main__ import convert_to_markdown


def test_file_uri_blocked_by_default(monkeypatch) -> None:
    """file:// URIs must raise ValueError when --allow-local-files is not set."""
    monkeypatch.delenv("MARKITDOWN_ALLOW_LOCAL_FILES", raising=False)

    with pytest.raises(ValueError, match="file:// URIs are disabled by default"):
        asyncio.run(convert_to_markdown("file:///C:/Windows/System32/drivers/etc/hosts"))


def test_file_uri_allowed_when_opted_in(monkeypatch) -> None:
    """file:// URIs must be accepted when MARKITDOWN_ALLOW_LOCAL_FILES is enabled."""
    monkeypatch.setenv("MARKITDOWN_ALLOW_LOCAL_FILES", "true")

    with patch("markitdown_mcp.__main__.MarkItDown") as mock_markitdown:
        mock_instance = MagicMock()
        mock_instance.convert_uri.return_value.markdown = "# Test"
        mock_markitdown.return_value = mock_instance

        result = asyncio.run(
            convert_to_markdown("file:///C:/Windows/System32/drivers/etc/hosts")
        )
        assert result == "# Test"


def test_http_uri_not_affected_by_restriction(monkeypatch) -> None:
    """http:// and https:// URIs must pass through regardless of the local files flag."""
    monkeypatch.delenv("MARKITDOWN_ALLOW_LOCAL_FILES", raising=False)

    with patch("markitdown_mcp.__main__.MarkItDown") as mock_markitdown:
        mock_instance = MagicMock()
        mock_instance.convert_uri.return_value.markdown = "# Test"
        mock_markitdown.return_value = mock_instance

        result = asyncio.run(convert_to_markdown("https://example.com"))
        assert result == "# Test"


def test_data_uri_not_affected_by_restriction(monkeypatch) -> None:
    """data: URIs must pass through regardless of the local files flag."""
    monkeypatch.delenv("MARKITDOWN_ALLOW_LOCAL_FILES", raising=False)

    with patch("markitdown_mcp.__main__.MarkItDown") as mock_markitdown:
        mock_instance = MagicMock()
        mock_instance.convert_uri.return_value.markdown = "# Test"
        mock_markitdown.return_value = mock_instance

        result = asyncio.run(convert_to_markdown("data:text/plain;base64,SGVsbG8="))
        assert result == "# Test"
