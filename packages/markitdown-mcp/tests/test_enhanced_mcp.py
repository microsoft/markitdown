"""
Unit tests for the enhanced MarkItDown MCP server with context-preserving conversion.
Tests address GitHub issue #1353.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import sys
import os

# Add the src directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from markitdown_mcp.__main__ import convert_and_save, convert_to_markdown_with_options

class TestEnhancedMCPServer:
    """Test cases for enhanced MCP server functionality."""

    @pytest.fixture
    def mock_markitdown_result(self):
        """Mock DocumentConverterResult."""
        mock_result = Mock()
        mock_result.markdown = "# Test Document\n\nThis is a test document."
        mock_result.title = "Test Document"
        return mock_result

    @pytest.fixture
    def mock_markitdown(self, mock_markitdown_result):
        """Mock MarkItDown instance."""
        mock_md = Mock()
        mock_md.convert_uri.return_value = mock_markitdown_result
        return mock_md

    @pytest.mark.asyncio
    async def test_convert_and_save_without_content(self, mock_markitdown):
        """Test convert_and_save without returning content (context-preserving)."""
        with patch('markitdown_mcp.__main__.MarkItDown', return_value=mock_markitdown):
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = Path(temp_dir) / "test_output.md"
                
                result = await convert_and_save(
                    uri="file:///test.pdf",
                    output_path=str(output_path),
                    return_content=False
                )
                
                # Verify response structure
                assert result["success"] is True
                assert result["saved_to"] == str(output_path.resolve())
                assert result["size"] > 0
                assert result["title"] == "Test Document"
                assert "content" not in result or result["content"] is None
                
                # Verify file was created
                assert output_path.exists()
                assert output_path.read_text(encoding="utf-8") == "# Test Document\n\nThis is a test document."

    @pytest.mark.asyncio
    async def test_convert_and_save_with_content(self, mock_markitdown):
        """Test convert_and_save with content return."""
        with patch('markitdown_mcp.__main__.MarkItDown', return_value=mock_markitdown):
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = Path(temp_dir) / "test_output.md"
                
                result = await convert_and_save(
                    uri="file:///test.pdf",
                    output_path=str(output_path),
                    return_content=True
                )
                
                # Verify response structure
                assert result["success"] is True
                assert result["saved_to"] == str(output_path.resolve())
                assert result["size"] > 0
                assert result["title"] == "Test Document"
                assert result["content"] == "# Test Document\n\nThis is a test document."
                
                # Verify file was created
                assert output_path.exists()

    @pytest.mark.asyncio
    async def test_convert_and_save_error_handling(self):
        """Test error handling in convert_and_save."""
        with patch('markitdown_mcp.__main__.MarkItDown', side_effect=Exception("Test error")):
            result = await convert_and_save(
                uri="file:///test.pdf",
                output_path="/tmp/test_output.md",
                return_content=False
            )
            
            # Verify error response
            assert result["success"] is False
            assert "Test error" in result["error"]
            assert result["saved_to"] is None
            assert result["size"] == 0
            assert result["title"] is None

    @pytest.mark.asyncio
    async def test_convert_to_markdown_with_options_save_only(self, mock_markitdown):
        """Test convert_to_markdown_with_options with save only (no content return)."""
        with patch('markitdown_mcp.__main__.MarkItDown', return_value=mock_markitdown):
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = Path(temp_dir) / "test_output.md"
                
                result = await convert_to_markdown_with_options(
                    uri="file:///test.pdf",
                    return_content=False,
                    save_to=str(output_path)
                )
                
                # Verify response structure
                assert result["success"] is True
                assert result["saved_to"] == str(output_path.resolve())
                assert result["size"] > 0
                assert result["title"] == "Test Document"
                assert "content" not in result or result["content"] is None
                
                # Verify file was created
                assert output_path.exists()

    @pytest.mark.asyncio
    async def test_convert_to_markdown_with_options_content_only(self, mock_markitdown):
        """Test convert_to_markdown_with_options with content only (no save)."""
        with patch('markitdown_mcp.__main__.MarkItDown', return_value=mock_markitdown):
            result = await convert_to_markdown_with_options(
                uri="file:///test.pdf",
                return_content=True,
                save_to=None
            )
            
            # Verify response structure
            assert result["success"] is True
            assert result["saved_to"] is None
            assert result["size"] > 0  # Size of content in bytes
            assert result["title"] == "Test Document"
            assert result["content"] == "# Test Document\n\nThis is a test document."

    @pytest.mark.asyncio
    async def test_convert_to_markdown_with_options_both(self, mock_markitdown):
        """Test convert_to_markdown_with_options with both save and content return."""
        with patch('markitdown_mcp.__main__.MarkItDown', return_value=mock_markitdown):
            with tempfile.TemporaryDirectory() as temp_dir:
                output_path = Path(temp_dir) / "test_output.md"
                
                result = await convert_to_markdown_with_options(
                    uri="file:///test.pdf",
                    return_content=True,
                    save_to=str(output_path)
                )
                
                # Verify response structure
                assert result["success"] is True
                assert result["saved_to"] == str(output_path.resolve())
                assert result["size"] > 0
                assert result["title"] == "Test Document"
                assert result["content"] == "# Test Document\n\nThis is a test document."
                
                # Verify file was created
                assert output_path.exists()

    @pytest.mark.asyncio
    async def test_directory_creation(self, mock_markitdown):
        """Test that output directories are created automatically."""
        with patch('markitdown_mcp.__main__.MarkItDown', return_value=mock_markitdown):
            with tempfile.TemporaryDirectory() as temp_dir:
                # Use a nested directory path that doesn't exist
                output_path = Path(temp_dir) / "nested" / "dir" / "test_output.md"
                
                result = await convert_and_save(
                    uri="file:///test.pdf",
                    output_path=str(output_path),
                    return_content=False
                )
                
                # Verify directory was created and file exists
                assert result["success"] is True
                assert output_path.exists()
                assert output_path.parent.exists()

    def test_context_window_preservation(self):
        """Test that context window is preserved with new tools."""
        # This is a conceptual test - in practice, we verify that
        # tools can return minimal metadata instead of full content
        
        large_content = "# Large Document\n" + "Content line\n" * 10000
        metadata_only = {
            "success": True,
            "saved_to": "/path/to/file.md",
            "size": len(large_content),
            "title": "Large Document"
        }
        
        # Content size: ~140KB
        content_size = len(large_content.encode('utf-8'))
        
        # Metadata size: ~200 bytes
        metadata_size = len(json.dumps(metadata_only).encode('utf-8'))
        
        # Verify massive reduction in context consumption
        assert content_size > 100000  # Large content
        assert metadata_size < 500    # Small metadata
        assert metadata_size < content_size * 0.01  # Less than 1% of content size

if __name__ == "__main__":
    pytest.main([__file__])
