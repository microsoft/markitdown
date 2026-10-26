#!/usr/bin/env python3 -m pytest
"""Tests for the default n-ary operator in DOCX math conversion.

``m:chr`` under ``m:naryPr`` names the n-ary operator. ISO/IEC 29500-1 states
that when the element is omitted the operator is U+222B INTEGRAL, so producers
write ``m:chr`` only for the non-default operators such as the summation sign.
``do_nary`` passed no default to ``get_char``, so an integral yielded ``None``
and ``None + ""`` raised ``TypeError``.

That failure is not local to the equation. ``pre_process_docx`` runs
``_pre_process_math`` over the whole of ``word/document.xml`` inside a blanket
``except Exception`` and, on error, writes the *original* unprocessed XML back.
Mammoth does not render OMML, so one integral silently removes every equation
in the document.
"""

from xml.etree import ElementTree as ET

from markitdown.converter_utils.docx.math.omml import OMML_NS, oMath2Latex

MATH_NS_DECL = f'xmlns:m="{OMML_NS[1:-1]}"'

SUMMATION = "∑"  # N-ARY SUMMATION, written out by Word as it is not the default


def _nary(nary_pr: str):
    xml = (
        f"<m:oMath {MATH_NS_DECL}><m:nary>"
        f"{nary_pr}"
        "<m:sub><m:r><m:t>0</m:t></m:r></m:sub>"
        "<m:sup><m:r><m:t>1</m:t></m:r></m:sup>"
        "<m:e><m:r><m:t>x</m:t></m:r></m:e>"
        "</m:nary></m:oMath>"
    )
    return oMath2Latex(ET.fromstring(xml)).latex


def test_nary_without_chr_defaults_to_integral():
    # No m:chr, so the operator is U+222B. Previously raised TypeError.
    latex = _nary('<m:naryPr><m:limLoc m:val="subSup"/><m:ctrlPr/></m:naryPr>')
    assert latex == "\\int_{0}^{1}x"


def test_nary_with_explicit_chr_is_unchanged():
    latex = _nary(f'<m:naryPr><m:chr m:val="{SUMMATION}"/></m:naryPr>')
    assert latex == "\\sum_{0}^{1}x"


def test_nary_without_nary_pr_defaults_to_integral():
    # m:naryPr is optional. Absent, every property takes its default, so the
    # operator is still U+222B rather than nothing.
    assert _nary("") == "\\int_{0}^{1}x"
