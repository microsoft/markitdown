"""
Tests for two unreported bugs:
  1. _merge_partial_numbering_lines() merging consecutive partial numbers together
  2. IpynbConverter failing to extract title when cell source is a string
"""

import io
import json
import pytest

from markitdown import MarkItDown
from markitdown.converters._pdf_converter import _merge_partial_numbering_lines


# ---------------------------------------------------------------------------
# Bug 1: consecutive partial numbering lines
# ---------------------------------------------------------------------------

class TestMergePartialNumberingLines:

    def test_consecutive_numbers_not_merged(self):
        """Two consecutive .N lines must stay separate, not be joined together."""
        text = ".1\n.2\nContractor shall furnish all materials."
        result = _merge_partial_numbering_lines(text)
        assert ".1 .2" not in result, (
            f"Consecutive partial numbers were wrongly merged: {result!r}"
        )

    def test_consecutive_numbers_preserved(self):
        """.1 must stay on its own line; .2 must merge with the text below it."""
        text = ".1\n.2\nContractor shall furnish all materials."
        result = _merge_partial_numbering_lines(text)
        lines = result.splitlines()
        assert lines[0] == ".1"
        assert lines[1] == ".2 Contractor shall furnish all materials."

    def test_number_merges_with_text(self):
        """A lone .N line followed by text (not another number) must still merge."""
        text = ".1\nContractor shall furnish all materials."
        result = _merge_partial_numbering_lines(text)
        assert ".1 Contractor shall furnish all materials." in result

    def test_three_consecutive_numbers(self):
        """.1, .2, .3 each followed immediately by another number — none merged."""
        text = ".1\n.2\n.3\nWork shall comply with local codes."
        result = _merge_partial_numbering_lines(text)
        assert ".1 .2" not in result
        assert ".2 .3" not in result
        lines = result.splitlines()
        assert lines[0] == ".1"
        assert lines[1] == ".2"

    def test_number_then_text_then_number(self):
        """Mixed case: .1 merges with its text, .2 merges with its text."""
        text = ".1\nFirst clause text.\n.2\nSecond clause text."
        result = _merge_partial_numbering_lines(text)
        assert ".1 First clause text." in result
        assert ".2 Second clause text." in result


# ---------------------------------------------------------------------------
# Bug 2: ipynb cell source as string
# ---------------------------------------------------------------------------

def _make_notebook(source) -> io.BytesIO:
    """Build a minimal .ipynb with one markdown cell whose source is `source`."""
    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3",
                "language": "python",
            }
        },
        "cells": [
            {
                "cell_type": "markdown",
                "source": source,
                "metadata": {},
            }
        ],
    }
    return io.BytesIO(json.dumps(nb).encode())


class TestIpynbSourceAsString:

    @pytest.fixture
    def md(self):
        return MarkItDown()

    def test_title_extracted_when_source_is_string(self, md):
        """Title must be extracted even when cell source is a plain string."""
        buf = _make_notebook("# My Report\n\nSome content here.")
        result = md.convert(buf, url="nb.ipynb")
        assert result.title == "My Report", (
            f"Title not extracted from string source; got {result.title!r}"
        )

    def test_title_same_for_list_and_string_source(self, md):
        """Source as string and source as list must produce the same title."""
        as_list = _make_notebook(["# My Report\n", "\n", "Some content here."])
        as_str  = _make_notebook("# My Report\n\nSome content here.")

        r_list = md.convert(as_list, url="a.ipynb")
        r_str  = md.convert(as_str,  url="b.ipynb")

        assert r_list.title == r_str.title, (
            f"Title mismatch: list={r_list.title!r}, string={r_str.title!r}"
        )

    def test_content_correct_when_source_is_string(self, md):
        """Markdown content must be rendered correctly regardless of source type."""
        buf = _make_notebook("# My Report\n\nSome content here.")
        result = md.convert(buf, url="nb.ipynb")
        assert "My Report" in result.text_content
        assert "Some content here." in result.text_content

    def test_no_title_when_no_heading(self, md):
        """A string source with no # heading should still produce no title."""
        buf = _make_notebook("Just some text without a heading.")
        result = md.convert(buf, url="nb.ipynb")
        assert result.title is None
