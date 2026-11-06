---
name: markitdown
description: Convert PDF, PPT/PPTX, DOCX, XLSX, HTML, CSV, etc. to Markdown locally using Microsoft MarkItDown, without spending LLM tokens on the conversion. Use when the user says "markit", "markitdown", "down", or asks to read/convert/summarize a pdf, ppt, pptx, doc, docx, xls, xlsx file.
---

# markitdown

Conversion runs locally via a script. Do NOT read the original binary file and do NOT convert it yourself.

## Steps
1. Run: `<skill-dir>/scripts/md.sh "<file path>"`
   (set `MD_OUTDIR=<dir>` to write the .md elsewhere). Multiple files: run once per file.
2. The script prints only the `.md` path and its size. Do NOT cat the whole file.
3. Token-saving rules:
   - If the user only asked to convert, report the output path and stop.
   - Otherwise use `grep -n` or Read with `offset`/`limit` to pull only the sections needed.
   - Read the whole file only if it is small (under ~2000 lines) and the task needs all of it.
4. If a file is scanned/image-only, the output will be near-empty; say so rather than guessing.
