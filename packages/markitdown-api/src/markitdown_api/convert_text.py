from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from io import BytesIO

from markitdown import StreamInfo
from markitdown_api.commons import OpenAIOptions, ConvertResponse, _build_markitdown

TAG = "Convert Text"


class ConvertTextRequest(BaseModel):
    text: str
    mimetype: str = Field(default="text/plain", description="MIME type of the input text")
    openai: OpenAIOptions | None = Field(default=None, description="OpenAI options")


router = APIRouter(
    prefix="/convert/text",
    tags=[TAG],
)


@router.post(path="/", response_model=ConvertResponse)
async def convert_text(request: ConvertTextRequest):
    if not request.text or len(request.text) > 100_000:
        raise HTTPException(status_code=400, detail="Invalid input text length")

    text_binary = request.text.encode('utf-8')
    binary_io = BytesIO(text_binary)

    stream_info = StreamInfo(mimetype=request.mimetype)
    convert_result = _build_markitdown(request.openai).convert_stream(stream=binary_io, stream_info=stream_info)

    return {"title": convert_result.title, "markdown": convert_result.markdown}

