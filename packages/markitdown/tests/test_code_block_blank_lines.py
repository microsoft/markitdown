#!/usr/bin/env python3 -m pytest
"""Blank lines inside a fenced code block are content, not layout.

``MarkItDown._convert`` collapses runs of blank lines as it normalizes a
converter's output. Applied inside a code fence that rewrites the document's
own code -- PEP 8's two blank lines between top-level definitions came back
as one.
"""

import io
import json
from typing import List

from markitdown import MarkItDown, StreamInfo

CODE = "def first():\n    return 1\n\n\ndef second():\n    return 2"


def _convert(stream: io.BytesIO, extension: str, **kwargs: object) -> str:
    return (
        MarkItDown()
        .convert_stream(stream, stream_info=StreamInfo(extension=extension, **kwargs))
        .markdown
    )


def _notebook(source: str) -> io.BytesIO:
    lines: List[str] = source.splitlines(keepends=True)
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": lines,
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return io.BytesIO(json.dumps(notebook).encode("utf-8"))


def _html(body: str) -> io.BytesIO:
    return io.BytesIO(f"<html><body>{body}</body></html>".encode("utf-8"))


def test_notebook_code_cell_keeps_its_blank_lines() -> None:
    markdown = _convert(_notebook(CODE), ".ipynb")

    assert CODE in markdown


def test_html_code_block_keeps_its_blank_lines() -> None:
    markdown = _convert(
        _html(f"<pre><code>{CODE}\n</code></pre>"),
        ".html",
        mimetype="text/html",
        charset="utf-8",
    )

    assert CODE in markdown


def test_blank_lines_between_paragraphs_are_still_collapsed() -> None:
    markdown = _convert(
        _html("<p>First</p><p>Second</p>"),
        ".html",
        mimetype="text/html",
        charset="utf-8",
    )

    assert markdown == "First\n\nSecond"


def test_blank_lines_around_a_code_block_are_still_collapsed() -> None:
    markdown = _convert(
        _html("<p>Before</p><pre><code>x = 1\n</code></pre><p>After</p>"),
        ".html",
        mimetype="text/html",
        charset="utf-8",
    )

    assert markdown == "Before\n\n```\nx = 1\n```\n\nAfter"


def test_unterminated_fence_is_not_treated_as_a_code_block() -> None:
    """Only a closed fence protects its content; an open one is normalized."""
    markdown = _convert(
        io.BytesIO("```\nx = 1\n\n\n\ny = 2\n".encode("utf-8")),
        ".md",
        mimetype="text/markdown",
        charset="utf-8",
    )

    assert markdown == "```\nx = 1\n\ny = 2\n"
