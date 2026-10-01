#!/usr/bin/env python3 -m pytest
"""Tests for PDF metadata extraction in PdfConverter.

Verifies that:
- PDF metadata fields (title, author, dates, etc.) appear in the output
- PDF date strings are parsed into YYYY-MM-DD format
- Missing or empty metadata fields are silently skipped
- Documents with no metadata produce no metadata section
"""

import io
from unittest.mock import patch, MagicMock

import pytest

from markitdown.converters._pdf_converter import _parse_pdf_date, _extract_pdf_metadata
from markitdown import MarkItDown, StreamInfo


# ---------------------------------------------------------------------------
# Unit tests for helper functions
# ---------------------------------------------------------------------------


class TestParsePdfDate:
    def test_full_date_string(self):
        assert _parse_pdf_date("D:20230615120000+00'00'") == "2023-06-15"

    def test_date_only(self):
        assert _parse_pdf_date("D:20210101") == "2021-01-01"

    def test_year_and_month(self):
        # Day defaults to "01" when not present
        assert _parse_pdf_date("D:202306") == "2023-06-01"

    def test_no_d_prefix_returned_as_is(self):
        assert _parse_pdf_date("20230615") == "20230615"

    def test_empty_string(self):
        assert _parse_pdf_date("") == ""

    def test_non_string_returns_as_is(self):
        assert _parse_pdf_date(None) is None  # type: ignore[arg-type]


class TestExtractPdfMetadata:
    def test_full_metadata(self):
        meta = {
            "Title": "Annual Report 2023",
            "Author": "Jane Smith",
            "Subject": "Finance",
            "Keywords": "finance, annual",
            "Creator": "Microsoft Word",
            "Producer": "Adobe PDF Library",
            "CreationDate": "D:20230615",
            "ModDate": "D:20230620",
        }
        result = _extract_pdf_metadata(meta)
        assert "## Document Properties" in result
        assert "**Title:** Annual Report 2023" in result
        assert "**Author:** Jane Smith" in result
        assert "**Subject:** Finance" in result
        assert "**Keywords:** finance, annual" in result
        assert "**Creator:** Microsoft Word" in result
        assert "**Producer:** Adobe PDF Library" in result
        assert "**Created:** 2023-06-15" in result
        assert "**Modified:** 2023-06-20" in result

    def test_empty_metadata_returns_empty_string(self):
        assert _extract_pdf_metadata({}) == ""

    def test_all_empty_values_returns_empty_string(self):
        assert _extract_pdf_metadata({"Title": "", "Author": ""}) == ""

    def test_partial_metadata(self):
        result = _extract_pdf_metadata({"Title": "My Doc", "Author": "Bob"})
        assert "**Title:** My Doc" in result
        assert "**Author:** Bob" in result
        assert "Subject" not in result

    def test_bytes_values_decoded(self):
        result = _extract_pdf_metadata({"Title": b"Bytes Title"})
        assert "**Title:** Bytes Title" in result

    def test_dates_are_parsed(self):
        result = _extract_pdf_metadata({"CreationDate": "D:20220101"})
        assert "**Created:** 2022-01-01" in result
        assert "D:" not in result


# ---------------------------------------------------------------------------
# Integration tests via MarkItDown.convert_stream
# ---------------------------------------------------------------------------


def _mock_pdfplumber_open(metadata: dict, pages=None):
    """Return a pdfplumber.open mock with the given metadata and optional pages."""
    if pages is None:
        page = MagicMock()
        page.width = 612
        page.close = MagicMock()
        page.extract_words.return_value = []
        page.extract_text.return_value = "Sample text content."
        pages = [page]

    def mock_open(stream):
        mock_pdf = MagicMock()
        mock_pdf.pages = pages
        mock_pdf.metadata = metadata
        mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
        mock_pdf.__exit__ = MagicMock(return_value=False)
        return mock_pdf

    return mock_open


class TestPdfMetadataInOutput:
    def test_title_and_author_appear_in_output(self):
        metadata = {"Title": "Test Document", "Author": "Alice"}

        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber, patch(
            "markitdown.converters._pdf_converter.pdfminer"
        ) as mock_pdfminer:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open(metadata)
            mock_pdfminer.high_level.extract_text.return_value = "Body text here."

            md = MarkItDown()
            result = md.convert_stream(
                io.BytesIO(b"fake pdf"),
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        assert "## Document Properties" in result.text_content
        assert "**Title:** Test Document" in result.text_content
        assert "**Author:** Alice" in result.text_content

    def test_creation_date_parsed(self):
        metadata = {"CreationDate": "D:20240301"}

        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber, patch(
            "markitdown.converters._pdf_converter.pdfminer"
        ) as mock_pdfminer:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open(metadata)
            mock_pdfminer.high_level.extract_text.return_value = "Body."

            md = MarkItDown()
            result = md.convert_stream(
                io.BytesIO(b"fake pdf"),
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        assert "**Created:** 2024-03-01" in result.text_content

    def test_no_metadata_section_when_empty(self):
        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber, patch(
            "markitdown.converters._pdf_converter.pdfminer"
        ) as mock_pdfminer:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open({})
            mock_pdfminer.high_level.extract_text.return_value = "Just text."

            md = MarkItDown()
            result = md.convert_stream(
                io.BytesIO(b"fake pdf"),
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        assert "## Document Properties" not in result.text_content

    def test_metadata_precedes_body_text(self):
        metadata = {"Title": "First"}

        with patch(
            "markitdown.converters._pdf_converter.pdfplumber"
        ) as mock_pdfplumber, patch(
            "markitdown.converters._pdf_converter.pdfminer"
        ) as mock_pdfminer:
            mock_pdfplumber.open.side_effect = _mock_pdfplumber_open(metadata)
            mock_pdfminer.high_level.extract_text.return_value = "Body content."

            md = MarkItDown()
            result = md.convert_stream(
                io.BytesIO(b"fake pdf"),
                stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            )

        content = result.text_content
        meta_pos = content.find("## Document Properties")
        body_pos = content.find("Body content.")
        assert meta_pos < body_pos, "Metadata section should appear before body text"
