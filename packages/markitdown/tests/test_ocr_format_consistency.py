"""Test OCR format consistency across converters."""

import re
from typing import Pattern

import pytest


# Standard OCR format pattern (without backend info)
OCR_FORMAT_PATTERN: Pattern[str] = re.compile(
    r"\[Image OCR: ([^\]]+)\]\n"  # Header with identifier
    r"(.+?)\n"  # OCR text content (non-greedy)
    r"\[End Image OCR\]",  # Footer
    re.DOTALL,  # Allow . to match newlines in content
)


def validate_ocr_format(text: str, expected_count: int) -> list[dict[str, str]]:
    """
    Validate that text contains OCR blocks in the standard format.

    Args:
        text: Text to validate
        expected_count: Expected number of OCR blocks

    Returns:
        List of dicts with 'identifier' and 'content' keys

    Raises:
        AssertionError: If format doesn't match or count is wrong
    """
    matches = OCR_FORMAT_PATTERN.findall(text)

    assert len(matches) == expected_count, (
        f"Expected {expected_count} OCR blocks, found {len(matches)}. "
        f"Text:\n{text}"
    )

    results = []
    for match in matches:
        identifier, content = match
        results.append(
            {
                "identifier": identifier,
                "content": content.strip(),
            }
        )

    return results


class TestOCRFormatConsistency:
    """Test OCR output format consistency."""

    def test_word_ocr_format(self) -> None:
        """Test Word document OCR format."""
        # Example Word OCR output
        text = """
Some text before image.

[Image OCR: rId9]
FOOTER: Document ID: DOC-2024-001
[End Image OCR]

Some text after image.
        """.strip()

        results = validate_ocr_format(text, expected_count=1)
        assert results[0]["identifier"] == "rId9"
        assert "DOC-2024-001" in results[0]["content"]

    def test_powerpoint_ocr_format(self) -> None:
        """Test PowerPoint OCR format."""
        # Example PowerPoint OCR output
        text = """
Slide title

[Image OCR: slide_1_img_Picture_3]
Diagram: System Components
Architecture Overview
[End Image OCR]

More slide content.
        """.strip()

        results = validate_ocr_format(text, expected_count=1)
        assert results[0]["identifier"].startswith("slide_")
        assert "System Components" in results[0]["content"]

    def test_pdf_ocr_format(self) -> None:
        """Test PDF OCR format."""
        # Example PDF OCR output - embedded image
        text = """
## Page 1

Regular text content.

[Image OCR: page_1_img_0]
Complex Layout Diagram
With Multiple Elements
[End Image OCR]

More page content.
        """.strip()

        results = validate_ocr_format(text, expected_count=1)
        assert results[0]["identifier"].startswith("page_")
        assert "Complex Layout" in results[0]["content"]

    def test_pdf_scanned_page_format(self) -> None:
        """Test scanned PDF page OCR format."""
        # Example scanned PDF OCR output
        text = """
## Page 5

[Image OCR: page_5_fullpage]
Entire page was scanned
All text extracted via OCR
Multiple paragraphs preserved
[End Image OCR]
        """.strip()

        results = validate_ocr_format(text, expected_count=1)
        assert results[0]["identifier"] == "page_5_fullpage"
        assert "scanned" in results[0]["content"]

    def test_multiple_ocr_blocks(self) -> None:
        """Test multiple OCR blocks in same document."""
        text = """
Header

[Image OCR: rId5]
First image text
[End Image OCR]

Middle content

[Image OCR: rId7]
Second image text
[End Image OCR]

Footer
        """.strip()

        results = validate_ocr_format(text, expected_count=2)
        assert results[0]["identifier"] == "rId5"
        assert results[1]["identifier"] == "rId7"

    def test_ocr_format_invalid(self) -> None:
        """Test that invalid formats are rejected."""
        # Old PowerPoint format (should fail)
        invalid_text = """
![Diagram: System Components](Picture 3.jpg)
        """.strip()

        with pytest.raises(AssertionError, match="Expected 1 OCR blocks, found 0"):
            validate_ocr_format(invalid_text, expected_count=1)


def test_ocr_format_pattern_extraction() -> None:
    """Test OCR format pattern can extract all components."""
    text = """
[Image OCR: slide_3_img_Chart_1]
Multi-line
OCR content
with newlines
[End Image OCR]
    """.strip()

    match = OCR_FORMAT_PATTERN.search(text)
    assert match is not None
    identifier, content = match.groups()

    assert identifier == "slide_3_img_Chart_1"
    assert "Multi-line" in content
    assert "newlines" in content
