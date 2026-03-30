import sys
import types
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StreamInfo:
    extension: str | None = None
    mimetype: str | None = None


class StubMarkItDown:
    def __init__(self) -> None:
        self.calls = []

    def register_converter(self, converter, *, priority=0.0):  # noqa: ANN001, ANN201
        self.calls.append((converter, priority))


markitdown_module = types.ModuleType("markitdown")
markitdown_module.MarkItDown = StubMarkItDown
markitdown_module.StreamInfo = StreamInfo

sys.modules["markitdown"] = markitdown_module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from markitdown_paddleocr import register_converters  # noqa: E402
from markitdown_paddleocr._ocr_service import PaddleOCRService  # noqa: E402


def test_registers_pdf_converter_even_when_disabled() -> None:
    md = StubMarkItDown()
    register_converters(md)
    assert len(md.calls) == 1
    _, priority = md.calls[0]
    assert priority == -1.0


def test_registers_enabled_service_with_kwargs() -> None:
    md = StubMarkItDown()
    register_converters(
        md,
        paddleocr_enabled=True,
        paddleocr_lang="en",
        paddleocr_kwargs={"use_doc_orientation_classify": False},
    )
    converter, _ = md.calls[0]
    assert isinstance(converter.ocr_service, PaddleOCRService)
    assert converter.ocr_service._lang == "en"  # noqa: SLF001
    assert converter.ocr_service._paddleocr_kwargs == {  # noqa: SLF001
        "use_doc_orientation_classify": False
    }
