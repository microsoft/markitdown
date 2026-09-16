import io
import os
import struct
import zipfile
from typing import Any, BinaryIO, Optional

import pytest

from markitdown import (
    DocumentConverter,
    DocumentConverterResult,
    MarkItDown,
    StreamInfo,
)
from markitdown.converters._zip_converter import ZipConverter

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


class _RecordingConverter(DocumentConverter):
    def __init__(self):
        super().__init__()
        self.seen_kwargs = []

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        return (stream_info.extension or "").lower() == ".txt"

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        self.seen_kwargs.append(dict(kwargs))
        return DocumentConverterResult(markdown=file_stream.read().decode("utf-8"))


def test_zip_forwards_kwargs_to_nested_converters() -> None:
    markitdown = MarkItDown(enable_builtins=False)
    recorder = _RecordingConverter()
    markitdown.register_converter(recorder)
    markitdown.register_converter(ZipConverter(markitdown=markitdown))

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("hello.txt", "Hello world")
    buf.seek(0)

    result = markitdown.convert_stream(
        buf,
        stream_info=StreamInfo(mimetype="application/zip", extension=".zip"),
        keep_data_uris=True,
    )

    assert "Hello world" in result.markdown
    assert len(recorder.seen_kwargs) == 1
    assert recorder.seen_kwargs[0].get("keep_data_uris") is True


def test_zip_does_not_forward_outer_file_metadata() -> None:
    """The archive's own extension/url must not override a member's."""
    markitdown = MarkItDown(enable_builtins=False)
    recorder = _RecordingConverter()
    markitdown.register_converter(recorder)
    markitdown.register_converter(ZipConverter(markitdown=markitdown))

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("hello.txt", "Hello world")
    buf.seek(0)

    result = markitdown.convert_stream(
        buf,
        stream_info=StreamInfo(
            mimetype="application/zip",
            extension=".zip",
            url="https://example.com/archive.zip",
        ),
    )

    assert "Hello world" in result.markdown
    assert len(recorder.seen_kwargs) == 1
    # The member sees its own extension, not the archive's
    assert recorder.seen_kwargs[0].get("file_extension") == ".txt"
    assert "url" not in recorder.seen_kwargs[0]


def test_zip_member_reaches_its_own_converter() -> None:
    """A ZIP-based member (docx) must not be unpacked as a nested archive."""
    markitdown = MarkItDown()
    result = markitdown.convert(
        os.path.join(TEST_FILES_DIR, "test_files.zip"),
    )

    assert "## File: test.docx" in result.markdown
    # Raw OOXML parts would appear if the docx were treated as a plain zip
    assert "[Content_Types].xml" not in result.markdown


@pytest.mark.parametrize(
    "archive_url",
    [None, "https://example.test/archive.zip"],
    ids=["no_archive_url", "with_archive_url"],
)
def test_zip_member_docx_converts_as_docx(archive_url: Optional[str]) -> None:
    """A DOCX member converts via the DOCX converter, archive URL or not.

    Regression: the archive's own file_extension/url used to be forwarded into
    the nested convert_stream call, where they take precedence over the
    member's StreamInfo -- so the DOCX was re-selected as a ZIP and unpacked
    into its raw OOXML parts instead of being converted.
    """
    markitdown = MarkItDown()
    docx_path = os.path.join(TEST_FILES_DIR, "test.docx")
    standalone = markitdown.convert(docx_path).markdown

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.write(docx_path, "test.docx")
    buf.seek(0)

    result = markitdown.convert_stream(
        buf,
        stream_info=StreamInfo(extension=".zip", url=archive_url),
    ).markdown

    assert "## File: test.docx" in result
    # The member's real conversion output is present ...
    assert standalone.strip() in result
    # ... and it was not unpacked as a nested archive
    assert "word/document.xml" not in result
    assert "[Content_Types].xml" not in result


def _mark_entry_encrypted(raw: bytes, target: bytes) -> bytes:
    """Set general purpose bit 0 for one member, in both headers that carry it.

    `zipfile` can read an encrypted archive but cannot write one, so the flag the
    reader dispatches on is set directly on the bytes. Local file header: signature
    at 0, flag at 6, name length at 26, extra length at 28, name at 30. Central
    directory header: signature at 0, flag at 8, name length at 28, extra at 30,
    comment at 32, name at 46.
    """
    data = bytearray(raw)

    offset = 0
    while offset + 30 <= len(data) and data[offset : offset + 4] == b"PK\x03\x04":
        name_len = struct.unpack_from("<H", data, offset + 26)[0]
        extra_len = struct.unpack_from("<H", data, offset + 28)[0]
        comp_size = struct.unpack_from("<I", data, offset + 18)[0]
        if data[offset + 30 : offset + 30 + name_len] == target:
            data[offset + 6] |= 0x1
        offset += 30 + name_len + extra_len + comp_size

    offset = data.find(b"PK\x01\x02")
    while offset >= 0 and data[offset : offset + 4] == b"PK\x01\x02":
        name_len = struct.unpack_from("<H", data, offset + 28)[0]
        extra_len = struct.unpack_from("<H", data, offset + 30)[0]
        comment_len = struct.unpack_from("<H", data, offset + 32)[0]
        if data[offset + 46 : offset + 46 + name_len] == target:
            data[offset + 8] |= 0x1
        offset += 46 + name_len + extra_len + comment_len

    return bytes(data)


def _archive(**members: str) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for name, content in members.items():
            archive.writestr(name, content)
    return buffer.getvalue()


def _convert_archive(raw: bytes) -> str:
    return (
        MarkItDown()
        .convert_stream(
            io.BytesIO(raw),
            stream_info=StreamInfo(extension=".zip", filename="archive.zip"),
        )
        .markdown
    )


def test_zip_keeps_readable_members_when_one_is_encrypted() -> None:
    """One password-protected member must not cost the reader the whole archive."""
    raw = _mark_entry_encrypted(
        _archive(**{"plain.txt": "readable content", "secret.txt": "ciphertext"}),
        b"secret.txt",
    )

    # Without the guard the read raises straight out of the converter.
    with pytest.raises(RuntimeError):
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            archive.read("secret.txt")

    markdown = _convert_archive(raw)

    assert "readable content" in markdown
    assert "## File: secret.txt" in markdown
    assert "encrypted" in markdown
    assert "ciphertext" not in markdown


def test_zip_keeps_readable_members_when_one_has_a_bad_crc() -> None:
    """A corrupt member is reported in place, not raised over the whole archive."""
    raw = bytearray(
        _archive(**{"plain.txt": "readable content", "damaged.txt": "0000000000"})
    )
    start = raw.find(b"0000000000")
    assert start > 0
    raw[start] = ord("X")

    with pytest.raises(zipfile.BadZipFile):
        with zipfile.ZipFile(io.BytesIO(bytes(raw))) as archive:
            archive.read("damaged.txt")

    markdown = _convert_archive(bytes(raw))

    assert "readable content" in markdown
    assert "## File: damaged.txt" in markdown
    assert "could not be read" in markdown


def test_zip_without_unreadable_members_is_unchanged() -> None:
    markdown = _convert_archive(_archive(**{"a.txt": "alpha", "b.txt": "bravo"}))

    assert "## File: a.txt\n\nalpha" in markdown
    assert "## File: b.txt\n\nbravo" in markdown
    assert "could not be read" not in markdown
    assert "encrypted" not in markdown
