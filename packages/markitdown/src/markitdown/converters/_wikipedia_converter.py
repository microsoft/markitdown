import re
from typing import Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._markdown import _CustomMarkdown, _document_title, _parse_html

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/html",
    "application/xhtml",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".html",
    ".htm",
]


class WikipediaConverter(DocumentConverter):
    """Handle Wikipedia pages separately, focusing only on the main document content."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        """
        Make sure we're dealing with HTML content *from* Wikipedia.
        """

        url = stream_info.url or ""
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if not re.search(r"^https?:\/\/[a-zA-Z]{2,3}\.wikipedia.org\/", url):
            # Not a Wikipedia URL
            return False

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        # Not HTML content
        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        doc = _parse_html(file_stream, stream_info)

        # Print only the main content
        body_elm = doc.select_one("div#mw-content-text")
        title_elm = doc.select_one("span.mw-page-title-main")

        webpage_text = ""
        main_title = _document_title(doc)

        if body_elm:
            # What's the title
            if title_elm:
                main_title = title_elm.text or None

            # Treat whitespace-only titles as if they were absent
            if main_title:
                main_title = main_title.strip() or None

            # Convert the page
            webpage_text = (
                f"# {main_title}\n\n" if main_title else ""
            ) + _CustomMarkdown(**kwargs).convert(body_elm)
        else:
            webpage_text = _CustomMarkdown(**kwargs).convert(doc)

        return DocumentConverterResult(
            markdown=webpage_text,
            title=main_title,
        )
