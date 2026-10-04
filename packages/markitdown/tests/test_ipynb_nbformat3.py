# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

"""Regression tests for reading notebooks saved in the nbformat 3 layout.

nbformat 3 (IPython 3, Jupyter 4.0) nests cells under ``worksheets[*].cells`` and
stores code cell text under ``input``. Reading only the nbformat 4 layout produced
an empty document with a success exit code, so every cell was silently dropped.
"""

import io
import json

from markitdown import MarkItDown, StreamInfo
from markitdown.converters._ipynb_converter import IpynbConverter

_NBFORMAT_3 = {
    "metadata": {},
    "nbformat": 3,
    "nbformat_minor": 0,
    "worksheets": [
        {
            "cells": [
                {
                    "cell_type": "code",
                    "language": "python",
                    "input": ["print('hello')\n"],
                    "outputs": [],
                },
                {
                    "cell_type": "markdown",
                    "source": ["# Quarterly notes\n", "\n", "Revenue grew.\n"],
                },
            ]
        }
    ],
}

# The same notebook in the nbformat 4 layout: flat `cells`, and `source` everywhere.
_NBFORMAT_4 = {
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 5,
    "cells": [
        {"cell_type": "code", "source": ["print('hello')\n"], "outputs": []},
        {
            "cell_type": "markdown",
            "source": ["# Quarterly notes\n", "\n", "Revenue grew.\n"],
        },
    ],
}


def _convert(notebook: dict):
    data = json.dumps(notebook).encode("utf-8")
    return IpynbConverter().convert(
        io.BytesIO(data), StreamInfo(extension=".ipynb", charset="utf-8")
    )


def test_nbformat_3_notebook_is_not_empty() -> None:
    """An accepted notebook must never convert to an empty document."""
    result = _convert(_NBFORMAT_3)

    assert result.markdown.strip(), "nbformat 3 notebook converted to nothing"


def test_nbformat_3_code_cells_use_their_input_key() -> None:
    result = _convert(_NBFORMAT_3)

    assert "```python\nprint('hello')" in result.markdown


def test_nbformat_3_markdown_cells_are_kept_and_title_extracted() -> None:
    result = _convert(_NBFORMAT_3)

    assert "# Quarterly notes" in result.markdown
    assert "Revenue grew." in result.markdown
    assert result.title == "Quarterly notes"


def test_nbformat_3_matches_nbformat_4_for_the_same_notebook() -> None:
    """The two layouts describe the same document and must produce the same Markdown."""
    assert _convert(_NBFORMAT_3).markdown == _convert(_NBFORMAT_4).markdown


def test_nbformat_3_converts_through_the_public_entry_point() -> None:
    """The whole stack must see the content, not fall through to plain text."""
    data = json.dumps(_NBFORMAT_3).encode("utf-8")

    result = MarkItDown().convert_stream(
        io.BytesIO(data), stream_info=StreamInfo(extension=".ipynb")
    )

    assert "print('hello')" in result.markdown
    assert "Revenue grew." in result.markdown


def test_nbformat_3_with_several_worksheets_keeps_every_cell() -> None:
    notebook = {
        "metadata": {},
        "nbformat": 3,
        "nbformat_minor": 0,
        "worksheets": [
            {"cells": [{"cell_type": "code", "input": ["first = 1\n"], "outputs": []}]},
            {
                "cells": [
                    {"cell_type": "code", "input": ["second = 2\n"], "outputs": []}
                ]
            },
        ],
    }

    markdown = _convert(notebook).markdown

    assert "first = 1" in markdown
    assert "second = 2" in markdown


def test_nbformat_3_title_from_metadata_still_wins() -> None:
    notebook = dict(_NBFORMAT_3, metadata={"title": "From metadata"})

    assert _convert(notebook).title == "From metadata"


def test_nbformat_4_is_unchanged() -> None:
    """The nbformat 4 path must be untouched by this change."""
    result = _convert(_NBFORMAT_4)

    assert "```python\nprint('hello')" in result.markdown
    assert result.title == "Quarterly notes"
