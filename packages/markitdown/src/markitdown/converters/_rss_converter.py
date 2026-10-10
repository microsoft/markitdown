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

# Boundaries to retain when reducing markup to readable heading/plain text.
# Inline elements must not introduce spaces (e.g. co<b>op</b>erate).
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


def _resolve_url(base_url: str, reference: str) -> str:
    """Resolve a reference without letting a malformed URI drop the body."""
    try:
        return urljoin(base_url, reference)
    except ValueError:
        # Leave malformed links to the Markdown converter's existing handling.
        return reference


def _atom_content_kind(content_type: str, *, allow_media_types: bool) -> str:
    """Classify an Atom ``type`` attribute as text, html, xhtml or binary.

    Text constructs (title, summary, rights) admit only the ``text``/``html``/
    ``xhtml`` keywords, while atom:content additionally admits a MIME media
    type -- ``text/html`` is markup, any other ``text/*`` is plain text, inline
    XML is markup, and everything else is base64-encoded binary.
    See RFC 4287 sections 3.1 and 4.1.3.1.
    """
    content_type = content_type.strip().lower()
    if content_type in ("", "text"):
        return "text"
    if content_type in ("html", "xhtml"):
        return content_type
    if not allow_media_types:
        # An out-of-spec type on a text construct; the safe reading is text.
        return "text"

    media_type = content_type.split(";", 1)[0].strip()
    if media_type == "text/html":
        return "html"
    if media_type.endswith(("+xml", "/xml")):
        # Inline XML, carried as child elements just like xhtml content.
        return "xhtml"
    if media_type.startswith("text/"):
        return "text"
    return "binary"


class RssConverter(DocumentConverter):
    """Convert RSS / Atom type to markdown"""

    def __init__(self) -> None:
        super().__init__()
        self._kwargs: _FeedOptions = {}

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: _OPTION_VALUE,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

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

    def _check_xml(self, file_stream: BinaryIO) -> bool:
        cur_pos: Final = file_stream.tell()
        try:
            doc = minidom.parse(file_stream)
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
            and root.namespaceURI in (None, _ATOM_NAMESPACE)
            and self._get_children(root, "entry")
        ):
            return "atom"
        return None

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: _OPTION_VALUE,
    ) -> DocumentConverterResult:
        self._kwargs = cast("_FeedOptions", kwargs)
        doc = minidom.parse(file_stream)
        doc.documentURI = stream_info.url or self._kwargs.get("url")
        feed_type = self._feed_type(doc)

        if feed_type == "rss":
            return self._parse_rss_type(doc)
        elif feed_type == "atom":
            return self._parse_atom_type(doc)
        else:
            raise ValueError("Unknown feed type")

    def _parse_atom_type(self, doc: Document) -> DocumentConverterResult:
        root: Final = doc.documentElement
        assert root is not None
        title = self._get_flattened_text(root, "title", atom_text=True)
        subtitle = self._get_flattened_text(root, "subtitle", atom_text=True)
        entries = self._get_children(root, "entry")
        md_text = f"# {title}\n" if title else ""

        if subtitle:
            md_text += f"{subtitle}\n"
        for entry in entries:
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

    def _get_atom_content(
        self, entry: Element, tag_name: str
    ) -> tuple[str | None, bool]:
        """Return an Atom text construct or content, and whether it is markup.

        Values flagged as markup are converted by ``_parse_content``; plain text
        is returned verbatim for the caller to emit as-is.
        """
        node = self._get_child(entry, tag_name)
        if node is None:
            return None, True

        kind = _atom_content_kind(
            node.getAttribute("type"), allow_media_types=tag_name == "content"
        )
        if kind == "binary":
            # A base64-encoded payload; there is no text to render.
            return None, True

        text = self._read_content(node, kind=kind)
        if kind != "text":
            return text or None, True

        # Plain text carries no markup.  Drop the whitespace the feed used to
        # lay the element out -- indentation carried into the output would read
        # as a Markdown code block -- but leave the text itself alone.  The
        # first line is excluded from the dedent because it may start on the
        # element's own line, where it carries no indentation to share.
        lines = text.splitlines()
        if len(lines) > 1:
            text = lines[0] + "\n" + textwrap.dedent("\n".join(lines[1:]))
        return text.strip(), False

    def _get_flattened_text(
        self, element: Element, tag_name: str, *, atom_text: bool = False
    ) -> str | None:
        """Get a value that is rendered as a heading or a metadata line.

        Feeds are routinely pretty-printed, so a value written as
        ``<title>\\n  Example feed\\n</title>`` carries the indentation of the
        element it sits in. Emitted verbatim it ends the Markdown heading
        before the text begins, leaving a bare ``#`` and the title as body
        text, so the layout whitespace is dropped here. A value that is
        nothing but whitespace is reported as absent.
        """
        if atom_text:
            value, is_markup = self._get_atom_content(element, tag_name)
            if value and is_markup:
                soup = BeautifulSoup(value, "html.parser")
                for block in soup.find_all(_TEXT_BREAK_ELEMENTS):
                    block.insert_before("\n")
                    block.append("\n")
                value = soup.get_text()
        else:
            value = self._get_data_by_tag_name(element, tag_name)
        if value is None:
            return None
        # Block boundaries become line breaks, and adjacent blocks leave blank
        # lines between them; drop the empty parts so the flattened value is
        # separated by single spaces rather than by runs of them.
        parts = (part.strip() for part in value.splitlines())
        return " ".join(part for part in parts if part) or None

    def _parse_rss_type(self, doc: Document) -> DocumentConverterResult:
        root: Final = doc.documentElement
        assert root is not None
        channel = self._get_child(root, "channel")
        if channel is None:
            raise ValueError("No channel found in RSS feed")
        channel_title = self._get_flattened_text(channel, "title")
        # A channel description is a text field; item descriptions carry HTML.
        # Preserve its existing whitespace while collecting the complete value.
        channel_description = self._get_data_by_tag_name(channel, "description")
        items = self._get_children(channel, "item")
        md_text = ""
        if channel_title:
            md_text += f"# {channel_title}\n"
        if channel_description:
            md_text += f"{channel_description}\n"
        for item in items:
            title = self._get_flattened_text(item, "title")
            description = self._get_data_by_tag_name(item, "description", kind="html")
            pubDate = self._get_flattened_text(item, "pubDate")
            content = self._get_data_by_tag_name(item, "content:encoded", kind="html")

            if title:
                md_text += f"\n## {title}\n"
            if pubDate:
                md_text += f"Published on: {pubDate}\n"
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

    def _parse_content(self, content: str, *, base_url: str = "") -> str:
        if sys.version_info < (3, 11):
            return convert_feed(content, base_url, self._kwargs)
        fragment: Final = turbohtml.parse_fragment(content)
        self._resolve_content_links(fragment, base_url)
        return _CustomMarkdown(**cast("_MarkdownOptions", self._kwargs)).convert(
            fragment
        )

    def _get_field_base_url(self, element: Element, tag_name: str) -> str:
        """Apply xml:base from the document root through the selected field.

        Relative overrides resolve against their parent's base. An empty
        xml:base inherits that base; it does not reset it to the document URL.
        The document URI is local to this conversion, even when a converter is
        reused. The source stream's URL also supplies a base for RSS HTML.
        """
        bases: list[str] = []
        node: Node | None = self._get_child(element, tag_name)
        while node is not None:
            if isinstance(node, Element) and node.hasAttributeNS(
                _XML_NAMESPACE, "base"
            ):
                bases.append(node.getAttributeNS(_XML_NAMESPACE, "base"))
            node = node.parentNode
        document = element.ownerDocument
        base_url = (document.documentURI or "") if document is not None else ""
        for reference in reversed(bases):
            base_url = _resolve_url(base_url, reference)
        return base_url

    def _resolve_content_links(
        self, fragment: turbohtml.Element, base_url: str
    ) -> None:
        """Resolve rendered links/images, retaining nested XML Base scopes.

        Inline XHTML keeps its xml:base attributes during serialization; HTML
        carried in text/CDATA inherits the enclosing field's base.
        """
        stack: list[tuple[turbohtml.Element, str]] = [(fragment, base_url)]
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

    def _get_children(self, element: Element, tag_name: str) -> list[Element]:
        """Select fields on their owner, without borrowing descendant metadata."""
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

    def _get_child(self, element: Element, tag_name: str) -> Element | None:
        return next(iter(self._get_children(element, tag_name)), None)

    def _get_data_by_tag_name(
        self, element: Element, tag_name: str, *, kind: str = "text"
    ) -> str | None:
        """Read the complete value of the first matching direct child field."""
        node = self._get_child(element, tag_name)
        if node is None:
            return None
        return self._read_content(node, kind=kind) or None

    def _read_content(self, element: Element, *, kind: str) -> str:
        """Collect plain text, encoded HTML, or inline XML in document order.

        Encoded HTML's direct text/CDATA children are parts of one HTML string.
        Text inside actual XML elements is already literal and must be escaped
        when serializing those elements for the HTML parser. In XHTML, all text
        is literal, including CDATA. Comments and processing instructions carry
        no display content.

        Use an explicit stack: minidom's recursive cloning/serialization can
        fail on deep XML before the Markdown renderer's fallback is reached.
        """
        parts: list[str] = []
        stack: list[Node | str] = list(reversed(element.childNodes))
        while stack:
            child = stack.pop()
            if isinstance(child, str):
                parts.append(child)
            elif child.nodeType in (Node.TEXT_NODE, Node.CDATA_SECTION_NODE):
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


__all__ = ["RssConverter"]
