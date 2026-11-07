#!/usr/bin/env python3
"""
Test script to demonstrate the new MCP tools for context-preserving conversion.
This script shows how the new tools can be used to convert large documents
without consuming agent context.
"""

import asyncio
import json
from pathlib import Path
from markitdown_mcp.__main__ import convert_to_markdown, convert_and_save, convert_to_markdown_with_options

async def test_tools():
    """Test the new MCP tools with a sample document."""
    
    # Use a test file from the markitdown package
    test_file = Path(__file__).parent.parent / "markitdown" / "tests" / "test_files" / "test.pdf"
    if not test_file.exists():
        print(f"Test file not found: {test_file}")
        return
    
    file_uri = f"file://{test_file.resolve()}"
    
    print("Testing MCP tools for context-preserving conversion...")
    print(f"Test file: {file_uri}")
    print("=" * 60)
    
    # Test 1: Original tool (returns full content)
    print("\n1. Testing convert_to_markdown (original tool):")
    try:
        content = await convert_to_markdown(file_uri)
        print(f"   Content length: {len(content)} characters")
        print(f"   First 100 chars: {content[:100]}...")
        print("   Returns full content (consumes agent context)")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Convert and save without returning content
    print("\n2. Testing convert_and_save (context-preserving):")
    try:
        output_path = Path("test_output.md")
        result = await convert_and_save(file_uri, str(output_path), return_content=False)
        print(f"   Result: {json.dumps(result, indent=2)}")
        print("   Converted and saved without returning content")
        print("   Preserves agent context window")
        
        # Clean up
        if output_path.exists():
            output_path.unlink()
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Convert and save WITH content return
    print("\n3. Testing convert_and_save with return_content=True:")
    try:
        output_path = Path("test_output_with_content.md")
        result = await convert_and_save(file_uri, str(output_path), return_content=True)
        print(f"   Success: {result['success']}")
        print(f"   Saved to: {result['saved_to']}")
        print(f"   Size: {result['size']} bytes")
        print(f"   Content length: {len(result.get('content', ''))} characters")
        print("   Converted, saved, and returned content")
        
        # Clean up
        if output_path.exists():
            output_path.unlink()
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Flexible tool - save only (no content return)
    print("\n4. Testing convert_to_markdown_with_options (save only):")
    try:
        output_path = Path("test_output_flexible.md")
        result = await convert_to_markdown_with_options(
            file_uri, 
            return_content=False, 
            save_to=str(output_path)
        )
        print(f"   Result: {json.dumps(result, indent=2)}")
        print("   Flexible tool - saved without returning content")
        
        # Clean up
        if output_path.exists():
            output_path.unlink()
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Flexible tool - return content only (no save)
    print("\n5. Testing convert_to_markdown_with_options (return content only):")
    try:
        result = await convert_to_markdown_with_options(
            file_uri, 
            return_content=True, 
            save_to=None
        )
        print(f"   Success: {result['success']}")
        print(f"   Content length: {len(result.get('content', ''))} characters")
        print(f"   Size: {result['size']} bytes")
        print("   Flexible tool - returned content without saving")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("convert_to_markdown: Returns full content (original behavior)")
    print("convert_and_save: Saves file with optional content return")
    print("convert_to_markdown_with_options: Maximum flexibility")
    print("\nThese new tools solve the context window problem by allowing")
    print("agents to convert large documents without consuming context space.")

if __name__ == "__main__":
    asyncio.run(test_tools())
