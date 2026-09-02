#!/usr/bin/env python3 -m pytest
"""Tests for resource-exhaustion guards when converting untrusted input.

Verifies that:
- ZipConverter refuses archives with too many members, excessive total
  uncompressed size, or extreme per-member compression ratios.
- URL fetches apply an explicit timeout and refuse oversized responses.
"""

import io
import zipfile

import pytest
import requests

from unittest.mock import MagicMock

from markitdown import (
    MarkItDown,
    StreamInfo,
    FileConversionException,
)


def _make_zip(members, compression=zipfile.ZIP_DEFLATED):
    """Build an in-memory ZIP archive from a {name: bytes} mapping."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=compression) as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    buffer.seek(0)
    return buffer


def _convert_zip(markitdown, zip_stream, **kwargs):
    return markitdown.convert_stream(
        zip_stream,
        stream_info=StreamInfo(extension=".zip", mimetype="application/zip"),
        **kwargs,
    )


class TestZipConverterGuards:
    """ZipConverter refuses archives that exceed resource limits."""

    def test_member_count_limit(self):
        markitdown = MarkItDown()
        archive = _make_zip({f"file_{i}.txt": b"hello" for i in range(3)})

        with pytest.raises(FileConversionException, match="members"):
            _convert_zip(markitdown, archive, zip_max_members=2)

    def test_compression_ratio_limit(self):
        markitdown = MarkItDown()
        # 2 MB of zeros compresses to ~2 KB (a ratio of roughly 1000:1)
        archive = _make_zip({"zeros.bin": b"\x00" * (2 * 1024 * 1024)})
        assert archive.getbuffer().nbytes < 100 * 1024

        with pytest.raises(FileConversionException, match="compression ratio"):
            _convert_zip(markitdown, archive)

    def test_small_compressible_members_allowed(self):
        # Members below the ratio-check floor compress well legitimately
        markitdown = MarkItDown()
        archive = _make_zip({"small.txt": b"a" * 4096})

        result = _convert_zip(markitdown, archive)

        assert "a" * 100 in result.markdown

    def test_total_uncompressed_size_limit(self):
        markitdown = MarkItDown()
        archive = _make_zip(
            {
                "a.txt": b"a" * 600,
                "b.txt": b"b" * 600,
            }
        )

        with pytest.raises(FileConversionException, match="total uncompressed size"):
            _convert_zip(markitdown, archive, zip_max_total_uncompressed_size=1024)

    def test_normal_archive_converts(self):
        markitdown = MarkItDown()
        archive = _make_zip({"notes.txt": b"Sample text for resource guard tests."})

        result = _convert_zip(markitdown, archive)

        assert "Sample text for resource guard tests." in result.markdown


def _mock_response(chunks, headers=None, url="https://example.com/file.txt"):
    """Build a mock requests.Response streaming the given chunks."""
    response = MagicMock(spec=requests.Response)
    response.headers = headers or {}
    response.url = url
    response.raise_for_status = MagicMock()
    response.iter_content = MagicMock(return_value=iter(chunks))
    return response


class TestUrlFetchGuards:
    """URL fetches apply an explicit timeout and a response size limit."""

    def test_default_timeout_applied(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response([b"Hello from the mock server."])
        markitdown = MarkItDown(requests_session=session)

        result = markitdown.convert("https://example.com/file.txt")

        session.get.assert_called_once_with(
            "https://example.com/file.txt", stream=True, timeout=30
        )
        assert "Hello from the mock server." in result.markdown

    def test_custom_timeout_applied(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response([b"Hello from the mock server."])
        markitdown = MarkItDown(requests_session=session)

        markitdown.convert("https://example.com/file.txt", timeout=5)

        session.get.assert_called_once_with(
            "https://example.com/file.txt", stream=True, timeout=5
        )

    def test_timeout_error_surfaces(self):
        session = MagicMock(spec=requests.Session)
        session.get.side_effect = requests.Timeout("Connection timed out")
        markitdown = MarkItDown(requests_session=session)

        with pytest.raises(requests.Timeout):
            markitdown.convert("https://example.com/file.txt")

    def test_content_length_over_limit_rejected(self):
        session = MagicMock(spec=requests.Session)
        response = _mock_response(
            [b"x" * 512],
            headers={"content-length": str(200 * 1024 * 1024)},
        )
        session.get.return_value = response
        markitdown = MarkItDown(requests_session=session)

        with pytest.raises(FileConversionException, match="maximum supported size"):
            markitdown.convert("https://example.com/file.txt")

        # The body is never streamed when the declared length is over the limit
        response.iter_content.assert_not_called()

    def test_streaming_over_limit_aborted(self):
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response([b"x" * 512] * 4)
        markitdown = MarkItDown(requests_session=session)

        with pytest.raises(FileConversionException, match="maximum supported size"):
            markitdown.convert("https://example.com/file.txt", max_response_size=1024)

    def test_response_at_limit_converts(self):
        text_chunk = (b"Hello world. " * 44)[:512]
        session = MagicMock(spec=requests.Session)
        session.get.return_value = _mock_response([text_chunk, text_chunk])
        markitdown = MarkItDown(requests_session=session)

        # Exactly 1024 bytes is allowed when the limit is 1024
        result = markitdown.convert(
            "https://example.com/file.txt", max_response_size=1024
        )

        assert "Hello world." in result.markdown
