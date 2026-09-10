import io
import sys
import types
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch


class DocumentConverter:
    pass


class MarkItDown:
    pass


@dataclass
class DocumentConverterResult:
    markdown: str


@dataclass
class StreamInfo:
    extension: str | None = None
    mimetype: str | None = None


class MissingDependencyException(Exception):
    pass


markitdown_module = types.ModuleType("markitdown")
markitdown_module.DocumentConverter = DocumentConverter
markitdown_module.DocumentConverterResult = DocumentConverterResult
markitdown_module.MarkItDown = MarkItDown
markitdown_module.StreamInfo = StreamInfo

exceptions_module = types.ModuleType("markitdown._exceptions")
exceptions_module.MissingDependencyException = MissingDependencyException
exceptions_module.MISSING_DEPENDENCY_MESSAGE = "{converter} requires {feature}"

converters_module = types.ModuleType("markitdown.converters")
pdfplumber_module = types.ModuleType("pdfplumber")


class PdfConverter:
    def convert(self, file_stream, stream_info, **kwargs):  # noqa: ANN001, ANN201
        return DocumentConverterResult(markdown="")


def _pdfplumber_open(*args, **kwargs):  # noqa: ANN001, ANN202
    raise RuntimeError("pdfplumber unavailable in unit test")


converters_module.PdfConverter = PdfConverter
pdfplumber_module.open = _pdfplumber_open

sys.modules["markitdown"] = markitdown_module
sys.modules["markitdown._exceptions"] = exceptions_module
sys.modules["markitdown.converters"] = converters_module
sys.modules["pdfplumber"] = pdfplumber_module

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_paddleocr._ocr_service import OCRResult, PaddleOCRService  # noqa: E402
from markitdown_paddleocr._pdf_converter import PdfConverterWithPaddleOCR  # noqa: E402


class StubPdfConverter:
    def __init__(self, markdown: str) -> None:
        self.markdown = markdown

    def convert(self, file_stream, stream_info, **kwargs):  # noqa: ANN001, ANN201
        return DocumentConverterResult(markdown=self.markdown)


class StubOCRService:
    def __init__(self, text: str) -> None:
        self.text = text

    def extract_text(self, image_stream):  # noqa: ANN001, ANN201
        return OCRResult(text=self.text, backend_used="paddleocr")


class _FakePageImage:
    def __init__(self) -> None:
        self.original = self

    def save(self, stream, format="PNG"):  # noqa: ANN001, ANN201
        stream.write(b"fake-image")


class _FakePage:
    def to_image(self, resolution=300):  # noqa: ANN001, ANN201
        return _FakePageImage()


class _FakePdf:
    def __init__(self) -> None:
        self.pages = [_FakePage()]

    def __enter__(self):  # noqa: ANN204
        return self

    def __exit__(self, exc_type, exc, tb):  # noqa: ANN001, ANN204
        return False


def test_returns_builtin_result_when_text_exists() -> None:
    converter = PdfConverterWithPaddleOCR(
        pdf_converter=StubPdfConverter("already extracted")
    )
    result = converter.convert(
        io.BytesIO(b"fake"),
        StreamInfo(extension=".pdf"),
    )
    assert result.markdown == "already extracted"


def test_returns_builtin_result_when_ocr_disabled() -> None:
    converter = PdfConverterWithPaddleOCR(pdf_converter=StubPdfConverter(""))
    result = converter.convert(
        io.BytesIO(b"fake"),
        StreamInfo(extension=".pdf"),
    )
    assert result.markdown == ""


def test_pymupdf_fallback_error_path_when_no_renderer_available() -> None:
    converter = PdfConverterWithPaddleOCR(pdf_converter=StubPdfConverter(""))
    result = converter.convert(
        io.BytesIO(b"fake"),
        StreamInfo(extension=".pdf"),
        ocr_service=StubOCRService(""),
    )
    assert result.markdown == "*[Error: Could not process scanned PDF]*"


def test_ocr_full_pages_formats_markdown_output() -> None:
    converter = PdfConverterWithPaddleOCR(pdf_converter=StubPdfConverter(""))
    with patch("markitdown_paddleocr._pdf_converter.pdfplumber.open", return_value=_FakePdf()):
        result = converter.convert(
            io.BytesIO(b"fake"),
            StreamInfo(extension=".pdf"),
            ocr_service=StubOCRService("hello\nworld"),
        )

    assert result.markdown == "## Page 1\n\n*[Image OCR]\nhello\nworld\n[End OCR]*"


def test_ocr_service_extracts_texts_from_nested_result() -> None:
    service = PaddleOCRService(ocr_instance=object())
    parsed = service._result_to_text(  # noqa: SLF001
        [{"res": {"rec_texts": ["alpha", "beta"]}}]
    )
    assert parsed == "alpha\nbeta"


def test_ocr_service_extracts_text_from_single_key() -> None:
    service = PaddleOCRService(ocr_instance=object())
    parsed = service._result_to_text({"rec_text": "single"})
    assert parsed == "single"
