#!/usr/bin/env python3 -m pytest
import io
from unittest.mock import ANY, MagicMock, call, patch

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import PdfConverter


def _make_page(text: str | None) -> MagicMock:
    page = MagicMock()
    page.extract_text.return_value = text
    return page


def _mock_pdfplumber_open(pages: list[MagicMock]):
    def mock_open(stream):
        pdf = MagicMock()
        pdf.pages = pages
        pdf.__enter__.return_value = pdf
        pdf.__exit__.return_value = False
        return pdf

    return mock_open


def _convert_with_markers(pages: list[MagicMock]):
    with patch(
        "markitdown.converters._pdf_converter.pdfplumber.open",
        side_effect=_mock_pdfplumber_open(pages),
    ), patch(
        "markitdown.converters._pdf_converter._extract_form_content_from_words",
        return_value=None,
    ):
        return MarkItDown().convert_stream(
            io.BytesIO(b"pdf"),
            stream_info=StreamInfo(extension=".pdf"),
            pdf_page_markers=True,
        )


def test_default_pdf_output_remains_unmarked() -> None:
    pages = [_make_page("pdfplumber text")]
    with patch(
        "markitdown.converters._pdf_converter.pdfplumber.open",
        side_effect=_mock_pdfplumber_open(pages),
    ), patch(
        "markitdown.converters._pdf_converter._extract_form_content_from_words",
        return_value=None,
    ), patch(
        "markitdown.converters._pdf_converter.pdfminer.high_level.extract_text",
        return_value="default output",
    ):
        result = MarkItDown().convert_stream(
            io.BytesIO(b"pdf"),
            stream_info=StreamInfo(extension=".pdf"),
        )

    assert result.markdown == "default output"
    assert "<!-- page" not in result.markdown


def test_plain_text_pages_have_one_based_markers_in_order() -> None:
    result = _convert_with_markers(
        [_make_page("first"), _make_page("second"), _make_page("third")]
    )

    assert result.markdown == (
        "<!-- page 1 -->\n\nfirst\n\n"
        "<!-- page 2 -->\n\nsecond\n\n"
        "<!-- page 3 -->\n\nthird"
    )


def test_empty_pages_keep_their_page_index() -> None:
    result = _convert_with_markers(
        [_make_page("first"), _make_page(None), _make_page("third")]
    )

    assert result.markdown == (
        "<!-- page 1 -->\n\nfirst\n\n"
        "<!-- page 2 -->\n\n"
        "<!-- page 3 -->\n\nthird"
    )


def test_table_and_plain_text_pages_preserve_boundaries() -> None:
    pages = [_make_page(None), _make_page("plain text")]
    with patch(
        "markitdown.converters._pdf_converter.pdfplumber.open",
        side_effect=_mock_pdfplumber_open(pages),
    ), patch(
        "markitdown.converters._pdf_converter._extract_form_content_from_words",
        side_effect=["| Name | Value |\n| --- | --- |\n| A | 1 |", None],
    ):
        result = MarkItDown().convert_stream(
            io.BytesIO(b"pdf"),
            stream_info=StreamInfo(extension=".pdf"),
            pdf_page_markers=True,
        )

    assert result.markdown == (
        "<!-- page 1 -->\n\n"
        "| Name | Value |\n| --- | --- |\n| A | 1 |\n\n"
        "<!-- page 2 -->\n\nplain text"
    )


def test_page_extraction_failure_falls_back_only_for_that_page() -> None:
    pages = [_make_page("unused"), _make_page("second")]
    with patch(
        "markitdown.converters._pdf_converter.pdfplumber.open",
        side_effect=_mock_pdfplumber_open(pages),
    ), patch(
        "markitdown.converters._pdf_converter._extract_form_content_from_words",
        side_effect=[RuntimeError("page failure"), None],
    ), patch(
        "markitdown.converters._pdf_converter.pdfminer.high_level.extract_text",
        return_value="fallback first",
    ) as extract_text:
        result = MarkItDown().convert_stream(
            io.BytesIO(b"pdf"),
            stream_info=StreamInfo(extension=".pdf"),
            pdf_page_markers=True,
        )

    assert result.markdown == (
        "<!-- page 1 -->\n\nfallback first\n\n"
        "<!-- page 2 -->\n\nsecond"
    )
    extract_text.assert_called_once()
    assert extract_text.call_args.kwargs["page_numbers"] == [0]


def test_pdfplumber_failure_falls_back_page_by_page() -> None:
    with patch(
        "markitdown.converters._pdf_converter.pdfplumber.open",
        side_effect=RuntimeError("open failure"),
    ), patch(
        "markitdown.converters._pdf_converter.pdfminer.pdfpage.PDFPage.get_pages",
        return_value=iter([object(), object(), object()]),
    ), patch(
        "markitdown.converters._pdf_converter.pdfminer.high_level.extract_text",
        side_effect=["first", "", "third"],
    ) as extract_text:
        result = PdfConverter().convert(
            io.BytesIO(b"pdf"),
            StreamInfo(extension=".pdf"),
            pdf_page_markers=True,
        )

    assert result.markdown == (
        "<!-- page 1 -->\n\nfirst\n\n"
        "<!-- page 2 -->\n\n"
        "<!-- page 3 -->\n\nthird"
    )
    assert extract_text.call_args_list == [
        call(ANY, page_numbers=[0]),
        call(ANY, page_numbers=[1]),
        call(ANY, page_numbers=[2]),
    ]


def test_page_fallback_failure_is_not_replaced_by_whole_document_output() -> None:
    page = _make_page("unused")
    with patch(
        "markitdown.converters._pdf_converter.pdfplumber.open",
        side_effect=_mock_pdfplumber_open([page]),
    ), patch(
        "markitdown.converters._pdf_converter._extract_form_content_from_words",
        side_effect=RuntimeError("page failure"),
    ), patch(
        "markitdown.converters._pdf_converter.pdfminer.high_level.extract_text",
        side_effect=RuntimeError("fallback failure"),
    ) as extract_text:
        with pytest.raises(RuntimeError, match="fallback failure"):
            PdfConverter().convert(
                io.BytesIO(b"pdf"),
                StreamInfo(extension=".pdf"),
                pdf_page_markers=True,
            )

    extract_text.assert_called_once()
    page.close.assert_called_once()
