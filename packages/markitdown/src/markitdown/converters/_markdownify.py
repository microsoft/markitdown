import re
import markdownify

from bs4 import Comment
from typing import Any, Optional
from urllib.parse import quote, urlparse, urlunparse


_PERCENT_ENCODED_OCTET = re.compile(r"%[0-9A-Fa-f]{2}")


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


def _shows_content(nodes: Any) -> bool:
    """Whether any of these sibling nodes shows text or an image."""
    for node in nodes:
        if isinstance(node, Comment):
            continue
        if isinstance(node, str):
            if node.strip():
                return True
        elif node.name == "img" or node.get_text(strip=True) or node.find("img"):
            return True
    return False


class _CustomMarkdownify(markdownify.MarkdownConverter):
    """
    A custom version of markdownify's MarkdownConverter. Changes include:

    - Altering the default heading style to use '#', '##', etc.
    - Writing hard line breaks as backslashes, which survive whitespace normalization.
    - Removing javascript hyperlinks.
    - Truncating images with large data:uri sources.
    - Ensuring URIs are properly escaped, and do not conflict with Markdown syntax
    """

    def __init__(self, **options: Any):
        options["heading_style"] = options.get("heading_style", markdownify.ATX)
        options["keep_data_uris"] = options.get("keep_data_uris", False)
        # Explicitly cast options to the expected type if necessary
        super().__init__(**options)

    def convert_hn(
        self,
        n: int,
        el: Any,
        text: str,
        convert_as_inline: Optional[bool] = False,
        **kwargs,
    ) -> str:
        """Same as usual, but be sure to start with a new line"""
        if not convert_as_inline:
            if not re.search(r"^\n", text):
                return "\n" + super().convert_hn(n, el, text, convert_as_inline)  # type: ignore

        return super().convert_hn(n, el, text, convert_as_inline)  # type: ignore

    def convert_a(
        self,
        el: Any,
        text: str,
        convert_as_inline: Optional[bool] = False,
        **kwargs,
    ):
        """Same as usual converter, but removes JavaScript links and escapes URIs."""
        prefix, suffix, text = markdownify.chomp(text)  # type: ignore
        if not text:
            return ""

        if el.find_parent("pre") is not None:
            return text

        href = el.get("href")
        title = el.get("title")

        # Escape URIs and skip non-http or file schemes
        if href:
            try:
                parsed_url = urlparse(href)  # type: ignore
                if parsed_url.scheme and parsed_url.scheme.lower() not in ["http", "https", "file"]:  # type: ignore
                    return "%s%s%s" % (prefix, text, suffix)
                href = urlunparse(
                    parsed_url._replace(
                        path=_quote_path_preserving_percent_encoded_octets(
                            parsed_url.path
                        )
                    )
                )  # type: ignore
            except ValueError:  # It's not clear if this ever gets thrown
                return "%s%s%s" % (prefix, text, suffix)

        # For the replacement see #29: text nodes underscores are escaped
        if (
            self.options["autolinks"]
            and text.replace(r"\_", "_") == href
            and not title
            and not self.options["default_title"]
        ):
            # Shortcut syntax
            return "<%s>" % href
        if self.options["default_title"] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        return (
            "%s[%s](%s%s)%s" % (prefix, text, href, title_part, suffix)
            if href
            else text
        )

    def convert_img(
        self,
        el: Any,
        text: str,
        convert_as_inline: Optional[bool] = False,
        **kwargs,
    ) -> str:
        """Same as usual converter, but removes data URIs"""

        alt = el.attrs.get("alt", None) or ""
        src = el.attrs.get("src", None) or ""
        data_src = el.attrs.get("data-src", None) or ""
        # Lazy-loading libraries commonly leave a tiny placeholder data URI in
        # src and put the real image in data-src. Prefer data-src when src
        # isn't a usable URL, so the placeholder doesn't win over actual
        # content. When keep_data_uris is set the caller explicitly wants the
        # embedded bytes, so a data URI in src is left alone.
        if data_src and (
            not src
            or (src[:5].lower() == "data:" and not self.options["keep_data_uris"])
        ):
            src = data_src
        title = el.attrs.get("title", None) or ""
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        # Remove all line breaks from alt
        alt = alt.replace("\n", " ")
        if (
            convert_as_inline
            and el.parent.name not in self.options["keep_inline_images_in"]
        ):
            return alt

        # Remove dataURIs
        if src[:5].lower() == "data:" and not self.options["keep_data_uris"]:
            src = src.split(",")[0] + "..."

        return "![%s](%s%s)" % (alt, src, title_part)

    def convert_br(
        self,
        el: Any,
        text: str,
        parent_tags: Any = None,
        **kwargs,
    ) -> str:
        """Write a hard line break as a backslash rather than two trailing spaces.

        MarkItDown strips trailing whitespace from every output line, which removes
        markdownify's two-space hard breaks. A break with text or an image on both sides
        of it in its parent element is written as a backslash, which survives. Other
        breaks, and those in table cells, headings, and preformatted text, keep
        markdownify's handling.
        """
        if (
            isinstance(parent_tags, (set, frozenset))
            and not parent_tags & {"_inline", "_noformat"}
            and _shows_content(el.previous_siblings)
            and _shows_content(el.next_siblings)
        ):
            return "\\\n" + text
        return super().convert_br(el, text, parent_tags, **kwargs)  # type: ignore

    def convert_input(
        self,
        el: Any,
        text: str,
        convert_as_inline: Optional[bool] = False,
        **kwargs,
    ) -> str:
        """Convert checkboxes to Markdown [x]/[ ] syntax."""

        if el.get("type") == "checkbox":
            return "[x] " if el.has_attr("checked") else "[ ] "
        return ""

    def convert_u(
        self,
        el: Any,
        text: str,
        convert_as_inline: Optional[bool] = False,
        **kwargs,
    ) -> str:
        if not text.strip():
            return text

        prefix, suffix, text = markdownify.chomp(text)  # type: ignore
        if not text:
            return ""
        return f"{prefix}<u>{text}</u>{suffix}"

    def convert_strike(self, el: Any, text: str, *args, **kwargs) -> str:
        """Obsolete <strike> is still in the wild; treat it like <s>/<del>."""
        return self.convert_s(el, text, *args, **kwargs)  # type: ignore

    def convert_soup(self, soup: Any) -> str:
        return super().convert_soup(soup)  # type: ignore
