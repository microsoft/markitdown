import contextlib
import sys
from collections.abc import AsyncIterator
from mcp.server.mcpserver import MCPServer
from starlette.applications import Starlette
from markitdown import MarkItDown
import uvicorn

# Initialize the MCP server for MarkItDown
mcp = MCPServer("markitdown")


@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    return MarkItDown().convert_uri(uri).markdown


def create_starlette_app(mcp_server: MCPServer, *, debug: bool = False) -> Starlette:
    # Two sub-apps supply the routes: /sse + /messages/ from the SSE transport,
    # and /mcp from Streamable HTTP. Their routes are merged into one app so the
    # published URL surface is unchanged.
    sse_app = mcp_server.sse_app()
    http_app = mcp_server.streamable_http_app(
        json_response=True,
        stateless_http=True,
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
        starlette_app = create_starlette_app(mcp, debug=True)
        uvicorn.run(
            starlette_app,
            host=args.host if args.host else "127.0.0.1",
            port=args.port if args.port else 3001,
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
