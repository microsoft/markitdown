# MarkItDown-MCP

[![PyPI](https://img.shields.io/pypi/v/markitdown-mcp.svg)](https://pypi.org/project/markitdown-mcp/)
![PyPI - Downloads](https://img.shields.io/pypi/dd/markitdown-mcp)
[![Built by AutoGen Team](https://img.shields.io/badge/Built%20by-AutoGen%20Team-blue)](https://github.com/microsoft/autogen)

The `markitdown-mcp` package provides a lightweight STDIO and SSE MCP server for calling MarkItDown.

It exposes one tool: `convert_to_markdown(uri)`, where uri can be any `http:`, `https:`, `file:`, or `data:` URI.

## Installation

To install the package, use pip:

```bash
pip install markitdown-mcp
```

## Usage

To run the MCP server, ussing STDIO (default) use the following command:


```bash	
markitdown-mcp
```

To run the MCP server, using SSE use the following command:

```bash	
markitdown-mcp --sse --host 127.0.0.1 --port 3001
```

## Running in Docker

To run `markitdown-mcp` in Docker, build the Docker image using the provided Dockerfile:
```bash
docker build -t markitdown-mcp:latest .
```

And run it using:
```bash
docker run -it --rm markitdown-mcp:latest
```
This will be sufficient for remote URIs. To access local files, you need to mount the local directory into the container. For example, if you want to access files in `/home/user/data`, you can run:

```bash
docker run -it --rm -v /home/user/data:/workdir markitdown-mcp:latest
```

Once mounted, all files under data will be accessible under `/workdir` in the container. For example, if you have a file `example.txt` in `/home/user/data`, it will be accessible in the container at `/workdir/example.txt`.

## Accessing from Claude Desktop

It is recommended to use the Docker image when running the MCP server for Claude Desktop.

Follow [these instrutions](https://modelcontextprotocol.io/quickstart/user#for-claude-desktop-users) to access Claude's `claude_desktop_config.json` file.

Edit it to include the following JSON entry:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "markitdown-mcp:latest"
      ]
    }
  }
}
```

If you want to mount a directory, adjust it accordingly:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": [
	"run",
	"--rm",
	"-i",
	"-v",
	"/home/user/data:/workdir",
	"markitdown-mcp:latest"
      ]
    }
  }
}
```

## Accessing from VS Code

For quick installation, use one of the one-click install buttons below...

[![Install with PyPI in VS Code](https://img.shields.io/badge/VS_Code-PyPI-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=markitdown&config=%7B%22command%22%3A%22pip%22%2C%22args%22%3A%5B%22install%22%2C%22markitdown-mcp%22%5D%7D) [![Install with PyPI in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-PyPI-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=markitdown&config=%7B%22command%22%3A%22pip%22%2C%22args%22%3A%5B%22install%22%2C%22markitdown-mcp%22%5D%7D&quality=insiders)

[![Install with Docker in VS Code](https://img.shields.io/badge/VS_Code-Docker-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=markitdown&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22markitdown-mcp%3Alatest%22%5D%7D) [![Install with Docker in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Docker-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=markitdown&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22-i%22%2C%22--rm%22%2C%22markitdown-mcp%3Alatest%22%5D%7D&quality=insiders)

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open User Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace. This will allow you to share the configuration with others.

> Note that the `mcp` key is not needed in the `.vscode/mcp.json` file.

Using pip:

```json
{
  "mcp": {
    "servers": {
      "markitdown": {
        "command": "markitdown-mcp"
      }
    }
  }
}
```

Using Docker:

```json
{
  "mcp": {
    "servers": {
      "markitdown": {
        "command": "docker",
        "args": ["run", "-i", "--rm", "markitdown-mcp:latest"]
      }
    }
  }
}
```

If you need to access local files, you can mount a directory using Docker:

```json
{
  "mcp": {
    "servers": {
      "markitdown": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
          "-v",
      	  "/home/user/data:/workdir",
	        "markitdown-mcp:latest"
        ]
      }
    }
  }
}
```

## Debugging

To debug the MCP server you can use the `mcpinspector` tool.

```bash
npx @modelcontextprotocol/inspector
```

You can then connect to the insepctor through the specified host and port (e.g., `http://localhost:5173/`).

If using STDIO:
* select `STDIO` as the transport type,
* input `markitdown-mcp` as the command, and
* click `Connect`

If using SSE:
* select `SSE` as the transport type,
* input `http://127.0.0.1:3001/sse` as the URL, and
* click `Connect`

Finally:
* click the `Tools` tab,
* click `List Tools`,
* click `convert_to_markdown`, and
* run the tool on any valid URI.

## Security Considerations

The server does not support authentication, and runs with the privileges if the user running it. For this reason, when running in SSE mode, it is recommended to run the server bound to `localhost` (default).


## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
