import re
import base64
import binascii
from urllib.parse import parse_qs, urlparse
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


class BingSerpConverter(DocumentConverter):
    """
    Handle Bing results pages (only the organic search results).
    NOTE: It is better to use the Bing API
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        """
        Make sure we're dealing with HTML content *from* Bing.
        """

        url = stream_info.url or ""
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if not re.search(r"^https://www\.bing\.com/search\?q=", url):
            # Not a Bing SERP URL
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
        assert stream_info.url is not None

        # Parse the query parameters
        parsed_params = parse_qs(urlparse(stream_info.url).query)
        query = parsed_params.get("q", [""])[0]

        doc = _parse_html(file_stream, stream_info)

        # Clean up some formatting
        for tptt in doc.select(".tptt"):
            if len(tptt.children) == 1 and tptt.text:
                tptt.set_text(tptt.text + " ")
        for slug in doc.select(".algoSlug_icon"):
            slug.extract()

        # Parse the algorithmic results
        _markdown = _CustomMarkdown(**kwargs)
        results = list()
        for result in doc.select(".b_algo"):
            # Rewrite redirect urls
            for a in result.select("a[href]"):
                parsed_href = urlparse(a.attr("href") or "")
                qs = parse_qs(parsed_href.query)

                # The destination is contained in the u parameter,
                # but appears to be base64 encoded, with some prefix
                if "u" in qs:
                    u = (
                        qs["u"][0][2:].strip() + "=="
                    )  # Python 3 doesn't care about extra padding

                    try:
                        # RFC 4648 / Base64URL variant, which uses "-" and "_"
                        a.attrs["href"] = base64.b64decode(u, altchars="-_").decode(
                            "utf-8"
                        )
                    except UnicodeDecodeError:
                        pass
                    except binascii.Error:
                        pass

            # Convert to markdown
            md_result = _markdown.convert(result).strip()
            lines = [line.strip() for line in re.split(r"\n+", md_result)]
            results.append("\n".join([line for line in lines if len(line) > 0]))

        webpage_text = (
            f"## A Bing search for '{query}' found the following results:\n\n"
            + "\n\n".join(results)
        )

        return DocumentConverterResult(
            markdown=webpage_text,
            title=_document_title(doc),
        )
