"""Regression test: whitespace inside fenced code blocks must survive conversion.

MarkItDown._convert used to rstrip every line and collapse runs of 3+ newlines
across the whole result, which corrupts code blocks: two consecutive blank
lines inside a fence collapsed to one, and trailing spaces were stripped.
"""

import io

from markitdown import MarkItDown, StreamInfo


def _convert_markdown(content: bytes) -> str:
    return (
        MarkItDown()
        .convert(
            io.BytesIO(content),
            stream_info=StreamInfo(mimetype="text/markdown", extension=".md"),
        )
        .markdown
    )


def test_blank_line_runs_inside_code_fence_are_preserved() -> None:
    content = b"# Title\n\n```python\ndef a():\n    pass\n\n\ndef b():\n    pass\n```\n\nEnd\n"
    result = _convert_markdown(content)
    assert "pass\n\n\ndef b" in result


def test_trailing_spaces_inside_code_fence_are_preserved() -> None:
    content = b"```text\nline with trailing spaces   \n```\n"
    result = _convert_markdown(content)
    assert "line with trailing spaces   \n" in result


def test_normalization_still_applies_outside_code_fence() -> None:
    content = b"para   \n\n\n\nother\n"
    result = _convert_markdown(content)
    assert result == "para\n\nother\n"


def test_tilde_fence_content_is_preserved() -> None:
    # An info string ("text") keeps the sample away from charset misdetection
    # of bare "~~~" lines (charset_normalizer reads them as shift_jis_2004).
    content = b"~~~text\n\n\nkept\n~~~\n"
    result = _convert_markdown(content)
    assert "~~~text\n\n\nkept\n~~~" in result
