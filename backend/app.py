import os
import io
import tempfile
import traceback
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from markitdown import MarkItDown, StreamInfo, UnsupportedFormatException, FileConversionException

app = FastAPI(title="MarkItDown API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class ConvertUrlRequest(BaseModel):
    url: str


class ConvertResponse(BaseModel):
    success: bool
    markdown: str = ""
    error: str = ""
    filename: str = ""


def _get_markitdown() -> MarkItDown:
    return MarkItDown()


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/convert/file", response_model=ConvertResponse)
async def convert_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Save uploaded file to temp location
    safe_name = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_name

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        md = _get_markitdown()
        result = md.convert(str(file_path))

        return ConvertResponse(
            success=True,
            markdown=result.text_content,
            filename=safe_name,
        )
    except UnsupportedFormatException as e:
        return ConvertResponse(
            success=False,
            error=f"Unsupported file format: {str(e)}",
            filename=safe_name,
        )
    except FileConversionException as e:
        return ConvertResponse(
            success=False,
            error=f"File conversion failed: {str(e)}",
            filename=safe_name,
        )
    except Exception as e:
        return ConvertResponse(
            success=False,
            error=f"Error: {str(e)}",
            filename=safe_name,
        )
    finally:
        if file_path.exists():
            file_path.unlink()


@app.post("/api/convert/url", response_model=ConvertResponse)
async def convert_url(req: ConvertUrlRequest):
    if not req.url.strip():
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        md = _get_markitdown()
        result = md.convert(req.url.strip())

        return ConvertResponse(
            success=True,
            markdown=result.text_content,
            filename=req.url.strip(),
        )
    except UnsupportedFormatException as e:
        return ConvertResponse(
            success=False,
            error=f"Unsupported format: {str(e)}",
            filename=req.url.strip(),
        )
    except FileConversionException as e:
        return ConvertResponse(
            success=False,
            error=f"Conversion failed: {str(e)}",
            filename=req.url.strip(),
        )
    except Exception as e:
        return ConvertResponse(
            success=False,
            error=f"Error: {str(e)}",
            filename=req.url.strip(),
        )


@app.post("/api/convert/file/raw")
async def convert_file_raw(file: UploadFile = File(...)):
    """Convert file and return raw markdown text."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    safe_name = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_name

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        md = _get_markitdown()
        result = md.convert(str(file_path))

        return PlainTextResponse(
            content=result.text_content,
            media_type="text/markdown; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename={safe_name}.md"
            },
        )
    except UnsupportedFormatException as e:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {str(e)}")
    except FileConversionException as e:
        raise HTTPException(status_code=422, detail=f"File conversion failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if file_path.exists():
            file_path.unlink()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)