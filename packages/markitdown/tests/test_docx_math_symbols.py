#!/usr/bin/env python3 -m pytest
"""Tests for the OMML -> LaTeX symbol tables used by the DOCX converter.

Two independent defects are covered here:

``CHR`` maps a combining accent to a LaTeX template. U+20EE COMBINING LEFT
ARROW BELOW mapped to ``\\underledtarrow``, which is not a LaTeX macro -- the
name is a scrambled ``\\underleftarrow``. Its two neighbours in the same table
(U+20D6 -> ``\\overleftarrow``, U+20EF -> ``\\underrightarrow``) show the
intent. The template still formats, so nothing raises: the document simply ends
up with an undefined control sequence that no renderer can typeset.

``T`` normalizes the Mathematical Alphanumeric Symbols back to ASCII, so that
an equation written with math italic letters yields ``h(x)`` rather than a
string of astral-plane codepoints. U+1D455 -- the slot where math italic small
h would sit -- is permanently reserved, because Unicode unifies that letter
with U+210E PLANCK CONSTANT. The table followed the contiguous block and so
skipped h, leaving it as the single letter of the alphabet that survived
untranslated into the LaTeX output.
"""

from markitdown.converter_utils.docx.math.latex_dict import T
from markitdown.converter_utils.docx.math.omml import load_string

# Math italic Latin: A-Z is contiguous, a-z has a hole at U+1D455 (small h),
# which Unicode unifies with U+210E.
ITALIC_UPPERCASE = {
    chr(0x1D434 + i): c for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
}
ITALIC_LOWERCASE = {
    chr(0x1D44E + i): c for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")
}
ITALIC_LOWERCASE.pop(chr(0x1D455))  # reserved codepoint, never assigned
ITALIC_LOWERCASE["ℎ"] = "h"

_DOC = (
    "<w:document "
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
    "{0}</w:document>"
)

_ACCENT = (
    "<m:oMath><m:acc>"
    '<m:accPr><m:chr m:val="{chr}"/></m:accPr>'
    "<m:e><m:r><m:t>x</m:t></m:r></m:e>"
    "</m:acc></m:oMath>"
)

_RUN = "<m:oMath><m:r><m:t>{text}</m:t></m:r></m:oMath>"


def _latex(fragment: str) -> str:
    return next(load_string(_DOC.format(fragment))).latex


def _accent_latex(accent_char: str) -> str:
    return _latex(_ACCENT.format(chr=accent_char))


def _run_latex(text: str) -> str:
    return _latex(_RUN.format(text=text))


def test_combining_left_arrow_below() -> None:
    """U+20EE must produce \\underleftarrow, not the misspelled macro."""
    assert _accent_latex("⃮") == "\\underleftarrow{x}"


def test_arrow_accents_are_consistent() -> None:
    """The three arrow accents share one naming scheme; none may be misspelled."""
    assert _accent_latex("⃖") == "\\overleftarrow{x}"  # left arrow above
    assert _accent_latex("⃯") == "\\underrightarrow{x}"  # right arrow below
    assert _accent_latex("⃮") == "\\underleftarrow{x}"  # left arrow below


def test_math_italic_small_h_is_normalized() -> None:
    """U+210E is the math italic h; it must not survive into the LaTeX."""
    assert _run_latex("ℎ") == "h"


def test_math_italic_latin_alphabet_is_complete() -> None:
    """No math italic Latin letter may leak through untranslated."""
    for char, expected in {**ITALIC_UPPERCASE, **ITALIC_LOWERCASE}.items():
        assert T.get(char) == expected, f"U+{ord(char):04X} is missing from T"
        assert _run_latex(char) == expected


def test_math_italic_expression_is_fully_normalized() -> None:
    """A whole expression must come out as plain ASCII LaTeX."""
    # h(x) = g(x), written entirely with math italic codepoints.
    expression = "ℎ(\U0001d465)=\U0001d454(\U0001d465)"
    assert _run_latex(expression) == "h(x)=g(x)"


if __name__ == "__main__":
    test_combining_left_arrow_below()
    test_arrow_accents_are_consistent()
    test_math_italic_small_h_is_normalized()
    test_math_italic_latin_alphabet_is_complete()
    test_math_italic_expression_is_fully_normalized()
    print("All tests passed!")
