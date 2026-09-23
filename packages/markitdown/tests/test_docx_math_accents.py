#!/usr/bin/env python3 -m pytest
"""Tests for DOCX math accent templates.

Every accent in ``latex_dict.CHR`` is a ``str.format`` template applied by
``oMath2Latex.do_acc`` as ``latex_s.format(c_dict["e"])``. A template whose
braces are unbalanced raises ``ValueError`` at that call.

That failure is not local to the equation. ``pre_process_docx`` runs
``_pre_process_math`` over the whole of ``word/document.xml`` inside a blanket
``except Exception`` and, on error, writes the *original* unprocessed XML back.
Mammoth does not render OMML, so a single unformattable accent silently removes
every equation in the document -- with no error and a zero exit code.

``test_accent_templates_are_formattable`` guards the whole table against that
class of typo; ``test_caron_and_ring_accents`` covers the two entries that
carried an extra closing brace.
"""

from markitdown.converter_utils.docx.math.latex_dict import (
    CHR,
    CHR_BO,
    CHR_DEFAULT,
    POS,
    POS_DEFAULT,
)
from markitdown.converter_utils.docx.math.omml import load_string

# Accent characters, as Word writes them into <m:chr m:val="...">.
CARON = "\u030c"  # COMBINING CARON        -> \check
RING_ABOVE = "\u030a"  # COMBINING RING ABOVE   -> \ocirc
CIRCUMFLEX = "\u0302"  # COMBINING CIRCUMFLEX   -> \hat

_OMML_DOC = (
    "<w:document "
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
    "<m:oMath><m:acc>"
    '<m:accPr><m:chr m:val="{chr}"/></m:accPr>'
    "<m:e><m:r><m:t>x</m:t></m:r></m:e>"
    "</m:acc></m:oMath></w:document>"
)


def _latex_for_accent(accent_char: str) -> str:
    """Convert a single accented variable to LaTeX, as pre_process_docx would."""
    return next(load_string(_OMML_DOC.format(chr=accent_char))).latex


def test_accent_templates_are_formattable() -> None:
    """Every {0} template must survive .format(); do_acc calls it unguarded."""
    unformattable = []
    for name, table in (
        ("CHR", CHR),
        ("CHR_BO", CHR_BO),
        ("CHR_DEFAULT", CHR_DEFAULT),
        ("POS", POS),
        ("POS_DEFAULT", POS_DEFAULT),
    ):
        for key, template in table.items():
            if not isinstance(template, str) or "{0}" not in template:
                continue
            try:
                template.format("x")
            except ValueError as exc:
                unformattable.append(f"{name}[{key!r}] = {template!r}: {exc}")

    assert not unformattable, "unformattable accent templates: " + "; ".join(
        unformattable
    )


def test_caron_and_ring_accents() -> None:
    """U+030C and U+030A each carried an extra '}' and raised ValueError."""
    assert _latex_for_accent(CARON) == "\\check{x}"
    assert _latex_for_accent(RING_ABOVE) == "\\ocirc{x}"


def test_unmodified_accent_still_converts() -> None:
    """Control: a neighbouring accent that was never broken."""
    assert _latex_for_accent(CIRCUMFLEX) == "\\hat{x}"
