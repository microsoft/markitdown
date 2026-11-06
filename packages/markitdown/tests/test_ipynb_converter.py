"""The notebook converter assumed two shapes nbformat does not guarantee.

`source` is a `multiline_string` — a list of lines *or* a single string — and
the language of the code cells is recorded in the notebook's own metadata
rather than being Python by definition.
"""

import io
import json
from typing import Any

import pytest

from markitdown import MarkItDown, StreamInfo


def _convert(notebook: dict[str, Any]) -> tuple[str, str | None]:
    result = MarkItDown(enable_plugins=False).convert_stream(
        io.BytesIO(json.dumps(notebook).encode("utf-8")),
        stream_info=StreamInfo(extension=".ipynb"),
    )
    return result.markdown, result.title


def _notebook(cells: list[dict[str, Any]], metadata: Any = None) -> dict[str, Any]:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {} if metadata is None else metadata,
        "cells": cells,
    }


@pytest.mark.parametrize(
    "metadata, expected",
    [
        ({"language_info": {"name": "R"}, "kernelspec": {"language": "R"}}, "R"),
        ({"kernelspec": {"language": "julia"}}, "julia"),  # older notebooks
        ({"language_info": {"name": "python"}}, "python"),
        ({}, "python"),  # unchanged for a notebook that records neither
        ({"language_info": {"name": ""}}, "python"),
        ({"language_info": "not a dict"}, "python"),
        (
            {"language_info": {"name": "with space"}},
            "python",
        ),  # not a fence info string
        ({"language_info": {"name": "back`tick"}}, "python"),
    ],
)
def test_code_cells_use_the_notebooks_own_language(
    metadata: Any, expected: str
) -> None:
    markdown, _ = _convert(
        _notebook(
            [{"cell_type": "code", "source": ["1 + 1\n"], "outputs": []}],
            metadata=metadata,
        )
    )

    assert markdown == f"```{expected}\n1 + 1\n\n```"


def test_a_string_source_is_read_as_lines() -> None:
    """nbformat allows `source` to be one string rather than a list of lines."""
    markdown, title = _convert(
        _notebook(
            [
                {"cell_type": "markdown", "source": "# My Title\n\nsome text"},
                {"cell_type": "code", "source": "print(1)\n", "outputs": []},
            ]
        )
    )

    assert markdown == "# My Title\n\nsome text\n\n```python\nprint(1)\n\n```"
    assert title == "My Title"


def test_a_list_source_is_unchanged() -> None:
    """Guard: the shape the converter already handled must render identically."""
    markdown, title = _convert(
        _notebook(
            [
                {
                    "cell_type": "markdown",
                    "source": ["# My Title\n", "\n", "some text"],
                },
                {"cell_type": "code", "source": ["print(1)\n"], "outputs": []},
            ]
        )
    )

    assert markdown == "# My Title\n\nsome text\n\n```python\nprint(1)\n\n```"
    assert title == "My Title"


def test_metadata_title_still_wins() -> None:
    _, title = _convert(
        _notebook(
            [{"cell_type": "markdown", "source": "# Heading Title"}],
            metadata={"title": "Metadata Title"},
        )
    )

    assert title == "Metadata Title"


def test_a_source_that_is_neither_a_string_nor_a_list_is_skipped() -> None:
    markdown, _ = _convert(
        _notebook(
            [
                {"cell_type": "code", "source": None, "outputs": []},
                {"cell_type": "code", "source": ["ok\n"], "outputs": []},
            ]
        )
    )

    assert markdown == "```python\n\n```\n\n```python\nok\n\n```"


def test_raw_cells_keep_an_untagged_fence() -> None:
    """Guard: only code cells carry the language."""
    markdown, _ = _convert(
        _notebook(
            [{"cell_type": "raw", "source": ["raw text\n"]}],
            metadata={"language_info": {"name": "R"}},
        )
    )

    assert markdown == "```\nraw text\n\n```"
