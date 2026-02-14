"""API models for request/response handling."""

from pydantic import BaseModel, HttpUrl


class ConvertUrlRequest(BaseModel):
    """Request model for URL conversion."""

    url: HttpUrl


class ConvertResponse(BaseModel):
    """Response model for conversion results."""

    markdown: str
    text_content: str | None = None
    metadata: dict | None = None