import contextlib
import logging
import ntpath
import os
import sys
from pathlib import Path
from collections.abc import AsyncIterator, Iterator
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from starlette.applications import Starlette
from markitdown import MarkItDown, FileConversionException, UnsupportedFormatException
import requests
import uvicorn

logger = logging.getLogger(__name__)

# Initialize the MCP server for MarkItDown
mcp = MCPServer("markitdown")


@contextlib.contextmanager
def _tool_errors() -> Iterator[None]:
    """Translate conversion failures into ToolErrors the client may see."""
    try:
        yield

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
        # URI and path validation failures, which only restate the URI or
        # path the client supplied.
        raise ToolError(str(exc)) from exc


def _is_unc_or_device_path(path: str) -> bool:
    """Recognize Windows UNC and device namespace prefixes on any platform."""
    drive, _ = ntpath.splitdrive(path)
    return drive.replace("\\", "/").startswith("//")


def _resolve_local_path(path: str) -> Path:
    """Resolve a client-supplied filesystem path, rejecting UNC and device paths.

    The check runs before resolution, since resolving a UNC path already opens
    a connection to the remote host, and again after it, to catch relative
    paths below a UNC working directory.
    """
    expanded = os.path.expanduser(path)
    if _is_unc_or_device_path(expanded):
        raise ValueError(
            f"Unsupported path: {path}. UNC and Windows device paths are not supported."
        )
    resolved = Path(expanded).resolve(strict=True)
    if _is_unc_or_device_path(str(resolved)):
        raise ValueError(
            f"Unsupported path: {path}. UNC and Windows device paths are not supported."
        )
    return resolved


@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    converter = MarkItDown(enable_plugins=check_plugins_enabled())
    with _tool_errors():
        return converter.convert_uri(uri).markdown


@mcp.tool()
async def convert_file(file_path: str) -> str:
    """Convert a local file (given as an absolute or relative filesystem path) to markdown.

    This is a convenience wrapper around ``convert_to_markdown`` for callers that already
    have a plain path rather than a ``file:`` URI. Paths are resolved against the current
    working directory. UNC and Windows device paths are rejected.
    """
    converter = MarkItDown(enable_plugins=check_plugins_enabled())
    with _tool_errors():
        resolved = _resolve_local_path(file_path)
        return converter.convert_local(str(resolved)).markdown


@mcp.tool()
async def convert_directory(dir_path: str, recursive: bool = True) -> dict[str, str]:
    """Convert every file in a directory to markdown.

    Returns a mapping of ``relative_path`` to converted markdown. Unreadable or
    unsupported files are skipped silently so a single bad file does not abort
    the batch; their paths simply don't appear in the result dictionary.
    ``recursive=True`` descends into sub-directories, ``False`` processes only
    the immediate directory. UNC and Windows device paths are rejected.
    """
    with _tool_errors():
        base = _resolve_local_path(dir_path)
        if not base.is_dir():
            raise ValueError(f"Not a directory: {dir_path}")

    md = MarkItDown(enable_plugins=check_plugins_enabled())
    files = base.rglob("*") if recursive else base.iterdir()

    result: dict[str, str] = {}
    for path in files:
        if not path.is_file():
            continue
        try:
            result[str(path.relative_to(base))] = md.convert_local(str(path)).markdown
        except Exception:
            # Best-effort batch: skip files that fail individually.
            continue
    return result


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
