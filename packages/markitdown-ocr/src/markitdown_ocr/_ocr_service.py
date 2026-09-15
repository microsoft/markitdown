"""
OCR Service Layer for MarkItDown
Provides LLM Vision-based image text extraction.
"""

import base64
from typing import Any, BinaryIO
from dataclasses import dataclass

from markitdown import StreamInfo


_DEFAULT_PROMPT = (
    "Extract all text from this image. "
    "Return ONLY the extracted text, maintaining the original "
    "layout and order. Do not add any commentary or description."
)


@dataclass
class OCRResult:
    """Result from OCR extraction."""

    text: str
    confidence: float | None = None
    backend_used: str | None = None
    error: str | None = None


_ANTHROPIC_MEDIA_TYPES = ("image/jpeg", "image/png", "image/gif", "image/webp")


def _sniff_content_type(
    image_stream: BinaryIO, stream_info: StreamInfo | None
) -> str | None:
    """Best-effort image content type: stream_info first, then Pillow."""
    if stream_info and stream_info.mimetype:
        return stream_info.mimetype

    try:
        from PIL import Image

        image_stream.seek(0)
        img = Image.open(image_stream)
        fmt = img.format.lower() if img.format else "png"
        return f"image/{fmt}"
    except Exception:
        return None


class LLMVisionOCRService:
    """OCR service using LLM vision models (OpenAI-compatible)."""

    def __init__(
        self,
        client: Any,
        model: str,
        default_prompt: str | None = None,
    ) -> None:
        """
        Initialize LLM Vision OCR service.

        Args:
            client: OpenAI-compatible client
            model: Model name (e.g., 'gpt-4o', 'gemini-2.0-flash')
            default_prompt: Default prompt for OCR extraction
        """
        self.client = client
        self.model = model
        self.default_prompt = default_prompt or _DEFAULT_PROMPT

    def extract_text(
        self,
        image_stream: BinaryIO,
        prompt: str | None = None,
        stream_info: StreamInfo | None = None,
        **kwargs: Any,
    ) -> OCRResult:
        """Extract text using LLM vision."""
        if self.client is None:
            return OCRResult(
                text="",
                backend_used="llm_vision",
                error="LLM client not configured",
            )

        try:
            image_stream.seek(0)

            content_type = _sniff_content_type(image_stream, stream_info) or "image/png"

            image_stream.seek(0)
            base64_image = base64.b64encode(image_stream.read()).decode("utf-8")
            data_uri = f"data:{content_type};base64,{base64_image}"

            actual_prompt = prompt or self.default_prompt
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": actual_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": data_uri},
                            },
                        ],
                    }
                ],
            )

            text = response.choices[0].message.content
            return OCRResult(
                text=text.strip() if text else "",
                backend_used="llm_vision",
            )
        except Exception as e:
            return OCRResult(text="", backend_used="llm_vision", error=str(e))
        finally:
            image_stream.seek(0)


class AnthropicVisionOCRService:
    """OCR service using Claude vision models via the Anthropic SDK.

    Same interface as :class:`LLMVisionOCRService`, but speaks the Messages
    API rather than OpenAI's chat completions, so it takes an ``anthropic``
    client (``Anthropic()``, ``AnthropicBedrockMantle()``, ``AnthropicVertex()``,
    ...) instead of an OpenAI-compatible one.
    """

    def __init__(
        self,
        client: Any,
        model: str,
        default_prompt: str | None = None,
        max_tokens: int = 16000,
    ) -> None:
        """
        Initialize Anthropic Vision OCR service.

        Args:
            client: Anthropic SDK client
            model: Model name (e.g., 'claude-opus-5')
            default_prompt: Default prompt for OCR extraction
            max_tokens: Response cap; a dense page can need several thousand
        """
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.default_prompt = default_prompt or _DEFAULT_PROMPT

    def extract_text(
        self,
        image_stream: BinaryIO,
        prompt: str | None = None,
        stream_info: StreamInfo | None = None,
        **kwargs: Any,
    ) -> OCRResult:
        """Extract text using Claude vision."""
        if self.client is None:
            return OCRResult(
                text="",
                backend_used="anthropic_vision",
                error="Anthropic client not configured",
            )

        try:
            content_type = _sniff_content_type(image_stream, stream_info)
            # The Messages API accepts a fixed set of image media types;
            # anything else (image/bmp, image/tiff, ...) is rejected, so fall
            # back to the most likely decodable label rather than erroring.
            if content_type not in _ANTHROPIC_MEDIA_TYPES:
                content_type = "image/png"

            image_stream.seek(0)
            base64_image = base64.b64encode(image_stream.read()).decode("utf-8")

            actual_prompt = prompt or self.default_prompt
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": content_type,
                                    "data": base64_image,
                                },
                            },
                            {"type": "text", "text": actual_prompt},
                        ],
                    }
                ],
            )

            # Safety classifiers can decline a request with HTTP 200; the
            # content blocks are empty in that case, so check before reading.
            if getattr(response, "stop_reason", None) == "refusal":
                return OCRResult(
                    text="",
                    backend_used="anthropic_vision",
                    error="Request was refused by the model",
                )

            text = "".join(
                block.text
                for block in getattr(response, "content", [])
                if getattr(block, "type", None) == "text"
            )
            return OCRResult(
                text=text.strip(),
                backend_used="anthropic_vision",
            )
        except Exception as e:
            return OCRResult(text="", backend_used="anthropic_vision", error=str(e))
        finally:
            image_stream.seek(0)


def create_ocr_service(
    client: Any,
    model: str,
    default_prompt: str | None = None,
) -> LLMVisionOCRService | AnthropicVisionOCRService:
    """Build the OCR service matching the client that was passed in.

    MarkItDown's own ``llm_client`` contract is OpenAI-shaped, so an
    OpenAI-compatible client stays the default; a client exposing the
    Anthropic Messages API instead gets the Claude backend.
    """
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        return LLMVisionOCRService(
            client=client, model=model, default_prompt=default_prompt
        )

    if hasattr(client, "messages") and hasattr(client.messages, "create"):
        return AnthropicVisionOCRService(
            client=client, model=model, default_prompt=default_prompt
        )

    raise ValueError(
        "Unrecognized llm_client: expected an OpenAI-compatible client "
        "(client.chat.completions.create) or an Anthropic client "
        "(client.messages.create), got "
        f"{type(client).__name__}."
    )
