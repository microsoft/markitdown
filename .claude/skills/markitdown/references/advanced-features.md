# MarkItDown Advanced Features

Advanced functionality for custom converters, URI handling, and plugins.

## Conversion Methods

MarkItDown provides multiple conversion entry points.

### convert()

Universal method that auto-detects source type.

```python
from markitdown import MarkItDown

md = MarkItDown()

# File path
result = md.convert("document.pdf")

# URL
result = md.convert("https://example.com/page.html")

# HTTP Response object
import requests
response = requests.get("https://example.com/doc.pdf")
result = md.convert(response)
```

### convert_local()

For local file paths only.

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert_local("./documents/report.pdf")
print(result.text_content)
```

### convert_stream()

For binary file-like objects.

```python
from markitdown import MarkItDown
import io

md = MarkItDown()

# From bytes
with open("document.pdf", "rb") as f:
    content = f.read()

stream = io.BytesIO(content)
result = md.convert_stream(stream)

# From HTTP response
import requests
response = requests.get("https://example.com/doc.pdf")
stream = io.BytesIO(response.content)
result = md.convert_stream(stream)
```

> **Note:** `convert_stream()` requires binary streams only (v0.1.0+).
> Text streams (`io.StringIO`) are not supported.

### convert_url()

For HTTP/HTTPS URLs.

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert_url("https://example.com/document.pdf")
print(result.text_content)
```

### convert_uri()

For any URI scheme (http, https, file, data).

```python
from markitdown import MarkItDown

md = MarkItDown()

# HTTP URL
result = md.convert_uri("https://example.com/page.html")

# Local file URI
result = md.convert_uri("file:///path/to/document.pdf")

# Data URI
result = md.convert_uri("data:text/plain;base64,SGVsbG8gV29ybGQ=")
```

### convert_response()

For `requests.Response` objects.

```python
from markitdown import MarkItDown
import requests

md = MarkItDown()
response = requests.get("https://example.com/report.pdf")
result = md.convert_response(response)
print(result.text_content)
```

## Result Object

The `DocumentConverterResult` contains conversion output.

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")

# Main content
print(result.text_content)

# Alias for text_content
print(result.markdown)

# Document title (if available)
if result.title:
    print(f"Title: {result.title}")
```

## Custom Converters

Create custom converters for unsupported formats.

### Basic Custom Converter

```python
from markitdown import MarkItDown
from markitdown._base_converter import DocumentConverter
from markitdown._base_converter import DocumentConverterResult
from typing import BinaryIO

class MyFormatConverter(DocumentConverter):
    """Converter for .myformat files."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: "StreamInfo",
        **kwargs
    ) -> bool:
        """Check if this converter handles the file."""
        # Check by extension
        if stream_info.extension:
            return stream_info.extension.lower() == ".myformat"
        # Check by MIME type
        if stream_info.mime_type:
            return stream_info.mime_type == "application/x-myformat"
        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: "StreamInfo",
        **kwargs
    ) -> DocumentConverterResult:
        """Convert the file to markdown."""
        content = file_stream.read().decode("utf-8")

        # Process content...
        markdown = f"# My Format\n\n{content}"

        return DocumentConverterResult(
            title="My Document",
            text_content=markdown
        )

# Register the converter
md = MarkItDown()
md.register_converter(MyFormatConverter())

# Use it
result = md.convert("document.myformat")
```

### Converter Priority

Converters are matched in priority order (lower = higher priority).

```python
from markitdown import MarkItDown

md = MarkItDown()

# Register with high priority (runs first)
md.register_converter(MyConverter(), priority=10)

# Register with default priority
md.register_converter(AnotherConverter())  # Default priority

# Register with low priority (fallback)
md.register_converter(FallbackConverter(), priority=100)
```

## Plugin Development

Create distributable plugins for MarkItDown.

### Plugin Structure

```text
markitdown-my-plugin/
  src/
    markitdown_my_plugin/
      __init__.py
      __about__.py
      _plugin.py
  pyproject.toml
```

### Plugin Entry Point

```python
# _plugin.py
from markitdown import MarkItDown
from ._converter import MyConverter

def register_converters(markitdown: MarkItDown, **kwargs):
    """Called when MarkItDown is instantiated with plugins."""
    markitdown.register_converter(MyConverter())
```

### pyproject.toml

```toml
[project]
name = "markitdown-my-plugin"
version = "0.1.0"
dependencies = ["markitdown>=0.1.0"]

[project.entry-points."markitdown.plugin"]
my_plugin = "markitdown_my_plugin._plugin:register_converters"
```

### Using Plugins

```python
from markitdown import MarkItDown

# Enable all installed plugins
md = MarkItDown(enable_plugins=True)
result = md.convert("document.myformat")
```

```bash
# CLI: List installed plugins
markitdown --list-plugins

# CLI: Enable plugins
markitdown --use-plugins document.myformat
```

## Built-in Converters Reference

| Converter | Formats | Notes |
|-----------|---------|-------|
| `PdfConverter` | .pdf | Requires `[pdf]` extra |
| `DocxConverter` | .docx | Requires `[docx]` extra |
| `PptxConverter` | .pptx | Requires `[pptx]` extra |
| `XlsxConverter` | .xlsx | Requires `[xlsx]` extra |
| `XlsConverter` | .xls | Requires `[xls]` extra |
| `HtmlConverter` | .html, .htm | Built-in |
| `CsvConverter` | .csv | Built-in |
| `PlainTextConverter` | .txt, .md | Built-in |
| `ImageConverter` | .jpg, .png, .gif | EXIF + optional LLM |
| `AudioConverter` | .wav, .mp3 | Requires `[audio-transcription]` |
| `YouTubeConverter` | YouTube URLs | Requires `[youtube-transcription]` |
| `WikipediaConverter` | Wikipedia URLs | Built-in |
| `RssConverter` | RSS/Atom feeds | Built-in |
| `IpynbConverter` | .ipynb | Built-in |
| `EpubConverter` | .epub | Built-in |
| `ZipConverter` | .zip | Built-in |
| `OutlookMsgConverter` | .msg | Requires `[outlook]` extra |
| `DocumentIntelligenceConverter` | Various | Requires `[az-doc-intel]` |

## MCP Server

MarkItDown provides an MCP server for LLM integration.

### Installation

```bash
pip install markitdown-mcp
```

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "markitdown-mcp"
    }
  }
}
```

### MCP Tool

The MCP server exposes a single tool:

```python
convert_to_markdown(uri: str) -> str
```

Accepts `http:`, `https:`, `file:`, or `data:` URIs.
