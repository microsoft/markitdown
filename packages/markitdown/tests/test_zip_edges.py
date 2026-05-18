"""Edge-case tests for ZipConverter — corrupt, empty, nested archives.

Tests ZIP handling beyond the happy-path test vector.
"""

import io
import os
import zipfile
import pytest

from markitdown import MarkItDown, StreamInfo, FileConversionException


def _make_md():
    return MarkItDown()


def _make_empty_zip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        pass
    return buf.getvalue()


def _make_zip_with_txt(name: str, content: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        zf.writestr(name, content)
    return buf.getvalue()


def _convert_zip(data: bytes) -> str:
    md = _make_md()
    result = md.convert(
        io.BytesIO(data),
        stream_info=StreamInfo(extension=".zip", mimetype="application/zip"),
    )
    return result.markdown


# ============================================================
# Empty ZIP
# ============================================================


def test_empty_zip_converts_without_error():
    result = _convert_zip(_make_empty_zip())
    assert isinstance(result, str)
    # Should produce some output (at least the heading)
    assert len(result) > 0


# ============================================================
# ZIP with various file types
# ============================================================


def test_zip_with_single_txt_file():
    result = _convert_zip(
        _make_zip_with_txt("readme.txt", "Hello from ZIP!")
    )
    assert "readme.txt" in result
    assert "Hello from ZIP!" in result


def test_zip_with_multiple_txt_files():
    result = _convert_zip(
        _make_zip_with_txt("a.txt", "A content") +
        b"=" * 0  # placeholder — actually build separately
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        zf.writestr("a.txt", "Content A")
        zf.writestr("b.txt", "Content B")
    result = _convert_zip(buf.getvalue())
    assert "a.txt" in result
    assert "b.txt" in result


def test_zip_with_subdirectory():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        zf.writestr("subdir/file.txt", "Inside subdirectory")
    result = _convert_zip(buf.getvalue())
    assert "subdir/file.txt" in result
    assert "Inside subdirectory" in result


def test_zip_with_csv_file():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        zf.writestr("data.csv", "Name,Value\nA,1\nB,2")
    result = _convert_zip(buf.getvalue())
    assert "data.csv" in result
    # CSV should be converted to markdown table
    assert "Name" in result
    assert "Value" in result


# ============================================================
# ZIP with unsupported files
# ============================================================


def test_zip_with_unsupported_extension():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        zf.writestr("data.bin", b"\x00\x01\x02\x03")
    result = _convert_zip(buf.getvalue())
    # Should still produce output with the filename
    assert "data.bin" in result


# ============================================================
# Corrupt ZIP
# ============================================================


def test_corrupt_zip_not_a_zip():
    md = _make_md()
    # Falls through to PlainTextConverter when ZIP parsing fails
    result = md.convert(
        io.BytesIO(b"this is not a zip file at all"),
        stream_info=StreamInfo(extension=".zip", mimetype="application/zip"),
    )
    assert isinstance(result.markdown, str)


def test_truncated_zip():
    md = _make_md()
    truncated = b"PK\x03\x04" + b"\x00" * 20
    # Some truncated ZIPs cause BadZipFile → raises FileConversionException
    try:
        result = md.convert(
            io.BytesIO(truncated),
            stream_info=StreamInfo(extension=".zip", mimetype="application/zip"),
        )
        assert isinstance(result.markdown, str)
    except FileConversionException:
        pass  # Also acceptable


# ============================================================
# ZIP with binary data
# ============================================================


def test_zip_with_image_file():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        zf.writestr("photo.jpg", b"\xff\xd8\xff\xe0" + b"\x00" * 100)
    result = _convert_zip(buf.getvalue())
    assert "photo.jpg" in result


def test_zip_with_mixed_content():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_STORED) as zf:
        zf.writestr("docs/readme.md", "# Project")
        zf.writestr("data.csv", "id,name\n1,foo\n2,bar")
        zf.writestr("images/logo.png", b"\x89PNG\r\n\x1a\n" + b"\x00" * 20)
    result = _convert_zip(buf.getvalue())
    assert "docs/readme.md" in result
    assert "data.csv" in result
    assert "images/logo.png" in result
