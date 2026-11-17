import os

# numpy (pulled in by markitdown's converters) ships OpenBLAS, which on import
# commits a work buffer per CPU core (~30MB each: 360MB+ on a 12-core machine)
# and keeps idle worker threads. MarkItDown does no heavy linear algebra, and a
# server process runs per MCP client session, so cap the pools before anything
# can import numpy. Explicit settings in the environment still win.
for _var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_var, "1")

import contextlib
import logging
import sys
import threading
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any
import anyio
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from starlette.applications import Starlette
import requests
import uvicorn

if TYPE_CHECKING:
    from markitdown import MarkItDown as _MarkItDown

logger = logging.getLogger(__name__)

# Initialize the MCP server for MarkItDown
mcp = MCPServer("markitdown")

# markitdown imports its whole converter stack (numpy, pandas, onnxruntime,
# pdfminer, ...) eagerly. Defer it to the first conversion so sessions that
# never convert anything stay small and the MCP handshake is fast.
MarkItDown: "type[_MarkItDown] | None" = None

# One MarkItDown instance is shared, and only one conversion runs on it at a
# time: converters keep per-call state on the instance (RssConverter sets
# self._kwargs), and plugins may too. This also bounds CPU and peak memory.
_conversion_lock = threading.Lock()
_converter: "_MarkItDown | None" = None
_converter_key: tuple[object, bool] | None = None

# (connect, read) seconds. Without a timeout a hung server would hold the
# conversion lock, and with it every later conversion, forever.
FETCH_TIMEOUT = (10, 60)


class _TimeoutSession(requests.Session):
    """A requests session that applies FETCH_TIMEOUT unless a call sets one."""

    def __init__(self) -> None:
        super().__init__()
        # The header MarkItDown sets on the session it creates by default.
        self.headers.update(
            {"Accept": "text/markdown, text/html;q=0.9, text/plain;q=0.8, */*;q=0.1"}
        )

    def request(self, *args: Any, **kwargs: Any) -> requests.Response:  # type: ignore[override]
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = FETCH_TIMEOUT
        return super().request(*args, **kwargs)


def _get_converter() -> "_MarkItDown":
    """Return the shared MarkItDown instance. Call with _conversion_lock held.

    Construction registers every converter and loads Magika's ONNX model with
    its own thread pool, so building one per call costs ~0.25s and leaks memory.
    """
    global MarkItDown, _converter, _converter_key
    if MarkItDown is None:
        from markitdown import MarkItDown as _loaded

        MarkItDown = _loaded
    # Keyed on the class too, so a substituted MarkItDown takes effect.
    key = (MarkItDown, check_plugins_enabled())
    if _converter is None or _converter_key != key:
        _converter = MarkItDown(
            enable_plugins=key[1], requests_session=_TimeoutSession()
        )
        _converter_key = key
    return _converter


@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    # Conversion is blocking and CPU-bound: keep it off the event loop so the
    # server keeps serving pings, cancellations and other clients meanwhile.
    return await anyio.to_thread.run_sync(_convert_to_markdown, uri)


def _convert_to_markdown(uri: str) -> str:
    from markitdown import FileConversionException, UnsupportedFormatException

    try:
        with _conversion_lock:
            return _get_converter().convert_uri(uri).markdown

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
        starlette_app = create_starlette_app(mcp, host=host)
        uvicorn.run(
            starlette_app,
            host=host,
            port=args.port if args.port else 3001,
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
