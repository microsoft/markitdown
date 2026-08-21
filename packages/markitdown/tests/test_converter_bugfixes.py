#!/usr/bin/env python3 -m pytest
"""Regression tests for a set of small converter correctness fixes."""
import io
import sys
import types
import zipfile

from markitdown import MarkItDown, StreamInfo
from markitdown._base_converter import DocumentConverterResult
from markitdown._uri_utils import parse_data_uri
from markitdown.__main__ import _handle_output
from markitdown.converters import RssConverter
import markitdown.converters._plain_text_converter as plain_text_converter


def test_parse_data_uri_accepts_unpadded_base64() -> None:
    # "SGVsbG8" is base64 for b"Hello" with the trailing "=" padding omitted,
    # which base64.b64decode would otherwise reject with binascii.Error.
    mimetype, _attributes, data = parse_data_uri("data:text/plain;base64,SGVsbG8")
    assert data == b"Hello"
    assert mimetype == "text/plain"


def test_rss_without_channel_title_or_description() -> None:
    # A <channel> lacking both <title> and <description> previously raised
    # UnboundLocalError because md_text was only bound inside `if channel_title`.
    rss = (
        b'<?xml version="1.0"?><rss version="2.0"><channel>'
        b"<item><title>Item Title</title><description>Body</description></item>"
        b"</channel></rss>"
    )
    result = RssConverter().convert(
        io.BytesIO(rss), StreamInfo(mimetype="application/rss+xml", extension=".rss")
    )
    assert "## Item Title" in result.markdown


def test_zip_without_name_does_not_leak_none() -> None:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as archive:
        archive.writestr("a.txt", "hello")
    buf.seek(0)
    markdown = MarkItDown().convert_stream(buf, file_extension=".zip").markdown
    assert "`None`" not in markdown.splitlines()[0]


def test_plaintext_none_detection_yields_empty_string(monkeypatch) -> None:
    # charset_normalizer's .best() returns None when nothing matches; the
    # converter must not stringify that into the literal "None".
    monkeypatch.setattr(
        plain_text_converter,
        "from_bytes",
        lambda _data: types.SimpleNamespace(best=lambda: None),
    )
    result = plain_text_converter.PlainTextConverter().convert(
        io.BytesIO(b"\x00\x01\x02"),
        StreamInfo(extension=".txt", mimetype="text/plain"),
    )
    assert result.markdown == ""


def test_handle_output_tolerates_none_stdout_encoding(monkeypatch) -> None:
    class _FakeStdout:
        encoding = None

        def __init__(self) -> None:
            self.buffer = ""

        def write(self, text: str) -> int:
            self.buffer += text
            return len(text)

        def flush(self) -> None:
            pass

    fake = _FakeStdout()
    monkeypatch.setattr(sys, "stdout", fake)
    _handle_output(
        types.SimpleNamespace(output=None),
        DocumentConverterResult(markdown="café"),
    )
    assert "caf" in fake.buffer


if __name__ == "__main__":
    import subprocess

    subprocess.run(["python", "-m", "pytest", __file__, "-v"])
