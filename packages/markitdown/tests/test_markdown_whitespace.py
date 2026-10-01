"""Trailing spaces that encode a hard break must survive normalization.

``MarkItDown._convert`` strips trailing whitespace from every converter's
Markdown. Two or more trailing spaces are a CommonMark hard line break, so
those are kept. A single trailing space, a trailing tab, and a line that is
only whitespace are still removed. Runs of blank lines are still collapsed.
"""

import io
from typing import Any, BinaryIO

import pytest

from markitdown import (
    DocumentConverter,
    DocumentConverterResult,
    MarkItDown,
    StreamInfo,
)
from markitdown._markitdown import _rstrip_preserving_hard_break


class _PassthroughConverter(DocumentConverter):
    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        return (stream_info.extension or "").lower() == ".fixture"

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        return DocumentConverterResult(markdown=file_stream.read().decode("utf-8"))


def _convert(source: str) -> str:
    markitdown = MarkItDown(enable_builtins=False, enable_plugins=False)
    markitdown.register_converter(_PassthroughConverter(), priority=-1.0)
    return markitdown.convert_stream(
        io.BytesIO(source.encode("utf-8")),
        stream_info=StreamInfo(extension=".fixture", charset="utf-8"),
    ).markdown


def _convert_builtin(source: str, *, extension: str, mimetype: str) -> str:
    return (
        MarkItDown(enable_plugins=False)
        .convert_stream(
            io.BytesIO(source.encode("utf-8")),
            stream_info=StreamInfo(
                extension=extension, mimetype=mimetype, charset="utf-8"
            ),
        )
        .markdown
    )


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("First line  ", "First line  "),
        ("First line   ", "First line   "),
        ("First line ", "First line"),
        ("First line\t", "First line"),
        ("First line \t", "First line"),
        ("First line  \t", "First line"),
        ("First line\t  ", "First line\t  "),
        ("   ", ""),
        ("", ""),
        ("First line\u00a0\u00a0", "First line"),
    ],
)
def test_rstrip_keeps_only_a_hard_break(line: str, expected: str) -> None:
    assert _rstrip_preserving_hard_break(line) == expected


def test_hard_line_breaks_survive_normalization() -> None:
    source = "First line  \nSecond line\n"

    assert _convert(source) == source


def test_single_trailing_space_is_still_trimmed() -> None:
    source = "First line \nSecond line\n"

    assert _convert(source) == "First line\nSecond line\n"


def test_hard_line_breaks_with_more_than_two_spaces_are_preserved() -> None:
    source = "First line   \nSecond line\n"

    assert _convert(source) == source


def test_several_hard_breaks_in_one_document_are_preserved() -> None:
    source = "One  \nTwo  \nThree\n"

    assert _convert(source) == source


def test_crlf_hard_break_becomes_lf_and_keeps_the_spaces() -> None:
    source = "First line  \r\nSecond line\r\n"

    assert _convert(source) == "First line  \nSecond line\n"


def test_backslash_hard_break_is_unchanged() -> None:
    source = "First line\\\nSecond line\n"

    assert _convert(source) == source


def test_trailing_tab_is_still_trimmed() -> None:
    source = "First line\t\nSecond line\n"

    assert _convert(source) == "First line\nSecond line\n"


def test_spaces_followed_by_a_tab_are_not_a_hard_break() -> None:
    source = "First line  \t\nSecond line\n"

    assert _convert(source) == "First line\nSecond line\n"


def test_whitespace_only_line_is_still_trimmed() -> None:
    source = "First line\n   \nSecond line\n"

    assert _convert(source) == "First line\n\nSecond line\n"


def test_blank_line_runs_are_still_collapsed() -> None:
    source = "First line\n\n\n\nSecond line\n"

    assert _convert(source) == "First line\n\nSecond line\n"


def test_hard_break_survives_beside_a_collapsed_blank_run() -> None:
    source = "First line  \n\n\n\nSecond line  \nThird\n"

    assert _convert(source) == "First line  \n\nSecond line  \nThird\n"


def test_two_trailing_spaces_inside_a_fence_are_kept() -> None:
    source = "```\ncode  \n```\n"

    assert _convert(source) == source


def test_one_trailing_space_inside_a_fence_is_still_trimmed() -> None:
    source = "```\ncode \n```\n"

    assert _convert(source) == "```\ncode\n```\n"


def test_empty_output_stays_empty() -> None:
    assert _convert("") == ""


def test_hard_break_without_a_final_newline_is_kept() -> None:
    source = "First line  "

    assert _convert(source) == source


def test_markdown_files_keep_hard_line_breaks() -> None:
    source = "First line  \nSecond line\n"

    assert _convert_builtin(source, extension=".md", mimetype="text/markdown") == source


def test_markdown_crlf_file_keeps_the_hard_break() -> None:
    source = "- item one  \r\n  continuation\r\n"

    assert (
        _convert_builtin(source, extension=".markdown", mimetype="text/markdown")
        == "- item one  \n  continuation\n"
    )


def test_html_br_keeps_a_hard_line_break() -> None:
    html = "<p>First<br>Second</p><p>Third<br/>Fourth</p>"

    assert (
        _convert_builtin(html, extension=".html", mimetype="text/html")
        == "First  \nSecond\n\nThird  \nFourth"
    )


def test_html_paragraphs_do_not_gain_trailing_spaces() -> None:
    html = "<p>First </p><p>Second</p>"

    assert (
        _convert_builtin(html, extension=".html", mimetype="text/html")
        == "First\n\nSecond"
    )
