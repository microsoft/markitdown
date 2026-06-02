#!/usr/bin/env python3 -m pytest
"""
Unit tests for DOCX page extraction functionality.
"""

import os
import tempfile
import pytest
from typing import Optional

from markitdown import MarkItDown, PageInfo, DocumentConverterResult


class TestDocxPageExtraction:
    """Test cases for DOCX page extraction functionality."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        self.markitdown = MarkItDown()
        self.test_docx_path = os.path.join(
            os.path.dirname(__file__), "test_files", "test.docx"
        )

    def test_traditional_docx_conversion(self):
        """Test that traditional DOCX conversion works unchanged."""
        if not os.path.exists(self.test_docx_path):
            pytest.skip("Test DOCX file not found")

        result = self.markitdown.convert(self.test_docx_path)

        # Verify result structure
        assert isinstance(result, DocumentConverterResult)
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0
        assert result.pages is None  # Should be None by default

        # Verify backward compatibility
        assert hasattr(result, "text_content")
        assert result.text_content == result.markdown
        assert str(result) == result.markdown

    def test_docx_page_extraction_enabled(self):
        """Test DOCX conversion with page extraction enabled.

        Note: DOCX files don't have fixed pages like PDFs.
        Page breaks depend on rendering settings. Currently,
        this returns None for pages even with extract_pages=True.
        """
        if not os.path.exists(self.test_docx_path):
            pytest.skip("Test DOCX file not found")

        result = self.markitdown.convert(self.test_docx_path, extract_pages=True)

        # Verify result structure
        assert isinstance(result, DocumentConverterResult)
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0

        # Currently, DOCX doesn't support page extraction due to dynamic pagination
        assert result.pages is None

    def test_docx_page_extraction_disabled(self):
        """Test DOCX conversion with page extraction explicitly disabled."""
        if not os.path.exists(self.test_docx_path):
            pytest.skip("Test DOCX file not found")

        result = self.markitdown.convert(self.test_docx_path, extract_pages=False)

        # Should behave the same as default
        assert isinstance(result, DocumentConverterResult)
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0
        assert result.pages is None

    def test_backward_compatibility(self):
        """Test that all existing functionality remains intact."""
        if not os.path.exists(self.test_docx_path):
            pytest.skip("Test DOCX file not found")

        # Test different ways of calling convert
        result1 = self.markitdown.convert(self.test_docx_path)
        result2 = self.markitdown.convert(self.test_docx_path, extract_pages=False)
        result3 = self.markitdown.convert(self.test_docx_path, extract_pages=True)

        # Results should be equivalent for markdown content
        assert result1.markdown == result2.markdown
        assert result1.markdown == result3.markdown
        assert result1.title == result2.title
        assert result1.title == result3.title

        # All should have None for pages (DOCX limitation)
        assert result1.pages is None
        assert result2.pages is None
        assert result3.pages is None

        # All should work with string conversion
        assert str(result1) == str(result2)
        assert str(result1) == str(result3)

        # All should work with text_content property
        assert result1.text_content == result2.text_content
        assert result1.text_content == result3.text_content

    def test_extract_pages_parameter_types(self):
        """Test different types for extract_pages parameter."""
        if not os.path.exists(self.test_docx_path):
            pytest.skip("Test DOCX file not found")

        # Test with different truthy/falsy values
        result_false = self.markitdown.convert(self.test_docx_path, extract_pages=False)
        result_true = self.markitdown.convert(self.test_docx_path, extract_pages=True)
        result_none = self.markitdown.convert(self.test_docx_path, extract_pages=None)
        result_zero = self.markitdown.convert(self.test_docx_path, extract_pages=0)
        result_one = self.markitdown.convert(self.test_docx_path, extract_pages=1)

        # All should return None for pages (DOCX limitation)
        assert result_false.pages is None
        assert result_true.pages is None
        assert result_none.pages is None
        assert result_zero.pages is None
        assert result_one.pages is None
