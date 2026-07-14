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

### PDF

- Embedded images are extracted by position (via `page.images` / page XObjects) and OCR'd inline, interleaved with the surrounding text in vertical reading order.
- **Scanned PDFs** (pages with no extractable text) are detected automatically: each page is rendered at 300 DPI and sent to the LLM as a full-page image.
- **Malformed PDFs** that pdfplumber/pdfminer cannot open (e.g. truncated EOF) are retried with PyMuPDF page rendering, so content is still recovered.

### DOCX

- Images are extracted via document part relationships (`doc.part.rels`).
- OCR is run before the DOCX→HTML→Markdown pipeline executes: placeholder tokens are injected into the HTML so that the markdown converter does not escape the OCR markers, and the final placeholders are replaced with the formatted `*[Image OCR]...[End OCR]*` blocks after conversion.
- Document flow (headings, paragraphs, tables) is fully preserved around the OCR blocks.

### PPTX

- Picture shapes, placeholder shapes with images, and images inside groups are all supported.
- Shapes are processed in top-to-left reading order per slide.
- If an `llm_client` is configured, the LLM is asked for a description first; OCR is used as the fallback when no description is returned.

### XLSX

- Images embedded in worksheets (`sheet._images`) are extracted per sheet.
- Cell position is calculated from the image anchor coordinates (column/row → Excel letter notation).
- Images are listed under a `### Images in this sheet:` section after the sheet's data table — they are not interleaved into the table rows.

### Output format

Every extracted OCR block is wrapped as:

```text
*[Image OCR]
<extracted text>
[End OCR]*
```

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
