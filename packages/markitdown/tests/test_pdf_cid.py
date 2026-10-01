#!/usr/bin/env python3 -m pytest
"""Tests for CID decoding of LaTeX math PDFs (on by default; decode_cid=False to opt out).

LaTeX engines embed Computer Modern math glyphs without a ToUnicode CMap, so
pdfminer emits them as literal (cid:N) tokens. The decoder resolves them
font-aware. Fixtures:

* test_math_cid.pdf - a pdflatex document whose math produces CMEX10 (cid:N).
* test.pdf          - a clean Unicode PDF with no (cid:N) tokens (control).

The CMMI/CMSY tables are checked directly against the lookup tables, since a
freshly compiled document only emits (cid:N) for the CMEX delimiters/operators
(modern pdflatex attaches ToUnicode to the symbol and Greek fonts).
"""
import os

import pytest

from markitdown import MarkItDown
from markitdown.converter_utils.pdf.cid_fonts import lookup

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
MATH_CID_PDF = os.path.join(TEST_FILES_DIR, "test_math_cid.pdf")
CLEAN_PDF = os.path.join(TEST_FILES_DIR, "test.pdf")


@pytest.fixture
def markitdown():
    return MarkItDown()


def test_math_cids_are_resolved(markitdown):
    """decode_cid=True replaces every (cid:N) and yields the expected glyphs."""
    if not os.path.exists(MATH_CID_PDF):
        pytest.skip(f"Test file not found: {MATH_CID_PDF}")

    result = markitdown.convert(MATH_CID_PDF, decode_cid=True)
    text = result.text_content

    assert "(cid:" not in text
    for glyph in ("∑", "∫", "√", "∏", "∪", "|", "⟨", "⟩"):
        assert glyph in text, f"missing decoded glyph {glyph!r}"


def test_font_tables_resolve_cmsy_cmmi():
    """CMSY/CMMI tables map their glyphs, including point-size variants."""
    assert lookup("ABCDEF+CMMI10", 64) == "∂"  # partialdiff
    assert lookup("ABCDEF+CMMI10", 11) == "α"  # alpha
    assert lookup("ABCDEF+CMMI10", 15) == "ε"  # epsilon1 (varepsilon)
    assert lookup("ABCDEF+CMMI10", 34) == "ϵ"  # epsilon (lunate)
    assert lookup("ABCDEF+CMSY10", 114) == "∇"  # nabla
    assert lookup("ABCDEF+CMSY10", 11) == "⊘"  # circledivide
    assert lookup("ABCDEF+CMSY10", 10) == "⊗"  # circlemultiply
    # Design-size and Latin Modern variants share the family table.
    assert lookup("ABCDEF+CMSY8", 48) == "′"  # prime
    assert lookup("ABCDEF+LMMI10", 11) == "α"


def test_bold_and_ams_fonts():
    """Bold-math (CMBSY/CMMIB) and AMS symbol fonts (MSAM/MSBM/LASY) resolve."""
    # Bold math fonts share the plain CM encodings.
    assert lookup("ABCDEF+CMBSY10", 0) == "−"  # bold cmsy minus
    assert lookup("ABCDEF+CMMIB10", 11) == "α"  # bold math italic alpha
    # AMS symbols.
    assert lookup("ABCDEF+MSAM10", 3) == "□"  # square
    assert lookup("ABCDEF+MSBM10", 82) == "ℝ"  # blackboard R (Letterlike U+211D)
    assert lookup("ABCDEF+MSBM10", 65) == "𝔸"  # blackboard A (1D5 block)
    # Letterlike exception overrides the double-struck range: Z is U+2124, not 1D56B.
    assert lookup("ABCDEF+MSBM10", 90) == "ℤ"
    assert lookup("ABCDEF+LASY10", 0) == "⊲"  # \lhd
    # Fallback path stays active for codes outside an authored table.
    assert lookup("ABCDEF+MSAM10", 200) is None


def test_cmex_full_coverage_and_operators():
    """Every cmex10 code 0-127 resolves, including the rarer big operators."""
    # Big operators / contour integrals added from the full AFM encoding.
    assert lookup("ABCDEF+CMEX10", 72) == "∮"  # contintegraltext
    assert lookup("ABCDEF+CMEX10", 76) == "⊕"  # circleplustext
    assert lookup("ABCDEF+CMEX10", 96) == "∐"  # coproducttext
    assert lookup("ABCDEF+CMEX10", 106) == "⌊"  # floorleftBig
    # Extensible delimiter extenders collapse to nothing (single delimiter out).
    assert lookup("ABCDEF+CMEX10", 66) == ""  # parenleftex
    # No cmex code in 0-127 is left unresolved.
    assert all(lookup("ABCDEF+CMEX10", c) is not None for c in range(128))


def test_prose_pdf_unaffected_by_decode(markitdown):
    """A CID-free prose PDF must convert identically with the flag on vs off."""
    if not os.path.exists(CLEAN_PDF):
        pytest.skip(f"Test file not found: {CLEAN_PDF}")

    off = markitdown.convert(CLEAN_PDF).text_content
    on = markitdown.convert(CLEAN_PDF, decode_cid=True).text_content

    assert on == off
    assert "(cid:" not in on


def test_decode_on_by_default(markitdown):
    """Decoding is the default: math glyphs resolve without passing the flag."""
    if not os.path.exists(MATH_CID_PDF):
        pytest.skip(f"Test file not found: {MATH_CID_PDF}")

    text = markitdown.convert(MATH_CID_PDF).text_content

    assert "(cid:" not in text
    assert "∑" in text


def test_decode_can_be_disabled(markitdown):
    """decode_cid=False opts out, leaving the raw pdfminer (cid:N) tokens."""
    if not os.path.exists(MATH_CID_PDF):
        pytest.skip(f"Test file not found: {MATH_CID_PDF}")

    text = markitdown.convert(MATH_CID_PDF, decode_cid=False).text_content

    assert "(cid:" in text
    assert "∑" not in text


def test_clean_unicode_not_corrupted(markitdown):
    """Running the decoder on a clean Unicode PDF must not mangle its text."""
    if not os.path.exists(CLEAN_PDF):
        pytest.skip(f"Test file not found: {CLEAN_PDF}")

    result = markitdown.convert(CLEAN_PDF, decode_cid=True)
    text = result.text_content

    # A known prose sentence from the document survives intact, no comments injected.
    assert (
        "While there is contemporaneous exploration of multi-agent approaches" in text
    )
    assert "<!-- FORMULA:" not in text


if __name__ == "__main__":
    import sys

    pytest.main([__file__] + sys.argv[1:])
