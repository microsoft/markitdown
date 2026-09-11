import io
import sys
import warnings
from typing import Any, BinaryIO, Optional
from bs4 import BeautifulSoup

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo
from ._markdownify import _CustomMarkdownify

_dependency_exc_info = None
try:
    from readability import Document as ReadabilityDocument
except ImportError:
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/html",
    "application/xhtml",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".html",
    ".htm",
]


class HtmlConverter(DocumentConverter):
    """Anything with content type text/html"""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Pop our own keywords before forwarding the rest to markdownify.
        # strict=True raises RecursionError instead of falling back to plain text.
        strict: bool = kwargs.pop("strict", False)
        reader_mode: bool = kwargs.pop("reader_mode", False)

        # Parse the stream
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        raw_html = file_stream.read()

        title = None

        if reader_mode:
            if _dependency_exc_info is not None:
                raise MissingDependencyException(
                    MISSING_DEPENDENCY_MESSAGE.format(
                        converter="HtmlConverter",
                        extension="html (reader mode)",
                        feature="readability",
                    )
                )
            html_text = raw_html.decode(encoding, errors="replace")
            doc = ReadabilityDocument(html_text, url=stream_info.url)
            article_html = doc.summary()
            title = doc.short_title()
            soup = BeautifulSoup(article_html, "html.parser")
        else:
            soup = BeautifulSoup(raw_html, "html.parser", from_encoding=encoding)

        # Remove javascript and style blocks
        for script in soup(["script", "style"]):
            script.extract()

        # Print only the main content
        body_elm = soup.find("body")
        webpage_text = ""
        try:
            if body_elm:
                webpage_text = _CustomMarkdownify(**kwargs).convert_soup(body_elm)
            else:
                webpage_text = _CustomMarkdownify(**kwargs).convert_soup(soup)
        except RecursionError:
            if strict:
                raise
            # Large or deeply-nested HTML can exceed Python's recursion limit
            # during markdownify's recursive DOM traversal.  Fall back to
            # BeautifulSoup's iterative get_text() so the caller still gets
            # usable plain-text content instead of raw HTML.
            warnings.warn(
                "HTML document is too deeply nested for markdown conversion "
                "(RecursionError). Falling back to plain-text extraction.",
                stacklevel=2,
            )
            target = body_elm if body_elm else soup
            webpage_text = target.get_text("\n", strip=True)

        assert isinstance(webpage_text, str)

        # remove leading and trailing \n
        webpage_text = webpage_text.strip()

        if title is None:
            title = None if soup.title is None else soup.title.string

        return DocumentConverterResult(
            markdown=webpage_text,
            title=title,
        )

    def convert_string(
        self, html_content: str, *, url: Optional[str] = None, **kwargs
    ) -> DocumentConverterResult:
        """
        Non-standard convenience method to convert a string to markdown.
        Given that many converters produce HTML as intermediate output, this
        allows for easy conversion of HTML to markdown.
        """
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
