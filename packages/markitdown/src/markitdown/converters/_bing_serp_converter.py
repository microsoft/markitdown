from __future__ import annotations

import base64
import binascii
import re
from typing import TYPE_CHECKING, BinaryIO, Final, cast
from urllib.parse import parse_qs, urlparse

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


class BingSerpConverter(DocumentConverter):
    """Exclude adverts from Bing search results."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: _OPTION_VALUE,
    ) -> bool:
        url: Final = stream_info.url or ""
        mimetype: Final = (stream_info.mimetype or "").lower()
        extension: Final = (stream_info.extension or "").lower()

        if not re.search(r"^https://www\.bing\.com/search\?q=", url):
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
        assert stream_info.url is not None

        query: Final = parse_qs(urlparse(stream_info.url).query).get("q", [""])[0]

        doc: Final = _parse_html(file_stream, stream_info)

        for tptt in doc.select(".tptt"):
            if len(tptt.children) == 1 and tptt.text:
                tptt.set_text(tptt.text + " ")
        for slug in doc.select(".algoSlug_icon"):
            slug.extract()

        markdown: Final = _CustomMarkdown(**cast("_MarkdownOptions", kwargs))
        results: Final[list[str]] = []
        for result in doc.select(".b_algo"):
            for anchor in result.select("a[href]"):
                parameters = parse_qs(urlparse(anchor.attr("href") or "").query)

                # Bing prefixes the Base64URL destination with two characters.
                if destination := parameters.get("u"):
                    try:
                        anchor.attrs["href"] = base64.b64decode(
                            destination[0][2:].strip() + "==", altchars="-_"
                        ).decode("utf-8")
                    except (UnicodeDecodeError, binascii.Error):
                        pass

            results.append(
                "\n".join(
                    line.strip()
                    for line in re.split(r"\n+", markdown.convert(result).strip())
                    if line.strip()
                )
            )

        webpage_text: Final = (
            f"## A Bing search for '{query}' found the following results:\n\n"
            + "\n\n".join(results)
        )

        return DocumentConverterResult(
            markdown=webpage_text,
            title=_document_title(doc),
        )


__all__ = ["BingSerpConverter"]
