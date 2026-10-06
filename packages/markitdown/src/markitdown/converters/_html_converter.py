import io
import warnings
from typing import Any, BinaryIO, Optional
from urllib.parse import urljoin
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

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Pop our own keyword before forwarding the rest to markdownify.
        # strict=True raises RecursionError instead of falling back to plain text.
        strict: bool = kwargs.pop("strict", False)

        # Parse the stream
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        soup = BeautifulSoup(file_stream, "html.parser", from_encoding=encoding)

        # Remove javascript and style blocks
        for script in soup(["script", "style"]):
            script.extract()

        # Determine effective base URL per WHATWG HTML spec:
        # First <base href="..."> resolved against stream_info.url if present.
        effective_base_url: Optional[str] = stream_info.url
        base_tag = soup.find("base", href=True)
        if base_tag and isinstance(base_tag, dict) and "href" in base_tag.attrs:
            pass  # handled below
        if base_tag and base_tag.get("href"):
            base_href = str(base_tag.get("href")).strip()
            if effective_base_url:
                effective_base_url = urljoin(effective_base_url, base_href)
            else:
                effective_base_url = base_href

        if effective_base_url:
            for a_tag in soup.find_all("a", href=True):
                href_val = a_tag.get("href")
                if href_val:
                    a_tag["href"] = urljoin(effective_base_url, str(href_val))

            for img_tag in soup.find_all("img"):
                src_val = img_tag.get("src")
                if src_val and not str(src_val).lower().startswith("data:"):
                    img_tag["src"] = urljoin(effective_base_url, str(src_val))
                data_src_val = img_tag.get("data-src")
                if data_src_val and not str(data_src_val).lower().startswith("data:"):
                    img_tag["data-src"] = urljoin(effective_base_url, str(data_src_val))

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
