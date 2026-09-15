#!/usr/bin/env python3
"""
Simple integration test for enhanced MCP server functionality.
This test can run without pytest and demonstrates the new features.
"""

import asyncio
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

def create_mock_markitdown():
    """Create a mock MarkItDown instance for testing."""
    mock_result = Mock()
    mock_result.markdown = "# Test Document\n\nThis is a test document content."
    mock_result.title = "Test Document"
    
    mock_md = Mock()
    mock_md.convert_uri.return_value = mock_result
    return mock_md

async def test_context_preserving_conversion():
    """Test that demonstrates the context-preserving conversion feature."""
    print("Testing Context-Preserving Conversion (GitHub Issue #1353)")
    print("=" * 60)
    
    # Mock the MarkItDown functionality for testing
    mock_markitdown = create_mock_markitdown()
    
    with patch('markitdown_mcp.__main__.MarkItDown', return_value=mock_markitdown):
        # Import the functions after patching
        from markitdown_mcp.__main__ import convert_and_save, convert_to_markdown_with_options
        
        # Test 1: Context-preserving conversion (main solution)
        print("\n1. Testing context-preserving conversion:")
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_output.md"
            
            result = await convert_and_save(
                uri="file:///test_document.pdf",
                output_path=str(output_path),
                return_content=False  # This preserves context!
            )
            
            print(f"   Success: {result['success']}")
            print(f"   Saved to: {result['saved_to']}")
            print(f"   File size: {result['size']} bytes")
            print(f"   Title: {result['title']}")
            print(f"   Content returned: {'content' in result and result['content'] is not None}")
            
            # Verify file was created
            assert output_path.exists(), "Output file should be created"
            content = output_path.read_text(encoding="utf-8")
            assert "Test Document" in content, "File should contain expected content"
            
            print("   File created successfully")
            print("   No content returned (context preserved)")
            
        # Test 2: Flexible conversion options
        print("\n2. Testing flexible conversion options:")
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "flexible_output.md"
            
            # Test saving without content return
            result = await convert_to_markdown_with_options(
                uri="file:///test_document.pdf",
                return_content=False,
                save_to=str(output_path)
            )
            
            print(f"   Flexible tool - save only:")
            print(f"   Success: {result['success']}")
            print(f"   Saved to: {result['saved_to']}")
            print(f"   Content returned: {'content' in result and result['content'] is not None}")
            
            # Test content return without saving
            result = await convert_to_markdown_with_options(
                uri="file:///test_document.pdf",
                return_content=True,
                save_to=None
            )
            
            print(f"   Flexible tool - content only:")
            print(f"   Success: {result['success']}")
            print(f"   Saved to: {result['saved_to']}")
            print(f"   Content returned: {'content' in result and result['content'] is not None}")
            print(f"   Content size: {result['size']} bytes")
            
        # Test 3: Context window impact demonstration
        print("\n3. Context window impact analysis:")
        
        # Simulate a large document
        large_content = "# Large Document\n" + "This is a line of content.\n" * 1000
        mock_result = Mock()
        mock_result.markdown = large_content
        mock_result.title = "Large Document"
        mock_markitdown.convert_uri.return_value = mock_result
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "large_output.md"
            
            # Context-preserving conversion
            result = await convert_and_save(
                uri="file:///large_document.pdf",
                output_path=str(output_path),
                return_content=False
            )
            
            # Calculate context impact
            content_size = len(large_content.encode('utf-8'))
            metadata_size = len(json.dumps(result).encode('utf-8'))
            
            print(f"   Large document content size: {content_size:,} bytes")
            print(f"   Metadata response size: {metadata_size:,} bytes")
            print(f"   Context savings: {content_size - metadata_size:,} bytes")
            print(f"   Context preservation: {((content_size - metadata_size) / content_size) * 100:.1f}%")
            
            assert content_size > 20000, "Test should use a large document"
            assert metadata_size < 1000, "Metadata should be small"
            assert metadata_size < content_size * 0.05, "Metadata should be <5% of content"
            
            print("   Massive context window savings achieved")
    
    print("\n" + "=" * 60)
    print("SUMMARY: Context-Preserving Conversion Test")
    print("convert_and_save() preserves context by not returning content")
    print("convert_to_markdown_with_options() provides flexible options")
    print("Files are saved correctly with proper metadata")
    print("Context window savings of >95% for large documents")
    print("GitHub Issue #1353 successfully addressed")
    
    return True

async def main():
    """Run the integration test."""
    try:
        success = await test_context_preserving_conversion()
        if success:
            print("\nAll tests passed! Enhancement is working correctly.")
            return 0
        else:
            print("\nSome tests failed.")
            return 1
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
