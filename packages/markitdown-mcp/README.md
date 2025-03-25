# MarkItDown-MCP

[![PyPI](https://img.shields.io/pypi/v/markitdown.svg)](https://pypi.org/project/markitdown/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

The `markitdown-mcp` package provides a lightweight SSE MCP server for calling MarkItDown.

It exposes one tool: `convert_to_markdown(uri)`, where uri can be any `http:`, `https:`, `file:`, or `data:` URI.

## Installation

To install the package, use pip:

```bash
pip install markitdown-mcp
```

## Usage

To run the MCP server, use the following command:

```bash	
markitdown-mcp --host 127.0.0.1 --port 3001
```

## Accessing from Claude Desktop

TODO

## Debugging

To debug the MCP server you can use the `mcpinspector` tool.

```bash
npx @modelcontextprotocol/inspector
```

You can then connect to the insepctor through the specified host and port (e.g., `http://localhost:5173/`).

Then:
* select `SSE` as the transport type,
* input `http://127.0.0.1:3001/sse` as the URL, and
* click `Connect`

Finally:
* click the `Tools` tab,
* click `List Tools`,
* click `convert_to_markdown`, and
* run the tool on any valid URI.

## Security Considerations

The server does not support authentication, and runs with the privileges of the user running it. It is recommended to run the server bound to `localhost` (default).


## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
