import re
import markdownify

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


class _CustomMarkdownify(markdownify.MarkdownConverter):
    """
    A custom version of markdownify's MarkdownConverter. Changes include:

    - Altering the default heading style to use '#', '##', etc.
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

    def convert_colgroup(self, el, text, *args, **kwargs):
        """<colgroup> carries presentational metadata only; skip its text."""
        return ""

    def convert_caption(self, el, text, parent_tags, *args, **kwargs):
        """Emit the caption as a paragraph above the table, not inline
        between header rows where it breaks the header-delimiter line."""
        return text.strip() + "\n\n"

    def convert_tfoot(self, el, text, parent_tags, *args, **kwargs):
        """Render <tfoot> rows as plain body rows (no extra header)."""
        return text

    def convert_thead(self, el, text, parent_tags, *args, **kwargs):
        return text

    def convert_tbody(self, el, text, parent_tags, *args, **kwargs):
        return text

    def convert_table(self, el, text, parent_tags, *args, **kwargs):
        """Reassemble a table so the header delimiter row sits under the
        first header row, regardless of intervening <caption>/<colgroup>.

        markdownify's default convert_tr keys off el.find_previous_sibling()
        to detect "first row", which miscounts when a <caption> or
        <colgroup> precedes the header <tr> (causing the delimiter line to
        vanish). It also treats <tfoot> as a new header section, emitting
        a spurious empty-header overline + delimiter for it. We fix
        this by post-processing the rendered text: extract caption text,
        locate the real delimiter row, and strip any spurious empty-header
        rows / duplicate delimiters introduced by tfoot."""
        import re as _re

        rows = [r for r in text.split("\n") if r.strip().startswith("|")]
        if not rows:
            return "\n\n" + text.strip() + "\n\n"

        ncols = max(r.count("|") - 1 for r in rows)
        if ncols < 1:
            ncols = 1

        # Pattern for a delimiter row (|---|---|).
        delim_re = _re.compile(r"^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
        # Pattern for an empty header overline markdownify inserts when it
        # thinks a new "section" starts (|  |  |).
        empty_row_re = _re.compile(r"^\|(\s*\|)+\s*$")

        # Find the real delimiter: the first delimiter row that comes after
        # the first non-empty row (the header). Drop any other delimiters
        # and any empty-row overlines that precede them (the tfoot bug).
        cleaned: list[str] = []
        real_delim_added = False
        i = 0
        while i < len(rows):
            r = rows[i]
            is_delim = bool(delim_re.match(r.strip()))
            is_empty = bool(empty_row_re.match(r.strip()))
            if is_delim and not real_delim_added and i >= 1:
                cleaned.append(r)
                real_delim_added = True
            elif is_delim:
                # duplicate delimiter (from tfoot) - drop
                pass
            elif is_empty and not real_delim_added:
                cleaned.append(r)
            elif is_empty and real_delim_added:
                # spurious empty-header overline from a <tfoot> (or any
                # section after the real header) - drop it. The next row
                # is the real content row.
                pass
            else:
                cleaned.append(r)
            i += 1

        # If no real delimiter was present, insert one after the first row.
        if not real_delim_added and len(cleaned) >= 1:
            separator = "| " + " | ".join(["---"] * ncols) + " |"
            cleaned = [cleaned[0], separator] + cleaned[1:]

        # Pull the caption text out: it appears before the first |row|.
        prefix_parts = []
        for segment in text.split("\n"):
            if segment.strip().startswith("|"):
                break
            if segment.strip():
                prefix_parts.append(segment.strip())
        prefix = ""
        if prefix_parts:
            prefix = " ".join(prefix_parts) + "\n\n"

        return "\n\n" + prefix + "\n".join(cleaned).strip() + "\n\n"

    def convert_soup(self, soup: Any) -> str:
        return super().convert_soup(soup)  # type: ignore
