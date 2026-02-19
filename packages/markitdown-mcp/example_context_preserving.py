"""
Example demonstrating the context-preserving conversion feature.
This addresses GitHub issue #1353 by showing how to convert large documents
without consuming agent context window space.
"""

# Example of the problem (current behavior):
# When converting a large PDF with the original tool, all content is returned
# to the agent, consuming valuable context window space.

# BEFORE (problematic):
# result = convert_to_markdown("large_document.pdf")
# # Returns entire document content → consumes context window

# AFTER (solution):
# Use the new convert_and_save tool to save without returning content
# result = convert_and_save("large_document.pdf", "output.md", return_content=False)
# # Returns: {"success": true, "saved_to": "output.md", "size": 150000}
# # No content returned → preserves context window

async def example_context_preserving_conversion():
    """Example showing context-preserving conversion."""
    
    # Scenario: Convert a large PDF without consuming context
    large_pdf = "file:///path/to/large_document.pdf"
    
    # Convert and save without returning content (preserves context)
    result = await convert_and_save(
        uri=large_pdf,
        output_path="converted_document.md",
        return_content=False  # This is the key - don't return content
    )
    
    print(f"Conversion result: {result}")
    # Output: {
    #   "success": true,
    #   "saved_to": "/full/path/to/converted_document.md",
    #   "size": 150000,
    #   "title": "Document Title",
    #   "content": None  # No content returned - context preserved
    # }
    
    # Later, if you need to work with the content, you can read it selectively
    # or use the flexible tool with return_content=True for specific portions
    
    return result

async def example_flexible_conversion():
    """Example showing flexible conversion options."""
    
    # Scenario: Sometimes you want content, sometimes you don't
    document_uri = "file:///path/to/document.pdf"
    
    # Option 1: Just convert and return content (like original tool)
    result1 = await convert_to_markdown_with_options(
        uri=document_uri,
        return_content=True,
        save_to=None
    )
    
    # Option 2: Save and return content (for smaller documents)
    result2 = await convert_to_markdown_with_options(
        uri=document_uri,
        return_content=True,
        save_to="document.md"
    )
    
    # Option 3: Just save, don't return content (for large documents)
    result3 = await convert_to_markdown_with_options(
        uri=document_uri,
        return_content=False,
        save_to="large_document.md"
    )
    
    return result1, result2, result3

# Use cases for each tool:

# 1. convert_to_markdown(uri)
#    - Original behavior
#    - Use for small documents where you need the content
#    - Returns full content string

# 2. convert_and_save(uri, output_path, return_content=False)
#    - Best for large documents
#    - Saves file and returns metadata only
#    - Preserves agent context window

# 3. convert_to_markdown_with_options(uri, return_content=True, save_to=None)
#    - Maximum flexibility
#    - Can save, return content, or both
#    - Adapt to any use case
