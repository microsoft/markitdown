# -*- coding: utf-8 -*-
"""
Regression test for a crash in the OMML -> LaTeX converter when a math run
(<m:r>) has no <m:t> text child (e.g. a run that only carries formatting
properties). Previously `do_r()` called `elm.findtext(...)` directly and
iterated over the result, which raised `TypeError: 'NoneType' object is not
iterable` when the run had no text, aborting equation conversion for the
entire document.
"""

from xml.etree import ElementTree as ET

from markitdown.converter_utils.docx.math.omml import OMML_NS, oMath2Latex

MATH_NS_DECL = f'xmlns:m="{OMML_NS[1:-1]}"'


def _parse_omath(xml_fragment: str):
    wrapped = f"<m:oMath {MATH_NS_DECL}>{xml_fragment}</m:oMath>"
    return ET.fromstring(wrapped)


def test_run_without_text_child_does_not_crash():
    # <m:r> with only <m:rPr>, no <m:t> child.
    element = _parse_omath("<m:r><m:rPr/></m:r>")
    # Should not raise TypeError: 'NoneType' object is not iterable
    result = oMath2Latex(element)
    assert result.latex == ""


def test_run_with_text_still_converts():
    element = _parse_omath("<m:r><m:t>x</m:t></m:r>")
    result = oMath2Latex(element)
    assert result.latex == "x"


def test_subscript_with_missing_text_run_does_not_crash():
    # Mirrors a real-world document: a subscript expression where one of the
    # runs involved has no text (e.g. produced by some Word equation editors).
    element = _parse_omath(
        "<m:sSub>"
        "<m:e><m:r><m:t>l</m:t></m:r></m:e>"
        "<m:sub><m:r><m:rPr/></m:r><m:r><m:t>1</m:t></m:r></m:sub>"
        "</m:sSub>"
    )
    result = oMath2Latex(element)
    assert "l" in result.latex
    assert "1" in result.latex
