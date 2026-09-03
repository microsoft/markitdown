import textwrap
import warnings

from defusedxml import minidom
from xml.dom import Node
from xml.dom.minidom import Document, Element
from typing import BinaryIO, Any, Union
from bs4 import BeautifulSoup

from ._markdownify import _CustomMarkdownify
from .._stream_info import StreamInfo
from .._base_converter import DocumentConverter, DocumentConverterResult

PRECISE_MIME_TYPE_PREFIXES = [
    "application/rss",
    "application/rss+xml",
    "application/atom",
    "application/atom+xml",
]

PRECISE_FILE_EXTENSIONS = [".rss", ".atom"]

CANDIDATE_MIME_TYPE_PREFIXES = [
    "text/xml",
    "application/xml",
]

CANDIDATE_FILE_EXTENSIONS = [
    ".xml",
]

XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"


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

    def __init__(self):
        super().__init__()
        self._kwargs = {}

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        # Check for precise mimetypes and file extensions
        if extension in PRECISE_FILE_EXTENSIONS:
            return True

        for prefix in PRECISE_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        # Check for precise mimetypes and file extensions
        if extension in CANDIDATE_FILE_EXTENSIONS:
            return self._check_xml(file_stream)

        for prefix in CANDIDATE_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return self._check_xml(file_stream)

        return False

    def _check_xml(self, file_stream: BinaryIO) -> bool:
        cur_pos = file_stream.tell()
        try:
            doc = minidom.parse(file_stream)
            return self._feed_type(doc) is not None
        except BaseException as _:
            pass
        finally:
            file_stream.seek(cur_pos)
        return False

    def _feed_type(self, doc: Any) -> str | None:
        if doc.getElementsByTagName("rss"):
            return "rss"
        elif doc.getElementsByTagName("feed"):
            root = doc.getElementsByTagName("feed")[0]
            if root.getElementsByTagName("entry"):
                # An Atom feed must have a root element of <feed> and at least one <entry>
                return "atom"
        return None

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Pop our own keyword before forwarding the rest to markdownify.
        # strict=True raises RecursionError instead of falling back to plain text.
        strict: bool = kwargs.pop("strict", False)
        self._kwargs = kwargs
        doc = minidom.parse(file_stream)
        feed_type = self._feed_type(doc)

        if feed_type == "rss":
            return self._parse_rss_type(doc, strict=strict)
        elif feed_type == "atom":
            return self._parse_atom_type(doc, strict=strict)
        else:
            raise ValueError("Unknown feed type")

    def _parse_atom_type(
        self, doc: Document, *, strict: bool = False
    ) -> DocumentConverterResult:
        """Parse the type of an Atom feed.

        Returns None if the feed type is not recognized or something goes wrong.
        """
        root = doc.getElementsByTagName("feed")[0]
        title = self._get_data_by_tag_name(root, "title")
        subtitle = self._get_data_by_tag_name(root, "subtitle")
        entries = root.getElementsByTagName("entry")
        md_text = f"# {title}\n"
        if subtitle:
            md_text += f"{subtitle}\n"
        for entry in entries:
            entry_title = self._get_data_by_tag_name(entry, "title")
            entry_summary, summary_is_markup = self._get_atom_content(entry, "summary")
            entry_updated = self._get_data_by_tag_name(entry, "updated")
            entry_content, content_is_markup = self._get_atom_content(entry, "content")

            if entry_title:
                md_text += f"\n## {entry_title}\n"
            if entry_updated:
                md_text += f"Updated on: {entry_updated}\n"
            if entry_summary:
                md_text += self._render_atom_content(
                    entry_summary, is_markup=summary_is_markup, strict=strict
                )
            if entry_content:
                md_text += self._render_atom_content(
                    entry_content, is_markup=content_is_markup, strict=strict
                )

        return DocumentConverterResult(
            markdown=md_text,
            title=title,
        )

    def _get_atom_content(
        self, entry: Element, tag_name: str
    ) -> tuple[Union[str, None], bool]:
        """Return an Atom summary or content value, and whether it is markup.

        Values flagged as markup are converted by ``_parse_content``; plain text
        is returned verbatim for the caller to emit as-is.
        """
        nodes = entry.getElementsByTagName(tag_name)
        if not nodes:
            return None, True

        node = nodes[0]
        kind = _atom_content_kind(
            node.getAttribute("type"), allow_media_types=tag_name == "content"
        )
        if kind == "xhtml":
            return (
                "".join(
                    self._localize_xhtml_names(child.cloneNode(True)).toxml()
                    for child in node.childNodes
                    if child.nodeType == Node.ELEMENT_NODE
                ),
                True,
            )
        if kind == "binary":
            # A base64-encoded payload; there is no text to render.
            return None, True

        text = self._get_data_by_tag_name(entry, tag_name)
        if text is None or kind == "html":
            return text, True

        # Plain text carries no markup.  Drop the whitespace the feed used to
        # lay the element out -- indentation carried into the output would read
        # as a Markdown code block -- but leave the text itself alone.  The
        # first line is excluded from the dedent because it may start on the
        # element's own line, where it carries no indentation to share.
        lines = text.splitlines()
        if len(lines) > 1:
            text = lines[0] + "\n" + textwrap.dedent("\n".join(lines[1:]))
        return text.strip(), False

    def _render_atom_content(
        self, value: str, *, is_markup: bool, strict: bool = False
    ) -> str:
        """Render one Atom summary or content value as markdown."""
        if not is_markup:
            # Plain text is returned verbatim: routing it through the HTML
            # parser drops tag-shaped text such as ``<job_id>`` entirely.
            return value
        return self._parse_content(value, strict=strict)

    def _localize_xhtml_names(self, node: Node) -> Node:
        """Rewrite prefixed XHTML element names to their local HTML names.

        Atom permits XHTML content to be namespace-prefixed (e.g. ``x:strong``).
        The downstream HTML converter dispatches on HTML tag names, so the
        prefix has to be dropped or the element is treated as an unknown tag
        and its formatting is lost.
        """
        if node.nodeType == Node.ELEMENT_NODE:
            if node.prefix and node.namespaceURI == XHTML_NAMESPACE:
                node.tagName = node.nodeName = node.localName
                node.prefix = None
            for child in node.childNodes:
                self._localize_xhtml_names(child)
        return node

    def _parse_rss_type(
        self, doc: Document, *, strict: bool = False
    ) -> DocumentConverterResult:
        """Parse the type of an RSS feed.

        Returns None if the feed type is not recognized or something goes wrong.
        """
        root = doc.getElementsByTagName("rss")[0]
        channel_list = root.getElementsByTagName("channel")
        if not channel_list:
            raise ValueError("No channel found in RSS feed")
        channel = channel_list[0]
        channel_title = self._get_data_by_tag_name(channel, "title")
        channel_description = self._get_data_by_tag_name(channel, "description")
        items = channel.getElementsByTagName("item")
        md_text = ""
        if channel_title:
            md_text += f"# {channel_title}\n"
        if channel_description:
            md_text += f"{channel_description}\n"
        for item in items:
            title = self._get_data_by_tag_name(item, "title")
            description = self._get_data_by_tag_name(item, "description")
            pubDate = self._get_data_by_tag_name(item, "pubDate")
            content = self._get_data_by_tag_name(item, "content:encoded")

            if title:
                md_text += f"\n## {title}\n"
            if pubDate:
                md_text += f"Published on: {pubDate}\n"
            if description:
                md_text += self._parse_content(description, strict=strict)
            if content:
                md_text += self._parse_content(content, strict=strict)

        return DocumentConverterResult(
            markdown=md_text,
            title=channel_title,
        )

    def _parse_content(self, content: str, *, strict: bool = False) -> str:
        """Parse the content of an RSS feed item"""
        try:
            # using bs4 because many RSS feeds have HTML-styled content
            soup = BeautifulSoup(content, "html.parser")
            return _CustomMarkdownify(**self._kwargs).convert_soup(soup)
        except RecursionError:
            if strict:
                raise
            # Deeply nested item content can exceed Python's recursion limit
            # during markdownify's recursive DOM traversal.  Fall back to
            # BeautifulSoup's iterative get_text() so the caller still gets
            # usable plain-text content instead of raw HTML.
            warnings.warn(
                "RSS item content is too deeply nested for markdown conversion "
                "(RecursionError). Falling back to plain-text extraction.",
                stacklevel=2,
            )
            return BeautifulSoup(content, "html.parser").get_text("\n", strip=True)
        except BaseException as _:
            return content

    def _get_data_by_tag_name(
        self, element: Element, tag_name: str
    ) -> Union[str, None]:
        """Get data from first child element with the given tag name.
        Returns None when no such element is found.
        """
        nodes = element.getElementsByTagName(tag_name)
        if not nodes:
            return None
        fc = nodes[0].firstChild
        if fc:
            if hasattr(fc, "data"):
                return fc.data
        return None
