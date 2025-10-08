import contextlib
import sys
import os
import base64
import uuid
import tempfile
import time
import asyncio
from pathlib import Path
from typing import Dict
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.responses import JSONResponse, FileResponse, Response
from starlette.routing import Mount, Route
from starlette.types import Receive, Scope, Send
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from markitdown import MarkItDown
import uvicorn

# Try importing OpenAI for LLM-based image descriptions
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Initialize FastMCP server for MarkItDown (SSE)
mcp = FastMCP("markitdown")

# Temporary file storage for uploads (file_id -> {path, expires_at, filename, accessed})
_temp_files: Dict[str, dict] = {}
_temp_dir = tempfile.mkdtemp(prefix="markitdown_")
_cleanup_task = None

# Server mode tracking
_server_mode = "stdio"  # "stdio" or "http"
_server_host = "127.0.0.1"
_server_port = 3001


@mcp.tool()
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    # Check if this is a request to our own temp endpoint to avoid deadlock
    # If it is, convert to file:// URI to read directly from disk
    if uri.startswith(("http://", "https://")):
        # Parse the URL to check if it's pointing to our temp endpoint
        try:
            from urllib.parse import urlparse
            parsed = urlparse(uri)

            # Check if this is our temp endpoint: /temp/{file_id}
            if parsed.path.startswith("/temp/"):
                file_id = parsed.path.split("/")[-1]

                # Check if this file exists in our temp storage
                if file_id in _temp_files:
                    # Convert to file:// URI to avoid HTTP request to ourselves (deadlock)
                    from pathlib import Path
                    file_path = Path(_temp_files[file_id]["path"])
                    uri = file_path.as_uri()
        except Exception:
            # If parsing fails, continue with original URI
            pass

    return create_markitdown().convert_uri(uri).markdown


@mcp.tool()
async def upload_file(content: str, filename: str = "") -> str:
    """
    FALLBACK METHOD: Upload file via MCP (uses tokens once for base64 content).

    ⚠️ Consider using get_upload_instructions() instead for ZERO-token uploads!
    That method tells the user to upload via curl directly, avoiding all token costs.

    Use this upload_file() tool ONLY when:
        - User cannot run curl/HTTP commands
        - Server is in STDIO mode (no HTTP endpoint)
        - Need programmatic upload through MCP

    Token cost: ~500K tokens for a 5MB file (sent once during upload)

    Args:
        content: Base64-encoded file content (max 10MB)
        filename: Optional filename for the upload

    Returns:
        A temporary file:// URL that can be used with convert_to_markdown()

    Workflow:
        1. You receive file from user and base64-encode it (USES TOKENS)
        2. Call upload_file() with base64 content
        3. Receive file:// URL
        4. Call convert_to_markdown(url) - only URL in context from this point

    Better alternative for HTTP mode:
        Call get_upload_instructions() and guide user to upload via curl.
        File never enters LLM context = TRUE zero tokens!

    Example:
        # Upload a file (base64 sent through context)
        url = await upload_file(base64_content, filename="report.pdf")
        # Returns: "file:///tmp/markitdown_xxx/550e8400-..."

        # Then convert using the URL
        markdown = await convert_to_markdown(url)
    """
    try:
        # Decode and validate
        decoded = base64.b64decode(content)

        # Check size (max 10MB)
        size_bytes = len(decoded)
        max_size = 10 * 1024 * 1024  # 10MB
        if size_bytes > max_size:
            raise ValueError(
                f"File too large ({size_bytes} bytes). Maximum size is {max_size} bytes (10MB)."
            )

        # Generate unique ID
        file_id = str(uuid.uuid4())

        # Save to temp directory
        file_path = os.path.join(_temp_dir, file_id)
        with open(file_path, "wb") as f:
            f.write(decoded)

        # Store metadata
        expires_in = 3600  # 1 hour
        _temp_files[file_id] = {
            "path": file_path,
            "filename": filename if filename else "uploaded_file",
            "expires_at": time.time() + expires_in,
            "accessed": False
        }

        # Return the URL
        # In STDIO mode, return a file:// URI since there's no HTTP server
        # In HTTP mode, return an HTTP URL to the temp endpoint
        # We detect mode by checking if we're running with uvicorn
        # For simplicity, we'll return a file:// URI that works in both modes
        # Use Path.as_uri() for proper cross-platform file:// URI formatting
        temp_url = Path(file_path).as_uri()

        return temp_url

    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Upload failed: {str(e)}")


@mcp.tool()
async def convert_file_to_markdown(
    content: str, filename: str = "", mimetype: str = ""
) -> str:
    """
    Convert a small file to markdown in one step (base64-encoded content).

    ⚠️ ONLY FOR SMALL FILES <1MB! For larger files:
        → HTTP mode: Use get_upload_instructions() for ZERO-token curl upload
        → STDIO mode: Use upload_file() for token-efficient two-step upload

    Token cost: ~500K tokens for a 5MB file (entire file in context)

    Use this tool ONLY for:
        - Small files (<1MB)
        - Quick one-off conversions where token cost is acceptable
        - When you need immediate single-step conversion

    Args:
        content: Base64-encoded file content (5MB hard limit, 1MB recommended)
        filename: Optional filename (for extension detection, e.g., "document.pdf")
        mimetype: Optional MIME type hint (e.g., "application/pdf", "image/png")

    Returns:
        The converted markdown text

    Better alternatives for large files:
        1. get_upload_instructions() → user uploads via curl → ZERO tokens
        2. upload_file() → returns URL → convert_to_markdown(url) → tokens used once

    Example:
        # Convert a small PDF file (entire file in context)
        content = base64.b64encode(pdf_bytes).decode('utf-8')
        markdown = await convert_file_to_markdown(content, filename="doc.pdf")
    """
    # Validate base64 content
    try:
        # Verify it's valid base64
        decoded = base64.b64decode(content)

        # Check size (max 1MB recommended, hard limit 5MB)
        size_bytes = len(decoded)
        max_size = 5 * 1024 * 1024  # 5MB hard limit
        recommended_size = 1 * 1024 * 1024  # 1MB recommended

        if size_bytes > max_size:
            raise ValueError(
                f"File too large ({size_bytes} bytes). Maximum size is {max_size} bytes (5MB). "
                f"For larger files, use the /upload endpoint (HTTP mode) or file:// URIs with volume mounts."
            )

        if size_bytes > recommended_size:
            import warnings
            warnings.warn(
                f"File size ({size_bytes} bytes) exceeds recommended limit ({recommended_size} bytes / 1MB). "
                f"This may consume significant tokens. Consider using /upload endpoint for better efficiency.",
                UserWarning
            )
    except ValueError:
        raise  # Re-raise ValueError from size check
    except Exception as e:
        raise ValueError(f"Invalid base64 content: {str(e)}")

    # Construct data URI
    # Format: data:[<mimetype>][;base64],<data>
    parts = []
    if mimetype:
        parts.append(mimetype)
    parts.append("base64")

    data_uri = f"data:{';'.join(parts)},{content}"

    # Use the existing convert_uri with the data URI
    # Pass filename as extension hint if provided
    md = create_markitdown()

    # Extract extension from filename if provided
    stream_info = None
    if filename:
        import os
        _, ext = os.path.splitext(filename)
        if ext:
            from markitdown import StreamInfo
            stream_info = StreamInfo(extension=ext, filename=filename)

    result = md.convert_uri(data_uri, stream_info=stream_info)
    return result.markdown


@mcp.tool()
async def get_upload_instructions() -> str:
    """
    🌟 PRIMARY METHOD for large files (>1MB) - Get instructions for ZERO-token file uploads.

    ⚠️ IMPORTANT: This tells the USER to upload files via curl/HTTP directly to the server.
    The /upload endpoint uses multipart/form-data (NOT base64, NOT through MCP).
    Files NEVER enter the LLM context - achieving true zero-token efficiency!

    When to use:
        - Server is running in HTTP mode
        - User has access to curl or similar HTTP client
        - Files are 1MB-10MB in size
        - Want absolute zero tokens used for file content

    Returns:
        Human-readable instructions for the user including:
        - curl command with the upload endpoint URL
        - Response format example
        - Next steps for using the returned URL

    Workflow:
        1. You call get_upload_instructions()
        2. You show the curl command to the USER
        3. USER runs curl (file uploaded directly to server, bypassing LLM)
        4. USER provides you the URL from the response
        5. You call convert_to_markdown(url) - only URL in context, ZERO file tokens!

    Note: This is different from upload_file() MCP tool which sends base64 through context.
    """
    global _server_mode, _server_host, _server_port

    if _server_mode == "http":
        upload_url = f"http://{_server_host}:{_server_port}/upload"

        instructions = f"""# 🌟 ZERO-TOKEN File Upload Instructions

⚠️ IMPORTANT: Upload files using curl/HTTP - NO BASE64 ENCODING NEEDED!
This is NOT the upload_file() MCP tool. This uploads directly to the HTTP server.

## Quick Start

**Run this command to upload your file:**
```bash
curl -X POST {upload_url} -F "file=@/path/to/your/file.pdf"
```

📌 Note: Use `-F "file=@..."` flag - this sends the file as multipart/form-data (NOT base64)

## What Happens Next

You'll get a JSON response:
```json
{{
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "http://{_server_host}:{_server_port}/temp/550e8400-...",
  "filename": "file.pdf",
  "size": 1048576,
  "expires_in": 3600
}}
```

**Then tell me:** "Convert <url> to markdown" (copy the URL from above)

## Why This Method?

✅ **ZERO tokens** - File content NEVER enters the LLM context
✅ **NO base64** - Direct binary upload via HTTP multipart/form-data
✅ **Larger files** - Up to 10MB (vs 1-5MB for base64 methods)
✅ **Faster** - No encoding/decoding overhead
✅ **Persistent** - URL valid for 1 hour

## Details

- Upload endpoint: {upload_url}
- Method: POST with multipart/form-data
- Field name: "file"
- Max size: 10MB
- Expiry: 1 hour or first access

## Can't use curl?

If you cannot run curl commands, use the upload_file() MCP tool instead.
Note: That method sends base64-encoded content through the LLM context (uses tokens once)."""

    else:  # STDIO mode
        instructions = """# Upload Instructions (STDIO Mode)

The server is running in STDIO mode (no HTTP endpoint available).

## Available options:

### Option 1: upload_file() tool (Recommended for 1-10MB files)
Use the `upload_file()` MCP tool to upload file content.
- File content sent through context once during upload
- Returns a file:// URL for conversion
- Max size: 10MB

### Option 2: convert_file_to_markdown() tool (For small files <1MB)
Direct one-step conversion for small files.
- Simple single-step process
- Max size: 5MB (1MB recommended)

### Option 3: Switch to HTTP mode for zero-token uploads
Restart the server with: markitdown-mcp --http --host 0.0.0.0 --port 3001
Then use curl to upload files without putting them in context!

## Recommendation:
For large files and token efficiency, consider running in HTTP mode to enable
direct file uploads that bypass the LLM context entirely."""

    return instructions


def check_plugins_enabled() -> bool:
    return os.getenv("MARKITDOWN_ENABLE_PLUGINS", "false").strip().lower() in (
        "true",
        "1",
        "yes",
    )


def create_markitdown() -> MarkItDown:
    """
    Create MarkItDown instance with optional LLM support for image descriptions.

    If OPENAI_API_KEY environment variable is set, enables LLM-based image descriptions.
    Otherwise, falls back to metadata-only extraction.

    Environment variables:
        OPENAI_API_KEY: OpenAI API key for image descriptions
        OPENAI_MODEL: Model to use (default: gpt-4o)
        MARKITDOWN_ENABLE_PLUGINS: Enable third-party plugins (default: false)

    Returns:
        Configured MarkItDown instance
    """
    enable_plugins = check_plugins_enabled()

    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and OPENAI_AVAILABLE:
        try:
            client = OpenAI(api_key=api_key)
            model = os.getenv("OPENAI_MODEL", "gpt-4o")
            return MarkItDown(
                enable_plugins=enable_plugins,
                llm_client=client,
                llm_model=model
            )
        except Exception as e:
            # Fall back to non-LLM version if OpenAI setup fails
            print(f"Warning: Failed to initialize OpenAI client: {e}", file=sys.stderr)
            print("Falling back to metadata-only image conversion", file=sys.stderr)

    return MarkItDown(enable_plugins=enable_plugins)


async def cleanup_temp_files():
    """Background task to cleanup expired temporary files."""
    while True:
        try:
            await asyncio.sleep(300)  # Run every 5 minutes
            current_time = time.time()
            expired_ids = []

            for file_id, info in _temp_files.items():
                if current_time > info["expires_at"] or info.get("accessed", False):
                    # Delete the file
                    try:
                        Path(info["path"]).unlink(missing_ok=True)
                    except Exception:
                        pass
                    expired_ids.append(file_id)

            # Remove from tracking
            for file_id in expired_ids:
                _temp_files.pop(file_id, None)

        except Exception:
            pass


async def handle_upload(request: Request) -> JSONResponse:
    """Handle file upload via multipart/form-data."""
    upload_file = None
    try:
        # Get the form data
        form = await request.form()

        # Get the uploaded file
        upload_file = form.get("file")
        if not upload_file or not hasattr(upload_file, "read"):
            return JSONResponse(
                {"error": "No file provided. Send file as multipart/form-data with field name 'file'."},
                status_code=400
            )

        # Read file content
        content = await upload_file.read()

        # Check size (max 10MB for uploads)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(content) > max_size:
            return JSONResponse(
                {"error": f"File too large. Maximum size is {max_size} bytes (10MB)."},
                status_code=413
            )

        # Generate unique ID
        file_id = str(uuid.uuid4())

        # Save to temp directory
        file_path = os.path.join(_temp_dir, file_id)
        with open(file_path, "wb") as f:
            f.write(content)

        # Store metadata
        expires_in = 3600  # 1 hour
        _temp_files[file_id] = {
            "path": file_path,
            "filename": getattr(upload_file, "filename", "uploaded_file"),
            "expires_at": time.time() + expires_in,
            "accessed": False
        }

        # Build the URL
        host = request.url.hostname or "localhost"
        port = request.url.port or 3001
        scheme = request.url.scheme or "http"
        temp_url = f"{scheme}://{host}:{port}/temp/{file_id}"

        return JSONResponse({
            "file_id": file_id,
            "url": temp_url,
            "filename": _temp_files[file_id]["filename"],
            "size": len(content),
            "expires_in": expires_in
        })

    except Exception as e:
        return JSONResponse(
            {"error": f"Upload failed: {str(e)}"},
            status_code=500
        )
    finally:
        # Ensure upload file handle is closed to prevent server hanging
        if upload_file and hasattr(upload_file, "close"):
            await upload_file.close()


async def handle_temp_file(request: Request) -> Response:
    """Serve a temporary uploaded file."""
    file_id = request.path_params.get("file_id")

    if not file_id or file_id not in _temp_files:
        return JSONResponse(
            {"error": "File not found or expired."},
            status_code=404
        )

    info = _temp_files[file_id]

    # Check if expired
    if time.time() > info["expires_at"]:
        # Cleanup
        try:
            Path(info["path"]).unlink(missing_ok=True)
        except Exception:
            pass
        _temp_files.pop(file_id, None)
        return JSONResponse(
            {"error": "File expired."},
            status_code=404
        )

    # Mark as accessed (will be cleaned up on next cleanup cycle)
    info["accessed"] = True

    # Serve the file
    return FileResponse(
        info["path"],
        filename=info["filename"],
        media_type="application/octet-stream"
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
        """Context manager for session manager and cleanup task."""
        global _cleanup_task

        # Start cleanup task
        _cleanup_task = asyncio.create_task(cleanup_temp_files())

        async with session_manager.run():
            print("Application started with StreamableHTTP session manager!")
            print(f"Temporary files directory: {_temp_dir}")
            print("Upload endpoint available at: /upload")
            try:
                yield
            finally:
                print("Application shutting down...")

                # Cancel cleanup task
                if _cleanup_task:
                    _cleanup_task.cancel()
                    try:
                        await _cleanup_task
                    except asyncio.CancelledError:
                        pass

                # Cleanup all temp files
                for info in _temp_files.values():
                    try:
                        Path(info["path"]).unlink(missing_ok=True)
                    except Exception:
                        pass

                # Remove temp directory
                try:
                    Path(_temp_dir).rmdir()
                except Exception:
                    pass

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/mcp", app=handle_streamable_http),
            Mount("/messages/", app=sse.handle_post_message),
            Route("/upload", endpoint=handle_upload, methods=["POST"]),
            Route("/temp/{file_id}", endpoint=handle_temp_file, methods=["GET"]),
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

    # Set global server mode and connection info
    global _server_mode, _server_host, _server_port

    if use_http:
        _server_mode = "http"
        _server_host = args.host if args.host else "127.0.0.1"
        _server_port = args.port if args.port else 3001

        print(f"Starting server in HTTP mode at http://{_server_host}:{_server_port}")
        print(f"Upload endpoint: http://{_server_host}:{_server_port}/upload")
        print("Use get_upload_instructions() MCP tool for zero-token file uploads!")

        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=_server_host,
            port=_server_port,
        )
    else:
        _server_mode = "stdio"
        print("Starting server in STDIO mode")
        print("For zero-token uploads, consider running with --http flag")
        mcp.run()


if __name__ == "__main__":
    main()
