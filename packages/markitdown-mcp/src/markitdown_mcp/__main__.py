import contextlib
import sys
import os
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.types import Receive, Scope, Send
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from markitdown import MarkItDown
import uvicorn
from pathlib import Path
from typing import Optional, Dict, Any
import json

# Initialize FastMCP server for MarkItDown (SSE)
mcp = FastMCP("markitdown")


@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    return MarkItDown(enable_plugins=check_plugins_enabled()).convert_uri(uri).markdown


@mcp.tool()
async def convert_and_save(
    uri: str,
    output_path: str,
    return_content: bool = False
) -> Dict[str, Any]:
    """Convert a resource to markdown and save to file, optionally returning content
    
    Args:
        uri: URI to convert (http, https, file, or data URI)
        output_path: Path where to save the markdown file
        return_content: Whether to return the markdown content (default: False)
        
    Returns:
        Dictionary with conversion metadata including success status, file path, and size
    """
    try:
        # Convert the document
        markitdown = MarkItDown(enable_plugins=check_plugins_enabled())
        result = markitdown.convert_uri(uri)
        
        # Ensure output directory exists
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        
        # Get file size
        file_size = output_path.stat().st_size
        
        # Prepare response
        response = {
            "success": True,
            "saved_to": str(output_path.resolve()),
            "size": file_size,
            "title": result.title if result.title else None,
        }
        
        # Optionally include content
        if return_content:
            response["content"] = result.markdown
            
        return response
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "saved_to": None,
            "size": 0,
            "title": None,
        }


@mcp.tool()
async def convert_to_markdown_with_options(
    uri: str,
    return_content: bool = True,
    save_to: Optional[str] = None
) -> Dict[str, Any]:
    """Convert a resource to markdown with flexible output options
    
    Args:
        uri: URI to convert (http, https, file, or data URI)
        return_content: Whether to return the markdown content (default: True)
        save_to: Optional path to save the markdown file
        
    Returns:
        Dictionary with conversion results and metadata
    """
    try:
        # Convert the document
        markitdown = MarkItDown(enable_plugins=check_plugins_enabled())
        result = markitdown.convert_uri(uri)
        
        # Prepare base response
        response = {
            "success": True,
            "title": result.title if result.title else None,
        }
        
        # Handle file saving
        if save_to:
            output_path = Path(save_to)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.markdown)
            
            response["saved_to"] = str(output_path.resolve())
            response["size"] = output_path.stat().st_size
        else:
            response["saved_to"] = None
            response["size"] = len(result.markdown.encode('utf-8'))
            
        # Optionally include content
        if return_content:
            response["content"] = result.markdown
            
        return response
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "content": None if return_content else None,
            "saved_to": None,
            "size": 0,
            "title": None,
        }


def check_plugins_enabled() -> bool:
    return os.getenv("MARKITDOWN_ENABLE_PLUGINS", "false").strip().lower() in (
        "true",
        "1",
        "yes",
    )


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    sse = SseServerTransport("/messages/")
    session_manager = StreamableHTTPSessionManager(
        app=mcp_server,
        event_store=None,
        json_response=True,
        stateless=True,
    )

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Context manager for session manager."""
        async with session_manager.run():
            print("Application started with StreamableHTTP session manager!")
            try:
                yield
            finally:
                print("Application shutting down...")

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/mcp", app=handle_streamable_http),
            Mount("/messages/", app=sse.handle_post_message),
        ],
        lifespan=lifespan,
    )


# Main entry point
def main():
    import argparse

    mcp_server = mcp._mcp_server

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
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=args.host if args.host else "127.0.0.1",
            port=args.port if args.port else 3001,
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
