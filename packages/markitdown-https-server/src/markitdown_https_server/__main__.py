import argparse
import io
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse

from markitdown import MarkItDown, StreamInfo


def _plugins_enabled() -> bool:
    return os.getenv("MARKITDOWN_ENABLE_PLUGINS", "false").strip().lower() in (
        "true",
        "1",
        "yes",
    )


app = FastAPI(title="markitdown-https-server")


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}


@app.post("/convert")
async def convert(file: UploadFile = File(...)) -> PlainTextResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    try:
        raw = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read upload: {e}") from e

    filename = Path(file.filename).name
    extension = Path(filename).suffix or None

    md = MarkItDown(enable_plugins=_plugins_enabled())
    try:
        res = md.convert_stream(
            io.BytesIO(raw),
            stream_info=StreamInfo(filename=filename, extension=extension),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return PlainTextResponse(
        res.text_content,
        media_type="text/markdown; charset=utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run an HTTPS server that converts uploaded files to Markdown using markitdown."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3443)
    parser.add_argument(
        "--certfile",
        required=True,
        help="Path to TLS certificate (PEM).",
    )
    parser.add_argument(
        "--keyfile",
        required=True,
        help="Path to TLS private key (PEM).",
    )
    args = parser.parse_args()

    certfile = os.path.abspath(args.certfile)
    keyfile = os.path.abspath(args.keyfile)
    if not os.path.exists(certfile):
        raise SystemExit(f"--certfile not found: {certfile}")
    if not os.path.exists(keyfile):
        raise SystemExit(f"--keyfile not found: {keyfile}")

    uvicorn.run(
        "markitdown_https_server.__main__:app",
        host=args.host,
        port=args.port,
        ssl_certfile=certfile,
        ssl_keyfile=keyfile,
    )


if __name__ == "__main__":
    main()
