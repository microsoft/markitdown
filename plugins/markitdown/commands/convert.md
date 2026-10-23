---
description: Convert a file or URL to Markdown and save it next to the source
argument-hint: <file-or-url> [output.md]
allowed-tools: Bash(uv run:*), Read, mcp__plugin_markitdown_markitdown__convert_to_markdown
---

Convert `$1` to Markdown with MarkItDown.

- If `$2` is given, save the result there; otherwise save it next to the source as `<name>.<ext>.md` (for a URL, in the current directory).
- Use the batch script, which writes the file for you:
  `uv run "${CLAUDE_PLUGIN_ROOT}/scripts/markitdown_batch.py" "$1" --overwrite` (add `-o <dir>` when `$2` points to another folder, then rename if needed).
- If `uv` is not available, fall back to the `convert_to_markdown` MCP tool (pass a `file://` URI with an absolute path) and write the result yourself.

Then tell me where the file was saved, how long it is, and give a 3–5 line summary of its content.
