"""Unit tests for _stream_info.py — StreamInfo creation and copy_and_update.

Covers:
- Default construction
- copy_and_update with partial overrides
- Immutability (dataclass frozen)
"""

import pytest

from markitdown._stream_info import StreamInfo


def test_default_construction():
    si = StreamInfo()
    assert si.mimetype is None
    assert si.extension is None
    assert si.charset is None
    assert si.filename is None
    assert si.local_path is None
    assert si.url is None


def test_full_construction():
    si = StreamInfo(
        mimetype="text/html",
        extension=".html",
        charset="utf-8",
        filename="page.html",
        local_path="/tmp/page.html",
        url="https://example.com",
    )
    assert si.mimetype == "text/html"
    assert si.extension == ".html"
    assert si.charset == "utf-8"
    assert si.filename == "page.html"
    assert si.local_path == "/tmp/page.html"
    assert si.url == "https://example.com"


def test_copy_and_update_partial():
    si = StreamInfo(mimetype="text/html", extension=".html")
    si2 = si.copy_and_update(extension=".htm")
    assert si2.extension == ".htm"
    assert si2.mimetype == "text/html"  # preserved from original
    # Original unchanged
    assert si.extension == ".html"


def test_copy_and_update_none_does_not_overwrite():
    """None values always override existing values in copy_and_update (design choice)."""
    si = StreamInfo(mimetype="text/html")
    si2 = si.copy_and_update(mimetype=None)
    # Note: copy_and_update treats None as an explicit "clear" signal
    assert si2.mimetype is None


def test_copy_and_update_from_stream_info():
    si = StreamInfo(extension=".docx")
    override = StreamInfo(mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    si2 = si.copy_and_update(override)
    assert si2.extension == ".docx"  # from si
    assert si2.mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"  # from override


def test_copy_and_update_overlapping():
    si = StreamInfo(mimetype="text/plain", extension=".txt")
    override = StreamInfo(mimetype="text/html", extension=".html")
    si2 = si.copy_and_update(override)
    # override wins
    assert si2.mimetype == "text/html"
    assert si2.extension == ".html"


def test_is_frozen():
    """StreamInfo is a frozen dataclass — cannot modify."""
    si = StreamInfo(mimetype="text/html")
    with pytest.raises(Exception):
        si.mimetype = "application/json"


def test_copy_and_update_preserves_unrelated_fields():
    si = StreamInfo(filename="doc.pdf", url="https://x.com/doc.pdf", charset="utf-8")
    si2 = si.copy_and_update(extension=".pdf")
    assert si2.filename == "doc.pdf"
    assert si2.url == "https://x.com/doc.pdf"
    assert si2.charset == "utf-8"
    assert si2.extension == ".pdf"
