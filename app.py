import os
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from markitdown import MarkItDown

app = FastAPI(title="markitdown-api")
md = MarkItDown(enable_plugins=False)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/convert", response_class=PlainTextResponse)
async def convert(file: UploadFile = File(...)):
    filename = file.filename or "upload.bin"
    suffix = os.path.splitext(filename)[1]
    data = await file.read()

    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        result = md.convert(tmp_path)
        return result.text_content

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "filename": filename},
        )

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
