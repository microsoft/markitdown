#!/usr/bin/env python3 -m pytest
"""
Unit tests for PPTX slide extraction functionality.
"""

import os
import tempfile
import pytest
from typing import Optional

from markitdown import MarkItDown, PageInfo, DocumentConverterResult


class TestPptxPageExtraction:
    """Test cases for PPTX slide extraction functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        self.markitdown = MarkItDown()
        self.test_pptx_path = os.path.join(
            os.path.dirname(__file__), 
            'test_files', 
            'test.pptx'
        )
    
    def test_traditional_pptx_conversion(self):
        """Test that traditional PPTX conversion works unchanged."""
        if not os.path.exists(self.test_pptx_path):
            pytest.skip("Test PPTX file not found")
        
        result = self.markitdown.convert(self.test_pptx_path)
        
        # Verify result structure
        assert isinstance(result, DocumentConverterResult)
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0
        assert result.pages is None  # Should be None by default
        
        # Verify backward compatibility
        assert hasattr(result, 'text_content')
        assert result.text_content == result.markdown
        assert str(result) == result.markdown
    
    def test_pptx_page_extraction_enabled(self):
        """Test PPTX conversion with slide extraction enabled."""
        if not os.path.exists(self.test_pptx_path):
            pytest.skip("Test PPTX file not found")
        
        result = self.markitdown.convert(self.test_pptx_path, extract_pages=True)
        
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
            # Slides can be empty, so we don't check content length
        
        # Verify page numbers are sequential
        page_numbers = [page.page_number for page in result.pages]
        assert page_numbers == list(range(1, len(result.pages) + 1))
        
        # Verify each slide has slide number comment
        for page in result.pages:
            assert f"<!-- Slide number: {page.page_number} -->" in page.content
    
    def test_pptx_page_extraction_disabled(self):
        """Test PPTX conversion with slide extraction explicitly disabled."""
        if not os.path.exists(self.test_pptx_path):
            pytest.skip("Test PPTX file not found")
        
        result = self.markitdown.convert(self.test_pptx_path, extract_pages=False)
        
        # Should behave the same as default
        assert isinstance(result, DocumentConverterResult)
        assert isinstance(result.markdown, str)
        assert len(result.markdown) > 0
        assert result.pages is None
    
    def test_backward_compatibility(self):
        """Test that all existing functionality remains intact."""
        if not os.path.exists(self.test_pptx_path):
            pytest.skip("Test PPTX file not found")
        
        # Test different ways of calling convert
        result1 = self.markitdown.convert(self.test_pptx_path)
        result2 = self.markitdown.convert(self.test_pptx_path, extract_pages=False)
        
        # Results should be equivalent
        assert result1.markdown == result2.markdown
        assert result1.title == result2.title
        assert result1.pages == result2.pages
        
        # Both should work with string conversion
        assert str(result1) == str(result2)
        
        # Both should work with text_content property
        assert result1.text_content == result2.text_content
    
    def test_extract_pages_parameter_types(self):
        """Test different types for extract_pages parameter."""
        if not os.path.exists(self.test_pptx_path):
            pytest.skip("Test PPTX file not found")
        
        # Test with different truthy/falsy values
        result_false = self.markitdown.convert(self.test_pptx_path, extract_pages=False)
        result_true = self.markitdown.convert(self.test_pptx_path, extract_pages=True)
        result_none = self.markitdown.convert(self.test_pptx_path, extract_pages=None)
        result_zero = self.markitdown.convert(self.test_pptx_path, extract_pages=0)
        result_one = self.markitdown.convert(self.test_pptx_path, extract_pages=1)
        
        # False, None, 0 should not extract pages
        assert result_false.pages is None
        assert result_none.pages is None
        assert result_zero.pages is None
        
        # True, 1 should extract pages
        assert result_true.pages is not None
        assert result_one.pages is not None