#!/usr/bin/env python3 -m pytest
"""Tests for the opt-in `source_anchors` option.

The option makes converters emit stable source coordinates so that extracted
text can be cited back to its location in the original file. It must be a pure
addition: with the option off, output is unchanged.
"""

import io
import os
import re

import pytest

from markitdown import MarkItDown

skip_deps = False
try:
    import pdfminer  # noqa: F401
    import pdfplumber  # noqa: F401
    import pandas as pd  # noqa: F401
    import openpyxl  # noqa: F401
except ImportError:
    skip_deps = True

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

MULTIPAGE_PDF = os.path.join(TEST_FILES_DIR, "REPAIR-2022-INV-001_multipage.pdf")
TABLE_PDF = os.path.join(TEST_FILES_DIR, "SPARSE-2024-INV-1234_borderless_table.pdf")
PROSE_PDF = os.path.join(TEST_FILES_DIR, "test.pdf")
XLSX_FILE = os.path.join(TEST_FILES_DIR, "test.xlsx")

PAGE_ANCHOR_RE = re.compile(r"^<!-- Page number: (\d+) -->$", re.MULTILINE)


@pytest.mark.skipif(skip_deps, reason="pdf/xlsx dependencies not installed")
@pytest.mark.parametrize("path", [PROSE_PDF, MULTIPAGE_PDF, TABLE_PDF, XLSX_FILE])
def test_default_output_is_unchanged(path):
    """Omitting the option, and passing it as False, must produce identical output."""
    markitdown = MarkItDown()
    assert (
        markitdown.convert(path).markdown
        == markitdown.convert(path, source_anchors=False).markdown
    )


@pytest.mark.skipif(skip_deps, reason="pdf dependencies not installed")
@pytest.mark.parametrize("path", [PROSE_PDF, MULTIPAGE_PDF, TABLE_PDF])
def test_pdf_pages_are_anchored(path):
    """Every emitted page carries an anchor, numbered from 1 without gaps."""
    result = MarkItDown().convert(path, source_anchors=True)
    pages = [int(m) for m in PAGE_ANCHOR_RE.findall(result.markdown)]

    assert pages, "no page anchors were emitted"
    assert pages == sorted(pages), "page anchors are out of order"
    assert len(pages) == len(set(pages)), "duplicate page anchors"
    assert pages[0] == 1, "page numbering does not start at 1"

    with pdfplumber.open(path) as pdf:
        assert pages[-1] <= len(pdf.pages), "anchor exceeds the document page count"


@pytest.mark.skipif(skip_deps, reason="pdf dependencies not installed")
def test_pdf_anchor_locates_text_on_the_right_page():
    """Text found under an anchor must actually live on that page of the PDF."""
    path = MULTIPAGE_PDF
    result = MarkItDown().convert(path, source_anchors=True)

    # Split the anchored output into (page number, body) pairs.
    parts = re.split(
        r"^<!-- Page number: (\d+) -->$", result.markdown, flags=re.MULTILINE
    )
    sections = list(zip(parts[1::2], parts[2::2]))
    assert sections, "no anchored sections found"

    with pdfplumber.open(path) as pdf:
        for page_number, body in sections:
            page_text = pdf.pages[int(page_number) - 1].extract_text() or ""
            page_words = set(re.findall(r"\w+", page_text.lower()))
            body_words = [w for w in re.findall(r"\w+", body.lower()) if len(w) > 3]
            if not body_words or not page_words:
                continue
            overlap = sum(1 for w in body_words if w in page_words) / len(body_words)
            assert overlap > 0.5, (
                f"page {page_number}: only {overlap:.0%} of the anchored text "
                f"appears on that page of the PDF"
            )


@pytest.mark.skipif(skip_deps, reason="pdf dependencies not installed")
def test_pdf_anchors_do_not_appear_by_default():
    result = MarkItDown().convert(MULTIPAGE_PDF)
    assert "<!-- Page number:" not in result.markdown


@pytest.mark.skipif(skip_deps, reason="xlsx dependencies not installed")
def test_xlsx_sheets_and_rows_are_anchored():
    result = MarkItDown().convert(XLSX_FILE, source_anchors=True)

    sheets = pd.read_excel(XLSX_FILE, sheet_name=None, engine="openpyxl")
    for sheet_name, frame in sheets.items():
        assert f"<!-- Sheet name: {sheet_name} -->" in result.markdown

        # Row numbers are 1-based spreadsheet rows: the header is row 1, so the
        # last data row is len(frame) + 1.
        if len(frame) > 0:
            assert re.search(r"\|\s*2\s*\|", result.markdown), "first data row missing"

    assert "xlsx-row" in result.markdown.replace("\\", "")


@pytest.mark.skipif(skip_deps, reason="xlsx dependencies not installed")
def test_xlsx_anchors_do_not_appear_by_default():
    result = MarkItDown().convert(XLSX_FILE)
    assert "<!-- Sheet name:" not in result.markdown
    assert "xlsx-row" not in result.markdown.replace("\\", "")


@pytest.mark.skipif(skip_deps, reason="pdf dependencies not installed")
def test_anchors_work_on_streams():
    """The option must reach converters through convert_stream as well."""
    with open(MULTIPAGE_PDF, "rb") as fh:
        data = fh.read()
    result = MarkItDown().convert_stream(
        io.BytesIO(data), file_extension=".pdf", source_anchors=True
    )
    assert "<!-- Page number: 1 -->" in result.markdown


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__, "-v"]))
