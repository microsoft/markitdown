# MarkItDown PaddleOCR Plugin

`markitdown-paddleocr` is a plugin-first OCR extension for MarkItDown.

The first release intentionally keeps scope narrow:

- PDF only
- opt-in via the existing MarkItDown plugin mechanism
- scanned PDF fallback only
- no changes to MarkItDown core behavior
- local / offline OCR backend
- Chinese document pages are the primary target for the first iteration

## Why this plugin exists

The built-in PDF converter already works well for machine-readable PDFs.
This plugin targets the complementary case: scanned PDFs where text extraction
returns little or no usable content, especially report-style Chinese pages with
mixed paragraphs, chart labels, captions, and numeric content.

When enabled, the plugin:

1. runs the built-in MarkItDown PDF conversion first
2. returns that result unchanged when text is extracted successfully
3. falls back to PaddleOCR only when the built-in result is empty

This preserves MarkItDown's current defaults while adding a separate path for:

- local CPU-friendly deployments
- cost-sensitive OCR workflows
- Chinese scanned reports and similar enterprise documents

## Installation

Install PaddlePaddle first, following the official PaddleOCR guidance for your
platform, then install this plugin:

```bash
pip install markitdown-paddleocr
```

In practice, most environments will install PaddlePaddle and PaddleOCR together:

```bash
pip install paddlepaddle paddleocr
pip install markitdown-paddleocr
```

## Python Usage

```python
from markitdown import MarkItDown

md = MarkItDown(
    enable_plugins=True,
    paddleocr_enabled=True,
)

result = md.convert("scanned.pdf")
print(result.markdown)
```

This package is intentionally Python-API-first. It does not extend MarkItDown's built-in CLI surface with new provider-specific flags.

Optional plugin kwargs:

- `paddleocr_lang`: OCR language, defaults to `"ch"`
- `paddleocr_kwargs`: extra keyword arguments forwarded to `paddleocr.PaddleOCR`

Example:

```python
md = MarkItDown(
    enable_plugins=True,
    paddleocr_enabled=True,
    paddleocr_lang="ch",
    paddleocr_kwargs={
        "use_doc_orientation_classify": False,
        "use_doc_unwarping": False,
        "use_textline_orientation": False,
    },
)
```

## Output format

OCR fallback output is emitted as:

```text
## Page 1

*[Image OCR]
...
[End OCR]*
```

## Notes

- This package does not modify MarkItDown core APIs.
- If `paddleocr_enabled` is not set, the plugin falls back to the built-in PDF converter.
- This package is intentionally PDF-only for the first iteration to keep review scope small.
- A first model initialization can take noticeable time because PaddleOCR downloads model files on demand.
- Setting `PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True` can skip the startup connectivity check in constrained environments.

## Non-goals for v0.1

- no DOCX, PPTX, or XLSX OCR
- no automatic OCR on all PDFs
- no vendor-specific settings added to MarkItDown core
- no attempt to replace the existing LLM-based `markitdown-ocr` plugin

## Demo

See [DEMO.md](DEMO.md) for before/after notes on representative Chinese samples.

You can also run the local comparison helper:

```bash
python run_demo.py /path/to/sample.png
```
