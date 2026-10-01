"""Page references preserve physical positions without changing default output."""

import io
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pdfminer.pdfparser import PDFSyntaxError

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import PdfConverter
from markitdown.converters._pdf_converter import (
    _extract_pdfminer_pages,
    _pdf_source_uri,
)

PDF = Path(__file__).parent / "test_files/test.pdf"


def test_default_output_is_unchanged():
    converter = MarkItDown()
    assert (
        converter.convert(PDF).markdown
        == converter.convert(PDF, pdf_page_links=False).markdown
    )


def test_real_pages_and_pdfminer_fallback_match():
    with PDF.open("rb") as stream:
        pages = _extract_pdfminer_pages(stream)
    assert pages
    converter = MarkItDown()
    result = converter.convert(PDF, pdf_page_links=True).markdown
    for index, body in enumerate(pages, 1):
        assert f"[Page {index}](<{PDF.resolve().as_uri()}#page={index}>)" in result
        assert body.strip() in result
    with patch(
        "markitdown.converters._pdf_converter.pdfplumber.open",
        side_effect=RuntimeError("open failed"),
    ):
        assert converter.convert(PDF, pdf_page_links=True).markdown == result


def test_real_blank_middle_page_keeps_physical_index():
    path = PDF.with_name("test_pdf_blank_middle.pdf")
    with path.open("rb") as stream:
        pages = _extract_pdfminer_pages(stream)
    assert len(pages) == 3
    assert [page.strip() for page in pages] == ["First page", "", "Third page"]
    result = MarkItDown().convert(path, pdf_page_links=True).markdown
    sections = result.split("[Page ")[1:]
    assert len(sections) == 3
    assert sections[0].startswith("1]") and sections[2].startswith("3]")
    assert sections[1].startswith("2]")
    assert not sections[1].split(">)", 1)[1].strip()


def test_mixed_pages_keep_blank_page_and_newline_cleanup():
    pages = [MagicMock(), MagicMock(), MagicMock()]
    pdf = MagicMock()
    pdf.__enter__.return_value.pages = pages
    pages[1].extract_text.return_value = ""
    pages[2].extract_text.return_value = ".1\nlast page"
    with patch(
        "markitdown.converters._pdf_converter.pdfplumber.open", return_value=pdf
    ), patch(
        "markitdown.converters._pdf_converter._extract_form_content_from_words",
        side_effect=["| A | B |", None, None],
    ):
        result = (
            PdfConverter()
            .convert(
                io.BytesIO(b"pdf"),
                StreamInfo(url="https://example.org/paper.pdf?download=1#old"),
                pdf_page_links=True,
            )
            .markdown
        )
    assert result == (
        "[Page 1](<https://example.org/paper.pdf?download=1#page=1>)\n\n| A | B |\n\n"
        "[Page 2](<https://example.org/paper.pdf?download=1#page=2>)\n\n\n\n"
        "[Page 3](<https://example.org/paper.pdf?download=1#page=3>)\n\n.1 last page"
    )
    for page in pages:
        page.close.assert_called_once()


def test_encoded_sources_and_override(tmp_path):
    path = tmp_path / "r\u00e9sum\u00e9 # (1).pdf"
    assert _pdf_source_uri(str(path)) == path.as_uri()
    assert _pdf_source_uri("https://example.org/a b.pdf?x=1#old") == (
        "https://example.org/a%20b.pdf?x=1"
    )
    result = (
        MarkItDown()
        .convert(PDF, pdf_page_links=True, pdf_source="https://example.org/paper.pdf")
        .markdown
    )
    assert "https://example.org/paper.pdf#page=1" in result
    assert "file:" not in result


def test_stream_requires_source_and_invalid_pdf_still_fails():
    with PDF.open("rb") as stream:
        with pytest.raises(ValueError, match="require a source"):
            PdfConverter().convert(stream, StreamInfo(), pdf_page_links=True)
    with pytest.raises(PDFSyntaxError):
        PdfConverter().convert(
            io.BytesIO(b"invalid pdf"),
            StreamInfo(local_path="paper.pdf"),
            pdf_page_links=True,
        )
    with pytest.raises(ValueError, match="local path"):
        _pdf_source_uri("javascript:alert(1)")


def test_pdfminer_boundaries_do_not_depend_on_form_feeds():
    bodies = ["first\finside\f\f", "\f", "third\f"]
    with patch(
        "markitdown.converters._pdf_converter.PDFPage.get_pages",
        return_value=iter(bodies),
    ), patch(
        "markitdown.converters._pdf_converter.PDFPageInterpreter.process_page",
        autospec=True,
        side_effect=lambda interpreter, body: interpreter.device.outfp.write(body),
    ):
        assert _extract_pdfminer_pages(io.BytesIO()) == ["first\finside\f", "", "third"]


def test_cli_forwards_pdf_options(monkeypatch, capsys):
    from markitdown import DocumentConverterResult
    from markitdown.__main__ import main

    convert = MagicMock(return_value=DocumentConverterResult(markdown="linked"))
    monkeypatch.setattr("markitdown.__main__.MarkItDown.convert", convert)
    monkeypatch.setattr(
        "sys.argv",
        ["markitdown", "--pdf-page-links", "--pdf-source", "paper.pdf", "input.pdf"],
    )
    main()
    assert convert.call_args.kwargs["pdf_page_links"] is True
    assert convert.call_args.kwargs["pdf_source"] == "paper.pdf"
    assert capsys.readouterr().out.strip() == "linked"
