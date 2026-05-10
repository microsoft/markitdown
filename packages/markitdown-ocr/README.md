# MarkItDown OCR Plugin

OCR plugin for MarkItDown that extracts text from images embedded in PDF, DOCX, PPTX, and XLSX files.

Supports **two OCR providers**:

- **glm-ocr** — ZhiPu AI's specialized layout parsing model (better table recognition, lower cost)
- **LLM Vision** — Any OpenAI-compatible vision model (GPT-4o, Gemini, etc.)

## Features

- **Enhanced PDF Converter**: Extracts text from images within PDFs, with full-page OCR fallback for scanned documents
- **Enhanced DOCX Converter**: OCR for images in Word documents
- **Enhanced PPTX Converter**: OCR for images in PowerPoint presentations
- **Enhanced XLSX Converter**: OCR for images in Excel spreadsheets
- **Context Preservation**: Maintains document structure and flow when inserting extracted text
- **Multiple Providers**: Choose glm-ocr for best table/Chinese text recognition, or LLM Vision for general use

## Installation

```bash
pip install markitdown-ocr
```

Then install at least one OCR provider:

```bash
# Option 1: glm-ocr (recommended for Chinese documents and tables)
pip install markitdown-ocr[glmocr]

# Option 2: LLM Vision (general purpose, any OpenAI-compatible model)
pip install markitdown-ocr[llm]
```

## Usage

### Using glm-ocr Provider (Recommended)

glm-ocr uses ZhiPu AI's specialized layout parsing model — better table recognition, structured output, and lower cost.

**Via environment variable:**

```bash
export GLMOCR_API_KEY="your-zhipu-api-key"
markitdown document.pdf --use-plugins
```

**Via Python API:**

```python
from markitdown import MarkItDown

# Option 1: Pass API key directly
md = MarkItDown(
    enable_plugins=True,
    glmocr_api_key="your-zhipu-api-key",
)

# Option 2: Use environment variable (GLMOCR_API_KEY)
md = MarkItDown(enable_plugins=True)

result = md.convert("document_with_tables.pdf")
print(result.text_content)
```

**Via config file** (`pyproject.toml`):

```toml
[tool.markitdown-ocr.glmocr]
# api_key = ""  # Recommended: use env var GLMOCR_API_KEY instead
model = "glm-ocr"
timeout = 120
```

### Using LLM Vision Provider

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

### Provider Priority

When both providers are configured, **glm-ocr takes priority**. To force LLM Vision instead, simply don't set `glmocr_api_key`:

```python
md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
    # glmocr_api_key not set → uses LLM Vision
)
```

If no provider is configured, the plugin still loads but OCR is silently skipped — falling back to the standard built-in converter.

### Custom Prompt (LLM Vision only)

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

### Provider Selection

When `MarkItDown(enable_plugins=True, ...)` is called:

1. MarkItDown discovers the plugin via the `markitdown.plugin` entry point group
2. It calls `register_converters()`, forwarding all kwargs
3. The plugin selects an OCR provider:
   - If `glmocr_api_key` or `GLMOCR_API_KEY` is set → **GlmOcrService** (zai-sdk + glm-ocr)
   - Else if `llm_client` + `llm_model` are set → **LLMVisionOCRService** (OpenAI-compatible)
   - Else → no OCR (standard text extraction)
4. Four OCR-enhanced converters are registered at **priority -1.0** — before the built-in converters at priority 0.0

### Conversion Flow

When a file is converted:

1. The OCR converter accepts the file
2. It extracts embedded images from the document
3. Each image is sent to the selected OCR provider
4. The returned text is inserted inline, preserving document structure
5. If the OCR call fails, conversion continues without that image's text

## Supported File Formats

### PDF

- Embedded images are extracted by position (via `page.images` / page XObjects) and OCR'd inline, interleaved with the surrounding text in vertical reading order.
- **Scanned PDFs** (pages with no extractable text) are detected automatically: each page is rendered at 300 DPI and sent to the OCR provider as a full-page image.
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

## Configuration Reference

### glm-ocr Provider

| Parameter | Env Variable | Default | Description |
|-----------|-------------|---------|-------------|
| `glmocr_api_key` | `GLMOCR_API_KEY` | — | ZhiPu AI API key (required) |
| `glmocr_model` | `GLMOCR_MODEL` | `"glm-ocr"` | Model name |
| `glmocr_timeout` | `GLMOCR_TIMEOUT` | `120` | Request timeout (seconds) |

### LLM Vision Provider

| Parameter | Description |
|-----------|-------------|
| `llm_client` | OpenAI-compatible client instance |
| `llm_model` | Model name (e.g., `'gpt-4o'`) |
| `llm_prompt` | Custom extraction prompt |

## Troubleshooting

### OCR text missing from output

The most likely cause is a missing provider configuration. Verify:

```python
# For glm-ocr
md = MarkItDown(enable_plugins=True, glmocr_api_key="your-key")

# For LLM Vision
from openai import OpenAI
md = MarkItDown(enable_plugins=True, llm_client=OpenAI(), llm_model="gpt-4o")
```

### glm-ocr import error

Make sure zai-sdk is installed:

```bash
pip install markitdown-ocr[glmocr]
```

### Plugin not loading

Confirm the plugin is installed and discovered:

```bash
markitdown --list-plugins   # should show: ocr
```

### API errors

The plugin propagates OCR API errors as warnings and continues conversion. Check your API key, quota, and that the chosen model supports vision inputs.

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

### 0.2.0

- **Added glm-ocr provider**: ZhiPu AI layout parsing via zai-sdk
- Provider selection: glm-ocr (priority) → LLM Vision (fallback)
- New `GlmOcrService` class with `extract_text()` interface
- New `GlmOcrConfig` for configuration management (env vars + TOML + kwargs)
- HTML → Markdown conversion for glm-ocr structured output
- Optional dependency: `markitdown-ocr[glmocr]`

### 0.1.0 (Initial Release)

- LLM Vision OCR for PDF, DOCX, PPTX, XLSX
- Full-page OCR fallback for scanned PDFs
- Context-aware inline text insertion
- Priority-based converter replacement (no code changes required)
