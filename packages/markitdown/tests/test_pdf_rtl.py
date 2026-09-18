"""Arabic presentation-form normalization (microsoft/markitdown#2336).

Every non-ASCII character below is a \\uXXXX escape: pasted
presentation forms look identical to standard letters, so literals
are banned in this file.
"""

from markitdown.converters._pdf_converter import (
    _normalize_arabic_presentation_forms as normalize,
)


def _has_presentation_forms(text: str) -> bool:
    return any(
        0xFB50 <= ord(char) <= 0xFDFF or 0xFE70 <= ord(char) <= 0xFEFF
        for char in text
    )


def test_forms_become_standard_letters() -> None:
    # U+FE8D U+FEDF U+FEE3 U+FB8B U+FE94 U+FEEB
    #   -> U+0627 U+0644 U+0645 U+0698 U+0629 U+0647
    given = '\uFE8D\uFEDF\uFEE3\uFB8B\uFE94\uFEEB'
    assert _has_presentation_forms(given)
    assert normalize(given) == '\u0627\u0644\u0645\u0698\u0629\u0647'


def test_ligature_expands_to_letters() -> None:
    # U+FEFB -> U+0644 U+0627
    assert normalize('\uFEFB') == '\u0644\u0627'


def test_other_text_is_untouched() -> None:
    # superscript-two, fi ligature (outside our ranges) and a standard
    # Arabic word must pass through byte-identical.
    text = 'Hello 604 / 2026 - \u00b2 \uFB01 \u0645\u0631\u062D\u0628\u0627'
    assert normalize(text) == text


def test_empty_and_plain_text_are_unchanged() -> None:
    assert normalize('') == ''
    assert normalize('Plain text 123.') == 'Plain text 123.'


def test_normalization_is_idempotent() -> None:
    once = normalize('\uFE8D report 604')
    assert once == '\u0627 report 604'
    assert normalize(once) == once
    assert not _has_presentation_forms(once)

