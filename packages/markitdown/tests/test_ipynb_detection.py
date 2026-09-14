import io
import json
import sys

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters._ipynb_converter import IpynbConverter


@pytest.mark.parametrize(
    "payload",
    [
        {"description": "nbformat_minor describes a notebook version"},
        {"notebook": {"nbformat": 4, "nbformat_minor": 5, "cells": []}},
        {"nbformat": 4, "nbformat_minor": 5, "description": "Format documentation"},
        {
            "nbformat": {"type": "integer"},
            "nbformat_minor": {"type": "integer"},
            "cells": [],
        },
    ],
    ids=["text-value", "nested-notebook", "missing-cells", "schema-fields"],
)
@pytest.mark.parametrize("entry_point", ["file", "stream"])
def test_json_notebook_references_are_preserved(payload, entry_point, tmp_path):
    """Mentioning notebook fields must not discard an ordinary JSON document."""
    text = json.dumps(payload)
    converter = MarkItDown()
    if entry_point == "file":
        path = tmp_path / "documentation.json"
        path.write_text(text, encoding="utf-8")
        result = converter.convert(path)
    else:
        result = converter.convert_stream(
            io.BytesIO(text.encode("utf-8")),
            stream_info=StreamInfo(mimetype="application/json"),
        )

    assert result.markdown == text


@pytest.mark.parametrize(
    "data, charset",
    [
        (b'["nbformat", "nbformat_minor"]', "utf-8"),
        (b'"nbformat_minor"', "utf-8"),
        (b'{"nbformat": 4, "nbformat_minor": 5, "cells": [}', "utf-8"),
        (b"[]", "unknown-charset"),
        (
            b"[" * sys.getrecursionlimit()
            + b'"nbformat_minor"'
            + b"]" * sys.getrecursionlimit(),
            "utf-8",
        ),
    ],
    ids=["array", "string", "invalid-json", "unknown-charset", "deep-json"],
)
def test_ipynb_json_probe_rejects_non_notebooks_without_consuming_stream(data, charset):
    stream = io.BytesIO(b"prefix" + data)
    stream.seek(len(b"prefix"))
    position = stream.tell()

    assert not IpynbConverter().accepts(
        stream, StreamInfo(mimetype="application/json", charset=charset)
    )
    assert stream.tell() == position
    assert stream.read() == data


@pytest.mark.parametrize(
    "encoding, charset",
    [
        ("utf-8", None),
        ("utf-8-sig", "utf-8"),
        ("utf-8-sig", "utf-8-sig"),
        ("utf-16", "utf-16"),
    ],
)
def test_ipynb_json_probe_preserves_notebook_conversion(encoding, charset):
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 0,
        "cells": [{"cell_type": "markdown", "source": ["# Notebook\n"]}],
    }
    stream = io.BytesIO(json.dumps(notebook).encode(encoding))
    stream_info = StreamInfo(mimetype="application/json", charset=charset)

    assert IpynbConverter().accepts(stream, stream_info)
    assert stream.tell() == 0
    result = MarkItDown().convert_stream(stream, stream_info=stream_info)
    assert result.markdown == "# Notebook\n"
    assert result.title == "Notebook"
