# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MarkItDown is a Python-based monorepo containing utilities for converting various file formats to Markdown for use with LLMs. The repository contains three packages:
- `packages/markitdown` - Core library for file-to-markdown conversion
- `packages/markitdown-mcp` - MCP (Model Context Protocol) server exposing MarkItDown functionality
- `packages/markitdown-sample-plugin` - Example plugin demonstrating the plugin system

## Architecture

### Core Library (`packages/markitdown`)

**Main Entry Point**: `src/markitdown/_markitdown.py:MarkItDown` - Primary class orchestrating file conversion

**Converter System**: The architecture uses a priority-based converter registration system:
- `DocumentConverter` base class at `_base_converter.py` - All converters inherit from this and implement `accepts()` and `convert()` methods
- Built-in converters in `src/markitdown/converters/` - Each handles specific file types (PDF, DOCX, PPTX, XLSX, images, audio, HTML, etc.)
- Converters are tried in priority order (lower priority values = higher precedence)
- Two priority constants: `PRIORITY_SPECIFIC_FILE_FORMAT` (0.0) for specific formats, `PRIORITY_GENERIC_FILE_FORMAT` (10.0) for catch-all converters

**Stream-Based Processing**: As of v0.1.0, all converters read from file-like binary streams (BinaryIO), not file paths - no temporary files are created. Each converter receives:
- `file_stream`: Binary file-like object with seek(), tell(), and read() support
- `stream_info`: Metadata (mimetype, extension, charset, URL, filename)
- `kwargs`: Additional converter-specific options

**Plugin System**: Third-party plugins can register custom converters via entry points (`markitdown.plugin`). Plugins are disabled by default and must implement `register_converters(markitdown, **kwargs)` function.

**Optional Dependencies**: Dependencies organized into feature groups (pdf, docx, pptx, xlsx, audio-transcription, youtube-transcription, az-doc-intel, etc.). Use `pip install 'markitdown[all]'` for all features.

**Key Classes**:
- `MarkItDown` at `_markitdown.py` - Main API for conversions
- `DocumentConverterResult` at `_base_converter.py` - Return value containing markdown text and optional metadata (title)
- `StreamInfo` at `_stream_info.py` - Encapsulates file metadata

## Development Commands

### Working with Core Library

Navigate to the package directory first:
```bash
cd packages/markitdown
```

**Install in editable mode with all dependencies**:
```bash
pip install -e '.[all]'
```

**Run tests** (requires hatch):
```bash
hatch test
```

**Type checking**:
```bash
hatch run types:check
```

**Run pre-commit hooks** (run from repository root):
```bash
pre-commit run --all-files
```

**Run CLI**:
```bash
markitdown path-to-file.pdf > output.md
markitdown path-to-file.pdf -o output.md
```

### Working with MCP Server

**Build Docker image** (from repository root):
```bash
docker build -f packages/markitdown-mcp/Dockerfile -t markitdown-mcp:latest .
```

**Note:** The Dockerfile must be built from the repository root to ensure both `markitdown` and `markitdown-mcp` are installed from the latest local source code, not from PyPI.

See `packages/markitdown-mcp/CLAUDE.md` for detailed MCP server commands.

### Working with Plugins

**List installed plugins**:
```bash
markitdown --list-plugins
```

**Use plugins during conversion**:
```bash
markitdown --use-plugins path-to-file.pdf
```

**Develop new plugin**: See `packages/markitdown-sample-plugin/README.md` for plugin development guide.

## Build System

All packages use `hatchling` as the build backend:
- Package versions managed in `src/<package>/__about__.py`
- Dependencies defined in `pyproject.toml` with optional extras
- Test environment managed by hatch with `hatch-test` environment
- Type checking via `types` environment in hatch

## Python Requirements

- Python 3.10 or higher (tested on 3.10, 3.11, 3.12, 3.13)
- Recommend using virtual environment (venv, uv, or conda)

## Testing

Tests located in `packages/markitdown/tests/`:
- `test_module_*.py` - Python API tests
- `test_cli_*.py` - CLI tests
- `_test_vectors.py` - Test file vectors/fixtures

## CI/CD

- `.github/workflows/tests.yml` - Runs `hatch test` on Python 3.10-3.12
- `.github/workflows/pre-commit.yml` - Runs Black formatter checks

## Converting Files with Azure Document Intelligence

MarkItDown supports Microsoft Azure Document Intelligence for enhanced conversion:

**CLI**:
```bash
markitdown path-to-file.pdf -d -e "<document_intelligence_endpoint>"
```

**Python API**:
```python
from markitdown import MarkItDown
md = MarkItDown(docintel_endpoint="<endpoint>")
result = md.convert("test.pdf")
```

## LLM-Enhanced Image Descriptions

For PPTX and image files, MarkItDown can use LLMs for image descriptions:

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o", llm_prompt="optional custom prompt")
result = md.convert("example.jpg")
```
