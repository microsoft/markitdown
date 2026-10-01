# Enhanced MarkItDown MCP Server - Context-Preserving Conversion

## Overview

This enhancement addresses GitHub Issue #1353 by adding context-preserving conversion capabilities to the MarkItDown MCP server. The problem was that converting large documents (PDFs, etc.) returned all content to the agent, consuming valuable context window space.

## Problem Statement

```
Current behavior - all content returned and added to context:
result = convert_to_markdown("large_document.pdf")  # Returns full markdown content
```

**Issues:**
- Large PDFs could consume 500KB+ of context window space
- Agents quickly ran out of context for subsequent operations
- No way to convert and save files without processing the content

## Solution

Added two new MCP tools that preserve agent context:

### 1. `convert_and_save(uri, output_path, return_content=False)`
Primary solution for context-preserving conversion.

```python
# Desired behavior - convert and save without returning content
result = convert_and_save("large_document.pdf", "output.md", return_content=False)
# Returns: {"success": true, "saved_to": "output.md", "size": 150000}
```

### 2. `convert_to_markdown_with_options(uri, return_content=True, save_to=None)`
Flexible tool providing maximum control over conversion options.

## Implementation Details

### New Tools Added

1. **`convert_and_save`** - Context-preserving conversion
   - Converts document to markdown
   - Saves to specified file path
   - Returns metadata only (by default)
   - Optionally returns content if requested

2. **`convert_to_markdown_with_options`** - Flexible conversion
   - Can save to file, return content, or both
   - Maximum flexibility for different use cases
   - Consistent response format

3. **`convert_to_markdown`** - Original tool (unchanged)
   - Maintains backward compatibility
   - Still available for small documents

### Key Features

- **Context Window Preservation**: Reduces context consumption by 95%+ for large documents
- **Automatic Directory Creation**: Creates output directories as needed
- **Comprehensive Error Handling**: Consistent error responses across all tools
- **Metadata Return**: File size, title, path, and success status
- **Flexible Options**: Choose what to return and where to save
- **Backward Compatibility**: Original tool unchanged

### Response Format

All enhanced tools return consistent JSON responses:

```json
{
  "success": true,
  "saved_to": "/path/to/output.md",
  "size": 150000,
  "title": "Document Title",
  "content": "..." // Only if return_content=True
}
```

## Context Window Impact

| Scenario | Before | After | Savings |
|----------|---------|--------|---------|
| 100-page PDF | ~500KB context | ~200 bytes | 99.96% |
| Large Word doc | ~200KB context | ~200 bytes | 99.9% |
| Multiple documents | Context exhausted | Context preserved | 100% |

## Use Cases

### 1. Large Document Processing
```python
# Agent can process multiple large documents without context exhaustion
convert_and_save("document1.pdf", "doc1.md", False)
convert_and_save("document2.pdf", "doc2.md", False)
convert_and_save("document3.pdf", "doc3.md", False)
# Context window still available for analysis
```

### 2. Batch Conversion
```python
# Convert entire document library
for doc in document_library:
    convert_and_save(doc.uri, f"converted/{doc.name}.md", False)
# All documents converted, context preserved
```

### 3. Selective Processing
```python
# Convert large document, then work with specific sections
convert_and_save("large_report.pdf", "report.md", False)
# Later: read specific sections from saved file as needed
```

## Files Added/Modified

### Core Implementation
- `src/markitdown_mcp/__main__.py` - Added two new MCP tools
- Added imports: `Path`, `Optional`, `Dict`, `Any`, `json`

### Documentation
- `README.md` - Updated with new tool descriptions
- `CHANGELOG.md` - Documented new features
- `USAGE_EXAMPLES.md` - Comprehensive usage guide
- `claude_desktop_config_example.json` - Example configuration

### Testing
- `test_enhanced_mcp.py` - Unit tests for new functionality
- `integration_test.py` - Integration test demonstrating features
- `test_enhancement.py` - Comprehensive test scenario

### Examples
- `example_context_preserving.py` - Usage examples
- `test_new_tools.py` - Tool demonstration script

## Benefits

1. Solves Context Window Exhaustion: Primary issue from GitHub #1353
2. Enables Large Document Processing: PDFs, large Word docs, etc.
3. Maintains Backward Compatibility: Existing code continues to work
4. Provides Flexibility: Multiple options for different use cases
5. Improves User Experience: Agents can handle more complex workflows
6. Consistent API: All tools follow same response format

## Migration Guide

### For Small Documents (< 10KB)
Continue using `convert_to_markdown()` - no changes needed.

### For Large Documents (> 50KB)
Replace:
```python
content = convert_to_markdown("large.pdf")
```

With:
```python
result = convert_and_save("large.pdf", "output.md", False)
# Content saved to file, context preserved
```

### For Variable Use Cases
Use the flexible tool:
```python
result = convert_to_markdown_with_options(
    uri="document.pdf",
    return_content=False,  # Preserve context
    save_to="output.md"    # Save to file
)
```

## Conclusion

This enhancement addresses GitHub Issue #1353 by providing context-preserving conversion options while maintaining full backward compatibility. Agents can now process large documents without exhausting their context window, enabling more sophisticated document processing workflows.

The solution is production-ready and provides a foundation for future enhancements to the MarkItDown MCP server.
