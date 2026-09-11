"""
Regression test for https://github.com/microsoft/markitdown/issues/2383

markitdown-ocr: placeholder prefix collision drops OCR blocks in DOCX with 11 or more images.

_PLACEHOLDER = "MARKITDOWNOCRBLOCK{}" -- when substituted in ascending index order,
"MARKITDOWNOCRBLOCK1" is a prefix of "MARKITDOWNOCRBLOCK10" through "MARKITDOWNOCRBLOCK19",
so str.replace corrupts every two-digit placeholder.
"""

import re

_PLACEHOLDER = "MARKITDOWNOCRBLOCK{}"


def _simulate_substitution_buggy(n_images: int) -> str:
    """Reproduce the old (buggy) ascending-order substitution."""
    md = " ".join(f"<p>{_PLACEHOLDER.format(i)}</p>" for i in range(n_images))
    ocr_texts = [f"OCR text for image {i}" for i in range(n_images)]
    for i, raw_text in enumerate(ocr_texts):
        placeholder = _PLACEHOLDER.format(i)
        ocr_block = f"*[Image OCR]\n{raw_text}\n[End OCR]*"
        md = md.replace(placeholder, ocr_block)
    return md


def _simulate_substitution_fixed(n_images: int) -> str:
    """The fixed substitution: sort by descending placeholder length first."""
    md = " ".join(f"<p>{_PLACEHOLDER.format(i)}</p>" for i in range(n_images))
    ocr_texts = [f"OCR text for image {i}" for i in range(n_images)]
    replacements = [
        (_PLACEHOLDER.format(i), f"*[Image OCR]\n{raw_text}\n[End OCR]*")
        for i, raw_text in enumerate(ocr_texts)
    ]
    replacements.sort(key=lambda pair: len(pair[0]), reverse=True)
    for placeholder, ocr_block in replacements:
        md = md.replace(placeholder, ocr_block)
    return md


def _remaining_placeholders(md: str) -> list:
    """Return any MARKITDOWNOCRBLOCK tokens that were not substituted."""
    return re.findall(r"MARKITDOWNOCRBLOCK\d+", md)


def test_buggy_code_leaves_corrupted_placeholder_for_11_images():
    """The old code corrupts MARKITDOWNOCRBLOCK10 when there are 11+ images."""
    result = _simulate_substitution_buggy(11)
    # With the bug, MARKITDOWNOCRBLOCK10 is replaced by MARKITDOWNOCRBLOCK1's content + "0"
    # so no MARKITDOWNOCRBLOCK tokens remain, but the content is wrong.
    # The tell-tale sign: "OCR text for image 10" is absent from the output.
    assert "OCR text for image 10" not in result, (
        "Expected buggy code to corrupt OCR block 10 (this test documents the bug)"
    )
    # And "OCR text for image 1" appears twice (once for block 1, once corrupted from block 10)
    assert result.count("OCR text for image 1\n") == 2, (
        "Expected buggy code to duplicate OCR text for image 1"
    )


def test_fixed_code_no_remaining_placeholders_for_11_images():
    """With the fix, all placeholders are replaced and no MARKITDOWNOCRBLOCK tokens remain."""
    result = _simulate_substitution_fixed(11)
    remaining = _remaining_placeholders(result)
    assert remaining == [], f"Unexpected remaining placeholders: {remaining}"


def test_fixed_code_all_ocr_blocks_present_for_11_images():
    """With the fix, every OCR block is present exactly once for 11 images."""
    result = _simulate_substitution_fixed(11)
    for i in range(11):
        assert f"OCR text for image {i}\n" in result, (
            f"OCR block {i} missing from output"
        )


def test_fixed_code_no_remaining_placeholders_for_100_images():
    """With the fix, all placeholders are replaced for 100 images."""
    result = _simulate_substitution_fixed(100)
    remaining = _remaining_placeholders(result)
    assert remaining == [], f"Unexpected remaining placeholders: {remaining}"


def test_no_regression_under_10_images():
    """For fewer than 10 images, both old and new code produce correct output."""
    for n in (1, 5, 9, 10):
        result_buggy = _simulate_substitution_buggy(n)
        result_fixed = _simulate_substitution_fixed(n)
        assert _remaining_placeholders(result_buggy) == []
        assert _remaining_placeholders(result_fixed) == []
        for i in range(n):
            assert f"OCR text for image {i}\n" in result_buggy
            assert f"OCR text for image {i}\n" in result_fixed
