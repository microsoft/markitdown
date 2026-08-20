#!/usr/bin/env python3 -m pytest
import io
from unittest.mock import MagicMock, patch

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters._pdf_converter import PdfConverter


PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde"
)


def _mock_pdfplumber_open(pages):
    def mock_open(stream):
        mock_pdf = MagicMock()
        mock_pdf.pages = pages
        mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
        mock_pdf.__exit__ = MagicMock(return_value=False)
        return mock_pdf

    return mock_open


def _make_pdf_page():
    stream = MagicMock()
    stream.get_data.return_value = PNG_BYTES

    page = MagicMock()
    page.width = 612
    page.height = 792
    page.images = [
        {
            "x0": 72,
            "x1": 144,
            "top": 40,
            "bottom": 120,
            "stream": stream,
        }
    ]
    page.extract_words.return_value = [
        {"text": "Before", "x0": 72, "x1": 120, "top": 10, "bottom": 20},
        {"text": "After", "x0": 72, "x1": 110, "top": 180, "bottom": 190},
    ]
    page.extract_text_lines.return_value = [
        {"text": "Before image", "top": 10},
        {"text": "After image", "top": 180},
    ]
    page.close = MagicMock()
    return page


def test_pdf_extract_images_writes_files_and_relative_links(tmp_path):
    page = _make_pdf_page()

    with patch(
        "markitdown.converters._pdf_converter._dependency_exc_info", None
    ), patch("markitdown.converters._pdf_converter.pdfplumber") as mock_pdfplumber:
        mock_pdfplumber.open.side_effect = _mock_pdfplumber_open([page])

        result = PdfConverter().convert(
            io.BytesIO(b"%PDF mock"),
            StreamInfo(extension=".pdf", mimetype="application/pdf"),
            extract_images=True,
            output_dir=tmp_path,
        )

    image_path = tmp_path / "images" / "page1-image1.png"
    assert image_path.exists()
    assert image_path.read_bytes().startswith(b"\x89PNG")
    assert "![Image 1 on page 1](images/page1-image1.png)" in result.markdown
    assert result.markdown.index("Before image") < result.markdown.index(
        "images/page1-image1.png"
    )
    assert result.markdown.index("images/page1-image1.png") < result.markdown.index(
        "After image"
    )
    assert "data:image" not in result.markdown
    assert page.close.called


def test_extract_images_requires_output_dir_in_constructor():
    with pytest.raises(ValueError, match="output_dir is required"):
        MarkItDown(extract_images=True)


def test_extract_images_requires_output_dir_per_call():
    md = MarkItDown()
    with pytest.raises(ValueError, match="output_dir is required"):
        md.convert_stream(
            io.BytesIO(b"%PDF mock"),
            stream_info=StreamInfo(extension=".pdf", mimetype="application/pdf"),
            extract_images=True,
        )
