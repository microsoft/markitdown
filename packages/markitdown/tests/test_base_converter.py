"""Unit tests for DocumentConverter base class methods.

Covers:
- _accepted_by_mime_or_ext() static method
- _accepted_by_url_pattern() static method
- DocumentConverterResult properties
"""

import re
import pytest

from markitdown._base_converter import DocumentConverter, DocumentConverterResult
from markitdown._stream_info import StreamInfo


# ============================================================
# _accepted_by_mime_or_ext
# ============================================================


def test_accepted_by_extension_match():
    si = StreamInfo(extension=".docx")
    assert DocumentConverter._accepted_by_mime_or_ext(
        si, [], [".docx"]
    )


def test_accepted_by_extension_case_insensitive():
    si = StreamInfo(extension=".DOCX")
    assert DocumentConverter._accepted_by_mime_or_ext(
        si, [], [".docx"]
    )


def test_accepted_by_mime_prefix():
    si = StreamInfo(mimetype="text/html; charset=utf-8")
    assert DocumentConverter._accepted_by_mime_or_ext(
        si, ["text/html"], []
    )


def test_accepted_by_mime_subtype_prefix():
    si = StreamInfo(mimetype="application/xhtml+xml")
    assert DocumentConverter._accepted_by_mime_or_ext(
        si, ["application/xhtml"], []
    )


def test_accepted_by_mime_case_insensitive():
    si = StreamInfo(mimetype="TEXT/HTML")
    assert DocumentConverter._accepted_by_mime_or_ext(
        si, ["text/html"], []
    )


def test_not_accepted_by_unknown_extension():
    si = StreamInfo(extension=".unknown")
    assert not DocumentConverter._accepted_by_mime_or_ext(
        si, ["text/html"], [".html"]
    )


def test_not_accepted_by_mismatched_mime():
    si = StreamInfo(mimetype="image/png")
    assert not DocumentConverter._accepted_by_mime_or_ext(
        si, ["text/html"], []
    )


def test_accepted_by_extension_when_mime_none():
    si = StreamInfo(extension=".csv")
    assert DocumentConverter._accepted_by_mime_or_ext(
        si, [], [".csv"]
    )


def test_accepted_by_mime_when_extension_none():
    si = StreamInfo(mimetype="text/markdown")
    assert DocumentConverter._accepted_by_mime_or_ext(
        si, ["text/markdown"], []
    )


# ============================================================
# _accepted_by_url_pattern
# ============================================================


def test_accepted_by_url_pattern_match():
    si = StreamInfo(url="https://www.youtube.com/watch?v=abc123")
    assert DocumentConverter._accepted_by_url_pattern(
        si, r"^https://www\.youtube\.com/watch\?"
    )


def test_accepted_by_url_pattern_no_match():
    si = StreamInfo(url="https://www.google.com/search")
    assert not DocumentConverter._accepted_by_url_pattern(
        si, r"^https://www\.youtube\.com/watch\?"
    )


def test_accepted_by_url_pattern_no_url():
    si = StreamInfo(url=None)
    assert not DocumentConverter._accepted_by_url_pattern(si, r"anything")


def test_accepted_by_url_pattern_empty_url():
    si = StreamInfo(url="")
    assert not DocumentConverter._accepted_by_url_pattern(si, r"anything")


def test_accepted_by_url_pattern_partial_match():
    si = StreamInfo(url="https://www.bing.com/search?q=test")
    assert DocumentConverter._accepted_by_url_pattern(
        si, r"bing\.com/search\?q="
    )


# ============================================================
# DocumentConverterResult
# ============================================================


def test_result_markdown():
    r = DocumentConverterResult(markdown="# Hello")
    assert r.markdown == "# Hello"
    assert r.text_content == "# Hello"
    assert str(r) == "# Hello"


def test_result_title():
    r = DocumentConverterResult(markdown="# Hello", title="Hello")
    assert r.title == "Hello"
    assert r.markdown == "# Hello"


def test_result_text_content_setter():
    r = DocumentConverterResult(markdown="old")
    r.text_content = "new"
    assert r.markdown == "new"
    assert r.text_content == "new"


def test_result_empty():
    r = DocumentConverterResult(markdown="")
    assert r.markdown == ""
    assert str(r) == ""


def test_result_title_none_by_default():
    r = DocumentConverterResult(markdown="content")
    assert r.title is None
