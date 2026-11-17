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

Requires `markitdown>=0.1.8,<0.2.0`, which provides the Office image-rendering hooks used by this plugin. Installing the plugin automatically resolves a compatible core version.

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

### MiniCPM-OCR (Local)

[MiniCPM-OCR 1.0](https://github.com/OpenBMB/MiniCPM-OCR) is a compact document-parsing model that can be served locally through vLLM or SGLang and used through their OpenAI-compatible API. Start the server:

```bash
vllm serve openbmb/MiniCPM-OCR-1.0 \
  --served-model-name minicpm-ocr \
  --max-model-len 40960 \
  --host 127.0.0.1 --port 8000
```

Then point MarkItDown at it:

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="EMPTY"),
    llm_model="minicpm-ocr",
)
```

When the model name contains `minicpm-ocr`, the plugin selects a MiniCPM-OCR-aware service. It asks the model for Markdown rather than plain text, so tables and formulas in scanned pages stay structured, and it converts MiniCPM-OCR's OTSL table output into Markdown tables. The service uses deterministic decoding and the image-first message order recommended by the model's deployment guide.

This selection uses the `model` name sent to the server, so keep `minicpm-ocr` in the served name (the example above does). Names containing `jev` are excluded because MiniCPM-OCR Jev is a reliability-scoring model, not an OCR model.

The OCR request does not send an `enable_thinking` flag. MiniCPM-OCR's chat template disables thinking by default; if your server overrides that default, pass `--default-chat-template-kwargs '{"enable_thinking":false}'` when launching it. A leading `<think>...</think>` block is removed defensively if one is returned. See the [MiniCPM-OCR deployment guide](https://github.com/OpenBMB/MiniCPM-OCR/blob/main/docs/minicpm_ocr_tutorial_en.md) for model weights, GPU requirements, and the full launch command (including DSpark acceleration).

No extra Python packages are required: the plugin talks to the server through the same OpenAI-compatible client path.

## How It Works

When `MarkItDown(enable_plugins=True, llm_client=..., llm_model=...)` is called:

1. MarkItDown discovers the plugin via the `markitdown.plugin` entry point group
2. It calls `register_converters()`, forwarding all kwargs including `llm_client` and `llm_model`
3. The plugin creates an OCR service from those kwargs — `MiniCPMOCRService` when the model name contains `minicpm-ocr`, otherwise `LLMVisionOCRService`
4. Four OCR-enhanced converters are registered at **priority -1.0** — before the built-in converters at priority 0.0

When a file is converted:

1. The OCR converter accepts the file
2. It extracts embedded images from the document
3. Each image is sent to the LLM with an extraction prompt
4. The returned text is placed alongside document content (XLSX images follow their sheet's table)
5. If the LLM call fails, conversion continues without that image's text

The DOCX, PPTX, and XLSX converters subclass their core counterparts and override the same semi-private `_image_to_html` method. Core handles native content, preprocessing, and placement; the plugin supplies escaped OCR HTML, which passes through the shared HTML-to-Markdown renderer. PDF uses its separate existing pipeline.

## Supported File Formats

### PDF

- Embedded images are extracted by position (via `page.images` / page XObjects) and OCR'd inline, interleaved with the surrounding text in vertical reading order.
- **Scanned PDFs** (pages with no extractable text) are detected automatically: each page is rendered at 300 DPI and sent to the LLM as a full-page image.
- **Malformed PDFs** that pdfplumber/pdfminer cannot open (e.g. truncated EOF) are retried with PyMuPDF page rendering, so content is still recovered.

### DOCX

- Inherits core DOCX preprocessing, styles, math, and Mammoth conversion.
- Mammoth provides each embedded image to `_image_to_html`. OCR fragments are inserted into the document's HTML before Markdown rendering, not substituted into finished Markdown.
- Block fragments split enclosing paragraphs where necessary and remain inside their table cell or list item. Table-cell line breaks follow the shared HTML converter's existing limitations.

### PPTX

- Picture shapes, placeholder shapes with images, and images inside groups are all supported.
- Inherits core shape ordering, native text, tables, charts, and speaker notes.
- Slide content now uses the core converter's real line breaks rather than the old plugin's literal `\n` text, and inherits its empty-title and empty-notes handling.
- If an `llm_client` is configured, the LLM is asked for a description first; OCR is used as the fallback when no description is returned.

### XLSX

- Inherits core workbook repair and table rendering; images are read from the same repaired workbook.
- Images are listed under a `### Images in this sheet:` section after the sheet's data table — they are not interleaved into the table rows.
- Sheet heading spacing follows the core converter; no new cell-position labels are added.
- Legacy `.xls` files remain handled by the existing core converter, without image OCR.

### Output format

Every extracted OCR block is wrapped as:

```text
*[Image OCR]
<extracted text>
[End OCR]*
```

For Office formats, recognized text is escaped as literal HTML text before Markdown rendering. Markdown escaping and line breaks therefore follow the shared HTML converter: for example, underscores may be backslash-escaped, and direct converter results use Markdown hard breaks. `MarkItDown` subsequently strips trailing whitespace from each output line. Empty recognition retains the native image representation (XLSX normally omits images).

Repeated image bytes are recognized once per conversion, while the result is placed at every occurrence. The cache is not shared across documents or service overrides.

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

For Office OCR, a service-reported error emits a warning and retains native image rendering. Exceptions raised by custom OCR services propagate from direct converter calls; `MarkItDown` can retry another applicable converter through its normal fallback behavior.

## Development

### Running Tests

```bash
cd packages/markitdown-ocr
pytest tests/ -v
```

### Building from Source

```bash
git clone https://github.com/microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[docx,pptx,xlsx]' -e packages/markitdown-ocr
```

## Contributing

Contributions are welcome! See the [MarkItDown repository](https://github.com/microsoft/markitdown) for guidelines.

## License

MIT — see [LICENSE](LICENSE).

## Changelog

### Unreleased

- MiniCPM-OCR support: model-name detection, Markdown-oriented OCR prompt, OTSL table conversion, and defensive thinking-block removal

### 0.1.0 (Initial Release)

- LLM Vision OCR for PDF, DOCX, PPTX, XLSX
- Full-page OCR fallback for scanned PDFs
- Context-aware inline text insertion
- Priority-based converter replacement (no code changes required)
