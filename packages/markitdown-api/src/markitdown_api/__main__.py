from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import Response

from markitdown import MarkItDown

app = FastAPI(
    title="MarkItDown API",
    description="A simple API for converting URLs to Markdown",
    version="1.0.0",
)


class ConvertResponse(BaseModel):
    title: Optional[str]
    markdown: str


@app.get("/convert", response_model=ConvertResponse)
async def convert(url: str):
    try:
        convert_result = MarkItDown().convert_uri(url)
        return {"title": convert_result.title, "markdown": convert_result.markdown}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class MarkdownResponse(Response):
    media_type = "text/markdown"

@app.get("/convert/markdown", response_class=MarkdownResponse)
async def convert_markdown(url: str):
    try:
        return MarkItDown().convert_uri(url).markdown
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
