---
description: OCR a scanned PDF or the images inside a DOCX/PPTX/XLSX into Markdown
argument-hint: <file> [model]
allowed-tools: Bash(uv run:*), Read
---

Extract the text of `$1`, including text inside images, using the markitdown-ocr plugin.

1. Check that `OPENAI_API_KEY` is set. If not, stop and tell me to set it.
2. Remind me in one line that page images are sent to OpenAI for OCR.
3. Run:
   `uv run "${CLAUDE_PLUGIN_ROOT}/scripts/markitdown_batch.py" "$1" --ocr --overwrite` and add `--model $2` if a model was given.
4. Tell me where the `.md` file was saved and show its first ~40 lines.
