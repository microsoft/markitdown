import io
import os
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
