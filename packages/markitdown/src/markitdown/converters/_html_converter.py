import io
import re
import warnings
from typing import Any, BinaryIO, Optional
from bs4 import BeautifulSoup

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

    def _detect_html_encoding(self, file_stream: BinaryIO) -> Optional[str]:
        """Peek at the HTML content to find charset declaration (<meta charset>).

        Follows the HTML5 encoding sniffing algorithm: the <meta charset> tag
        (or Content-Type http-equiv) is the authoritative source, taking
        precedence over heuristic detection that is unreliable for non-Latin
        scripts on some platforms.
        """
        cur_pos = file_stream.tell()
        try:
            # Read first 4 KB — enough to cover <head> and <meta> in any
            # reasonable HTML document (HTML5 spec uses 1024 bytes minimum).
            raw = file_stream.read(4096)
            # Decode as ASCII-superset (Latin-1) so we can scan for meta tags
            # without committing to the real encoding yet.
            try:
                head = raw.decode("ascii")
            except UnicodeDecodeError:
                head = raw.decode("latin-1")

            # Pattern 1: <meta charset="utf-8">   (HTML5)
            m = re.search(
                r'<meta\b[^>]*\bcharset\s*=\s*["\']?\s*([\w\-\d]+)\s*["\']?',
                head,
                re.IGNORECASE,
            )
            if m:
                return m.group(1)

            # Pattern 2: <meta http-equiv="Content-Type"
            #            content="text/html; charset=utf-8">
            m = re.search(
                r'<meta\b[^>]*\bhttp-equiv\s*=\s*["\']?Content-Type["\']?[^>]*\b'
                r'content\s*=\s*["\'][^"\']*\bcharset\s*=\s*([\w\-\d]+)',
                head,
                re.IGNORECASE,
            )
            if m:
                return m.group(1)

            return None
        finally:
            file_stream.seek(cur_pos)

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Pop our own keyword before forwarding the rest to markdownify.
        # strict=True raises RecursionError instead of falling back to plain text.
        strict: bool = kwargs.pop("strict", False)

        # Determine encoding — prefer the HTML <meta charset> declaration,
        # then the stream_info hint, then UTF-8:
        #   - <meta charset> is the HTML5-authoritative source.
        #   - stream_info.charset comes from charset_normalizer which can
        #     mis-detect non-Latin UTF-8 files (e.g. Chinese) on CJK-locale
        #     Windows systems.
        meta_encoding = self._detect_html_encoding(file_stream)
        if meta_encoding:
            encoding = meta_encoding
        elif stream_info.charset is not None:
            encoding = stream_info.charset
        else:
            encoding = "utf-8"

        # Parse the stream
        soup = BeautifulSoup(file_stream, "html.parser", from_encoding=encoding)

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

        return DocumentConverterResult(
            markdown=webpage_text,
            title=None if soup.title is None else soup.title.string,
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
