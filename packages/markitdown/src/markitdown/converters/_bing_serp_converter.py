"""Bing SERP HTML converter — extracts organic search results from Bing result pages."""

import re
import base64
import binascii
import logging
from urllib.parse import parse_qs, urlparse
from typing import Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import FileConversionException
from .._stream_info import StreamInfo
from ._markdownify import _CustomMarkdownify

logger = logging.getLogger(__name__)

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
        """Make sure we're dealing with HTML content *from* Bing."""
        url = stream_info.url or ""
        if not re.search(r"^https://www\.bing\.com/search\?q=", url):
            return False
        return self._accepted_by_mime_or_ext(
            stream_info, ACCEPTED_MIME_TYPE_PREFIXES, ACCEPTED_FILE_EXTENSIONS
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        if stream_info.url is None:
            raise FileConversionException(
                "BingSerpConverter requires a URL in stream_info"
            )

        # Parse the query parameters
        parsed_params = parse_qs(urlparse(stream_info.url).query)
        query = parsed_params.get("q", [""])[0]

        # Parse the stream as BeautifulSoup
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        try:
            soup = __import__("bs4", fromlist=["BeautifulSoup"]).BeautifulSoup(
                file_stream, "html.parser", from_encoding=encoding
            )
        except (IOError, UnicodeDecodeError) as e:
            logger.warning("BingSerpConverter: BeautifulSoup parse failed: %s", e)
            raise FileConversionException(
                f"BingSerpConverter: failed to parse HTML: {e}"
            ) from e

        # Clean up some formatting
        try:
            for tptt in soup.find_all(class_="tptt"):
                if hasattr(tptt, "string") and tptt.string:
                    tptt.string += " "
            for slug in soup.find_all(class_="algoSlug_icon"):
                slug.extract()
        except (AttributeError, RuntimeError) as e:
            logger.warning("BingSerpConverter: HTML cleanup failed: %s", e)

        # Parse the algorithmic results
        _markdownify = _CustomMarkdownify(**kwargs)
        results = list()
        for result in soup.find_all(class_="b_algo"):
            if not hasattr(result, "find_all"):
                continue

            # Rewrite redirect urls
            for a in result.find_all("a", href=True):
                parsed_href = urlparse(a["href"])
                qs = parse_qs(parsed_href.query)

                # The destination is contained in the u parameter,
                # but appears to be base64 encoded, with some prefix
                if "u" in qs:
                    u = (
                        qs["u"][0][2:].strip() + "=="
                    )  # Python 3 doesn't care about extra padding

                    try:
                        # RFC 4648 / Base64URL" variant, which uses "-" and "_"
                        a["href"] = base64.b64decode(u, altchars="-_").decode("utf-8")
                    except UnicodeDecodeError:
                        pass
                    except binascii.Error:
                        pass
                    except (ValueError, TypeError) as e:
                        logger.warning(
                            "BingSerpConverter: base64 decode failed for %s: %s",
                            u[:50],
                            e,
                        )

            # Convert to markdown
            try:
                md_result = _markdownify.convert_soup(result).strip()
            except (RuntimeError, ValueError, TypeError) as e:
                logger.warning(
                    "BingSerpConverter: markdownify conversion failed: %s", e
                )
                continue

            lines = [line.strip() for line in re.split(r"\n+", md_result)]
            results.append("\n".join([line for line in lines if len(line) > 0]))

        webpage_text = (
            f"## A Bing search for '{query}' found the following results:\n\n"
            + "\n\n".join(results)
        )

        title = None
        try:
            if soup.title is not None:
                title = soup.title.string
        except AttributeError:
            pass

        return DocumentConverterResult(
            markdown=webpage_text,
            title=title,
        )
