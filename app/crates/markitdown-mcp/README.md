# markitdown-mcp (Rust)

A lightweight MCP server (built on [rmcp](https://docs.rs/rmcp), the official
Rust MCP SDK) that lets Claude — or any MCP client — convert documents to
Markdown. Single static binary, stdio transport, no Docker, no Python, no
system dependencies. Light enough for low-RAM devices.

## Tools

| Tool | Arguments | Returns |
|---|---|---|
| `convert_to_markdown` | `uri` (path or `file:`/`data:`/`http(s):`), `max_chars?` (default 50000), `offset?`, `engine?` | Markdown text, paged. A trailing note gives the next `offset` when truncated. |
| `convert_file` | `path`, `output_path?`, `engine?` | Full markdown — or, with `output_path`, writes the file and returns only title/char-count/500-char preview (use for big docs). |
| `convert_batch` | `paths[]`, `output_dir`, `engine?` | Converts in parallel; one `ok:`/`FAILED:` line per file. |
| `list_supported_formats` | — | Format/extension/caveat table + whether the Python fallback and LLM captions are currently available. |

`engine`: `auto` (default — Rust, transparent Python retry on fidelity gaps),
`rust`, or `python` (force full Python fidelity, e.g. PDF table
reconstruction; needs `MARKITDOWN_PY_BIN`).

Supported formats: PDF, DOCX, XLSX/XLS, PPTX, HTML (incl. Wikipedia/Bing/
YouTube pages), CSV, EPUB, ZIP (recursive), Jupyter notebooks, Outlook `.msg`,
RSS/Atom, images (EXIF), audio (tags), plain text/JSON.

## Build

```bash
cd app
cargo build --release -p markitdown-mcp
# binary: app/target/release/markitdown-mcp
```

## Connect to Claude Code

```bash
claude mcp add markitdown -- /ABSOLUTE/PATH/TO/app/target/release/markitdown-mcp
```

Verify with `/mcp` inside Claude Code, or:

```bash
claude mcp list
```

## Connect to Claude Desktop

Add to `claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`,
Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "/ABSOLUTE/PATH/TO/app/target/release/markitdown-mcp"
    }
  }
}
```

Restart Claude Desktop; the four tools appear under the `markitdown` server.

## Optional: OCR / transcription fallback

Set `MARKITDOWN_PY_BIN` to a Python engine binary (see
`app/python-engine/README.md`) and the server transparently retries with it
whenever the Rust engine hits a fidelity gap — scanned PDFs (OCR), DOCX
comments/equations, RTF-only `.msg` bodies, audio transcription, YouTube
transcripts, image OCR — keeping whichever result has more content:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "/path/to/markitdown-mcp",
      "env": {
        "MARKITDOWN_PY_BIN": "/path/to/markitdown-py",
        "MARKITDOWN_LLM_API_KEY": "sk-... (optional: image captions)",
        "MARKITDOWN_LLM_MODEL": "gpt-4o-mini",
        "MARKITDOWN_PY_ARGS": "(optional: e.g. -d -e https://<res>.cognitiveservices.azure.com/)"
      }
    }
  }
}
```

URLs are handed to the Python engine *as URLs*, so YouTube transcripts,
Wikipedia and Bing SERP conversions reach full Python fidelity; local files
are passed as paths (zero-copy).

## Smoke test without a client

```bash
printf '%s\n%s\n%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}' \
 '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
 | ./target/release/markitdown-mcp
```

Or use the MCP Inspector: `npx @modelcontextprotocol/inspector /path/to/markitdown-mcp`.

## Design notes

- **stdio transport only** — what Claude uses; stdout carries the protocol,
  all logs go to stderr (`RUST_LOG=debug` for verbose).
- **Token-efficient by construction** — 4 focused tools; paged output;
  write-to-disk summaries for large documents.
- **Heavy jobs** — conversions run on a blocking thread pool; batches use all
  cores via rayon.

A companion skill that teaches Claude the cheapest call patterns lives at
`app/skill/markitdown/SKILL.md`.

## Tests

```bash
cargo test -p markitdown-mcp
```

Spawns the real binary and drives a full JSON-RPC session: initialize →
tools/list → tools/call on real fixtures, paging, batch, and error recovery.
