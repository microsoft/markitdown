#!/usr/bin/env python3 -m pytest
import io
import os

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import GoogleSheetsConverter

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
XLSX_FIXTURE = os.path.join(TEST_FILES_DIR, "test.xlsx")

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/abc123_DEF-456/edit?usp=sharing"
)
SHEET_URL_WITH_GID = (
    "https://docs.google.com/spreadsheets/d/abc123_DEF-456/edit#gid=789"
)


def _empty_stream() -> io.BytesIO:
    return io.BytesIO(b"")


class _FakeResponse:
    def __init__(self, content: bytes, status_code: int = 200) -> None:
        self.content = content
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def test_accepts_google_sheets_urls():
    converter = GoogleSheetsConverter()

    assert converter.accepts(_empty_stream(), StreamInfo(url=SHEET_URL))
    assert converter.accepts(_empty_stream(), StreamInfo(url=SHEET_URL_WITH_GID))


def test_rejects_non_sheets_urls():
    converter = GoogleSheetsConverter()

    assert not converter.accepts(_empty_stream(), StreamInfo(url=None))
    assert not converter.accepts(_empty_stream(), StreamInfo(url=""))
    assert not converter.accepts(
        _empty_stream(), StreamInfo(url="https://example.com/spreadsheets/d/abc")
    )
    assert not converter.accepts(
        _empty_stream(), StreamInfo(url="https://docs.google.com/document/d/abc/edit")
    )
    # Drive file URLs are not spreadsheet URLs.
    assert not converter.accepts(
        _empty_stream(),
        StreamInfo(url="https://drive.google.com/file/d/abc123/view"),
    )


def test_extract_spreadsheet_id():
    assert (
        GoogleSheetsConverter._extract_spreadsheet_id(SHEET_URL) == "abc123_DEF-456"
    )
    assert (
        GoogleSheetsConverter._extract_spreadsheet_id(SHEET_URL_WITH_GID)
        == "abc123_DEF-456"
    )
    assert GoogleSheetsConverter._extract_spreadsheet_id("https://example.com") is None


def test_convert_fetches_xlsx_export(monkeypatch):
    with open(XLSX_FIXTURE, "rb") as fh:
        xlsx_bytes = fh.read()

    calls = {}

    def fake_get(url, *args, **kwargs):
        calls["url"] = url
        return _FakeResponse(xlsx_bytes)

    import markitdown.converters._google_sheets_converter as mod

    monkeypatch.setattr(mod.requests, "get", fake_get)

    converter = GoogleSheetsConverter()
    result = converter.convert(_empty_stream(), StreamInfo(url=SHEET_URL))

    assert (
        calls["url"]
        == "https://docs.google.com/spreadsheets/d/abc123_DEF-456/export?format=xlsx"
    )
    assert result.markdown.strip() != ""


def test_markitdown_dispatches_google_sheets_url(monkeypatch):
    """End-to-end: convert() with a Google Sheets URL bypasses HtmlConverter
    and uses GoogleSheetsConverter, which then fetches the XLSX export."""
    with open(XLSX_FIXTURE, "rb") as fh:
        xlsx_bytes = fh.read()

    # Mock the session.get that convert_uri uses to fetch the page bytes.
    # Returning HTML here simulates Google Sheets' editor page response.
    class _SessionResponse:
        def __init__(self) -> None:
            self.headers = {"content-type": "text/html; charset=utf-8"}
            self.url = SHEET_URL
            self._body = b"<html><body>Sheets editor</body></html>"

        def raise_for_status(self):
            return None

        def iter_content(self, chunk_size=512):
            yield self._body

    md = MarkItDown()

    monkeypatch.setattr(
        md._requests_session, "get", lambda *a, **kw: _SessionResponse()
    )

    # Mock the export fetch performed by the converter itself.
    import markitdown.converters._google_sheets_converter as mod

    monkeypatch.setattr(
        mod.requests, "get", lambda *a, **kw: _FakeResponse(xlsx_bytes)
    )

    result = md.convert(SHEET_URL)
    assert result.markdown.strip() != ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
