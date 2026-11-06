---
description: Convert every supported file in a folder to Markdown
argument-hint: <folder> [output-folder] [--ocr] [-r]
allowed-tools: Bash(uv run:*), Bash(ls:*), Read
---

Convert the documents in the folder given in `$ARGUMENTS` to Markdown.

1. The first argument is the source folder. If a second non-flag argument is given, it is the output folder (`-o`); otherwise write `.md` files next to the sources.
2. Pass through `-r` (recurse) and `--ocr` if I included them. Before running with `--ocr`, check that `OPENAI_API_KEY` is set and remind me that page images are sent to OpenAI.
3. Run:
   `uv run "${CLAUDE_PLUGIN_ROOT}/scripts/markitdown_batch.py" <folder> [-o <output>] [-r] [--ocr]`
4. Report the `converted / skipped / failed` summary, list failures with their reason, and offer `--overwrite` if files were skipped.
