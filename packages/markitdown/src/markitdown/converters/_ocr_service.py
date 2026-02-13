"""
OCR Service Layer for MarkItDown
Provides unified interface for multiple OCR backends with graceful fallback.
"""

import base64
from dataclasses import dataclass
from enum import Enum
from typing import Any, BinaryIO, Optional, Protocol

from .._stream_info import StreamInfo


class OCRBackend(str, Enum):
    """Supported OCR backends."""

    LLM_VISION = "llm_vision"
    AZURE_DOC_INTEL = "azure_doc_intel"


@dataclass
class OCRResult:
    """Result from OCR extraction."""

    text: str
    confidence: Optional[float] = None
    language: Optional[str] = None
    backend_used: Optional[str] = None
    error: Optional[str] = None


class OCRService(Protocol):
    """Protocol for OCR services."""

    def extract_text(self, image_stream: BinaryIO, **kwargs: Any) -> OCRResult:
        """Extract text from an image stream."""
        ...


class LLMVisionOCRService:
    """OCR service using LLM vision models (OpenAI-compatible)."""

    def __init__(self, client: Any, model: str, default_prompt: Optional[str] = None):
        """
        Initialize LLM Vision OCR service.

        Args:
            client: OpenAI-compatible client
            model: Model name (e.g., 'gpt-4o', 'gemini-2.0-flash')
            default_prompt: Default prompt for OCR extraction
        """
        self.client = client
        self.model = model
        self.default_prompt = default_prompt or (
            "Extract all text from this image. "
            "Return ONLY the extracted text, maintaining the original layout and order. "
            "Do not add any commentary or description."
        )

    def extract_text(
        self,
        image_stream: BinaryIO,
        prompt: Optional[str] = None,
        stream_info: Optional[StreamInfo] = None,
        **kwargs: Any,
    ) -> OCRResult:
        """Extract text using LLM vision."""
        if self.client is None:
            return OCRResult(
                text="", backend_used="llm_vision", error="LLM client not configured"
            )

        try:
            # Reset stream position
            image_stream.seek(0)

            # Get content type
            content_type = None
            if stream_info:
                content_type = stream_info.mimetype

            if not content_type:
                # Guess from stream
                try:
                    from PIL import Image

                    image_stream.seek(0)
                    img = Image.open(image_stream)
                    fmt = img.format.lower() if img.format else "png"
                    content_type = f"image/{fmt}"
                except Exception:
                    content_type = "image/png"

            # Convert to base64
            image_stream.seek(0)
            base64_image = base64.b64encode(image_stream.read()).decode("utf-8")
            data_uri = f"data:{content_type};base64,{base64_image}"

            # Prepare message
            actual_prompt = prompt or self.default_prompt
            messages = [
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
            ]

            # Call LLM (handle both sync and async clients)
            import asyncio
            import inspect

            result = self.client.chat.completions.create(
                model=self.model, messages=messages
            )

            # If result is a coroutine, we need to run it in an event loop
            if inspect.iscoroutine(result):
                # Try to get the running event loop, or create a new one
                try:
                    asyncio.get_running_loop()
                    # We're already in an async context, but this is a sync function
                    # This shouldn't happen in normal usage
                    raise RuntimeError(
                        "Cannot use async LLM client in sync OCR context"
                    )
                except RuntimeError:
                    # No running loop, create a new one (this is the normal case)
                    response = asyncio.run(result)
            else:
                response = result

            text = response.choices[0].message.content

            return OCRResult(
                text=text.strip() if text else "",
                backend_used="llm_vision",
                confidence=None,  # LLMs don't provide confidence scores
            )
        except Exception as e:
            return OCRResult(text="", backend_used="llm_vision", error=str(e))
        finally:
            # Reset stream position
            image_stream.seek(0)


class MultiBackendOCRService:
    """
    OCR service with multiple backends and fallback strategy.
    Tries backends in order until one succeeds.
    """

    def __init__(
        self,
        backends: Optional[list[OCRBackend]] = None,
        llm_client: Any = None,
        llm_model: Optional[str] = None,
        llm_prompt: Optional[str] = None,
    ):
        """
        Initialize multi-backend OCR service.

        Args:
            backends: List of backends to try in order
            llm_client: OpenAI-compatible client for LLM vision
            llm_model: Model name for LLM vision
            llm_prompt: Default prompt for LLM vision
        """
        # Default backend: LLM Vision
        self.backends = backends or [OCRBackend.LLM_VISION]

        # Initialize backend services
        self.services: dict[OCRBackend, OCRService] = {}

        # LLM Vision
        if OCRBackend.LLM_VISION in self.backends:
            if llm_client and llm_model:
                self.services[OCRBackend.LLM_VISION] = LLMVisionOCRService(
                    client=llm_client, model=llm_model, default_prompt=llm_prompt
                )

    def extract_text(
        self,
        image_stream: BinaryIO,
        prompt: Optional[str] = None,
        stream_info: Optional[StreamInfo] = None,
        min_text_length: int = 3,
        **kwargs: Any,
    ) -> OCRResult:
        """
        Extract text using multiple backends with fallback.

        Args:
            image_stream: Image stream to extract text from
            prompt: Optional prompt for LLM-based OCR
            stream_info: Stream information for the image
            min_text_length: Minimum text length to consider successful
            **kwargs: Additional arguments

        Returns:
            OCRResult with extracted text and metadata
        """
        last_error = None

        for backend in self.backends:
            service = self.services.get(backend)
            if service is None:
                continue

            try:
                # Reset stream position before each attempt
                image_stream.seek(0)

                # Extract text
                if backend == OCRBackend.LLM_VISION:
                    result = service.extract_text(
                        image_stream, prompt=prompt, stream_info=stream_info
                    )
                else:
                    result = service.extract_text(image_stream)

                # Check if extraction was successful
                if (
                    result.text
                    and len(result.text) >= min_text_length
                    and not result.error
                ):
                    return result

                # Store error for potential reporting
                if result.error:
                    last_error = result.error

            except Exception as e:
                last_error = str(e)
                continue

        # All backends failed
        return OCRResult(
            text="",
            backend_used="none",
            error=f"All OCR backends failed. Last error: {last_error}",
        )
