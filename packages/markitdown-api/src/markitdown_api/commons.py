from typing import Optional

from openai import OpenAI
from pydantic import BaseModel
from starlette.responses import Response

from markitdown import MarkItDown


class ConvertResult(BaseModel):
    title: Optional[str]
    markdown: str


class MarkdownResponse(Response):
    media_type = "text/markdown"


class OpenAIOptions(BaseModel):
    base_url: Optional[str]
    api_key: Optional[str]
    model: str = "gpt-4o"
    prompt: str = ""


def is_blank(s: str) -> bool:
    return not s or s.isspace()


def blank_then_none(s: str) -> str | None:
    if is_blank(s):
        return None
    return s


def _build_markitdown(openai_options: Optional[OpenAIOptions] = None) -> MarkItDown:
    base_url = api_key = llm_model = prompt = None
    if openai_options:
        base_url = blank_then_none(openai_options.base_url)
        api_key = blank_then_none(openai_options.api_key)
        llm_model = blank_then_none(openai_options.model)
        prompt = blank_then_none(openai_options.prompt)

    llm_client = OpenAI(base_url=base_url, api_key=api_key)
    return MarkItDown(
        enable_plugins=True,
        enable_builtins=True,
        llm_client=llm_client,
        llm_model=llm_model,
        llm_prompt=prompt
    )
