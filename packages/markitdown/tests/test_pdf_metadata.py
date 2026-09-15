#!/usr/bin/env python3 -m pytest
"""Tests for PDF metadata extraction in PdfConverter."""

import os
import pytest

from markitdown import MarkItDown

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


@pytest.fixture
def markitdown():
    return MarkItDown()


class TestPdfMetadataExtraction:
    """Test that PDF metadata is correctly extracted and prepended."""

    def test_metadata_with_all_fields(self, markitdown):
        """Test PDF with complete metadata (title, author, subject, etc.)."""
        pdf_path = os.path.join(TEST_FILES_DIR, "test_pdf_metadata.pdf")
        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)

        # Verify title is set on the result object
        assert result.title == "Annual Report 2025"

        # Verify metadata fields appear in the output
        assert "**Title:** Annual Report 2025" in result.markdown
        assert "**Author:** Jane Smith" in result.markdown
        assert "**Subject:** Financial Results" in result.markdown
        assert "**Keywords:** annual report, financials, 2025" in result.markdown
        assert "**Creator:** Test Suite" in result.markdown
        assert "**Producer:** MarkItDown Test" in result.markdown
        assert "**Created:** 2025-03-15" in result.markdown

        # Verify separator exists between metadata and body
        assert "---" in result.markdown

        # Verify body content is still present
        assert "This is a test document with PDF metadata." in result.markdown

    def test_metadata_appears_before_body(self, markitdown):
        """Test that metadata block is prepended before the body text."""
        pdf_path = os.path.join(TEST_FILES_DIR, "test_pdf_metadata.pdf")
        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)

        # Metadata should appear before the body content
        metadata_pos = result.markdown.index("**Title:**")
        body_pos = result.markdown.index("This is a test document")
        assert metadata_pos < body_pos

    def test_existing_pdf_metadata(self, markitdown):
        """Test that existing test.pdf still works with metadata extraction."""
        pdf_path = os.path.join(TEST_FILES_DIR, "test.pdf")
        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)

        # The existing test.pdf has Creator and Producer metadata
        assert "**Creator:** LaTeX with hyperref" in result.markdown
        assert "**Producer:** pdfTeX" in result.markdown

        # The original content should still be present
        assert (
            "Large language models (LLMs) are becoming a crucial building block"
            in result.markdown
        )

    def test_empty_pdf_no_metadata_block(self, markitdown):
        """Test that scanned PDFs (no text) don't get a metadata-only output."""
        pdf_path = os.path.join(
            TEST_FILES_DIR, "MEDRPT-2024-PAT-3847_medical_report_scan.pdf"
        )
        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)

        # Scanned PDF with no text layer should produce empty output
        assert result.text_content.strip() == ""

    def test_title_on_result_object(self, markitdown):
        """Test that the title field is set on DocumentConverterResult."""
        pdf_path = os.path.join(TEST_FILES_DIR, "test_pdf_metadata.pdf")
        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        assert result.title == "Annual Report 2025"

    def test_no_title_returns_none(self, markitdown):
        """Test that PDFs without a title return None for the title field."""
        pdf_path = os.path.join(TEST_FILES_DIR, "test.pdf")
        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)
        # test.pdf has empty Title field
        assert result.title is None

    def test_date_formatting(self, markitdown):
        """Test that PDF dates are formatted in human-readable form."""
        pdf_path = os.path.join(TEST_FILES_DIR, "test_pdf_metadata.pdf")
        if not os.path.exists(pdf_path):
            pytest.skip(f"Test file not found: {pdf_path}")

        result = markitdown.convert(pdf_path)

        # Dates should be in YYYY-MM-DD HH:MM:SS format, not D:YYYYMMDDHHmmSS
        assert "D:" not in result.markdown.split("---")[0]
        assert "2025-03-15" in result.markdown
