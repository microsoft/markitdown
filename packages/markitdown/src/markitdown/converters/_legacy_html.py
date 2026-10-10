from __future__ import annotations

import base64
import binascii
import re
import warnings
from typing import TYPE_CHECKING, BinaryIO, Final
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup, Tag

from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from ._markdownify import _CustomMarkdownify

if TYPE_CHECKING:
    from ._markdown_options import _MarkdownOptions


def convert_html(
    stream: BinaryIO, info: StreamInfo, options: _MarkdownOptions
) -> DocumentConverterResult:
    soup: Final = _parse_html(stream, info)
    return DocumentConverterResult(
        markdown=_convert(soup.select_one("body") or soup, options).strip(),
        title=soup.title.string if soup.title else None,
    )


def convert_bing(
    stream: BinaryIO, info: StreamInfo, options: _MarkdownOptions
) -> DocumentConverterResult:
    soup: Final = BeautifulSoup(
        stream, "html.parser", from_encoding=info.charset or "utf-8"
    )
    for title in soup.select(".tptt"):
        if title.string:
            title.string += " "
    for slug in soup.select(".algoSlug_icon"):
        slug.extract()
    results: Final[list[str]] = []
    for result in soup.select(".b_algo"):
        for anchor in result.select("a[href]"):
            parameters = parse_qs(urlparse(str(anchor["href"])).query)
            # Bing prefixes the Base64URL destination with two characters.
            if destination := parameters.get("u"):
                try:
                    anchor["href"] = base64.b64decode(
                        destination[0][2:].strip() + "==", altchars="-_"
                    ).decode("utf-8")
                except (UnicodeDecodeError, binascii.Error):
                    pass
        results.append(
            "\n".join(
                line.strip()
                for line in re.split(
                    r"\n+", _CustomMarkdownify(**options).convert_soup(result).strip()
                )
                if line.strip()
            )
        )
    query: Final = parse_qs(urlparse(info.url or "").query).get("q", [""])[0]
    return DocumentConverterResult(
        markdown=f"## A Bing search for '{query}' found the following results:\n\n"
        + "\n\n".join(results),
        title=soup.title.string if soup.title else None,
    )


def convert_wikipedia(
    stream: BinaryIO, info: StreamInfo, options: _MarkdownOptions
) -> DocumentConverterResult:
    soup: Final = _parse_html(stream, info)
    body: Final = soup.select_one("div#mw-content-text")
    title = soup.title.string if soup.title else None
    if body:
        if heading := soup.select_one("span.mw-page-title-main") or soup.select_one(
            "h1#firstHeading"
        ):
            title = heading.get_text()
        title = title.strip() or None if title else None
        markdown = (f"# {title}\n\n" if title else "") + _CustomMarkdownify(
            **options
        ).convert_soup(body)
    else:
        markdown = _CustomMarkdownify(**options).convert_soup(soup)
    return DocumentConverterResult(markdown=markdown, title=title)


def convert_feed(content: str, base_url: str, options: _MarkdownOptions) -> str:
    soup: Final = BeautifulSoup(content, "html.parser")
    pending: Final[list[tuple[Tag, str]]] = [(soup, base_url)]
    while pending:
        node, inherited = pending.pop()
        override = node.get("xml:base")
        current = (
            _resolve_url(inherited, override)
            if isinstance(override, str)
            else inherited
        )
        attributes = (
            ("href",)
            if node.name == "a"
            else ("src", "data-src")
            if node.name == "img"
            else ()
        )
        for attribute in attributes:
            reference = node.get(attribute)
            if isinstance(reference, str) and (reference or attribute == "href"):
                node[attribute] = _resolve_url(current, reference)
        pending.extend(
            (child, current) for child in node.children if isinstance(child, Tag)
        )
    return _convert(soup, options)


def _parse_html(stream: BinaryIO, info: StreamInfo) -> BeautifulSoup:
    soup: Final = BeautifulSoup(
        stream, "html.parser", from_encoding=info.charset or "utf-8"
    )
    for element in soup.select("script, style"):
        element.extract()
    return soup


def _convert(soup: Tag, options: _MarkdownOptions) -> str:
    try:
        return _CustomMarkdownify(**options).convert_soup(soup)
    except RecursionError:
        if options.get("strict", False):
            raise
        warnings.warn(
            "HTML content is too deeply nested for markdown conversion (RecursionError). "
            "Falling back to plain-text extraction.",
            stacklevel=2,
        )
        return soup.get_text("\n", strip=True)


def _resolve_url(base: str, reference: str) -> str:
    try:
        return urljoin(base, reference)
    except ValueError:
        return reference


__all__ = ["convert_bing", "convert_feed", "convert_html", "convert_wikipedia"]
