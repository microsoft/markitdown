#!/usr/bin/env python3 -m pytest
"""Tests for merging paragraph breaks spuriously inserted mid-sentence by PDF
layout analysis (see: https://github.com/microsoft/markitdown/issues/2370)."""

from markitdown.converters._pdf_converter import _merge_wrapped_paragraph_breaks


class TestMergeWrappedParagraphBreaks:
    def test_merges_break_before_lowercase_continuation(self):
        """A blank-line break followed by a lowercase word is a wrapped line,
        not a real paragraph boundary, and should be joined with a space."""
        text = (
            "–  Federal Decree-Law No. 47 of 2022 on the Taxation of "
            "Corporations and Businesses, and\n\nits amendments,"
        )
        assert _merge_wrapped_paragraph_breaks(text) == (
            "–  Federal Decree-Law No. 47 of 2022 on the Taxation of "
            "Corporations and Businesses, and its amendments,"
        )

    def test_merges_break_before_parenthetical_continuation(self):
        """A break before a lowercase parenthetical aside is also a wrap."""
        text = (
            "distribution, warehousing, logistics or inventory management "
            "functions constitutes 51%\n\n(fifty one percent) or more of "
            "their Revenue for the relevant Tax Period."
        )
        assert _merge_wrapped_paragraph_breaks(text) == (
            "distribution, warehousing, logistics or inventory management "
            "functions constitutes 51% (fifty one percent) or more of "
            "their Revenue for the relevant Tax Period."
        )

    def test_does_not_merge_real_paragraph_break(self):
        """A real paragraph boundary -- previous text ends with terminal
        punctuation and/or the next block starts with an uppercase letter --
        must be left untouched."""
        text = (
            "This is the end of a sentence.\n\n"
            "This is a new paragraph that starts with a capital letter."
        )
        assert _merge_wrapped_paragraph_breaks(text) == text

    def test_does_not_merge_when_next_block_is_uppercase(self):
        """Even without terminal punctuation, an uppercase-starting next
        block (e.g. a heading or list item) is left alone, since only a
        lowercase start is an unambiguous continuation signal."""
        text = "Some heading fragment\n\nNext Heading"
        assert _merge_wrapped_paragraph_breaks(text) == text

    def test_single_paragraph_is_unchanged(self):
        text = "Just one paragraph with no breaks."
        assert _merge_wrapped_paragraph_breaks(text) == text

    def test_does_not_merge_lettered_list_items(self):
        """Lettered list markers (e.g. "a)", "b)") start with a lowercase
        letter but must stay separate paragraphs, not get glued together."""
        text = "a) first clause\n\nb) second clause"
        assert _merge_wrapped_paragraph_breaks(text) == text

    def test_does_not_merge_parenthetical_list_items(self):
        text = "some heading\n\n(i) first item\n\n(ii) second item"
        assert _merge_wrapped_paragraph_breaks(text) == text

    def test_does_not_merge_numeric_paragraph_into_next(self):
        """A paragraph that is just a number must not glue onto a following
        paragraph merely because that paragraph's first letter is lowercase."""
        text = "42\n\n7 apples were purchased."
        assert _merge_wrapped_paragraph_breaks(text) == text

    def test_does_not_merge_list_markers_with_no_space_after_marker(self):
        """PDF extraction sometimes drops the space after a list marker
        (e.g. "a)text" instead of "a) text"); the marker must still be
        recognized and kept on its own paragraph."""
        text = "some heading\n\na)first clause\n\nb)second clause"
        assert _merge_wrapped_paragraph_breaks(text) == text
