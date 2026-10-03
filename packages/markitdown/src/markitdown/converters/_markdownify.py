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


def _span(cell: Any, attribute: str, zero: int = 1) -> int:
    """A cell's rowspan or colspan, clamped the way markdownify clamps colspan.

    `zero` is what a span of `0` stands for. `rowspan="0"` reaches to the last
    row of the cell's row group, so its caller passes that many rows;
    `colspan="0"` is no longer part of HTML and a browser reads it as one column.
    """
    value = cell.attrs.get(attribute)
    if isinstance(value, str) and value.isdigit():
        number = int(value)
        if number == 0:
            return zero
        return max(1, min(1000, number))
    return 1


# A span attribute must not be able to make the output, or the conversion, much
# larger than the page: a table gets its placeholders only while they stay within
# a few per real cell, and is otherwise converted as markdownify converts it.
_PLACEHOLDERS_PER_CELL = 8
_MIN_PLACEHOLDERS = 64


def _fill_row_spans(soup: Any) -> None:
    """Give every row the cells a rowspan from an earlier row takes up.

    A Markdown table has no way to merge cells down, so a `rowspan` cell is
    written once and the rows it reaches into come out one cell short. Every
    value in those rows then reads under the wrong column: a table whose first
    column is a region spanning several product rows puts the product under
    `Region` and the count under `Product`.

    Adding the empty cells the span stands for keeps the columns lined up.

    A span is laid out inside its own row group, because a rowspan never reaches
    past the group it starts in, and `rowspan="0"` reaches exactly that far. A
    `thead`, `tbody` or `tfoot` is such a group, and so is a `table` for the rows
    written directly under it.
    """
    for group in soup.find_all(["table", "thead", "tbody", "tfoot"]):
        rows = group.find_all("tr", recursive=False)
        cells = [row.find_all(["td", "th"], recursive=False) for row in rows]
        layout = _row_span_layout(cells)
        if layout is None:
            continue
        placed, covered = layout
        for row, row_placed, row_covered in zip(rows, placed, covered):
            if row_covered:
                _pad_row(soup, row, row_placed, sorted(row_covered))


def _row_span_layout(
    cells: list[list[Any]],
) -> tuple[list[list[tuple[int, Any]]], list[set[int]]] | None:
    """Where each row's own cells sit, and which columns earlier rowspans take.

    Returns None once the placeholders would pass the row group's budget.
    """
    budget = _MIN_PLACEHOLDERS + _PLACEHOLDERS_PER_CELL * sum(map(len, cells))
    covered: list[set[int]] = [set() for _ in cells]
    placed: list[list[tuple[int, Any]]] = []
    needed = 0
    for index, row_cells in enumerate(cells):
        # The rows a span can still reach, which is also what `rowspan="0"` means.
        rows_left = len(cells) - index
        column = 0
        row_placed = []
        for cell in row_cells:
            while column in covered[index]:
                column += 1
            row_placed.append((column, cell))
            columns = _span(cell, "colspan")
            rows_below = min(_span(cell, "rowspan", zero=rows_left), rows_left) - 1
            needed += columns * rows_below
            if needed > budget:
                return None
            for below in range(index + 1, index + 1 + rows_below):
                covered[below].update(range(column, column + columns))
            column += columns
        placed.append(row_placed)
    return placed, covered


def _pad_row(
    soup: Any, row: Any, placed: list[tuple[int, Any]], columns: list[int]
) -> None:
    """Put an empty cell in front of the first own cell after each column.

    The row is rebuilt in one pass. Its children are taken out front to back,
    so every `extract()` finds its node at index 0, and put back in order; a
    placeholder inserted with `insert_before` would scan its siblings instead.
    """
    column_of = {id(cell): at for at, cell in placed}
    children = list(row.contents)
    for child in children:
        child.extract()
    pending = iter(columns)
    column = next(pending, None)
    for child in children:
        at = column_of.get(id(child))
        while at is not None and column is not None and column < at:
            row.append(soup.new_tag("td"))
            column = next(pending, None)
        row.append(child)
    while column is not None:
        row.append(soup.new_tag("td"))
        column = next(pending, None)


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

    def convert_soup(self, soup: Any) -> str:
        _fill_row_spans(soup)
        return super().convert_soup(soup)  # type: ignore
