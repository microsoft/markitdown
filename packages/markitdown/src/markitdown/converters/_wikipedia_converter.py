import re
import bs4
from typing import Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._markdownify import _CustomMarkdownify

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/html",
    "application/xhtml",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".html",
    ".htm",
]

# A Wikipedia article URL: http(s), a language subdomain, an optional mobile
# (.m) marker, then wikipedia.org. Language codes are BCP 47-style subdomains
# rather than always two or three letters: besides en/de/ja there is `simple`,
# and hyphenated codes such as be-tarask, zh-min-nan, zh-classical, be-x-old.
# The earlier `[a-zA-Z]{2,3}` form rejected all 13 of those editions, so their
# pages fell through to the generic HTML converter and came out wrapped in the
# site navigation and footer instead of the article alone.
_WIKIPEDIA_URL = re.compile(r"^https?:\/\/[a-z]{2,8}(?:-[a-z0-9]{1,9})*(?:\.m)?\.wikipedia\.org\/", re.IGNORECASE)


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

        if not _WIKIPEDIA_URL.search(url):
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
        # Parse the stream
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        soup = bs4.BeautifulSoup(file_stream, "html.parser", from_encoding=encoding)

        # Remove javascript and style blocks
        for script in soup(["script", "style"]):
            script.extract()

        # Print only the main content
        body_elm = soup.find("div", {"id": "mw-content-text"})
        # Wikipedia only wraps the title in mw-page-title-main when it is plain
        # text. Titles that carry markup -- italicised species, film, album and
        # journal names -- are written straight into the first heading instead.
        title_elm = soup.find("span", {"class": "mw-page-title-main"}) or soup.find(
            "h1", {"id": "firstHeading"}
        )

        webpage_text = ""
        main_title = None if soup.title is None else soup.title.string

        if body_elm:
            # What's the title
            if title_elm and isinstance(title_elm, bs4.Tag):
                # .string is None as soon as the element holds more than one
                # child, which is what a title mixing markup with plain text
                # looks like, so gather the descendant text instead.
                main_title = title_elm.get_text()

            # Treat whitespace-only titles as if they were absent
            if main_title:
                main_title = main_title.strip() or None

            # Convert the page
            webpage_text = (
                f"# {main_title}\n\n" if main_title else ""
            ) + _CustomMarkdownify(**kwargs).convert_soup(body_elm)
        else:
            webpage_text = _CustomMarkdownify(**kwargs).convert_soup(soup)

        return DocumentConverterResult(
            markdown=webpage_text,
            title=main_title,
        )
