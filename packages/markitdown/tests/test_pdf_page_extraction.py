#!/usr/bin/env python3 -m pytest
"""
Unit tests for PDF page extraction functionality.
"""

import os
import tempfile
import pytest
from typing import Optional

from markitdown import MarkItDown, PageInfo, DocumentConverterResult


class TestPdfPageExtraction:
    """Test cases for PDF page extraction functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        self.markitdown = MarkItDown()
        self.test_pdf_path = os.path.join(
            os.path.dirname(__file__), "test_files", "test.pdf"
        )

    def test_traditional_pdf_conversion(self):
        """Test that traditional PDF conversion works unchanged."""
        if not os.path.exists(self.test_pdf_path):
            pytest.skip("Test PDF file not found")

        result = self.markitdown.convert(self.test_pdf_path)

        # Verify result structure
        assert isinstance(result, DocumentConverterResult)
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0
        assert result.pages is None  # Should be None by default

        # Verify backward compatibility
        assert hasattr(result, "text_content")
        assert result.text_content == result.markdown
        assert str(result) == result.markdown

    def test_pdf_page_extraction_enabled(self):
        """Test PDF conversion with page extraction enabled."""
        if not os.path.exists(self.test_pdf_path):
            pytest.skip("Test PDF file not found")

        result = self.markitdown.convert(self.test_pdf_path, extract_pages=True)

        # Verify result structure
        assert isinstance(result, DocumentConverterResult)
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0
        assert result.pages is not None
        assert isinstance(result.pages, list)
        assert len(result.pages) > 0

        # Verify page structure
        for page in result.pages:
            assert isinstance(page, PageInfo)
            assert isinstance(page.page_number, int)
            assert page.page_number > 0
            assert isinstance(page.content, str)
            assert len(page.content) > 0

        # Verify page numbers are sequential
        page_numbers = [page.page_number for page in result.pages]
        assert page_numbers == list(range(1, len(result.pages) + 1))

    def test_pdf_page_extraction_disabled(self):
        """Test PDF conversion with page extraction explicitly disabled."""
        if not os.path.exists(self.test_pdf_path):
            pytest.skip("Test PDF file not found")

        result = self.markitdown.convert(self.test_pdf_path, extract_pages=False)

        # Should behave the same as default
        assert isinstance(result, DocumentConverterResult)
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0
        assert result.pages is None

    def test_page_info_class(self):
        """Test PageInfo class functionality."""
        page = PageInfo(page_number=1, content="Test content")

        assert page.page_number == 1
        assert page.content == "Test content"
        assert isinstance(page.page_number, int)
        assert isinstance(page.content, str)

    def test_document_converter_result_with_pages(self):
        """Test DocumentConverterResult with pages parameter."""
        pages = [
            PageInfo(page_number=1, content="Page 1 content"),
            PageInfo(page_number=2, content="Page 2 content"),
        ]

        result = DocumentConverterResult(
            markdown="Combined content", title="Test Document", pages=pages
        )

        assert result.markdown == "Combined content"
        assert result.title == "Test Document"
        assert len(result.pages) == 2
        assert result.pages[0].page_number == 1
        assert result.pages[1].page_number == 2

    def test_backward_compatibility(self):
        """Test that all existing functionality remains intact."""
        if not os.path.exists(self.test_pdf_path):
            pytest.skip("Test PDF file not found")

        # Test different ways of calling convert
        result1 = self.markitdown.convert(self.test_pdf_path)
        result2 = self.markitdown.convert(self.test_pdf_path, extract_pages=False)

        # Results should be equivalent
        assert result1.markdown == result2.markdown
        assert result1.title == result2.title
        assert result1.pages == result2.pages

        # Both should work with string conversion
        assert str(result1) == str(result2)

        # Both should work with text_content property
        assert result1.text_content == result2.text_content

    def test_non_pdf_file_with_extract_pages(self):
        """Test that extract_pages parameter doesn't affect non-PDF files."""
        # Create a temporary markdown file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\nThis is a test.")
            temp_path = f.name

        try:
            result1 = self.markitdown.convert(temp_path)
            result2 = self.markitdown.convert(temp_path, extract_pages=True)

            # Both should behave the same for non-PDF files
            assert result1.markdown == result2.markdown
            assert result1.pages is None
            assert result2.pages is None

        finally:
            os.unlink(temp_path)

    def test_extract_pages_parameter_types(self):
        """Test different types for extract_pages parameter."""
        if not os.path.exists(self.test_pdf_path):
            pytest.skip("Test PDF file not found")

        # Test with different truthy/falsy values
        result_false = self.markitdown.convert(self.test_pdf_path, extract_pages=False)
        result_true = self.markitdown.convert(self.test_pdf_path, extract_pages=True)
        result_none = self.markitdown.convert(self.test_pdf_path, extract_pages=None)
        result_zero = self.markitdown.convert(self.test_pdf_path, extract_pages=0)
        result_one = self.markitdown.convert(self.test_pdf_path, extract_pages=1)

        # False, None, 0 should not extract pages
        assert result_false.pages is None
        assert result_none.pages is None
        assert result_zero.pages is None

        # True, 1 should extract pages
        assert result_true.pages is not None
        assert result_one.pages is not None
