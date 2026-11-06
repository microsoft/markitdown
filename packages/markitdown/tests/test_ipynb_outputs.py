"""Code cell outputs (streams, errors, text results) survive conversion."""
import io
import json
import re

from markitdown import MarkItDown, StreamInfo


def _notebook_bytes(cells):
    nb = {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    return io.BytesIO(json.dumps(nb).encode())


def test_stream_and_error_outputs_rendered():
    buf = _notebook_bytes([
        {"cell_type": "code", "execution_count": 1, "metadata": {}, "source": ["print('hi')"],
         "outputs": [
             {"output_type": "stream", "name": "stdout", "text": ["hi\n"]},
             {"output_type": "error", "ename": "ValueError", "evalue": "bad",
              "traceback": ["Traceback (most recent call last):", "ValueError: bad"]},
         ]},
    ])
    result = MarkItDown().convert_stream(buf, stream_info=StreamInfo(extension=".ipynb"))
    assert "```python\nprint('hi')\n```" in result.markdown
    assert "hi" in result.markdown
    assert "ValueError: bad" in result.markdown


def test_execute_result_text_rendered():
    buf = _notebook_bytes([
        {"cell_type": "code", "execution_count": 2, "metadata": {}, "source": ["1+1"],
         "outputs": [{"output_type": "execute_result", "execution_count": 2,
                      "data": {"text/plain": ["2"]}, "metadata": {}}]},
    ])
    result = MarkItDown().convert_stream(buf, stream_info=StreamInfo(extension=".ipynb"))
    assert "| 2 |" not in result.markdown
    assert "```" in result.markdown and "\n2\n" in result.markdown


def test_no_outputs_leaves_cell_unchanged():
    buf = _notebook_bytes([
        {"cell_type": "code", "execution_count": None, "metadata": {}, "source": ["x = 1"], "outputs": []},
    ])
    result = MarkItDown().convert_stream(buf, stream_info=StreamInfo(extension=".ipynb"))
    assert result.markdown.strip() == "```python\nx = 1\n```"

def test_output_containing_backticks_gets_longer_fence():
    """A printed ``` run must not close the output fence early."""
    nb = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "source": ["print(markdown_example)"],
                "outputs": [
                    {"output_type": "stream", "name": "stdout", "text": ["before\n```\nafter\n"]}
                ],
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    buf = io.BytesIO(json.dumps(nb).encode())
    result = MarkItDown().convert_stream(buf, stream_info=StreamInfo(extension=".ipynb"))
    md = result.markdown
    assert "````text\nbefore\n```\nafter" in md
    fences = [len(run) for run in re.findall(r"^`+", md, re.MULTILINE)]
    # source fence stays 3 (no backticks in it), output fence grows to 4
    assert 4 in fences
