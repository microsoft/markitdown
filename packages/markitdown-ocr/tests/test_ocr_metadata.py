"""Office image metadata reaches compatible services without retrying OCR."""

import inspect
import io
from typing import Any, BinaryIO
from unittest.mock import Mock

import pytest

from markitdown import StreamInfo
from markitdown_ocr._docx_converter_with_ocr import DocxConverterWithOCR
from markitdown_ocr._ocr_service import OCRResult, _extract_text_with_metadata
from markitdown_ocr._pptx_converter_with_ocr import PptxConverterWithOCR
from markitdown_ocr._xlsx_converter_with_ocr import XlsxConverterWithOCR


_Converter = DocxConverterWithOCR | PptxConverterWithOCR | XlsxConverterWithOCR
_CONVERTERS = [DocxConverterWithOCR, PptxConverterWithOCR, XlsxConverterWithOCR]
_SVG = b'<svg xmlns="http://www.w3.org/2000/svg"><text>recognized</text></svg>'
_INFO = StreamInfo(mimetype="image/svg+xml", extension=".svg", filename="drawing.svg")


@pytest.mark.parametrize("converter_type", _CONVERTERS)
def test_bound_service_receives_metadata_by_keyword(
    converter_type: type[_Converter],
) -> None:
    seen = []

    class Service:
        def extract_text(
            self,
            image_stream: BinaryIO,
            prompt: str | None = None,
            *,
            stream_info: StreamInfo,
        ) -> OCRResult:
            assert prompt is None
            assert image_stream.tell() == 0
            seen.append((image_stream.read(), stream_info))
            return OCRResult(text="recognized")

    with io.BytesIO(_SVG) as stream:
        result = converter_type()._image_to_html(stream, _INFO, ocr_service=Service())
        assert not stream.closed

    assert seen == [(_SVG, _INFO)]
    assert seen[0][1] is _INFO
    assert result == "<p><em>[Image OCR]<br>recognized<br>[End OCR]</em></p>"


@pytest.mark.parametrize("converter_type", _CONVERTERS)
def test_service_accepting_kwargs_receives_only_image_metadata(
    converter_type: type[_Converter],
) -> None:
    seen = []

    class Service:
        def extract_text(self, image_stream: BinaryIO, **kwargs: Any) -> OCRResult:
            seen.append(kwargs)
            return OCRResult(text="recognized")

    with io.BytesIO(_SVG) as stream:
        converter_type()._image_to_html(
            stream,
            _INFO,
            ocr_service=Service(),
            url="https://example.test/parent.pptx",
            file_extension=".pptx",
        )

    assert seen == [{"stream_info": _INFO}]


@pytest.mark.parametrize("converter_type", _CONVERTERS)
def test_legacy_positional_only_service_remains_supported(
    converter_type: type[_Converter],
) -> None:
    seen = []

    class Service:
        def extract_text(self, image_stream: BinaryIO, /) -> OCRResult:
            seen.append(image_stream.read())
            return OCRResult(text="recognized")

    with io.BytesIO(_SVG) as stream:
        result = converter_type()._image_to_html(stream, _INFO, ocr_service=Service())

    assert seen == [_SVG]
    assert result == "<p><em>[Image OCR]<br>recognized<br>[End OCR]</em></p>"


@pytest.mark.parametrize("converter_type", _CONVERTERS)
def test_internal_type_error_is_not_retried(
    converter_type: type[_Converter],
) -> None:
    error = TypeError("service implementation failed")
    seen = []

    class Service:
        def extract_text(
            self, image_stream: BinaryIO, stream_info: StreamInfo | None = None
        ) -> OCRResult:
            seen.append(stream_info)
            raise error

    with io.BytesIO(_SVG) as stream:
        with pytest.raises(TypeError) as caught:
            converter_type()._image_to_html(stream, _INFO, ocr_service=Service())

    assert caught.value is error
    assert seen == [_INFO]


@pytest.mark.parametrize("signature_error", [TypeError, ValueError])
def test_uninspectable_service_retains_single_argument_invocation(
    signature_error: type[Exception],
) -> None:
    seen = []

    class Extractor:
        @property
        def __signature__(self) -> inspect.Signature:
            raise signature_error("signature unavailable")

        def __call__(self, image_stream: BinaryIO) -> OCRResult:
            seen.append(image_stream.read())
            return OCRResult(text="recognized")

    service = Mock(extract_text=Extractor())
    with io.BytesIO(_SVG) as stream:
        result = _extract_text_with_metadata(service, stream, _INFO)

    assert result.text == "recognized"
    assert seen == [_SVG]
