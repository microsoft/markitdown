from typing import Annotated

from fastapi import HTTPException, Query, Body, APIRouter
from pydantic import BaseModel, Field

from markitdown_api.commons import MarkdownResponse, OpenAIOptions, ConvertResponse, _build_markitdown

TAG = "Convert Uri"

URI_DESCRIPTION = """
The Uniform Resource Identifier (URI) to be converted.
Supported schemes are: file:, data:, http:, https:.
Example: https://example.com/document.docx
"""
URI_PATTERN = "^(file|data|http|https)://"

URI_QUERY = Query(description=URI_DESCRIPTION, pattern=URI_PATTERN)


class ConvertUrlRequest(BaseModel):
    uri: str = Field(description=URI_DESCRIPTION, pattern=URI_PATTERN)
    openai: OpenAIOptions | None = Field(default=None, description="OpenAI options")


router = APIRouter(
    prefix="/convert/uri",
    tags=[TAG]
)


def _convert_uri(uri: str, openai: OpenAIOptions | None = None) -> ConvertResponse:
    convert_result = _build_markitdown(openai).convert_uri(uri)
    return ConvertResponse(title=convert_result.title, markdown=convert_result.markdown)


@router.post(path="/", response_model=ConvertResponse)
async def convert_uri(request: Annotated[ConvertUrlRequest, Body(
    examples=[
        {
            "uri": "https://wow.ahoo.me/"
        }
    ]
)]):
    return _convert_uri(request.uri, request.openai)


@router.get(path="/", response_model=ConvertResponse)
async def convert_uri(uri: Annotated[str, URI_QUERY]):
    """
    The Uniform Resource Identifier (URI) to be converted.
    Supported schemes include 'http://', 'https://', 'file://', and custom protocols understood by MarkItDown.
    Example: https://example.com/document.docx
    """
    return _convert_uri(uri)


@router.get(path="/markdown", response_class=MarkdownResponse)
async def convert_uri_markdown(uri: Annotated[str, URI_QUERY]):
    return _convert_uri(uri).markdown
