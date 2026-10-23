# MarkItDown plugin for Claude Code

Turns PDF, Word, PowerPoint, Excel, CSV, HTML, EPUB, images, audio, ZIP files and web pages into Markdown that Claude can read.

## What's inside

| Piece | What it does |
|---|---|
| MCP server `markitdown` | The `markitdown-mcp` server from this repo, tool `convert_to_markdown(uri)`, with the `markitdown-ocr` and `markitdown-sample-plugin` (RTF) plugins loaded |
| Skill `markitdown` | Tells Claude when and how to convert documents |
| `/markitdown:convert <file-or-url>` | Convert one file or URL and save the `.md` |
| `/markitdown:batch <folder> [out] [-r] [--ocr]` | Convert a whole folder |
| `/markitdown:ocr <file> [model]` | OCR scanned PDFs and text inside images |
| `scripts/markitdown_batch.py` | Batch converter used by the commands (files, folders, URLs; OCR via OpenAI) |

The MCP server and the script use the same package versions as this repo (`markitdown 0.1.9`, `markitdown-mcp 0.0.1a8`, `markitdown-ocr 0.1.2`, `markitdown-sample-plugin 0.1.0a1`), installed from PyPI by `uv`.

## Requirements

- [`uv`](https://docs.astral.sh/uv/): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- For OCR only: `OPENAI_API_KEY` (optional `MARKITDOWN_LLM_MODEL`, default `gpt-4o`)

## Install

In Claude Code:

```
/plugin marketplace add mn526zwwfc-sketch/markitdown
/plugin install markitdown@markitdown
```

Or from a local clone: `/plugin marketplace add /path/to/markitdown`.

Restart Claude Code, then run `/mcp` to check that the `markitdown` server is connected. The first start downloads dependencies and can take a minute.

## Notes

- The MCP tool takes URIs: `file:///abs/path.pdf`, `https://…`, `data:…`.
- OCR is not available through the MCP tool (the server has no LLM client); use `/markitdown:ocr` or the script with `--ocr`.
- `--ocr` sends page images to OpenAI.
