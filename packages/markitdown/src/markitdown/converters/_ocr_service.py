"""
OCR Service Layer for MarkItDown
Provides unified interface for multiple OCR backends with graceful fallback.
"""

import sys
import io
import base64
import mimetypes
from typing import BinaryIO, Optional, Protocol, Any
from dataclasses import dataclass
from enum import Enum

from .._stream_info import StreamInfo


class OCRBackend(str, Enum):
    """Supported OCR backends."""
    TESSERACT = "tesseract"
    EASYOCR = "easyocr"
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


class TesseractOCRService:
    """OCR service using Tesseract via pytesseract."""

    def __init__(self, config: str = "--psm 6", lang: str = "eng"):
        """
        Initialize Tesseract OCR service.

        Args:
            config: Tesseract configuration string
            lang: Language code (default: eng)
        """
        self.config = config
        self.lang = lang
        self._pytesseract = None
        self._PIL_Image = None
        self._dependency_exc_info = None

        try:
            import pytesseract
            from PIL import Image
            self._pytesseract = pytesseract
            self._PIL_Image = Image
        except ImportError:
            self._dependency_exc_info = sys.exc_info()

    def extract_text(self, image_stream: BinaryIO, **kwargs: Any) -> OCRResult:
        """Extract text using Tesseract."""
        if self._dependency_exc_info is not None:
            return OCRResult(
                text="",
                backend_used="tesseract",
                error="pytesseract not installed"
            )

        try:
            # Reset stream position
            image_stream.seek(0)

            # Open image
            image = self._PIL_Image.open(image_stream)

            # Extract text
            text = self._pytesseract.image_to_string(
                image,
                lang=self.lang,
                config=self.config
            )

            # Try to get confidence if available
            try:
                data = self._pytesseract.image_to_data(
                    image,
                    lang=self.lang,
                    output_type=self._pytesseract.Output.DICT
                )
                confidences = [c for c in data['conf'] if c != -1]
                avg_confidence = sum(confidences) / len(confidences) if confidences else None
            except Exception:
                avg_confidence = None

            return OCRResult(
                text=text.strip(),
                confidence=avg_confidence,
                language=self.lang,
                backend_used="tesseract"
            )
        except Exception as e:
            return OCRResult(
                text="",
                backend_used="tesseract",
                error=str(e)
            )
        finally:
            # Reset stream position
            image_stream.seek(0)


class EasyOCRService:
    """OCR service using EasyOCR."""

    def __init__(self, langs: list[str] = None):
        """
        Initialize EasyOCR service.

        Args:
            langs: List of language codes (default: ['en'])
        """
        self.langs = langs or ['en']
        self._reader = None
        self._dependency_exc_info = None

        try:
            import easyocr
            # Lazy initialization - only create reader when needed
            self._easyocr = easyocr
        except ImportError:
            self._dependency_exc_info = sys.exc_info()

    def _get_reader(self):
        """Lazy load the EasyOCR reader."""
        if self._reader is None and self._easyocr is not None:
            self._reader = self._easyocr.Reader(self.langs, gpu=False)
        return self._reader

    def extract_text(self, image_stream: BinaryIO, **kwargs: Any) -> OCRResult:
        """Extract text using EasyOCR."""
        if self._dependency_exc_info is not None:
            return OCRResult(
                text="",
                backend_used="easyocr",
                error="easyocr not installed"
            )

        try:
            from PIL import Image
            import numpy as np

            # Reset stream position
            image_stream.seek(0)

            # Convert to numpy array
            image = Image.open(image_stream)
            image_np = np.array(image)

            # Get reader and extract text
            reader = self._get_reader()
            result = reader.readtext(image_np)

            # Combine all detected text
            texts = [text for (bbox, text, prob) in result]
            combined_text = "\n".join(texts)

            # Calculate average confidence
            confidences = [prob for (bbox, text, prob) in result]
            avg_confidence = sum(confidences) / len(confidences) if confidences else None

            return OCRResult(
                text=combined_text.strip(),
                confidence=avg_confidence,
                language=",".join(self.langs),
                backend_used="easyocr"
            )
        except Exception as e:
            return OCRResult(
                text="",
                backend_used="easyocr",
                error=str(e)
            )
        finally:
            # Reset stream position
            image_stream.seek(0)


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
        **kwargs: Any
    ) -> OCRResult:
        """Extract text using LLM vision."""
        if self.client is None:
            return OCRResult(
                text="",
                backend_used="llm_vision",
                error="LLM client not configured"
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

            # Call LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            text = response.choices[0].message.content

            return OCRResult(
                text=text.strip() if text else "",
                backend_used="llm_vision",
                confidence=None  # LLMs don't provide confidence scores
            )
        except Exception as e:
            return OCRResult(
                text="",
                backend_used="llm_vision",
                error=str(e)
            )
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
        tesseract_config: str = "--psm 6",
        tesseract_lang: str = "eng",
        easyocr_langs: Optional[list[str]] = None,
    ):
        """
        Initialize multi-backend OCR service.

        Args:
            backends: List of backends to try in order
            llm_client: OpenAI-compatible client for LLM vision
            llm_model: Model name for LLM vision
            llm_prompt: Default prompt for LLM vision
            tesseract_config: Tesseract configuration
            tesseract_lang: Tesseract language
            easyocr_langs: EasyOCR language list
        """
        # Default backend order: fast local OCR first, expensive LLM last
        self.backends = backends or [
            OCRBackend.TESSERACT,
            OCRBackend.EASYOCR,
            OCRBackend.LLM_VISION,
        ]

        # Initialize backend services
        self.services: dict[OCRBackend, OCRService] = {}

        # Tesseract
        if OCRBackend.TESSERACT in self.backends:
            self.services[OCRBackend.TESSERACT] = TesseractOCRService(
                config=tesseract_config,
                lang=tesseract_lang
            )

        # EasyOCR
        if OCRBackend.EASYOCR in self.backends:
            self.services[OCRBackend.EASYOCR] = EasyOCRService(
                langs=easyocr_langs or ['en']
            )

        # LLM Vision
        if OCRBackend.LLM_VISION in self.backends:
            if llm_client and llm_model:
                self.services[OCRBackend.LLM_VISION] = LLMVisionOCRService(
                    client=llm_client,
                    model=llm_model,
                    default_prompt=llm_prompt
                )

    def extract_text(
        self,
        image_stream: BinaryIO,
        prompt: Optional[str] = None,
        stream_info: Optional[StreamInfo] = None,
        min_text_length: int = 3,
        **kwargs: Any
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
                        image_stream,
                        prompt=prompt,
                        stream_info=stream_info
                    )
                else:
                    result = service.extract_text(image_stream)

                # Check if extraction was successful
                if result.text and len(result.text) >= min_text_length and not result.error:
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
            error=f"All OCR backends failed. Last error: {last_error}"
        )
