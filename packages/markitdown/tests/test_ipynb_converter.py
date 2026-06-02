import io
import json

from markitdown.converters._ipynb_converter import IpynbConverter
from markitdown._stream_info import StreamInfo

IPYNB_STREAM_INFO = StreamInfo(extension=".ipynb", mimetype="application/json")


def _convert(notebook: dict):
    data = json.dumps(notebook).encode("utf-8")
    return IpynbConverter().convert(io.BytesIO(data), IPYNB_STREAM_INFO)


def _notebook(first_markdown_line: str) -> dict:
    return {
        "cells": [
            {"cell_type": "markdown", "source": [first_markdown_line, "body text"]},
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def test_title_keeps_leading_hash_in_text():
    # The "# " marker should be removed as a prefix, not as a character set, so
    # a heading whose text itself starts with "#" must keep it.
    result = _convert(_notebook("# #100DaysOfCode\n"))
    assert result.title == "#100DaysOfCode"


def test_title_keeps_internal_spacing_after_marker():
    # Only the single "# " marker is stripped; extra spaces in the title text
    # must survive the prefix removal (outer whitespace is still trimmed).
    result = _convert(_notebook("#  Spaced   Title \n"))
    assert result.title == "Spaced   Title"


def test_plain_title_unchanged():
    result = _convert(_notebook("# Introduction\n"))
    assert result.title == "Introduction"
