from io import BufferedReader
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel, Field

from markitdown import StreamInfo
from markitdown_api.commons import OpenAIOptions, ConvertResponse, _build_markitdown, MarkdownResponse

TAG = "Convert File"


class ConvertFileRequest(BaseModel):
    openai: OpenAIOptions | None = Field(default=None, description="OpenAI options")


router = APIRouter(
    prefix="/convert/file",
    tags=[TAG],
)


def _convert_file(file: Annotated[UploadFile, File()],
                  openai_base_url: Annotated[str, Form()] = "",
                  openai_api_key: Annotated[str, Form()] = "",
                  openai_model: Annotated[str, Form()] = "",
                  openai_prompt: Annotated[str, Form()] = "",
                  ) -> ConvertResponse:
    stream_info = StreamInfo(mimetype=file.content_type)
    openai_options = OpenAIOptions(api_key=openai_api_key, base_url=openai_base_url, model=openai_model,
                                   prompt=openai_prompt)
    with BufferedReader(file.file) as buffered_reader:
        convert_result = _build_markitdown(openai_options).convert_stream(buffered_reader, stream_info=stream_info)
        return ConvertResponse(title=convert_result.title, markdown=convert_result.markdown)


@router.post(path="/", response_model=ConvertResponse)
async def convert_file(file: Annotated[UploadFile, File()],
                       openai_base_url: Annotated[str, Form()] = "",
                       openai_api_key: Annotated[str, Form()] = "",
                       openai_model: Annotated[str, Form()] = "",
                       openai_prompt: Annotated[str, Form()] = "",
                       ):
    return _convert_file(file, openai_base_url, openai_api_key, openai_model, openai_prompt)


@router.post(path="/markdown", response_class=MarkdownResponse)
async def convert_file_markdown(file: Annotated[UploadFile, File()],
                                openai_base_url: Annotated[str, Form()] = "",
                                openai_api_key: Annotated[str, Form()] = "",
                                openai_model: Annotated[str, Form()] = "",
                                openai_prompt: Annotated[str, Form()] = "",
                                ):
    return _convert_file(file, openai_base_url, openai_api_key, openai_model, openai_prompt).markdown
