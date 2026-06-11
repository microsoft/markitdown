import io
from pathlib import Path

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.streaming import (
    PdfStreamingConverter,
    PptxStreamingConverter,
    StreamingConverterController,
)

TEST_FILES_DIR = Path(__file__).parent / "test_files"

MULTIPAGE_PDF = TEST_FILES_DIR / "REPAIR-2022-INV-001_multipage.pdf"
PROSE_PDF = TEST_FILES_DIR / "test.pdf"
PPTX_FILE = TEST_FILES_DIR / "test.pptx"


@pytest.fixture
def controller():
    return StreamingConverterController()


def test_pdf_streams_one_fragment_per_content_page(controller):
    with open(MULTIPAGE_PDF, "rb") as f:
        fragments = list(controller.iter_markdown(f, StreamInfo(extension=".pdf")))

    assert len(fragments) == 3
    assert all(fragment.strip() for fragment in fragments)


def test_pdf_streaming_matches_standard_converter_for_table_documents(controller):
    """Documents with form/table pages use the same per-page extraction as
    the standard converter, so output is identical."""
    with open(MULTIPAGE_PDF, "rb") as f:
        fragments = list(controller.iter_markdown(f, StreamInfo(extension=".pdf")))
    streamed = "\n\n".join(fragments).strip()

    with open(MULTIPAGE_PDF, "rb") as f:
        full = (
            MarkItDown()
            .convert_stream(f, stream_info=StreamInfo(extension=".pdf"))
            .markdown
        )

    assert streamed == full


def test_pptx_streams_one_fragment_per_slide(controller):
    with open(PPTX_FILE, "rb") as f:
        fragments = list(controller.iter_markdown(f, StreamInfo(extension=".pptx")))

    assert len(fragments) > 1
    for slide_num, fragment in enumerate(fragments, start=1):
        assert f"<!-- Slide number: {slide_num} -->" in fragment


def test_pptx_streaming_matches_standard_converter_exactly(controller):
    with open(PPTX_FILE, "rb") as f:
        fragments = list(controller.iter_markdown(f, StreamInfo(extension=".pptx")))
    streamed = "\n\n".join(fragments).strip()

    with open(PPTX_FILE, "rb") as f:
        full = (
            MarkItDown()
            .convert_stream(f, stream_info=StreamInfo(extension=".pptx"))
            .markdown
        )

    assert streamed == full


def test_prose_pdf_still_produces_content(controller):
    """Prose PDFs stream per-page text (the standard converter re-extracts
    them in one pass, so whitespace may differ — content must not)."""
    with open(PROSE_PDF, "rb") as f:
        fragments = list(controller.iter_markdown(f, StreamInfo(extension=".pdf")))

    assert fragments
    combined = "\n\n".join(fragments)
    assert "While there is contemporaneous exploration" in combined


def test_unknown_format_returns_none(controller):
    stream = io.BytesIO(b"plain text content")
    assert controller.iter_markdown(stream, StreamInfo(extension=".txt")) is None


def test_mislabeled_pdf_rejected_by_magic_check(controller):
    stream = io.BytesIO(b"this is not a pdf")
    assert controller.converter_for(stream, StreamInfo(extension=".pdf")) is None
    # The accepts() probe must not consume the stream.
    assert stream.tell() == 0


def test_mislabeled_pptx_rejected_by_magic_check(controller):
    stream = io.BytesIO(b"this is not a zip archive")
    assert controller.converter_for(stream, StreamInfo(extension=".pptx")) is None
    assert stream.tell() == 0


def test_pdf_accepts_by_mimetype():
    converter = PdfStreamingConverter()
    with open(MULTIPAGE_PDF, "rb") as f:
        assert converter.accepts(f, StreamInfo(mimetype="application/pdf"))
        assert f.tell() == 0


def test_pptx_accepts_by_mimetype():
    converter = PptxStreamingConverter()
    with open(PPTX_FILE, "rb") as f:
        assert converter.accepts(
            f,
            StreamInfo(
                mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            ),
        )
        assert f.tell() == 0


def test_no_hints_returns_none(controller):
    with open(MULTIPAGE_PDF, "rb") as f:
        assert controller.converter_for(f, StreamInfo()) is None
