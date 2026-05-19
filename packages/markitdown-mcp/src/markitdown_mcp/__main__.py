import contextlib
import sys
import os
import re
from pathlib import Path
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import List, Optional
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


@dataclass
class SecurityConfig:
    """Security configuration for MCP server."""
    api_key: Optional[str] = None
    allowed_paths: Optional[List[Path]] = None
    allowed_schemes: List[str] = None
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allow_symlinks: bool = False

    def __post_init__(self):
        if self.allowed_schemes is None:
            self.allowed_schemes = ["file", "http", "https", "data"]


def _load_security_config() -> SecurityConfig:
    """Load security configuration from environment variables."""
    # API Key authentication
    api_key = os.getenv("MARKITDOWN_MCP_API_KEY") or None

    # Allowed paths (colon-separated on Unix, semicolon on Windows)
    allowed_paths_str = os.getenv("MARKITDOWN_MCP_ALLOWED_PATHS")
    allowed_paths = None
    if allowed_paths_str:
        separator = ";" if os.name == "nt" else ":"
        allowed_paths = [Path(p.strip()).resolve() for p in allowed_paths_str.split(separator) if p.strip()]

    # Allowed URI schemes
    allowed_schemes_str = os.getenv("MARKITDOWN_MCP_ALLOWED_SCHEMES")
    allowed_schemes = None
    if allowed_schemes_str:
        allowed_schemes = [s.strip().lower() for s in allowed_schemes_str.split(",")]

    # Max file size
    max_file_size_str = os.getenv("MARKITDOWN_MCP_MAX_FILE_SIZE")
    max_file_size = 50 * 1024 * 1024
    if max_file_size_str:
        try:
            max_file_size = int(max_file_size_str)
        except ValueError:
            pass

    # Allow symlinks
    allow_symlinks = os.getenv("MARKITDOWN_MCP_ALLOW_SYMLINKS", "false").strip().lower() in (
        "true", "1", "yes"
    )

    return SecurityConfig(
        api_key=api_key,
        allowed_paths=allowed_paths,
        allowed_schemes=allowed_schemes,
        max_file_size=max_file_size,
        allow_symlinks=allow_symlinks,
    )


def _validate_uri(uri: str, config: SecurityConfig) -> str:
    """Validate URI against security policy. Returns normalized path or raises ValueError."""
    from urllib.parse import urlparse, unquote

    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()

    # Check allowed schemes
    if scheme not in config.allowed_schemes:
        raise ValueError(
            f"URI scheme '{scheme}' not allowed. Allowed schemes: {', '.join(config.allowed_schemes)}"
        )

    # Validate file URIs
    if scheme == "file":
        file_path = unquote(parsed.path)
        # Handle cases where Windows drive letter ended up in netloc
        if not file_path and parsed.netloc:
            file_path = "/" + parsed.netloc
        elif not file_path.startswith("/") and parsed.netloc:
            file_path = "/" + parsed.netloc + file_path
        # Handle Windows file URIs: file:///C:/path...
        if file_path.startswith("/") and re.match(r"^/[A-Za-z]:/", file_path):
            file_path = file_path[1:]
        elif file_path.startswith("//"):
            # UNC path handling
            pass

        # R13: reject empty / whitespace-only paths before any disk IO
        if not file_path or not file_path.strip() or file_path.strip() == "/":
            raise ValueError(f"Empty or invalid file URI: {uri!r}")

        # Check path traversal BEFORE resolve() normalizes it away.
        # R13: also detect overlong dots ("..." / "...." / etc.) — some
        # path normalizers collapse these to ".." and escape sandboxes.
        parts = Path(file_path).parts
        if ".." in parts:
            raise ValueError(f"Path traversal detected: {file_path}")
        for seg in parts:
            # Pure-dot segments longer than 2 chars are never legitimate
            # (e.g. "...", "....", "....."). Block them as a CVE-style
            # traversal smuggling vector.
            if len(seg) >= 3 and set(seg) == {"."}:
                raise ValueError(
                    f"Overlong dot traversal detected in segment {seg!r}: {file_path}"
                )

        path = Path(file_path).resolve()

        # Check symlinks
        if not config.allow_symlinks and os.path.islink(file_path):
            raise ValueError(f"Symlinks not allowed: {file_path}")

        # Check allowed paths whitelist
        if config.allowed_paths is not None:
            allowed = any(path.is_relative_to(allowed) for allowed in config.allowed_paths)
            if not allowed:
                raise ValueError(
                    f"Path not in allowed list: {file_path}. "
                    f"Allowed paths: {[str(p) for p in config.allowed_paths]}"
                )

        # Check file size
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            if file_size > config.max_file_size:
                raise ValueError(
                    f"File too large: {file_path} ({file_size} bytes). "
                    f"Max allowed: {config.max_file_size} bytes ({config.max_file_size / 1024 / 1024:.1f}MB)"
                )

        return path.as_uri()

    # For http/https/data: return as-is, size checked during fetch
    return uri


# Global security config
_SECURITY_CONFIG = _load_security_config()

# Initialize FastMCP server for MarkItDown (SSE)
mcp = FastMCP("markitdown")


@mcp.tool()
async def convert_to_markdown(uri: str, api_key: str = "") -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown.

    Args:
        uri: The URI to convert (file:/http:/https:/data:)
        api_key: Optional API key for authenticated servers. Configure via MARKITDOWN_MCP_API_KEY env var.
    """
    # API Key validation
    if _SECURITY_CONFIG.api_key and api_key != _SECURITY_CONFIG.api_key:
        raise ValueError("Invalid API key. Configure via MARKITDOWN_MCP_API_KEY environment variable.")

    # Validate URI before conversion
    normalized_uri = _validate_uri(uri, _SECURITY_CONFIG)
    return MarkItDown(enable_plugins=check_plugins_enabled()).convert_uri(normalized_uri).markdown


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
    parser.add_argument(
        "--show-security-config",
        action="store_true",
        help="Show current security configuration and exit",
    )
    args = parser.parse_args()

    # Show security config and exit if requested
    if args.show_security_config:
        print("=== MarkItDown MCP Security Configuration ===")
        print(f"API Key required: {'YES' if _SECURITY_CONFIG.api_key else 'NO (not recommended)'}")
        print(f"Allowed schemes: {', '.join(_SECURITY_CONFIG.allowed_schemes)}")
        print(f"Max file size: {_SECURITY_CONFIG.max_file_size} bytes ({_SECURITY_CONFIG.max_file_size / 1024 / 1024:.1f} MB)")
        print(f"Symlinks allowed: {'YES' if _SECURITY_CONFIG.allow_symlinks else 'NO (recommended)'}")
        if _SECURITY_CONFIG.allowed_paths:
            print(f"Allowed paths (whitelist):")
            for p in _SECURITY_CONFIG.allowed_paths:
                print(f"  - {p}")
        else:
            print("Allowed paths: ALL (not recommended - set MARKITDOWN_MCP_ALLOWED_PATHS)")
        print("=" * 50)
        print("\nConfigure via environment variables:")
        print("  MARKITDOWN_MCP_API_KEY          - Require API key for all requests")
        print("  MARKITDOWN_MCP_ALLOWED_PATHS    - Path whitelist (; separated on Windows, : on Unix)")
        print("  MARKITDOWN_MCP_ALLOWED_SCHEMES  - URI scheme whitelist (comma separated)")
        print("  MARKITDOWN_MCP_MAX_FILE_SIZE    - Max file size in bytes (default: 52428800 = 50MB)")
        print("  MARKITDOWN_MCP_ALLOW_SYMLINKS   - Allow symbolic links (default: false)")
        sys.exit(0)

    use_http = args.http or args.sse

    if not use_http and (args.host or args.port):
        parser.error(
            "Host and port arguments are only valid when using streamable HTTP or SSE transport (see: --http)."
        )
        sys.exit(1)

    # Security warnings
    has_warnings = False
    if not _SECURITY_CONFIG.api_key:
        print(
            "\n"
            "⚠️  SECURITY WARNING: No API key configured.\n"
            "  Any process/user that can reach this server can execute conversions.\n"
            "  Recommendation: Set MARKITDOWN_MCP_API_KEY environment variable.\n",
            file=sys.stderr,
        )
        has_warnings = True

    if _SECURITY_CONFIG.allowed_paths is None:
        print(
            "\n"
            "⚠️  SECURITY WARNING: No path whitelist configured.\n"
            "  The server can read ANY file accessible to your user account.\n"
            "  Recommendation: Set MARKITDOWN_MCP_ALLOWED_PATHS to restrict accessible directories.\n",
            file=sys.stderr,
        )
        has_warnings = True

    if has_warnings:
        print("-" * 60, file=sys.stderr)
        print(
            "To see full security configuration: markitdown-mcp --show-security-config\n",
            file=sys.stderr,
        )

    if use_http:
        host = args.host if args.host else "127.0.0.1"
        if args.host and args.host not in ("127.0.0.1", "localhost"):
            print(
                "\n"
                "🚨 CRITICAL SECURITY WARNING: The server is being bound to a non-localhost interface "
                f"({host}).\n"
                "This exposes the server to other machines on the network or Internet.\n"
                "Without an API key and path whitelist, this is EXTREMELY DANGEROUS.\n"
                "Any machine that can reach this interface can read ALL your files.\n"
                "Only proceed if you understand the security implications AND have configured:\n"
                "  1. MARKITDOWN_MCP_API_KEY (required)\n"
                "  2. MARKITDOWN_MCP_ALLOWED_PATHS (strongly recommended)\n",
                file=sys.stderr,
            )
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=host,
            port=args.port if args.port else 3001,
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
