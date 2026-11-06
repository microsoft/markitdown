from __future__ import annotations

import sys
import textwrap
from html import escape
from typing import TYPE_CHECKING, BinaryIO, Final, cast
from urllib.parse import urljoin
from xml.dom.minidom import Document, Element, Node
from xml.parsers.expat import ExpatError

from bs4 import BeautifulSoup
from defusedxml import minidom
from defusedxml.common import DefusedXmlException

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._markdown_options import _MarkdownOptions

if sys.version_info < (3, 11):
    from ._legacy_html import convert_feed
else:
    import turbohtml

    from ._markdown import _CustomMarkdown

if TYPE_CHECKING:
    from ._markdown_options import _OPTION_VALUE

_PRECISE_MIME_TYPE_PREFIXES: Final = [
    "application/rss",
    "application/rss+xml",
    "application/atom",
    "application/atom+xml",
]

_PRECISE_FILE_EXTENSIONS: Final = [".rss", ".atom"]

_CANDIDATE_MIME_TYPE_PREFIXES: Final = [
    "text/xml",
    "application/xml",
]

_CANDIDATE_FILE_EXTENSIONS: Final = [
    ".xml",
]

_ATOM_NAMESPACE: Final = "http://www.w3.org/2005/Atom"
_XHTML_NAMESPACE: Final = "http://www.w3.org/1999/xhtml"
_CONTENT_NAMESPACE: Final = "http://purl.org/rss/1.0/modules/content/"
_XML_NAMESPACE: Final = "http://www.w3.org/XML/1998/namespace"

# Keep block boundaries without splitting inline words such as co<b>op</b>erate.
_TEXT_BREAK_ELEMENTS: Final = frozenset(
    [
        "address",
        "article",
        "aside",
        "blockquote",
        "br",
        "dd",
        "div",
        "dl",
        "dt",
        "figcaption",
        "figure",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "td",
        "th",
        "tr",
        "ul",
    ]
)


class RssConverter(DocumentConverter):
    def __init__(self) -> None:
        super().__init__()
        self._kwargs: _FeedOptions = {}

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: _OPTION_VALUE,
    ) -> bool:
        mimetype: Final = (stream_info.mimetype or "").lower()
        extension: Final = (stream_info.extension or "").lower()

        if extension in _PRECISE_FILE_EXTENSIONS:
            return True

        for prefix in _PRECISE_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        if extension in _CANDIDATE_FILE_EXTENSIONS:
            return self._check_xml(file_stream)

        for prefix in _CANDIDATE_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return self._check_xml(file_stream)

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: _OPTION_VALUE,
    ) -> DocumentConverterResult:
        self._kwargs = cast("_FeedOptions", kwargs)
        doc: Final = minidom.parse(file_stream)
        doc.documentURI = stream_info.url or self._kwargs.get("url")
        feed_type: Final = self._feed_type(doc)

        if feed_type == "rss":
            return self._parse_rss_type(doc)
        if feed_type == "atom":
            return self._parse_atom_type(doc)
        msg: Final = "Unknown feed type"
        raise ValueError(msg)

    def _check_xml(self, file_stream: BinaryIO) -> bool:
        cur_pos: Final = file_stream.tell()
        try:
            doc: Final = minidom.parse(file_stream)
            return self._feed_type(doc) is not None
        except (ExpatError, DefusedXmlException, OSError):
            return False
        finally:
            file_stream.seek(cur_pos)

    def _feed_type(self, doc: Document) -> str | None:
        root: Final = cast("Element", doc.documentElement)
        if root.tagName == "rss":
            return "rss"
        if (
            root.localName == "feed"
            and root.namespaceURI in {None, _ATOM_NAMESPACE}
            and self._get_children(root, "entry")
        ):
            return "atom"
        return None

    def _parse_rss_type(self, doc: Document) -> DocumentConverterResult:
        root: Final = cast("Element", doc.documentElement)
        channel: Final = self._get_child(root, "channel")
        if channel is None:
            msg: Final = "No channel found in RSS feed"
            raise ValueError(msg)
        channel_title: Final = self._get_flattened_text(channel, "title")
        # RSS channel descriptions contain plain text; item descriptions can contain HTML.
        channel_description: Final = self._get_data_by_tag_name(channel, "description")
        md_text = ""
        if channel_title:
            md_text += f"# {channel_title}\n"
        if channel_description:
            md_text += f"{channel_description}\n"
        for item in self._get_children(channel, "item"):
            title = self._get_flattened_text(item, "title")
            description = self._get_data_by_tag_name(item, "description", kind="html")
            published = self._get_flattened_text(item, "pubDate")
            content = self._get_data_by_tag_name(item, "content:encoded", kind="html")

            if title:
                md_text += f"\n## {title}\n"
            if published:
                md_text += f"Published on: {published}\n"
            body_parts = (
                self._parse_content(
                    value,
                    base_url=self._get_field_base_url(item, tag_name),
                )
                for value, tag_name in (
                    (description, "description"),
                    (content, "content:encoded"),
                )
                if value
            )
            body = "\n\n".join(part for part in body_parts if part)
            if body and md_text and not md_text.endswith("\n"):
                md_text += "\n\n"
            md_text += body

        return DocumentConverterResult(
            markdown=md_text,
            title=channel_title,
        )

    def _parse_atom_type(self, doc: Document) -> DocumentConverterResult:
        root: Final = cast("Element", doc.documentElement)
        title: Final = self._get_flattened_text(root, "title", atom_text=True)
        subtitle: Final = self._get_flattened_text(root, "subtitle", atom_text=True)
        md_text = f"# {title}\n" if title else ""

        if subtitle:
            md_text += f"{subtitle}\n"
        for entry in self._get_children(root, "entry"):
            entry_title = self._get_flattened_text(entry, "title", atom_text=True)
            entry_summary, summary_is_markup = self._get_atom_content(entry, "summary")
            entry_updated = self._get_flattened_text(entry, "updated")
            entry_content, content_is_markup = self._get_atom_content(entry, "content")

            if entry_title:
                md_text += f"\n## {entry_title}\n"
            if entry_updated:
                md_text += f"Updated on: {entry_updated}\n"
            # Keep tag-shaped plain text such as <job_id> outside the HTML parser.
            body_parts = (
                (
                    self._parse_content(
                        value,
                        base_url=self._get_field_base_url(entry, tag_name),
                    )
                    if is_markup
                    else value
                )
                for value, is_markup, tag_name in (
                    (entry_summary, summary_is_markup, "summary"),
                    (entry_content, content_is_markup, "content"),
                )
                if value
            )
            body = "\n\n".join(part for part in body_parts if part)
            if body and md_text and not md_text.endswith("\n"):
                md_text += "\n\n"
            md_text += body

        return DocumentConverterResult(
            markdown=md_text,
            title=title,
        )

    def _get_flattened_text(
        self, element: Element, tag_name: str, *, atom_text: bool = False
    ) -> str | None:
        """Feed indentation must not split Markdown headings or create code blocks."""
        if atom_text:
            value, is_markup = self._get_atom_content(element, tag_name)
            if value and is_markup:
                soup: Final = BeautifulSoup(value, "html.parser")
                for block in soup.find_all(_TEXT_BREAK_ELEMENTS):
                    block.insert_before("\n")
                    block.append("\n")
                value = soup.get_text()
        else:
            value = self._get_data_by_tag_name(element, tag_name)
        if value is None:
            return None
        return (
            " ".join(part for line in value.splitlines() if (part := line.strip()))
            or None
        )

    def _get_atom_content(
        self, entry: Element, tag_name: str
    ) -> tuple[str | None, bool]:
        node: Final = self._get_child(entry, tag_name)
        if node is None:
            return None, True

        kind: Final = _atom_content_kind(
            node.getAttribute("type"), allow_media_types=tag_name == "content"
        )
        if kind == "binary":
            return None, True

        text = self._read_content(node, kind=kind)
        if kind != "text":
            return text or None, True

        # The first line can share the opening tag and lack the other lines' indentation.
        lines: Final = text.splitlines()
        if len(lines) > 1:
            text = lines[0] + "\n" + textwrap.dedent("\n".join(lines[1:]))
        return text.strip(), False

    def _parse_content(self, content: str, *, base_url: str = "") -> str:
        if sys.version_info < (3, 11):
            return convert_feed(content, base_url, self._kwargs)
        fragment: Final = turbohtml.parse_fragment(content)
        self._resolve_content_links(fragment, base_url)
        return _CustomMarkdown(**cast("_MarkdownOptions", self._kwargs)).convert(
            fragment
        )

    def _get_field_base_url(self, element: Element, tag_name: str) -> str:
        """An empty xml:base inherits the parent base, including the source URL."""
        bases: Final[list[str]] = []
        node: Node | None = self._get_child(element, tag_name)
        while node is not None:
            if isinstance(node, Element) and node.hasAttributeNS(
                _XML_NAMESPACE, "base"
            ):
                bases.append(node.getAttributeNS(_XML_NAMESPACE, "base"))
            node = node.parentNode
        document: Final = element.ownerDocument
        base_url = (document.documentURI or "") if document is not None else ""
        for reference in reversed(bases):
            base_url = _resolve_url(base_url, reference)
        return base_url

    def _resolve_content_links(
        self, fragment: turbohtml.Element, base_url: str
    ) -> None:
        """Inline XHTML retains nested xml:base scopes; CDATA inherits the enclosing field base."""
        stack: Final[list[tuple[turbohtml.Element, str]]] = [(fragment, base_url)]
        while stack:
            node, inherited_base = stack.pop()
            override = node.attr("xml:base")
            current_base = (
                _resolve_url(inherited_base, override)
                if override is not None
                else inherited_base
            )
            attributes: tuple[str, ...] = ()
            if node.tag == "a":
                attributes = ("href",)
            elif node.tag == "img":
                attributes = ("src", "data-src")
            for attribute in attributes:
                reference = node.attr(attribute)
                # Empty src must still allow the data-src fallback.
                if reference is not None and (reference or attribute == "href"):
                    node.attrs[attribute] = _resolve_url(current_base, reference)
            stack.extend(
                (child, current_base)
                for child in node.children
                if isinstance(child, turbohtml.Element)
            )

    def _get_data_by_tag_name(
        self, element: Element, tag_name: str, *, kind: str = "text"
    ) -> str | None:
        node: Final = self._get_child(element, tag_name)
        if node is None:
            return None
        return self._read_content(node, kind=kind) or None

    def _get_child(self, element: Element, tag_name: str) -> Element | None:
        return next(iter(self._get_children(element, tag_name)), None)

    def _get_children(self, element: Element, tag_name: str) -> list[Element]:
        """Nested metadata belongs to its own element."""
        namespace: str | None
        if tag_name == "content:encoded":
            namespace, local_name = _CONTENT_NAMESPACE, "encoded"
        else:
            namespace, local_name = element.namespaceURI, tag_name
        return [
            child
            for child in element.childNodes
            if isinstance(child, Element)
            and child.namespaceURI == namespace
            and child.localName == local_name
        ]

    def _read_content(self, element: Element, *, kind: str) -> str:
        """Use a stack to avoid minidom recursion limits on nested XML."""
        parts: Final[list[str]] = []
        stack: Final[list[Node | str]] = list(reversed(element.childNodes))
        while stack:
            child = stack.pop()
            if isinstance(child, str):
                parts.append(child)
            elif child.nodeType in {Node.TEXT_NODE, Node.CDATA_SECTION_NODE}:
                text = child.nodeValue or ""
                if kind == "text" or (kind == "html" and child.parentNode is element):
                    parts.append(text)
                else:
                    parts.append(escape(text, quote=False))
            elif isinstance(child, Element):
                if kind == "text":
                    if child.localName.lower() in _TEXT_BREAK_ELEMENTS:
                        parts.append("\n")
                        stack.append("\n")
                else:
                    # The HTML parser recognizes local HTML names, not x:strong.
                    name = (
                        child.localName
                        if child.namespaceURI == _XHTML_NAMESPACE
                        else child.tagName
                    )
                    attrs = "".join(
                        f' {attr.name}="{escape(attr.value, quote=True)}"'
                        for attr in child.attributes.values()
                    )
                    if child.childNodes:
                        parts.append(f"<{name}{attrs}>")
                        stack.append(f"</{name}>")
                    else:
                        parts.append(f"<{name}{attrs}/>")
                stack.extend(reversed(child.childNodes))
        return "".join(parts)


class _FeedOptions(_MarkdownOptions, total=False):
    url: str | None


def _resolve_url(base_url: str, reference: str) -> str:
    """Malformed links must not discard the feed body."""
    try:
        return urljoin(base_url, reference)
    except ValueError:
        # Leave malformed links to the Markdown converter's existing handling.
        return reference


def _atom_content_kind(content_type: str, *, allow_media_types: bool) -> str:
    """RFC 4287 permits MIME types on content, but only text/html/xhtml keywords on text constructs."""
    content_type = content_type.strip().lower()
    if content_type in {"", "text"}:
        return "text"
    if content_type in {"html", "xhtml"}:
        return content_type
    if not allow_media_types:
        return "text"

    media_type: Final = content_type.split(";", 1)[0].strip()
    if media_type == "text/html":
        return "html"
    if media_type.endswith(("+xml", "/xml")):
        return "xhtml"
    if media_type.startswith("text/"):
        return "text"
    return "binary"


__all__ = ["RssConverter"]
