#!/usr/bin/env python3 -m pytest
"""Tests for MasterFormat-style partial numbering in PDF conversion."""

import os
import re
import pytest

from markitdown import MarkItDown
from markitdown.converters._pdf_converter import PARTIAL_NUMBERING_PATTERN

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


class TestMasterFormatPartialNumbering:
    """Test handling of MasterFormat-style partial numbering (.1, .2, etc.)."""

    def test_partial_numbering_pattern_regex(self):
        """Test that the partial numbering regex pattern correctly matches."""

        # Should match partial numbering patterns
        assert PARTIAL_NUMBERING_PATTERN.match(".1") is not None
        assert PARTIAL_NUMBERING_PATTERN.match(".2") is not None
        assert PARTIAL_NUMBERING_PATTERN.match(".10") is not None
        assert PARTIAL_NUMBERING_PATTERN.match(".99") is not None

        # Should NOT match other patterns
        assert PARTIAL_NUMBERING_PATTERN.match("1.") is None
        assert PARTIAL_NUMBERING_PATTERN.match("1.2") is None
        assert PARTIAL_NUMBERING_PATTERN.match(".1.2") is None
        assert PARTIAL_NUMBERING_PATTERN.match("text") is None
        assert PARTIAL_NUMBERING_PATTERN.match(".a") is None
        assert PARTIAL_NUMBERING_PATTERN.match("") is None

    def test_masterformat_partial_numbering_not_split(self):
        """Test that MasterFormat partial numbering stays with associated text.

        MasterFormat documents use partial numbering like:
            .1  The intent of this Request for Proposal...
            .2  Available information relative to...

        These should NOT be split into separate table columns, but kept
        as coherent text lines with the number followed by its description.
        """
        pdf_path = os.path.join(TEST_FILES_DIR, "masterformat_partial_numbering.pdf")

        markitdown = MarkItDown()
        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Partial numberings should NOT appear isolated on their own lines
        # If they're isolated, it means the parser incorrectly split them from their text
        lines = text_content.split("\n")
        isolated_numberings = []
        for line in lines:
            stripped = line.strip()
            # Check if line contains ONLY a partial numbering (with possible whitespace/pipes)
            cleaned = stripped.replace("|", "").strip()
            if cleaned in [".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9", ".10"]:
                isolated_numberings.append(stripped)

        assert len(isolated_numberings) == 0, (
            f"Partial numberings should not be isolated from their text. "
            f"Found isolated: {isolated_numberings}"
        )

        # Verify that partial numberings appear WITH following text on the same line
        # Look for patterns like ".1 The intent" or ".1  Some text"
        partial_with_text = re.findall(r"\.\d+\s+\w+", text_content)
        assert (
            len(partial_with_text) > 0
        ), "Expected to find partial numberings followed by text on the same line"

    def test_masterformat_content_preserved(self):
        """Test that MasterFormat document content is fully preserved."""
        pdf_path = os.path.join(TEST_FILES_DIR, "masterformat_partial_numbering.pdf")

        markitdown = MarkItDown()
        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Verify key content from the MasterFormat document is preserved
        expected_content = [
            "RFP for Construction Management Services",
            "Section 00 00 43",
            "Instructions to Respondents",
            "Ken Sargent House",
            "INTENT",
            "Request for Proposal",
            "KEN SARGENT HOUSE",
            "GRANDE PRAIRIE, ALBERTA",
            "Section 00 00 45",
        ]

        for content in expected_content:
            assert (
                content in text_content
            ), f"Expected content '{content}' not found in extracted text"

        # Verify partial numbering is followed by text on the same line
        # .1 should be followed by "The intent" on the same line
        assert re.search(
            r"\.1\s+The intent", text_content
        ), "Partial numbering .1 should be followed by 'The intent' text"

        # .2 should be followed by "Available information" on the same line
        assert re.search(
            r"\.2\s+Available information", text_content
        ), "Partial numbering .2 should be followed by 'Available information' text"

        # Ensure text content is not empty and has reasonable length
        assert (
            len(text_content.strip()) > 100
        ), "MasterFormat document should have substantial text content"

    def test_merge_partial_numbering_with_empty_lines_between(self):
        """Test that partial numberings merge correctly even with empty lines between.

        When PDF extractors produce output like:
            .1

            The intent of this Request...

        The merge logic should still combine them properly.
        """
        pdf_path = os.path.join(TEST_FILES_DIR, "masterformat_partial_numbering.pdf")

        markitdown = MarkItDown()
        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # The merged result should have .1 and .2 followed by text
        # Check that we don't have patterns like ".1\n\nThe intent" (unmerged)
        lines = text_content.split("\n")

        for i, line in enumerate(lines):
            stripped = line.strip()
            # If we find an isolated partial numbering, the merge failed
            if stripped in [".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8"]:
                # Check if next non-empty line exists and wasn't merged
                for j in range(i + 1, min(i + 3, len(lines))):
                    if lines[j].strip():
                        pytest.fail(
                            f"Partial numbering '{stripped}' on line {i} was not "
                            f"merged with following text '{lines[j].strip()[:30]}...'"
                        )
                        break

    def test_multiple_partial_numberings_all_merged(self):
        """Test that all partial numberings in a document are properly merged."""
        pdf_path = os.path.join(TEST_FILES_DIR, "masterformat_partial_numbering.pdf")

        markitdown = MarkItDown()
        result = markitdown.convert(pdf_path)
        text_content = result.text_content

        # Count occurrences of merged partial numberings (number followed by text)
        merged_count = len(re.findall(r"\.\d+\s+[A-Za-z]", text_content))

        # Count isolated partial numberings (number alone on a line)
        isolated_count = 0
        for line in text_content.split("\n"):
            stripped = line.strip()
            if re.match(r"^\.\d+$", stripped):
                isolated_count += 1

        assert (
            merged_count >= 2
        ), f"Expected at least 2 merged partial numberings, found {merged_count}"
        assert (
            isolated_count == 0
        ), f"Found {isolated_count} isolated partial numberings that weren't merged"
