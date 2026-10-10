from __future__ import annotations

import re
from typing import TYPE_CHECKING, BinaryIO, Final, cast

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._markdown import _CustomMarkdown, _document_title, _parse_html

if TYPE_CHECKING:
    from ._markdown import _OPTION_VALUE, _MarkdownOptions


_ACCEPTED_MIME_TYPE_PREFIXES: Final = [
    "text/html",
    "application/xhtml",
]

_ACCEPTED_FILE_EXTENSIONS: Final = [
    ".html",
    ".htm",
]


class WikipediaConverter(DocumentConverter):
    """Exclude navigation and preserve the article title."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: _OPTION_VALUE,
    ) -> bool:
        url: Final = stream_info.url or ""
        mimetype: Final = (stream_info.mimetype or "").lower()
        extension: Final = (stream_info.extension or "").lower()

        if not re.search(r"^https?:\/\/[a-zA-Z]{2,3}(\.m)?\.wikipedia.org\/", url):
            return False

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
        doc: Final = _parse_html(file_stream, stream_info)

        body_elm: Final = doc.select_one("div#mw-content-text")
        title_elm: Final = doc.select_one("span.mw-page-title-main") or doc.select_one(
            "h1#firstHeading"
        )

        webpage_text = ""
        main_title = _document_title(doc)

        if body_elm:
            if title_elm:
                main_title = title_elm.text or None

            if main_title:
                main_title = main_title.strip() or None

            webpage_text = (
                f"# {main_title}\n\n" if main_title else ""
            ) + _CustomMarkdown(**cast("_MarkdownOptions", kwargs)).convert(body_elm)
        else:
            webpage_text = _CustomMarkdown(**cast("_MarkdownOptions", kwargs)).convert(
                doc
            )

        return DocumentConverterResult(
            markdown=webpage_text,
            title=main_title,
        )


__all__ = ["WikipediaConverter"]
