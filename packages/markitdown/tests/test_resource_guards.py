#!/usr/bin/env python3 -m pytest
"""Tests for resource-exhaustion guards when converting untrusted input.

Verifies that ZipConverter refuses archives with too many members,
excessive total uncompressed size, or extreme per-member compression ratios.
"""

import io
import zipfile

import pytest

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
