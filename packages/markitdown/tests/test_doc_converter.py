import io
import sys
from types import SimpleNamespace

import pytest

from markitdown._exceptions import MissingDependencyException
from markitdown._stream_info import StreamInfo
from markitdown.converters._doc_converter import DocConverter


def _stream_info(extension: str) -> StreamInfo:
    return StreamInfo(mimetype=None, extension=extension, charset=None)


def test_accepts_doc_but_not_docx_or_other_extensions():
    converter = DocConverter()
    assert converter.accepts(io.BytesIO(b"binary"), _stream_info(".doc"))
    assert not converter.accepts(io.BytesIO(b"binary"), _stream_info(".docx"))
    assert not converter.accepts(io.BytesIO(b"binary"), _stream_info(".txt"))


def test_converts_body_text(monkeypatch):
    class Parsed:
        body_text = "# Heading\n\nLegacy Word text"

    monkeypatch.setitem(
        sys.modules, "unword", SimpleNamespace(parse_doc=lambda data: Parsed())
    )
    import markitdown.converters._doc_converter as module

    monkeypatch.setattr(module, "_dependency_exc_info", None)
    monkeypatch.setattr(module, "unword", sys.modules["unword"])

    result = DocConverter().convert(io.BytesIO(b"binary"), _stream_info(".doc"))
    assert result.markdown == "# Heading\n\nLegacy Word text"


def test_reports_missing_dependency(monkeypatch):
    import markitdown.converters._doc_converter as module

    monkeypatch.setattr(
        module,
        "_dependency_exc_info",
        (ImportError, ImportError("missing"), None),
    )
    with pytest.raises(MissingDependencyException, match="doc"):
        DocConverter().convert(io.BytesIO(b"binary"), _stream_info(".doc"))
