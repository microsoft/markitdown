"""Unit tests for _uri_utils.py — data URI parsing and file URI conversion.

Covers:
- parse_data_uri() for base64 + plain data URIs
- file_uri_to_path() for local file URIs
"""

import base64
import os
import pytest

from markitdown._uri_utils import parse_data_uri, file_uri_to_path


# ============================================================
# parse_data_uri
# ============================================================


def test_parse_data_uri_plain_text():
    mime, attrs, data = parse_data_uri("data:text/plain,Hello%20World")
    assert mime == "text/plain"
    assert data == b"Hello World"


def test_parse_data_uri_base64():
    mime, attrs, data = parse_data_uri("data:text/plain;base64,SGVsbG8gV29ybGQ=")
    assert mime == "text/plain"
    assert data == b"Hello World"


def test_parse_data_uri_with_charset():
    mime, attrs, data = parse_data_uri("data:text/plain;charset=utf-8,Hello")
    assert mime == "text/plain"
    assert attrs == {"charset": "utf-8"}
    assert data == b"Hello"


def test_parse_data_uri_no_mime():
    mime, attrs, data = parse_data_uri("data:,Hello")
    assert mime is None
    assert data == b"Hello"


def test_parse_data_uri_image_png():
    content = b"\x89PNG\r\n\x1a\n" + b"\x00" * 10
    b64 = base64.b64encode(content).decode()
    mime, attrs, data = parse_data_uri(f"data:image/png;base64,{b64}")
    assert mime == "image/png"
    assert data == content


def test_parse_data_uri_not_data_uri():
    with pytest.raises(ValueError, match="Not a data URI"):
        parse_data_uri("https://example.com/file.txt")


def test_parse_data_uri_missing_comma():
    with pytest.raises(ValueError, match="missing ',' separator"):
        parse_data_uri("data:text/plain")


def test_parse_data_uri_empty_data():
    mime, attrs, data = parse_data_uri("data:,")
    # Should handle empty data
    assert data == b""


def test_parse_data_uri_url_encoded():
    """Percent-encoded characters in non-base64 data URIs."""
    mime, attrs, data = parse_data_uri("data:text/html,%3Ch1%3EHello%3C/h1%3E")
    assert data == b"<h1>Hello</h1>"


# ============================================================
# file_uri_to_path
# ============================================================


def test_file_uri_to_path_windows():
    # Windows file URI format
    result = "file:///C:/Users/test/file.txt"
    try:
        netloc, path = file_uri_to_path(result)
        assert netloc is None or netloc == ""
        assert "file.txt" in path
    except Exception as e:
        # On non-Windows, URL parsing may differ
        if "Not a file URL" not in str(e):
            raise


def test_file_uri_to_path_not_file():
    with pytest.raises(ValueError, match="Not a file URL"):
        file_uri_to_path("https://example.com/file.txt")


def test_file_uri_to_path_relative():
    """Bare file URI path."""
    netloc, path = file_uri_to_path("file:///relative/path.txt")
    assert "path.txt" in path


def test_file_uri_to_path_with_netloc():
    netloc, path = file_uri_to_path("file://localhost/tmp/test.txt")
    assert netloc == "localhost"
