import re
import warnings
from typing import Any, BinaryIO

import bs4
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._markdownify import _CustomMarkdownify

# URL patterns for Confluence Cloud and Server
_CONFLUENCE_CLOUD_RE = re.compile(
    r"^https?://[^/]+\.atlassian\.net/wiki/", re.IGNORECASE
)
_CONFLUENCE_SERVER_RE = re.compile(
    r"^https?://[^/]+/wiki/spaces/", re.IGNORECASE
)

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/html",
    "application/xhtml",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".html",
    ".htm",
]

# Noise elements to remove from the rendered Confluence page
_CONFLUENCE_NOISE_SELECTORS = [
    "#navigation",
    "#breadcrumbs",
    "#header",
    "#footer",
    ".confluence-navigation",
    ".page-metadata",
    ".page-metadata-modification-info",
    ".page-metadata-secondary",
    "#likes-and-labels-container",
    "#children-section",
    "#comments-section",
    ".wiki-content .plugin_pagetree",
    ".confluence-information-macro-icon",
    "#sidebar",
    ".ia-fixed-sidebar",
    ".ia-splitter-left",
]

# Confluence macro names that are purely navigational (no content value)
_MACRO_SKIP = {
    "toc", "recently-updated", "children", "pagetree", "space-index", "anchor",
}

# Macro names that are informational panels → blockquote with a label
_MACRO_PANEL = {
    "info": "Info",
    "note": "Note",
    "warning": "Warning",
    "tip": "Tip",
    "panel": None,
    "excerpt-include": None,
}


class ConfluenceConverter(DocumentConverter):
    """Convert live Confluence Cloud / Server pages to Markdown.

    Triggered when the URL matches a known Confluence pattern.  The converter
    strips navigation chrome and focuses on the main content area, similar to
    how WikipediaConverter handles Wikipedia pages.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        url = stream_info.url or ""
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if not (
            _CONFLUENCE_CLOUD_RE.search(url) or _CONFLUENCE_SERVER_RE.search(url)
        ):
            return False

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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        soup = BeautifulSoup(file_stream, "html.parser", from_encoding=encoding)

        # Remove scripts, styles, and Confluence UI chrome
        for tag in soup(["script", "style"]):
            tag.extract()
        for selector in _CONFLUENCE_NOISE_SELECTORS:
            for el in soup.select(selector):
                el.extract()

        # Try to find the main content container
        content = (
            soup.find("div", {"id": "main-content"})  # Confluence Cloud
            or soup.find("div", {"id": "content"})  # Confluence Server
            or soup.find("div", {"class": "wiki-content"})  # fallback
            or soup.find("body")
            or soup
        )

        # Extract title
        title: str | None = None
        title_el = soup.find("h1", {"id": "title-text"}) or soup.find(
            "title"
        )
        if title_el and isinstance(title_el, bs4.Tag):
            title = title_el.get_text(strip=True)

        assert isinstance(content, bs4.PageElement)
        markdown = _CustomMarkdownify(**kwargs).convert_soup(content).strip()

        return DocumentConverterResult(markdown=markdown, title=title)


class ConfluenceStorageConverter(DocumentConverter):
    """Convert Confluence Storage Format XML files to Markdown.

    Confluence exports pages in an XHTML-based storage format that uses
    ``ac:`` and ``ri:`` namespaced tags for macros and resource identifiers.
    This converter pre-processes those tags into plain HTML before running
    the standard markdownify pass.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        extension = (stream_info.extension or "").lower()
        mimetype = (stream_info.mimetype or "").lower()

        is_xml = extension == ".xml" or any(
            mimetype.startswith(p)
            for p in ("text/xml", "application/xml", "application/xhtml+xml")
        )
        if not is_xml:
            return False

        # Peek into the stream to confirm Confluence namespaces are present
        cur_pos = file_stream.tell()
        try:
            sample = file_stream.read(2048)
            if isinstance(sample, bytes):
                sample = sample.decode("utf-8", errors="replace")
            return "<ac:" in sample or "<ri:" in sample
        finally:
            file_stream.seek(cur_pos)

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        raw = file_stream.read()
        if isinstance(raw, bytes):
            raw = raw.decode(encoding, errors="replace")

        # Strip the XML processing instruction so it doesn't bleed into output
        # when falling back to html.parser (lxml-xml handles it natively).
        raw = re.sub(r"<\?xml[^?]*\?>", "", raw, count=1).lstrip()

        # Use lxml-xml parser when available for proper namespace handling;
        # fall back to html.parser which is always present (suppress the
        # XMLParsedAsHTMLWarning that bs4 emits in that case).
        try:
            soup = BeautifulSoup(raw, "lxml-xml")
        except Exception:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
                soup = BeautifulSoup(raw, "html.parser")

        # Extract page title from the root <page> element if present
        title: str | None = None
        title_el = soup.find("title") or soup.find("page")
        if title_el and isinstance(title_el, bs4.Tag):
            t = title_el.get("title") or title_el.find("title")
            if isinstance(t, str):
                title = t
            elif isinstance(t, bs4.Tag):
                title = t.get_text(strip=True)

        self._transform_macros(soup)

        markdown = _CustomMarkdownify(**kwargs).convert_soup(soup).strip()
        return DocumentConverterResult(markdown=markdown, title=title)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _transform_macros(self, soup: BeautifulSoup) -> None:
        """Mutate *soup* in-place, translating Confluence-specific tags."""
        self._transform_structured_macros(soup)
        self._transform_links(soup)
        self._transform_images(soup)
        self._transform_emoticons(soup)
        self._transform_tasks(soup)

    def _transform_structured_macros(self, soup: BeautifulSoup) -> None:
        """Translate ``<ac:structured-macro>`` tags to plain HTML equivalents."""
        for macro in soup.find_all(
            re.compile(r"^ac:structured-macro$", re.IGNORECASE)
        ):
            if not isinstance(macro, bs4.Tag):
                continue
            name = (macro.get("ac:name") or "").lower()

            if name in _MACRO_SKIP:
                macro.decompose()
                continue

            if name == "code":
                self._transform_code_macro(macro)
            elif name == "excerpt":
                # Unwrap — keep the body content
                body = macro.find(re.compile(r"^ac:rich-text-body$", re.IGNORECASE))
                if body and isinstance(body, bs4.Tag):
                    macro.replace_with(body)
                else:
                    macro.decompose()
            elif name in _MACRO_PANEL:
                self._transform_panel_macro(macro, name)
            elif name == "status":
                self._transform_status_macro(macro)
            elif name == "jira":
                self._transform_jira_macro(macro)
            else:
                # Unknown macro: keep the rich-text-body content if present,
                # otherwise discard the entire macro tag.
                body = macro.find(re.compile(r"^ac:rich-text-body$", re.IGNORECASE))
                if body and isinstance(body, bs4.Tag):
                    macro.replace_with(body)
                else:
                    macro.decompose()

    def _transform_code_macro(self, macro: bs4.Tag) -> None:
        """Replace a ``code`` macro with a fenced ``<pre><code>`` block."""
        language = ""
        for param in macro.find_all(
            re.compile(r"^ac:parameter$", re.IGNORECASE)
        ):
            if isinstance(param, bs4.Tag) and (
                param.get("ac:name") or ""
            ).lower() == "language":
                language = param.get_text(strip=True)
                break

        body = macro.find(
            re.compile(r"^ac:plain-text-body$", re.IGNORECASE)
        ) or macro.find(re.compile(r"^ac:rich-text-body$", re.IGNORECASE))

        code_text = body.get_text() if body and isinstance(body, bs4.Tag) else ""

        lang_attr = f' class="language-{language}"' if language else ""
        replacement = BeautifulSoup(
            f"<pre><code{lang_attr}>{code_text}</code></pre>", "html.parser"
        )
        macro.replace_with(replacement)

    def _transform_panel_macro(self, macro: bs4.Tag, name: str) -> None:
        """Replace info/note/warning/tip/panel macros with a blockquote."""
        label = _MACRO_PANEL.get(name)

        body = macro.find(re.compile(r"^ac:rich-text-body$", re.IGNORECASE))
        if not body or not isinstance(body, bs4.Tag):
            macro.decompose()
            return

        # Build a simple <blockquote> wrapper
        inner_html = str(body.decode_contents())
        if label:
            prefix = f"<p><strong>{label}:</strong></p>"
        else:
            prefix = ""
        replacement = BeautifulSoup(
            f"<blockquote>{prefix}{inner_html}</blockquote>", "html.parser"
        )
        macro.replace_with(replacement)

    def _transform_status_macro(self, macro: bs4.Tag) -> None:
        """Replace a ``status`` macro with a bold badge, e.g. **[DONE]**."""
        title = ""
        for param in macro.find_all(re.compile(r"^ac:parameter$", re.IGNORECASE)):
            if isinstance(param, bs4.Tag) and (
                param.get("ac:name") or ""
            ).lower() == "title":
                title = param.get_text(strip=True)
                break
        if title:
            replacement = BeautifulSoup(
                f"<strong>[{title}]</strong>", "html.parser"
            )
            macro.replace_with(replacement)
        else:
            macro.decompose()

    def _transform_jira_macro(self, macro: bs4.Tag) -> None:
        """Replace a ``jira`` macro with the issue key as plain text."""
        key = ""
        for param in macro.find_all(re.compile(r"^ac:parameter$", re.IGNORECASE)):
            if isinstance(param, bs4.Tag) and (
                param.get("ac:name") or ""
            ).lower() == "key":
                key = param.get_text(strip=True)
                break
        if key:
            macro.replace_with(key)
        else:
            macro.decompose()

    def _transform_links(self, soup: BeautifulSoup) -> None:
        """Translate ``<ac:link>`` tags to plain text or anchor tags."""
        for link in soup.find_all(re.compile(r"^ac:link$", re.IGNORECASE)):
            if not isinstance(link, bs4.Tag):
                continue

            # Try to get a human-readable label from the link body
            link_body = link.find(re.compile(r"^ac:link-body$", re.IGNORECASE))
            if link_body and isinstance(link_body, bs4.Tag):
                link.replace_with(link_body.get_text())
                continue

            # Try to get the page title from ri:page
            ri_page = link.find(re.compile(r"^ri:page$", re.IGNORECASE))
            if ri_page and isinstance(ri_page, bs4.Tag):
                page_title = ri_page.get("ri:content-title") or ri_page.get(
                    "ri:space-key", ""
                )
                link.replace_with(str(page_title))
                continue

            link.decompose()

    def _transform_images(self, soup: BeautifulSoup) -> None:
        """Translate ``<ac:image>`` tags to standard ``<img>`` tags."""
        for img in soup.find_all(re.compile(r"^ac:image$", re.IGNORECASE)):
            if not isinstance(img, bs4.Tag):
                continue

            # Prefer ri:url, then ri:attachment filename
            ri_url = img.find(re.compile(r"^ri:url$", re.IGNORECASE))
            ri_att = img.find(re.compile(r"^ri:attachment$", re.IGNORECASE))

            src = ""
            alt = ""
            if ri_url and isinstance(ri_url, bs4.Tag):
                src = ri_url.get("ri:value") or ""
                alt = src
            elif ri_att and isinstance(ri_att, bs4.Tag):
                src = ri_att.get("ri:filename") or ""
                alt = src

            replacement = BeautifulSoup(
                f'<img src="{src}" alt="{alt}" />', "html.parser"
            )
            img.replace_with(replacement)

    def _transform_emoticons(self, soup: BeautifulSoup) -> None:
        """Remove ``<ac:emoticon>`` tags (no Markdown equivalent)."""
        for el in soup.find_all(re.compile(r"^ac:emoticon$", re.IGNORECASE)):
            el.decompose()

    def _transform_tasks(self, soup: BeautifulSoup) -> None:
        """Translate Confluence task lists to GitHub-flavoured checkboxes."""
        for task_list in soup.find_all(
            re.compile(r"^ac:task-list$", re.IGNORECASE)
        ):
            if not isinstance(task_list, bs4.Tag):
                continue
            ul = BeautifulSoup("<ul></ul>", "html.parser").find("ul")
            assert ul is not None and isinstance(ul, bs4.Tag)
            for task in task_list.find_all(
                re.compile(r"^ac:task$", re.IGNORECASE)
            ):
                if not isinstance(task, bs4.Tag):
                    continue
                status_el = task.find(
                    re.compile(r"^ac:task-status$", re.IGNORECASE)
                )
                body_el = task.find(
                    re.compile(r"^ac:task-body$", re.IGNORECASE)
                )
                status = (
                    status_el.get_text(strip=True).lower()
                    if status_el and isinstance(status_el, bs4.Tag)
                    else "incomplete"
                )
                body_html = (
                    str(body_el.decode_contents())
                    if body_el and isinstance(body_el, bs4.Tag)
                    else ""
                )
                checked = "checked" if status == "complete" else ""
                li = BeautifulSoup(
                    f"<li><input type='checkbox' {checked}/> {body_html}</li>",
                    "html.parser",
                ).find("li")
                if li:
                    ul.append(li)
            task_list.replace_with(ul)
