---
name: markitdown
description: Convert documents (PDF, DOCX, XLSX, PPTX, HTML, CSV, EPUB, ZIP, ipynb, Outlook .msg, RSS, images, audio) to Markdown via the markitdown MCP server. Use whenever the user wants to read, extract, summarize, or transform the contents of such files or URLs.
---

# markitdown MCP — efficient usage

Four tools on the `markitdown` server. Pick by size and count, not habit:

| Situation | Call |
|---|---|
| Small/medium file or URL, need content inline | `convert_to_markdown {uri}` |
| Large document (PDF/EPUB/book) | `convert_file {path, output_path}` → then Read/Grep the written .md selectively |
| Need a specific later section inline | `convert_to_markdown {uri, offset, max_chars}` (paged; truncation note gives next offset) |
| Many files | `convert_batch {paths[], output_dir}` — one call, parallel, never loop convert_file |
| Unsure a format is supported | `list_supported_formats {}` (once per session, max) |

## Rules (token efficiency)

1. **Never** pull a whole large document into context: use `convert_file` with
   `output_path` (returns title + char count + 500-char preview only), then
   read just the sections you need from the output file.
2. Default page size is 50,000 chars. Don't raise `max_chars` to "get it all";
   page with `offset` or switch to `convert_file {output_path}`.
3. Batch ≥3 files with `convert_batch` — one tool call, one status report.
4. `uri` accepts plain paths plus `file:` / `data:` / `http(s):` — fetchable
   web pages (incl. Wikipedia/Bing/YouTube) convert directly; no separate
   download step.
5. Optional `engine` param on every convert tool: leave unset (`auto`) unless
   the user explicitly needs maximum fidelity for a complex PDF (tables) —
   then `engine: "python"` (only works when the server reports the Python
   engine as available).

## Caveats

- `list_supported_formats` reports whether the Python fallback (OCR,
  transcription, YouTube transcripts, RTF bodies, DOCX comments/equations)
  and LLM image captions are available. When the Python engine is configured
  those all just work via `auto`; when not, scanned PDFs return an
  HTML-comment note, images → EXIF + dimensions, audio → tags + duration.
  Check before promising OCR/transcription.
- Failures come back as tool errors with the converter name; the server stays
  alive — no need to reconnect.
