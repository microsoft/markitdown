# MarkItDown OCR Plugin

LLM Vision plugin for MarkItDown that extracts text from images embedded in PDF, DOCX, PPTX, and XLSX files.

Uses the same `llm_client` / `llm_model` pattern that MarkItDown already supports for image descriptions — no new ML libraries or binary dependencies required.

## Features

- **Enhanced PDF Converter**: Extracts text from images within PDFs, with full-page OCR fallback for scanned documents
- **Enhanced DOCX Converter**: OCR for images in Word documents
- **Enhanced PPTX Converter**: OCR for images in PowerPoint presentations
- **Enhanced XLSX Converter**: OCR for images in Excel spreadsheets
- **Context Preservation**: Maintains document structure and flow when inserting extracted text

## Installation

```bash
pip install markitdown-ocr
```

The plugin uses whatever OpenAI-compatible client you already have. Install one if you don't have it yet:

```bash
pip install openai
```

## Usage

### Command Line

```bash
markitdown document.pdf --use-plugins --llm-client openai --llm-model gpt-4o
```

### Python API

Pass `llm_client` and `llm_model` to `MarkItDown()` exactly as you would for image descriptions:

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
)

result = md.convert("document_with_images.pdf")
print(result.text_content)
```

If no `llm_client` is provided the plugin still loads, but OCR is silently skipped — falling back to the standard built-in converter.

### Custom Prompt

Override the default extraction prompt for specialized documents:

```python
md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
    llm_prompt="Extract all text from this image, preserving table structure.",
)
```

### Any OpenAI-Compatible Client

Works with any client that follows the OpenAI API:

```python
from openai import AzureOpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=AzureOpenAI(
        api_key="...",
        azure_endpoint="https://your-resource.openai.azure.com/",
        api_version="2024-02-01",
    ),
    llm_model="gpt-4o",
)
```

## How It Works

When `MarkItDown(enable_plugins=True, llm_client=..., llm_model=...)` is called:

1. MarkItDown discovers the plugin via the `markitdown.plugin` entry point group
2. It calls `register_converters()`, forwarding all kwargs including `llm_client` and `llm_model`
3. The plugin creates an `LLMVisionOCRService` from those kwargs
4. Four OCR-enhanced converters are registered at **priority -1.0** — before the built-in converters at priority 0.0

When a file is converted:

1. The OCR converter accepts the file
2. It extracts embedded images from the document
3. Each image is sent to the LLM with an extraction prompt
4. The returned text is inserted inline, preserving document structure
5. If the LLM call fails, conversion continues without that image's text

## Supported File Formats

| Format | Behavior |
| ------ | --------- |
| **PDF** | OCR for embedded images; full-page LLM OCR fallback for scanned (text-free) documents |
| **DOCX** | OCR for inline images, maintaining document flow |
| **PPTX** | OCR for slide images |
| **XLSX** | OCR for embedded images, with cell-position context |

## Troubleshooting

### OCR text missing from output

The most likely cause is a missing `llm_client` or `llm_model`. Verify:

```python
from openai import OpenAI
from markitdown import MarkItDown

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),   # required
    llm_model="gpt-4o",    # required
)
```

### Plugin not loading

Confirm the plugin is installed and discovered:

```bash
markitdown --list-plugins   # should show: ocr
```

### API errors

The plugin propagates LLM API errors as warnings and continues conversion. Check your API key, quota, and that the chosen model supports vision inputs.

## Development

### Running Tests

```bash
cd packages/markitdown-ocr
pytest tests/ -v
```

### Building from Source

```bash
git clone https://github.com/microsoft/markitdown.git
cd markitdown/packages/markitdown-ocr
pip install -e .
```

## Contributing

Contributions are welcome! See the [MarkItDown repository](https://github.com/microsoft/markitdown) for guidelines.

## License

MIT — see [LICENSE](LICENSE).

## Changelog

### 0.1.0 (Initial Release)

- LLM Vision OCR for PDF, DOCX, PPTX, XLSX
- Full-page OCR fallback for scanned PDFs
- Context-aware inline text insertion
- Priority-based converter replacement (no code changes required)
