from __future__ import annotations

import io
import sys
from typing import TYPE_CHECKING, BinaryIO, Final, cast

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

if sys.version_info < (3, 11):
    from ._legacy_html import convert_html
else:
    import turbohtml

    from ._markdown import _CustomMarkdown, _document_title, _parse_html_with_source

if TYPE_CHECKING:
    from ._markdown_options import _OPTION_VALUE, _MarkdownOptions


_ACCEPTED_MIME_TYPE_PREFIXES: Final = [
    "text/html",
    "application/xhtml",
]

_ACCEPTED_FILE_EXTENSIONS: Final = [
    ".html",
    ".htm",
]


class HtmlConverter(DocumentConverter):
    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: _OPTION_VALUE,
    ) -> bool:
        mimetype: Final = (stream_info.mimetype or "").lower()
        extension: Final = (stream_info.extension or "").lower()

        if extension in _ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in _ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: _OPTION_VALUE,
    ) -> DocumentConverterResult:
        if sys.version_info < (3, 11):
            return convert_html(
                file_stream, stream_info, cast("_MarkdownOptions", kwargs)
            )
        doc, source = _parse_html_with_source(file_stream, stream_info)
        body_elm: Final = doc.select_one("body")
        # Fragment context retains content moved into a synthetic head.
        target: Final = (
            turbohtml.parse_fragment(source if source is not None else doc.to_source())
            if body_elm is not None and body_elm.source_line is None
            else body_elm or doc
        )
        if body_elm is not None and body_elm.source_line is None:
            for element in target.select("title, template"):
                element.unwrap()
        return DocumentConverterResult(
            markdown=_CustomMarkdown(**cast("_MarkdownOptions", kwargs))
            .convert(target)
            .strip(),
            title=_document_title(doc),
        )

    def convert_string(
        self,
        html_content: str,
        *,
        url: str | None = None,
        **kwargs: _OPTION_VALUE,
    ) -> DocumentConverterResult:
        return self.convert(
            file_stream=io.BytesIO(html_content.encode("utf-8")),
            stream_info=StreamInfo(
                mimetype="text/html",
                extension=".html",
                charset="utf-8",
                url=url,
            ),
            **kwargs,
        )


__all__ = ["HtmlConverter"]
