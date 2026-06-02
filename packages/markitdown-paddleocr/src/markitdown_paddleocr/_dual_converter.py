"""DualOcrConverter - glmocr (primary) → paddleocr (fallback) automatic degradation."""

import logging
from typing import Any, BinaryIO, Optional

from markitdown import (
    DocumentConverter,
    DocumentConverterResult,
    MarkItDown,
    StreamInfo,
)

logger = logging.getLogger(__name__)


class DualOcrConverter(DocumentConverter):
    """Dual OCR converter with automatic fallback: glmocr → paddleocr.

    Usage:
        converter = DualOcrConverter()
        md = MarkItDown(enable_plugins=False)
        md.register_converter(converter, priority=-1.0)
        result = md.convert("document.pdf")
    """

    def __init__(
        self,
        # glmocr kwargs
        glmocr_api_key: Optional[str] = None,
        glmocr_timeout: int = 1800,
        glmocr_enable_layout: bool = False,
        glmocr_force_ai: bool = False,
        # paddleocr kwargs
        paddleocr_token: Optional[str] = None,
        paddleocr_model: str = "PaddleOCR-VL-1.6",
        paddleocr_poll_interval: float = 2.0,
        paddleocr_poll_timeout: float = 300.0,
        paddleocr_force_ai: bool = False,
        paddleocr_use_doc_orientation_classify: bool = False,
        paddleocr_use_doc_unwarping: bool = False,
        paddleocr_use_chart_recognition: bool = False,
    ):
        self.glmocr_kwargs = {
            "api_key": glmocr_api_key,
            "timeout": glmocr_timeout,
            "enable_layout": glmocr_enable_layout,
            "force_ai": glmocr_force_ai,
        }
        self.paddleocr_kwargs = {
            "token": paddleocr_token,
            "model": paddleocr_model,
            "poll_interval": paddleocr_poll_interval,
            "poll_timeout": paddleocr_poll_timeout,
            "force_ai": paddleocr_force_ai,
            "use_doc_orientation_classify": paddleocr_use_doc_orientation_classify,
            "use_doc_unwarping": paddleocr_use_doc_unwarping,
            "use_chart_recognition": paddleocr_use_chart_recognition,
        }

        self._primary = None
        self._fallback = None
        self._init_converters()

    def _init_converters(self):
        """Lazily init both converters."""
        try:
            from markitdown_glmocr import GlmOcrConverter

            # Filter out None values
            kwargs = {k: v for k, v in self.glmocr_kwargs.items() if v is not None}
            self._primary = GlmOcrConverter(**kwargs)
            logger.info("glmocr converter initialized (primary)")
        except Exception as e:
            logger.warning("glmocr init failed: %s", e)
            self._primary = None

        try:
            from markitdown_paddleocr import PaddleOcrConverter

            kwargs = {k: v for k, v in self.paddleocr_kwargs.items() if v is not None}
            self._fallback = PaddleOcrConverter(**kwargs)
            logger.info("paddleocr converter initialized (fallback)")
        except Exception as e:
            logger.warning("paddleocr init failed: %s", e)
            self._fallback = None

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        """Accept if either converter accepts."""
        if self._primary:
            try:
                file_stream.seek(0)
                if self._primary.accepts(file_stream, stream_info, **kwargs):
                    return True
            except Exception:
                pass

        if self._fallback:
            try:
                file_stream.seek(0)
                if self._fallback.accepts(file_stream, stream_info, **kwargs):
                    return True
            except Exception:
                pass

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        """Convert with primary, fallback on failure."""
        data = file_stream.read()

        # Try primary (glmocr)
        if self._primary:
            try:
                result = self._primary.convert(io_bytes(data), stream_info, **kwargs)
                if result.markdown and result.markdown.strip():
                    logger.info("✓ glmocr succeeded")
                    return result
                logger.warning("glmocr returned empty result, falling back")
            except Exception as e:
                logger.warning("glmocr failed: %s, falling back to paddleocr", e)

        # Fallback (paddleocr)
        if self._fallback:
            try:
                result = self._fallback.convert(io_bytes(data), stream_info, **kwargs)
                if result.markdown and result.markdown.strip():
                    logger.info("✓ paddleocr succeeded (fallback)")
                    return result
                logger.warning("paddleocr returned empty result")
            except Exception as e:
                logger.error("paddleocr also failed: %s", e)

        # Both failed
        return DocumentConverterResult(
            markdown="<!-- Both OCR engines (glmocr, paddleocr) failed to convert this file -->"
        )

    def close(self):
        if self._primary and hasattr(self._primary, "close"):
            self._primary.close()
        if self._fallback and hasattr(self._fallback, "close"):
            self._fallback.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def io_bytes(data: bytes):
    """Create a seekable BytesIO from bytes."""
    import io

    buf = io.BytesIO(data)
    buf.seek(0)
    return buf
