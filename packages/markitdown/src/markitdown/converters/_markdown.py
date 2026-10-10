import re
from typing import TYPE_CHECKING, Any, BinaryIO, Final, Literal
from urllib.parse import quote, urlparse, urlunparse

import turbohtml
from bs4 import BeautifulSoup, Tag
from turbohtml import Document, Element, Markdown

from .._stream_info import StreamInfo

if TYPE_CHECKING:
    from collections.abc import Callable


_PERCENT_ENCODED_OCTET = re.compile(r"%[0-9A-Fa-f]{2}")

# The heading styles markdownify accepted, mapped onto turbohtml's names;
# markdownify treated any other value as ATX
_HEADING_STYLES: dict[str, Literal["atx", "atx_closed", "setext"]] = {
    "atx_closed": "atx_closed",
    "underlined": "setext",
}


def _quote_path_preserving_percent_encoded_octets(path: str) -> str:
    """Quote a URL path while preserving existing %HH byte encodings."""
    parts: list[str] = []
    last_end = 0

    for match in _PERCENT_ENCODED_OCTET.finditer(path):
        parts.append(quote(path[last_end : match.start()]))
        parts.append(match.group(0))
        last_end = match.end()

    parts.append(quote(path[last_end:]))
    return "".join(parts)


def _parse_html(file_stream: BinaryIO, stream_info: StreamInfo) -> Document:
    """Parse an HTML stream, decoding it with the charset the stream declares."""
    return _parse_html_with_source(file_stream, stream_info)[0]


def _parse_html_with_source(
    file_stream: BinaryIO, stream_info: StreamInfo
) -> tuple[Document, str | None]:
    data = file_stream.read()
    try:
        source = data.decode(stream_info.charset or "utf-8")
    except (LookupError, UnicodeDecodeError):
        # The declared charset is unknown or wrong, so sniff the bytes instead
        return turbohtml.parse(data, detect_encoding=True), None
    return turbohtml.parse(source), source


def _document_title(doc: Document | Element) -> str | None:
    title = doc.select_one("title")
    return None if title is None else title.text or None


class _CustomMarkdown:
    """
    Renders parsed HTML as Markdown. Changes from turbohtml's defaults include:

    - Accepting the markdownify options markitdown has always forwarded.
    - Removing javascript hyperlinks.
    - Truncating images with large data:uri sources.
    - Ensuring URIs are properly escaped, and do not conflict with Markdown syntax
    """

    def __init__(self, **options: Any) -> None:
        self._code_language: Final[str] = options.get("code_language", "")
        self._code_language_callback: Final[Callable[[Tag], str | None] | None] = (
            options.get("code_language_callback")
        )
        self._strip_pre: Final[str | None] = options.get("strip_pre", "strip")
        self._pre_languages: Final[dict[Element, str]] = {}
        self._keep_data_uris = options.get("keep_data_uris", False)
        self._autolinks = options.get("autolinks", True)
        self._default_title = options.get("default_title", False)
        strong_em_symbol = options.get("strong_em_symbol", "*")
        converters = {
            "a": self._convert_a,
            "img": self._convert_img,
            "pre": self._render_pre,
            "input": lambda el, text: (
                ("[x] " if "checked" in el.attrs else "[ ] ")
                if el.attr("type") == "checkbox"
                else ""
            ),
            "u": lambda el, text: f"<u>{text}</u>",
        }
        for tag in ("sub", "sup"):
            if symbol := options.get(f"{tag}_symbol"):
                closing = (
                    "</" + symbol[1:]
                    if symbol[:1] == "<" and symbol[-1:] == ">"
                    else symbol
                )
                converters[tag] = lambda el, text, symbol=symbol, closing=closing: (
                    f"{symbol}{text}{closing}"
                )
        # Tags that are stripped, or not converted, render as plain text, so
        # none of the converters above may apply to them
        strip = options.get("strip")
        convert = options.get("convert")
        if strip is not None:
            converters = {k: v for k, v in converters.items() if k not in strip}
        elif convert is not None:
            converters = {k: v for k, v in converters.items() if k in convert}
        self._convert_pre: Final[bool] = (
            "pre" not in strip
            if strip is not None
            else convert is None or "pre" in convert
        )
        self._markdown = Markdown(
            headings=Markdown.Headings(
                style=_HEADING_STYLES.get(
                    options.get("heading_style", "atx").lower(), "atx"
                )
            ),
            lists=Markdown.Lists(bullets=options.get("bullets", "*+-")),
            inline=Markdown.Inline(
                strong=strong_em_symbol * 2, emphasis=strong_em_symbol
            ),
            code=Markdown.Code(language=options.get("code_language", "")),
            tables=Markdown.Tables(
                header="first" if options.get("table_infer_header") else "detect",
                cell_blocks="text",
            ),
            escaping=Markdown.Escaping(
                mode="all" if options.get("escape_misc") else "none",
                asterisks=options.get("escape_asterisks", True),
                underscores=options.get("escape_underscores", True),
            ),
            wrapping=Markdown.Wrapping(
                width=options.get("wrap_width", 80) if options.get("wrap") else 0
            ),
            document=Markdown.Document(
                line_break=(
                    "backslash"
                    if options.get("newline_style", "spaces").lower() == "backslash"
                    else "spaces"
                ),
                trim=options.get("strip_document", "strip") or "none",
            ),
            strip=strip,
            convert=convert,
            converters=converters,
        )

    def convert(self, node: Document | Element) -> str:
        self._pre_languages.clear()
        if self._convert_pre:
            tags: Final[dict[Element, Tag]] = {}
            if self._code_language_callback is not None:
                root: turbohtml.Node = node
                while (parent := root.parent) is not None:
                    root = parent
                tags.update(
                    zip(
                        root.select("pre"),
                        BeautifulSoup(root.serialize(), "html.parser").find_all("pre"),
                        strict=True,
                    )
                )
            for pre in node.select("pre"):
                self._prepare_pre(
                    pre,
                    self._code_language_callback(tags[pre]) or self._code_language
                    if self._code_language_callback is not None and pre.text
                    else None,
                )
        # An underline around nothing but whitespace or a line break would
        # render as nothing at all, so let its content render in its place
        for underline in node.select("u"):
            if not underline.text.strip():
                underline.unwrap()
        return node.to_markdown(self._markdown)

    def _prepare_pre(self, pre: Element, language: str | None = None) -> None:
        if not pre.text:
            pre.extract()
            return
        opening, _, rendered = pre.to_markdown(
            Markdown(code=Markdown.Code(language=self._code_language))
        ).partition("\n")
        text, _, fence = rendered.rpartition("\n")
        # Native fences consume one trailing newline; restore it before applying strip_pre.
        if pre.text.endswith("\n"):
            text += "\n"
        if language is None:
            language = opening[len(fence) :]
        if self._strip_pre == "strip":
            text = re.sub(r"[ \n]*$", "", re.sub(r"^[ \n]*\n", "", text))
        elif self._strip_pre == "strip_one":
            text = re.sub(r"\n *$", "", re.sub(r"^ *\n", "", text))
        elif self._strip_pre is not None:
            msg = f"Invalid value for strip_pre: {self._strip_pre}"
            raise ValueError(msg)
        pre.clear()
        self._pre_languages[pre] = language
        code: Final = Element("code")
        code.append(turbohtml.Text(text + "\n" if text.endswith("\n") else text))
        pre.append(code)

    def _render_pre(self, pre: Element, text: str) -> str:
        ancestor = pre.parent
        while isinstance(ancestor, Element):
            if ancestor.tag in {"td", "th"}:
                return text
            ancestor = ancestor.parent
        return pre.to_markdown(
            Markdown(code=Markdown.Code(language=self._pre_languages[pre]))
        )

    def _convert_a(self, el: Element, text: str) -> str:
        """Same as usual converter, but removes JavaScript links and escapes URIs."""
        if not text:
            return ""
        href = el.attr("href")
        title = el.attr("title")

        # Escape URIs and skip non-http or file schemes
        if href:
            try:
                parsed_url = urlparse(href)
                if parsed_url.scheme and parsed_url.scheme.lower() not in [
                    "http",
                    "https",
                    "file",
                ]:
                    return text
                href = urlunparse(
                    parsed_url._replace(
                        path=_quote_path_preserving_percent_encoded_octets(
                            parsed_url.path
                        )
                    )
                )
            except ValueError:
                return text

        # For the replacement see #29: text nodes underscores are escaped
        if (
            self._autolinks
            and text.replace(r"\_", "_") == href
            and not title
            and not self._default_title
        ):
            return f"<{href}>"
        if self._default_title and not title:
            title = href
        title_part = ' "{}"'.format(title.replace('"', r"\"")) if title else ""
        return f"[{text}]({href}{title_part})" if href else text

    def _convert_img(self, el: Element, text: str) -> str:
        """Same as usual converter, but removes data URIs"""

        alt = el.attr("alt") or ""
        src = el.attr("src") or ""
        data_src = el.attr("data-src") or ""
        # Lazy-loading libraries commonly leave a tiny placeholder data URI in
        # src and put the real image in data-src. Prefer data-src when src
        # isn't a usable URL, so the placeholder doesn't win over actual
        # content. When keep_data_uris is set the caller explicitly wants the
        # embedded bytes, so a data URI in src is left alone.
        if data_src and (
            not src or (src[:5].lower() == "data:" and not self._keep_data_uris)
        ):
            src = data_src
        title = el.attr("title") or ""
        title_part = ' "{}"'.format(title.replace('"', r"\"")) if title else ""
        # Remove all line breaks from alt
        alt = alt.replace("\n", " ")

        # Remove dataURIs
        if src[:5].lower() == "data:" and not self._keep_data_uris:
            src = src.split(",")[0] + "..."

        return f"![{alt}]({src}{title_part})"


__all__ = [
    "_CustomMarkdown",
    "_document_title",
    "_parse_html",
    "_parse_html_with_source",
]
