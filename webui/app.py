"""MarkItDown Web UI: a small FastAPI server around the markitdown library."""
import base64
import os
import secrets
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from markitdown import MarkItDown, StreamInfo

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "50"))
AUTH_USER = os.getenv("AUTH_USER", "")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "")
STATIC_DIR = Path(__file__).parent / "static"
TEXT_EXTS = {".csv", ".txt", ".md", ".json", ".html", ".htm", ".xml", ".rss", ".atom"}

app = FastAPI(title="MarkItDown UI", docs_url=None, redoc_url=None)
md = MarkItDown(enable_plugins=False)


@app.middleware("http")
async def basic_auth(request: Request, call_next):
    """Optional HTTP Basic auth, enabled when AUTH_PASSWORD is set."""
    if AUTH_PASSWORD and request.url.path != "/health":
        ok = False
        header = request.headers.get("authorization", "")
        if header.lower().startswith("basic "):
            try:
                user, _, pwd = base64.b64decode(header[6:]).decode().partition(":")
                ok = secrets.compare_digest(user, AUTH_USER) and secrets.compare_digest(
                    pwd, AUTH_PASSWORD
                )
            except Exception:
                ok = False
        if not ok:
            return Response(
                status_code=401,
                headers={"WWW-Authenticate": 'Basic realm="MarkItDown"'},
            )
    return await call_next(request)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/config")
def config():
    return {"max_upload_mb": MAX_UPLOAD_MB}


@app.post("/api/convert")
def convert(file: UploadFile = File(...)):
    name = os.path.basename(file.filename or "file")
    suffix = Path(name).suffix[:16]
    limit = MAX_UPLOAD_MB * 1024 * 1024
    size = 0
    # The original name is never used as a path; only its extension is kept
    # so markitdown can detect the format.
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                raise HTTPException(413, f"File is larger than {MAX_UPLOAD_MB} MB")
            tmp.write(chunk)
        tmp.flush()
        stream_info = None
        if suffix.lower() in TEXT_EXTS:
            # Charset auto-detection is unreliable on short Arabic files;
            # prefer UTF-8 whenever the bytes are valid UTF-8.
            try:
                Path(tmp.name).read_bytes().decode("utf-8")
                stream_info = StreamInfo(charset="utf-8")
            except UnicodeDecodeError:
                pass
        try:
            result = md.convert(tmp.name, stream_info=stream_info)
        except Exception as e:  # unsupported format or corrupt file
            return JSONResponse(
                status_code=422,
                content={"filename": name, "error": f"{type(e).__name__}: {e}"[:500]},
            )
    return {"filename": name, "size": size, "markdown": result.markdown}


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
