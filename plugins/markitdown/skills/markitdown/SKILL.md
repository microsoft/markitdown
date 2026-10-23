---
name: markitdown
description: Convert documents to Markdown with MarkItDown. Use when the user wants to read, summarize, search, quote or extract data from a PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx/.xls), CSV, JSON, XML, HTML, EPUB, Jupyter notebook, Outlook .msg, RTF, ZIP, image (EXIF/OCR) or audio file (transcription), or a web page / YouTube URL, or when they ask to convert files or a whole folder to Markdown, including scanned PDFs that need OCR.
---

# MarkItDown

This plugin gives you two ways to turn files into Markdown. Pick by the job:

| Job | Use |
|---|---|
| Read one file or URL so you can answer about it | MCP tool `convert_to_markdown` |
| Convert several files, a folder, or save `.md` files to disk | `scripts/markitdown_batch.py` |
| Scanned PDF, or text inside images in PDF/DOCX/PPTX/XLSX | `scripts/markitdown_batch.py --ocr` |

## 1. MCP tool: `convert_to_markdown(uri)`

Takes a URI, not a bare path:

- Local file: `file:///absolute/path/to/report.pdf` (make the path absolute; percent-encode spaces as `%20`)
- Web: `https://example.com/page` (YouTube URLs return title, description and transcript)
- Inline: `data:text/csv;base64,...`

The server runs with plugins enabled, so `.rtf` files are handled by the RTF sample plugin. OCR is not available through the MCP tool because the server has no LLM client; use the script for that.

If the tool reports an unsupported format, tell the user which format failed instead of guessing at the content.

## 2. Batch script

```bash
uv run "${CLAUDE_PLUGIN_ROOT}/scripts/markitdown_batch.py" [options] INPUT [INPUT ...]
```

Inputs can be files, folders and URLs mixed together. Options:

- `-o DIR`: write `.md` files to `DIR`, mirroring folder structure (default: next to each source). Output is named `<file>.<ext>.md`, e.g. `report.pdf.md`
- `-r`: recurse into subfolders
- `--stdout`: print instead of writing files (good for reading a few files at once)
- `--overwrite`: replace existing `.md` files (default skips them)
- `--ocr`: OCR embedded images and scanned pages with an LLM. Needs `OPENAI_API_KEY`; model from `--model` or `$MARKITDOWN_LLM_MODEL` (default `gpt-4o`); `--prompt` overrides the extraction prompt
- `--keep-data-uris`: keep base64 images in the output

The script prints one `OK` / `SKIPPED` / `FAILED` line per file and a final `converted=… skipped=… failed=…` summary on stderr. Report that summary to the user, and list any failures.

The first run downloads dependencies through `uv`, which can take a minute.

## Requirements

`uv` must be installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`). If `uvx` or `uv` is missing, tell the user that rather than trying other installers.

## Tips

- For long documents, convert to a file with the script and then read the parts you need, instead of pulling the whole Markdown into the conversation.
- `--ocr` sends page images to OpenAI. Confirm with the user before using it on confidential documents.
