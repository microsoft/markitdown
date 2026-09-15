import io
import json
import zipfile

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown._exceptions import FileConversionException
from markitdown.converters._xmind_converter import MAX_CONTENT_SIZE


def _xmind(**entries: bytes) -> io.BytesIO:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    stream.seek(0)
    return stream


def _convert(stream: io.BytesIO) -> str:
    return MarkItDown().convert_stream(stream, StreamInfo(extension=".xmind")).markdown


def _mark_entry_encrypted(stream: io.BytesIO) -> io.BytesIO:
    """Set ZIP encryption flags without requiring a third-party ZIP writer."""
    archive = bytearray(stream.getvalue())
    for signature, flag_offset in ((b"PK\x03\x04", 6), (b"PK\x01\x02", 8)):
        offset = archive.find(signature)
        assert offset >= 0
        flags = int.from_bytes(archive[offset + flag_offset : offset + flag_offset + 2], "little")
        archive[offset + flag_offset : offset + flag_offset + 2] = (flags | 1).to_bytes(2, "little")
    return io.BytesIO(archive)


def test_converts_modern_xmind_outline_and_notes() -> None:
    content = [{
        "title": "Roadmap",
        "rootTopic": {
            "title": "Launch",
            "notes": {"plain": {"content": "Owner: Ada\nDue Friday"}},
            "children": {"attached": [{"title": "Build"}, {"title": "Ship"}]},
        },
    }]

    assert _convert(_xmind(**{"content.json": json.dumps(content).encode()})) == (
        "# Roadmap\n\n- Launch\n  > Owner: Ada\n  > Due Friday\n  - Build\n  - Ship"
    )


def test_converts_classic_xmind_outline() -> None:
    content = b'''<?xml version="1.0"?><xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0"><sheet><title>Classic <span>Sheet</span></title><topic><title>Root <span>Topic</span></title><children><topics type="attached"><topic><title>Child</title><notes><plain>Remember <span>this</span></plain></notes></topic></topics></children></topic></sheet></xmap-content>'''

    assert _convert(_xmind(**{"content.xml": content})) == "# Classic Sheet\n\n- Root Topic\n  - Child\n    > Remember this"


def test_omits_empty_topics_without_losing_children() -> None:
    content = [{"title": "Outline", "rootTopic": {"children": {"attached": [{"title": "Child"}]}}}]

    assert _convert(_xmind(**{"content.json": json.dumps(content).encode()})) == "# Outline\n\n- Child"


def test_prefers_modern_content_when_both_formats_are_present() -> None:
    modern = [{"title": "Modern", "rootTopic": {"title": "JSON"}}]
    assert _convert(_xmind(**{"content.json": json.dumps(modern).encode(), "content.xml": b"<bad"})) == "# Modern\n\n- JSON"


@pytest.mark.parametrize("entries", [{}, {"content.json": b""}, {"content.json": b"not json"}])
def test_rejects_missing_empty_or_malformed_content(entries: dict[str, bytes]) -> None:
    with pytest.raises(FileConversionException):
        _convert(_xmind(**entries))


def test_rejects_content_larger_than_the_uncompressed_size_limit() -> None:
    content = b"[" + b" " * MAX_CONTENT_SIZE + b"]"

    with pytest.raises(FileConversionException):
        _convert(_xmind(**{"content.json": content}))


def test_rejects_an_encrypted_content_entry() -> None:
    archive = _mark_entry_encrypted(_xmind(**{"content.json": b"[]"}))

    with pytest.raises(FileConversionException):
        _convert(archive)
