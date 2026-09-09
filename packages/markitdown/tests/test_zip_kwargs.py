import io
import zipfile
from typing import Any, BinaryIO

from markitdown import (
    DocumentConverter,
    DocumentConverterResult,
    MarkItDown,
    StreamInfo,
)
from markitdown.converters._zip_converter import ZipConverter


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
