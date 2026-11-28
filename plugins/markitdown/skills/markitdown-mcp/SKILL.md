---
name: markitdown-mcp
description: >-
  Run and wire up the markitdown-mcp server (STDIO, Streamable HTTP or SSE,
  or Docker) that exposes the convert_to_markdown(uri) tool. Use when adding
  MarkItDown to an MCP client config, debugging the server with MCP
  Inspector, or mounting local files into the Docker image.
---

# MarkItDown MCP server

Package: `packages/markitdown-mcp` (PyPI `markitdown-mcp`). It exposes one
tool, `convert_to_markdown(uri)`, where `uri` is an `http:`, `https:`,
`file:` or `data:` URI. It is meant for **local use with trusted agents**.

## Run

```bash
pip install markitdown-mcp
markitdown-mcp                                   # STDIO (default)
markitdown-mcp --http --host 127.0.0.1 --port 3001  # Streamable HTTP + SSE
```

HTTP binds to `localhost` by default. Do not bind other interfaces unless the
user understands the security implications: the tool can read any file and
URL the process can reach.

## Client config (STDIO)

```json
{
  "mcpServers": {
    "markitdown": { "command": "markitdown-mcp" }
  }
}
```

The plugin in this repository ships the same entry in `.mcp.json`, using
`uvx markitdown-mcp` so no global install is needed.

## Docker

```bash
cd packages/markitdown-mcp
docker build -t markitdown-mcp:latest .
docker run -it --rm -v /home/user/data:/workdir markitdown-mcp:latest
```

Files mounted at `/workdir` are reachable as `file:///workdir/<name>`. Client
config for Docker:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-v", "/home/user/data:/workdir", "markitdown-mcp:latest"]
    }
  }
}
```

## Debug

```bash
npx @modelcontextprotocol/inspector
```

- STDIO: transport `STDIO`, command `markitdown-mcp`.
- HTTP: transport `Streamable HTTP`, URL `http://127.0.0.1:3001/mcp`.

## Tips

- Local files must be passed as `file:` URIs, not bare paths.
- When conversion of a format fails, check that the server's environment has
  the matching `markitdown[...]` extra installed.
