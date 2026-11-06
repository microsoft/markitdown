import contextlib
import logging
import os
import sys
from collections.abc import AsyncIterator
from pathlib import Path
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from starlette.applications import Starlette
from markitdown import MarkItDown, FileConversionException, UnsupportedFormatException
import requests
import uvicorn

logger = logging.getLogger(__name__)

# Initialize the MCP server for MarkItDown
mcp = MCPServer("markitdown")


@mcp.tool()
async def convert_to_markdown(uri: str, output_file: str | None = None) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI.

    Set output_file to write the markdown to a new local file and return its
    absolute path. Existing files are never overwritten.
    """
    markdown = _convert_uri(uri)
    if output_file is None:
        return markdown

    try:
        return write_markdown_file(output_file, markdown)
    except OSError as exc:
        detail = (
            os.strerror(exc.errno) if exc.errno else "the file could not be written"
        )
        raise ToolError(f"Could not write the output file: {detail}.") from exc


def write_markdown_file(output_file: str, markdown: str) -> str:
    output_path = Path(output_file).expanduser()
    fd = os.open(
        output_path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600,
    )
    try:
        with os.fdopen(fd, "wb") as output:
            fd = -1
            output.write(markdown.encode("utf-8"))
    except BaseException:
        if fd >= 0:
            os.close(fd)
        output_path.unlink(missing_ok=True)
        raise
    return str(output_path.resolve())


def _convert_uri(uri: str) -> str:
    converter = MarkItDown(enable_plugins=check_plugins_enabled())
    try:
        return converter.convert_uri(uri).markdown

    # SDK 2.x only exposes ToolError messages.
    except UnsupportedFormatException as exc:
        raise ToolError(str(exc)) from exc
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        raise ToolError(
            f"Fetching the resource failed with HTTP status {status}."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise ToolError("Could not fetch the resource.") from exc
    except FileConversionException as exc:
        raise ToolError("File conversion failed.") from exc
    except OSError as exc:
        # str(exc) embeds the resolved path; errno's fixed strerror does not.
        detail = (
            os.strerror(exc.errno) if exc.errno else "the resource could not be read"
        )
        raise ToolError(f"Could not read the resource: {detail}.") from exc
    except ValueError as exc:
        # URI validation failures raised by convert_uri itself, which only
        # restate the URI the client supplied.
        raise ToolError(str(exc)) from exc


def check_plugins_enabled() -> bool:
    return os.getenv("MARKITDOWN_ENABLE_PLUGINS", "false").strip().lower() in (
        "true",
        "1",
        "yes",
    )


def create_starlette_app(
    mcp_server: MCPServer, *, host: str = "127.0.0.1", debug: bool = False
) -> Starlette:
    sse_app = mcp_server.sse_app(host=host)
    http_app = mcp_server.streamable_http_app(
        json_response=True,
        stateless_http=True,
        host=host,
    )

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Run both sub-apps' lifespans (the Streamable HTTP session manager)."""
        async with sse_app.router.lifespan_context(app):
            async with http_app.router.lifespan_context(app):
                yield

    return Starlette(
        debug=debug,
        routes=[*sse_app.routes, *http_app.routes],
        lifespan=lifespan,
    )


# Main entry point
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run a MarkItDown MCP server")

    parser.add_argument(
        "--http",
        action="store_true",
        help="Run the server with Streamable HTTP and SSE transport rather than STDIO (default: False)",
    )
    parser.add_argument(
        "--sse",
        action="store_true",
        help="(Deprecated) An alias for --http (default: False)",
    )
    parser.add_argument(
        "--host", default=None, help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=None, help="Port to listen on (default: 3001)"
    )
    args = parser.parse_args()

    use_http = args.http or args.sse

    if not use_http and (args.host or args.port):
        parser.error(
            "Host and port arguments are only valid when using streamable HTTP or SSE transport (see: --http)."
        )
        sys.exit(1)

    if use_http:
        host = args.host if args.host else "127.0.0.1"
        if args.host and args.host not in ("127.0.0.1", "localhost"):
            print(
                "\n"
                "WARNING: The server is being bound to a non-localhost interface "
                f"({host}).\n"
                "This exposes the server to other machines on the network or Internet.\n"
                "The server has NO authentication and runs with your user's privileges.\n"
                "Any process or user that can reach this interface can read files and\n"
                "fetch network resources accessible to this user.\n"
                "Only proceed if you understand the security implications.\n",
                file=sys.stderr,
            )
        starlette_app = create_starlette_app(mcp, host=host, debug=True)
        uvicorn.run(
            starlette_app,
            host=host,
            port=args.port if args.port else 3001,
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
