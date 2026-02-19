# Usage Examples for Enhanced MarkItDown MCP Server

This document provides examples of how to use the enhanced MCP server tools to address the context window preservation issue (GitHub issue #1353).

## Problem Statement

When converting large PDFs or documents with the original `convert_to_markdown()` tool, the entire converted markdown content is returned to the agent/LLM, consuming valuable context window space. This can quickly exhaust the available context for large documents.

## Solution: New Context-Preserving Tools

### 1. `convert_and_save()` - Primary Solution

**Purpose**: Convert documents and save to file without returning content to preserve context.

**Usage**:
```json
{
  "tool": "convert_and_save",
  "parameters": {
    "uri": "file:///workdir/large_document.pdf",
    "output_path": "/workdir/converted_document.md",
    "return_content": false
  }
}
```

**Response**:
```json
{
  "success": true,
  "saved_to": "/workdir/converted_document.md",
  "size": 156789,
  "title": "Large Document Title",
  "content": null
}
```

**Benefits**:
- Preserves agent context window (only around 200 bytes vs potentially 500KB+)
- Saves converted content to disk for later use
- Returns useful metadata about the conversion

### 2. `convert_to_markdown_with_options()` - Flexible Solution

**Purpose**: Maximum flexibility - can convert, save, return content, or any combination.

**Usage Examples**:

**A. Convert and save without returning content (like convert_and_save)**:
```json
{
  "tool": "convert_to_markdown_with_options",
  "parameters": {
    "uri": "file:///workdir/large_document.pdf",
    "return_content": false,
    "save_to": "/workdir/converted_document.md"
  }
}
```

**B. Convert and return content without saving (like original tool)**:
```json
{
  "tool": "convert_to_markdown_with_options",
  "parameters": {
    "uri": "file:///workdir/small_document.pdf",
    "return_content": true,
    "save_to": null
  }
}
```

**C. Convert, save, and return content (both)**:
```json
{
  "tool": "convert_to_markdown_with_options",
  "parameters": {
    "uri": "file:///workdir/document.pdf",
    "return_content": true,
    "save_to": "/workdir/backup.md"
  }
}
```

### 3. `convert_to_markdown()` - Original Tool

**Purpose**: Original behavior for backward compatibility.

**Usage**:
```json
{
  "tool": "convert_to_markdown",
  "parameters": {
    "uri": "file:///workdir/small_document.pdf"
  }
}
```

**Response**: Returns markdown content as string.

## Use Case Scenarios

### Scenario 1: Processing Large PDF Reports
```
Agent: "I need to convert this 100-page PDF report for analysis"
Solution: Use convert_and_save() to avoid context exhaustion
Result: PDF converted and saved, context window preserved for analysis
```

### Scenario 2: Batch Document Processing
```
Agent: "Convert multiple large documents for a research project"
Solution: Use convert_and_save() for each document
Result: All documents converted and saved, context available for research
```

### Scenario 3: Small Document Quick Processing
```
Agent: "Convert this 2-page document and analyze it immediately"
Solution: Use convert_to_markdown() for immediate content return
Result: Quick conversion with content ready for immediate analysis
```

## Migration Guide

### From Original Tool
**Before** (problematic for large documents):
```json
{
  "tool": "convert_to_markdown",
  "parameters": {
    "uri": "file:///workdir/large_document.pdf"
  }
}
```

**After** (context-preserving):
```json
{
  "tool": "convert_and_save",
  "parameters": {
    "uri": "file:///workdir/large_document.pdf",
    "output_path": "/workdir/converted_document.md",
    "return_content": false
  }
}
```

## Best Practices

1. **For Large Documents (>50KB)**: Use `convert_and_save()` with `return_content=false`
2. **For Small Documents (<10KB)**: Use `convert_to_markdown()` for immediate access
3. **For Variable Use Cases**: Use `convert_to_markdown_with_options()` for maximum flexibility
4. **File Organization**: Use descriptive output paths and organize by project/date
5. **Error Handling**: Always check the `success` field in responses

## Context Window Impact

| Tool | Document Size | Context Consumed | Best For |
|------|---------------|------------------|----------|
| convert_to_markdown | 500KB PDF | ~500KB | Small docs |
| convert_and_save | 500KB PDF | ~200 bytes | Large docs |
| convert_to_markdown_with_options | 500KB PDF | ~200 bytes or ~500KB | Flexible |

## Error Handling

All tools return consistent error responses:
```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "saved_to": null,
  "size": 0,
  "title": null,
  "content": null
}
```

This enhancement addresses GitHub issue #1353 by providing context-preserving conversion options while maintaining backward compatibility.
