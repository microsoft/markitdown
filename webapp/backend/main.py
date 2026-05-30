import os
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from markitdown import MarkItDown

app = FastAPI(title="MarkItDown Web API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

SUPPORTED_EXTENSIONS = {
    "pdf", "docx", "doc", "pptx", "ppt",
    "xlsx", "xls", "csv", "json", "xml",
    "html", "htm", "txt", "md",
    "png", "jpg", "jpeg", "webp",
    "zip", "epub",
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

converter = MarkItDown()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/formats")
def formats():
    return {"supported": sorted(SUPPORTED_EXTENSIONS)}


@app.post("/api/convert")
async def convert(file: UploadFile = File(...)):
    filename = file.filename or "upload"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format: .{ext}. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = converter.convert(tmp_path)
        return {
            "markdown": result.text_content,
            "filename": filename,
            "format": ext,
            "characters": len(result.text_content),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(exc)}")
    finally:
        os.unlink(tmp_path)
