"""
OCR Service Layer for MarkItDown
Provides LLM Vision-based image text extraction.
"""

import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, BinaryIO
from dataclasses import dataclass

from markitdown import StreamInfo


@dataclass
class OCRResult:
    """Result from OCR extraction."""

    text: str
    confidence: float | None = None
    backend_used: str | None = None
    error: str | None = None


class LLMVisionOCRService:
    """OCR service using LLM vision models (OpenAI-compatible)."""

    def __init__(
        self,
        client: Any,
        model: str,
        default_prompt: str | None = None,
        max_workers: int = 5,
    ) -> None:
        """
        Initialize LLM Vision OCR service.

        Args:
            client: OpenAI-compatible client
            model: Model name (e.g., 'gpt-4o', 'gemini-2.0-flash')
            default_prompt: Default prompt for OCR extraction
            max_workers: Maximum number of parallel OCR workers (default 5)
        """
        self.client = client
        self.model = model
        self.max_workers = max_workers
        self.default_prompt = default_prompt or (
            "Extract all text from this image. "
            "Return ONLY the extracted text, maintaining the original "
            "layout and order. Do not add any commentary or description."
        )

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

            content_type: str | None = None
            if stream_info:
                content_type = stream_info.mimetype

            if not content_type:
                try:
                    from PIL import Image

                    image_stream.seek(0)
                    img = Image.open(image_stream)
                    fmt = img.format.lower() if img.format else "png"
                    content_type = f"image/{fmt}"
                except Exception:
                    content_type = "image/png"

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

    def extract_text_batch(
        self,
        images: list[tuple[BinaryIO, StreamInfo | None]],
        prompt: str | None = None,
        **kwargs: Any,
    ) -> list[OCRResult]:
        """
        Extract text from multiple images in parallel using a thread pool.

        Args:
            images: List of (image_stream, stream_info) tuples
            prompt: Optional prompt override (shared across all images)
            **kwargs: Additional arguments (max_workers override, etc.)

        Returns:
            List of OCRResult, one per input image (same order as input).
            Individual failures are captured in the OCRResult's error field
            rather than raising an exception.
        """
        if not images:
            return []

        max_workers = kwargs.get("max_workers", self.max_workers)

        def _process_one(
            idx: int, img_stream: BinaryIO, stream_info: StreamInfo | None
        ) -> tuple[int, OCRResult]:
            """Wrapper that catches all exceptions so one failure doesn't
            kill the entire batch."""
            try:
                result = self.extract_text(
                    img_stream, prompt=prompt, stream_info=stream_info
                )
            except Exception as e:
                result = OCRResult(
                    text="", backend_used="llm_vision", error=str(e)
                )
            return idx, result

        results: list[OCRResult | None] = [None] * len(images)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_process_one, i, img, info): i
                for i, (img, info) in enumerate(images)
            }
            for future in as_completed(futures):
                idx, result = future.result()
                results[idx] = result

        # Defensive: any slot still None → empty result
        return [
            r if r is not None else OCRResult(text="", backend_used="llm_vision")
            for r in results
        ]
