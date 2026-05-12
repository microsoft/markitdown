"""
OCR Service Layer for MarkItDown
Provides LLM Vision-based and glm-ocr-based image text extraction.
"""

import base64
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


class GlmOcrService:
    """OCR service using zai-sdk + glm-ocr layout_parsing.

    Uses ZhiPu AI's specialized document layout parsing model which provides:
    - Better table recognition than general LLM Vision
    - Markdown formatted output via md_results
    - Lower cost per call compared to GPT-4o etc.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "glm-ocr",
        timeout: int = 120,
    ) -> None:
        """
        Initialize glm-ocr service.

        Args:
            api_key: ZhiPu AI API key
            model: Model name (default: 'glm-ocr')
            timeout: Request timeout in seconds

        Raises:
            ImportError: If zai-sdk is not installed
            ValueError: If api_key is empty
        """
        try:
            from zai import ZhipuAiClient
        except ImportError:
            raise ImportError(
                "zai-sdk is required for glm-ocr provider. "
                "Install with: pip install markitdown-ocr[glmocr]"
            )

        if not api_key:
            raise ValueError(
                "GLMOCR_API_KEY is required. "
                "Set it via environment variable or pass glmocr_api_key parameter."
            )

        self.client = ZhipuAiClient(api_key=api_key)
        self.model = model
        self.timeout = timeout

    def extract_text(
        self,
        image_stream: BinaryIO,
        prompt: str | None = None,
        stream_info: StreamInfo | None = None,
        **kwargs: Any,
    ) -> OCRResult:
        """Extract text using glm-ocr layout_parsing.

        The prompt parameter is accepted for interface compatibility but is
        not used — glm-ocr uses its own internal prompt for layout parsing.
        """
        try:
            image_stream.seek(0)
            image_bytes = image_stream.read()

            base64_image = base64.b64encode(image_bytes).decode("utf-8")

            # Detect content type
            content_type = "image/png"
            if stream_info and stream_info.mimetype:
                content_type = stream_info.mimetype
            else:
                # Simple heuristic from magic bytes
                if image_bytes[:3] == b"\xff\xd8\xff":
                    content_type = "image/jpeg"

            data_uri = f"data:{content_type};base64,{base64_image}"

            # Call glm-ocr layout_parsing
            response = self.client.layout_parsing.create(
                model=self.model,
                file=data_uri,
            )

            # Extract result — prefer md_results (already Markdown), fallback to layout_details
            text = ""
            if hasattr(response, "md_results") and response.md_results:
                text = response.md_results.strip()
            elif hasattr(response, "layout_details") and response.layout_details:
                parts = []
                for detail_list in response.layout_details:
                    for detail in detail_list:
                        if hasattr(detail, "content") and detail.content:
                            parts.append(detail.content.strip())
                text = "\n\n".join(parts)

            return OCRResult(
                text=text.strip(),
                backend_used="glm_ocr",
            )

        except Exception as e:
            return OCRResult(text="", backend_used="glm_ocr", error=str(e))
        finally:
            image_stream.seek(0)


