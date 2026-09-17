"""Regression checks for positioned text being mistaken for table content."""

from unittest.mock import MagicMock

import pytest

from markitdown.converters._pdf_converter import (
    _extract_form_content_from_words,
    _has_space_starved_words,
    _select_plain_text_extraction,
)


@pytest.mark.parametrize(
    "text",
    [
        "Ordinary prose with spaces between words. " * 100,
        "https://example.com/" + "a" * 600,
        "This single identifier is " + "a" * 600,
        "这是没有空格的正常中文文本。" * 100,
        "",
    ],
)
def test_ordinary_text_keeps_pdfminer_output(text):
    assert _select_plain_text_extraction(text, "different extraction") == text


def test_empty_alternative_does_not_replace_collapsed_text():
    collapsed = "\n".join(["NaturalLanguageProcessingResearch"] * 20)
    assert _select_plain_text_extraction(collapsed, " \n") == collapsed


def test_collapsed_prose_is_not_a_borderless_table():
    page = MagicMock(width=612)
    # Three aligned columns would otherwise look like a form. Repeated long
    # runs reveal that the word extraction has joined neighbouring words.
    words = [
        {
            "text": "NaturalLanguageProcessingResearch",
            "x0": 50 + column * 200,
            "x1": 140 + column * 200,
            "top": row * 12,
            "bottom": row * 12 + 10,
        }
        for row in range(20)
        for column in range(3)
    ]
    page.extract_words.return_value = words
    assert _extract_form_content_from_words(page) is None


def test_one_long_identifier_does_not_reclassify_a_page():
    words = [{"text": "short"}] * 100 + [{"text": "a" * 600}]
    assert not _has_space_starved_words(words)
