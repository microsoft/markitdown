#!/usr/bin/env python3 -m pytest
"""Code cells must be fenced with the language the notebook is written in."""

import io
import json
from typing import Any, Dict

from markitdown import MarkItDown, StreamInfo

SOURCE = "plot(cars)\n"


def _notebook(metadata: Dict[str, Any]) -> io.BytesIO:
    """A one-code-cell notebook carrying the given ``metadata``."""
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [],
                "source": [SOURCE],
            }
        ],
        "metadata": metadata,
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return io.BytesIO(json.dumps(notebook).encode("utf-8"))


def _convert(metadata: Dict[str, Any]) -> str:
    return (
        MarkItDown()
        .convert_stream(_notebook(metadata), stream_info=StreamInfo(extension=".ipynb"))
        .markdown
    )


def test_language_info_names_the_fence() -> None:
    """nbformat records the notebook's language in metadata.language_info."""
    markdown = _convert(
        {
            "kernelspec": {"display_name": "R", "language": "R", "name": "ir"},
            "language_info": {"name": "R", "file_extension": ".r"},
        }
    )

    assert "```R\n" + SOURCE in markdown
    assert "```python" not in markdown


def test_kernelspec_language_is_used_when_language_info_is_absent() -> None:
    """Some producers write only the kernel's own declaration."""
    markdown = _convert(
        {"kernelspec": {"display_name": "Julia 1.10", "language": "julia"}}
    )

    assert "```julia\n" + SOURCE in markdown
    assert "```python" not in markdown


def test_python_notebooks_are_still_labelled_python() -> None:
    markdown = _convert(
        {
            "kernelspec": {"display_name": "Python 3", "language": "python"},
            "language_info": {"name": "python"},
        }
    )

    assert "```python\n" + SOURCE in markdown


def test_notebook_without_language_metadata_falls_back_to_python() -> None:
    markdown = _convert({})

    assert "```python\n" + SOURCE in markdown
