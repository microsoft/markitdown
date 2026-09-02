import base64
import contextlib
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
from collections.abc import AsyncIterator
from pathlib import Path

import uvicorn
from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.types import Receive, Scope, Send

from markitdown import MarkItDown


# ---------------------------------------------------------------------------
# Temporary directory management (module-level)
# ---------------------------------------------------------------------------

_temp_root: str = os.path.realpath(tempfile.mkdtemp(prefix="markitdown_mcp_"))

# Image file extensions we recognise when scanning output directories
_IMAGE_EXTENSIONS = frozenset(
    {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".tif", ".svg", ".ico"}
)


def _cleanup_old_dirs(root: str, max_age_seconds: int = 86400) -> None:
    """Remove sub-directories under *root* that are older than *max_age_seconds*."""
    now = time.time()
    try:
        for entry in os.scandir(root):
            if entry.is_dir():
                try:
                    if now - entry.stat().st_mtime > max_age_seconds:
                        shutil.rmtree(entry.path, ignore_errors=True)
                except OSError:
                    pass
    except FileNotFoundError:
        pass


def _cleanup_all(root: str) -> None:
    """Remove the entire *root* directory tree."""
    shutil.rmtree(root, ignore_errors=True)


def _new_doc_image_dir(path: str) -> str:
    """Create and return a per-document image output directory."""
    doc_hash = hashlib.sha256(path.encode("utf-8", errors="replace")).hexdigest()[:16]
    image_dir = os.path.join(_temp_root, doc_hash, "images")
    os.makedirs(image_dir, exist_ok=True)
    return image_dir


# ---------------------------------------------------------------------------
# LLM client configuration (optional — for fully automatic OCR mode)
# ---------------------------------------------------------------------------

def _create_llm_client():
    """Create an OpenAI-compatible client from environment variables.

    Returns (client, model) tuple, or (None, None) if not configured.
    Environment variables:
        MARKITDOWN_LLM_API_KEY   — required to enable LLM mode
        MARKITDOWN_LLM_BASE_URL  — optional, defaults to OpenAI
        MARKITDOWN_LLM_MODEL     — optional, defaults to gpt-4o-mini
    """
    api_key = os.getenv("MARKITDOWN_LLM_API_KEY", "").strip()
    if not api_key:
        return None, None

    try:
        from openai import OpenAI
    except ImportError:
        print(
            "WARNING: MARKITDOWN_LLM_API_KEY is set but 'openai' package is not installed. "
            "Install with: pip install openai",
            file=sys.stderr,
        )
        return None, None

    base_url = os.getenv("MARKITDOWN_LLM_BASE_URL", "").strip() or None
    model = os.getenv("MARKITDOWN_LLM_MODEL", "gpt-4o-mini").strip()

    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url

    client = OpenAI(**kwargs)
    print(f"LLM vision enabled: model={model}" + (f", base_url={base_url}" if base_url else ""), file=sys.stderr)
    return client, model


def _get_llm_prompt() -> str | None:
    """Return custom LLM prompt from env, or None for default."""
    prompt = os.getenv("MARKITDOWN_LLM_PROMPT", "").strip()
    return prompt or None


# ---------------------------------------------------------------------------
# MarkItDown factory
# ---------------------------------------------------------------------------

def _make_markitdown(*, extract_only: bool = False, image_output_dir: str | None = None) -> MarkItDown:
    """Create a MarkItDown instance with plugin and optional LLM support."""
    kwargs: dict = {
        "enable_plugins": check_plugins_enabled(),
    }
    if extract_only:
        kwargs["extract_only"] = True
    if image_output_dir:
        kwargs["image_output_dir"] = image_output_dir

    # Inject LLM client if configured (for automatic OCR / image description)
    llm_client, llm_model = _create_llm_client()
    if llm_client:
        kwargs["llm_client"] = llm_client
        kwargs["llm_model"] = llm_model
        prompt = _get_llm_prompt()
        if prompt:
            kwargs["llm_prompt"] = prompt

    return MarkItDown(**kwargs)


# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------

mcp = FastMCP("markitdown")


@mcp.tool()
async def convert_to_markdown(uri: str, extract_images: bool = False) -> str:
    """Convert a document or URI resource to markdown.

    Args:
        uri: An http:, https:, file: or data: URI pointing to the resource.
             Local file paths are also accepted and will be converted to file: URIs.
        extract_images: If True, extract embedded images to disk and replace
            references with absolute file paths. Default False (original behavior).

    Returns:
        The markdown representation of the document. When extract_images=True,
        image references point to extracted files on disk that can be read directly.
    """
    # Normalise bare file paths to file: URIs
    if not re.match(r"^(https?|file|data):", uri):
        abs_path = os.path.abspath(uri)
        if os.path.exists(abs_path):
            uri = Path(abs_path).as_uri()

    if extract_images:
        image_dir = _new_doc_image_dir(uri)
        md = _make_markitdown(image_output_dir=image_dir)
        result = md.convert_uri(uri)
        text = result.markdown or ""
        # Rewrite relative image references to absolute disk paths
        text = _resolve_image_refs(text, image_dir)
        return text
    else:
        md = _make_markitdown()
        return md.convert_uri(uri).markdown


@mcp.tool()
async def analyze_document(path: str) -> str:
    """Analyze a document and extract its text skeleton together with embedded images.

    This is the primary tool for AI-assistant-driven document processing.
    It extracts the document structure (text skeleton) and all embedded images
    to disk, so the AI assistant can read each image with its own vision capability
    to perform OCR, chart understanding, or semantic analysis.

    Accepts a local file path or a URI (http:, https:, file:, data:).

    Returns a JSON string containing:
      - text_skeleton: the markdown text with image references (absolute paths on disk)
      - images: a list of extracted images, each with:
          path: absolute file path on disk (readable by AI assistant)
          uri: file:// URI for the image
          position: surrounding context showing where the image appears
          size_bytes: file size
          width, height: pixel dimensions
      - metadata: source path, image count, and ocr_mode indicator

    Workflow for AI assistants:
      1. Call analyze_document to get text + image list
      2. Use your vision capability to read each image path for OCR/understanding
      3. Insert the extracted text back into the text_skeleton at the image positions
    """
    # ---- validate input ------------------------------------------------
    is_uri = re.match(r"^(https?|file|data):", path) is not None
    if not is_uri and not os.path.exists(path):
        return json.dumps({"error": f"File not found: {path}"})

    # ---- prepare per-document temp directory ----------------------------
    image_dir = _new_doc_image_dir(path)

    # ---- run conversion -------------------------------------------------
    try:
        md_instance = _make_markitdown(extract_only=True, image_output_dir=image_dir)
        result = md_instance.convert(path)
        text_skeleton: str = result.markdown or ""
    except Exception as exc:
        return json.dumps({"error": f"Conversion failed: {exc}"})

    # ---- resolve image references to absolute paths ---------------------
    text_skeleton = _resolve_image_refs(text_skeleton, image_dir)

    # ---- collect image files on disk ------------------------------------
    image_files: list[str] = []
    for fname in sorted(os.listdir(image_dir)):
        ext = os.path.splitext(fname)[1].lower()
        if ext in _IMAGE_EXTENSIONS:
            image_files.append(os.path.join(image_dir, fname))

    # ---- parse image references from text skeleton ----------------------
    img_ref_pattern = re.compile(
        r"(?:<!--\s*image:\s*(?P<meta>[^>]*?)\s*-->\s*\n?)?"
        r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)"
    )

    images_out: list[dict] = []
    for match in img_ref_pattern.finditer(text_skeleton):
        src = match.group("src")
        meta_str = match.group("meta") or ""

        # Resolve to absolute path
        if os.path.isabs(src):
            img_path = src
        else:
            base_dir = os.path.dirname(path) if not is_uri else ""
            img_path = os.path.normpath(os.path.join(base_dir, src))

        images_out.append(_build_image_info(img_path, meta_str, text_skeleton, match))

    # Account for unreferenced images
    referenced_paths = {img["path"] for img in images_out}
    for fpath in image_files:
        if fpath not in referenced_paths:
            images_out.append(
                _build_image_info(fpath, "", text_skeleton, None, position="[unreferenced image]")
            )

    # ---- determine OCR mode ---------------------------------------------
    llm_client, _ = _create_llm_client()
    ocr_mode = "llm_vision" if llm_client else "ai_assistant_driven"

    # ---- build response -------------------------------------------------
    response = {
        "text_skeleton": text_skeleton,
        "images": images_out,
        "metadata": {
            "source": path,
            "image_count": len(images_out),
            "ocr_mode": ocr_mode,
        },
    }
    return json.dumps(response, ensure_ascii=False)


@mcp.tool()
async def ocr_image(path: str, prompt: str = "") -> str:
    """Extract text content from an image file.

    Args:
        path: Local file path to the image (png, jpg, pdf, etc.)
        prompt: Optional custom prompt for OCR extraction.
            Default: "Extract all text from this image, maintaining layout and order."

    Returns:
        JSON string with extracted text and image metadata.
        If LLM is configured, uses vision model for automatic OCR.
        Otherwise, returns the image path and metadata for the AI assistant
        to read directly with its own vision capability.
    """
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        return json.dumps({"error": f"File not found: {abs_path}"})

    # Basic image metadata
    info: dict = {"path": abs_path, "uri": Path(abs_path).as_uri()}

    try:
        from PIL import Image as PILImage
        with PILImage.open(abs_path) as img:
            info["width"], info["height"] = img.size
            info["format"] = img.format
    except Exception:
        pass

    try:
        info["size_bytes"] = os.path.getsize(abs_path)
    except OSError:
        pass

    # Try LLM-based OCR if configured
    llm_client, llm_model = _create_llm_client()
    if llm_client:
        try:
            ocr_prompt = prompt or (
                "Extract all text from this image. Return ONLY the extracted text, "
                "maintaining the original layout and order. Do not add any commentary."
            )
            text = _llm_vision_extract(llm_client, llm_model, abs_path, ocr_prompt)
            info["text"] = text
            info["ocr_mode"] = "llm_vision"
            return json.dumps(info, ensure_ascii=False)
        except Exception as exc:
            info["error"] = str(exc)

    # No LLM — return metadata for AI assistant to process
    info["text"] = None
    info["ocr_mode"] = "ai_assistant_driven"
    info["hint"] = (
        "No LLM configured. Use your vision capability to read this image directly: "
        f"Read tool with path={abs_path}"
    )
    return json.dumps(info, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _resolve_image_refs(text: str, image_dir: str) -> str:
    """Rewrite relative image references in markdown to absolute paths on disk."""
    def _replace(match: re.Match) -> str:
        alt = match.group("alt")
        src = match.group("src")
        if os.path.isabs(src) or src.startswith(("http:", "https:", "data:")):
            return match.group(0)
        # Resolve relative path against image_dir
        abs_src = os.path.normpath(os.path.join(image_dir, src))
        return f"![{alt}]({abs_src})"

    return re.sub(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)", _replace, text)


def _build_image_info(
    img_path: str,
    meta_str: str,
    text_skeleton: str,
    match: re.Match | None,
    position: str | None = None,
) -> dict:
    """Build an image info dict for the response."""
    size_bytes: int | None = None
    try:
        size_bytes = os.path.getsize(img_path)
    except OSError:
        pass

    width: int | None = None
    height: int | None = None

    # Try metadata comment first (e.g. "1920x1080, 239KB")
    dim_match = re.search(r"(\d+)\s*x\s*(\d+)", meta_str) if meta_str else None
    if dim_match:
        width, height = int(dim_match.group(1)), int(dim_match.group(2))
    else:
        try:
            from PIL import Image as PILImage
            with PILImage.open(img_path) as img:
                width, height = img.size
        except Exception:
            pass

    # Build position context
    if position is None and match is not None:
        start = max(0, match.start() - 60)
        end = min(len(text_skeleton), match.end() + 60)
        ctx_before = text_skeleton[start:match.start()].strip().split("\n")[-1]
        ctx_after = text_skeleton[match.end():end].strip().split("\n")[0]
        parts: list[str] = []
        if ctx_before:
            parts.append(f"...{ctx_before}")
        parts.append("[image]")
        if ctx_after:
            parts.append(f"{ctx_after}...")
        position = " ".join(parts)

    return {
        "path": img_path,
        "uri": Path(img_path).as_uri() if os.path.exists(img_path) else None,
        "position": position or "",
        "size_bytes": size_bytes,
        "width": width,
        "height": height,
    }


def _llm_vision_extract(client, model: str, image_path: str, prompt: str) -> str:
    """Use an OpenAI-compatible vision model to extract text from an image."""
    import mimetypes

    content_type, _ = mimetypes.guess_type(image_path)
    if not content_type:
        content_type = "image/png"

    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    data_uri = f"data:{content_type};base64,{b64}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ],
            }
        ],
    )
    return response.choices[0].message.content.strip()


def check_plugins_enabled() -> bool:
    """Check if plugins should be enabled. Default is True (load plugins if available)."""
    return os.getenv("MARKITDOWN_ENABLE_PLUGINS", "true").strip().lower() not in (
        "false",
        "0",
        "no",
        "off",
    )


# ---------------------------------------------------------------------------
# HTTP/SSE transport
# ---------------------------------------------------------------------------

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
        """Context manager for session manager with temp-dir lifecycle."""
        _cleanup_old_dirs(_temp_root, max_age_seconds=86400)
        async with session_manager.run():
            print("Application started with StreamableHTTP session manager!")
            try:
                yield
            finally:
                print("Application shutting down...")
                _cleanup_all(_temp_root)

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/mcp", app=handle_streamable_http),
            Mount("/messages/", app=sse.handle_post_message),
        ],
        lifespan=lifespan,
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

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
        host = args.host if args.host else "127.0.0.1"
        if args.host and args.host not in ("127.0.0.1", "localhost"):
            print(
                "\n"
                "WARNING: The server is being bound to a non-localhost interface "
                f"({host}).\n"
                "This exposes the server to other machines on the network or Internet.\n"
                "The server has NO authentication and runs with the user's privileges.\n"
                "Any process or user that can reach this interface can read files and\n"
                "fetch network resources accessible to this user.\n"
                "Only proceed if you understand the security implications.\n",
                file=sys.stderr,
            )
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=host,
            port=args.port if args.port else 3001,
        )
    else:
        # STDIO mode: clean stale dirs on start, clean up on exit
        _cleanup_old_dirs(_temp_root, max_age_seconds=86400)
        try:
            mcp.run()
        finally:
            _cleanup_all(_temp_root)


if __name__ == "__main__":
    main()
