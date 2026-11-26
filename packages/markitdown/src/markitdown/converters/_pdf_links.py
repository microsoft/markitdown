import re
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from io import BytesIO, StringIO
from typing import Any
from urllib.parse import quote, urlsplit

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTContainer, LTItem, LTText, LTTextBox
from pdfminer.pdftypes import dict_value, list_value, str_value
from pdfminer.psparser import LIT
from pdfminer.utils import Matrix, Rect, apply_matrix_rect, decode_text, get_bound
from pdfplumber.page import Page
from pdfplumber.utils.text import LIGATURES


def _destination(raw_uri: bytes) -> str | None:
    try:
        uri = raw_uri.decode("utf-8-sig")
    except UnicodeDecodeError:
        uri = decode_text(raw_uri)
    try:
        parsed = urlsplit(uri)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return None
    except ValueError:
        return None
    # Preserve URL delimiters and existing escapes, including in the query.
    url = quote(uri, safe=":/?#[]@!$&'()*+,;=%")
    return url.replace("(", r"\(").replace(")", r"\)")


@dataclass
class PageLinks:
    rectangles: list[tuple[Rect, str]]
    x_offset: float

    @classmethod
    def from_page(cls, page: Page) -> "PageLinks | None":
        pdf_page = page.page_obj
        if not pdf_page.annots:
            return None

        # PDF annotations use unrotated user space. Match pdfminer's page
        # transform so their rectangles line up with the extracted glyphs.
        x0, y0, x1, y1 = pdf_page.mediabox
        matrix: Matrix = {
            90: (0, -1, 1, 0, -y0, x1),
            180: (-1, 0, 0, -1, x1, y1),
            270: (0, 1, -1, 0, y1, -x0),
        }.get(pdf_page.rotate, (1, 0, 0, 1, -x0, -y0))
        rectangles = []
        for ref in list_value(pdf_page.annots):
            annotation = dict_value(ref)
            if annotation.get("Subtype") is not LIT("Link"):
                continue
            action = dict_value(annotation.get("A"))
            if action.get("S") is not LIT("URI"):
                continue
            rect = list_value(annotation.get("Rect"))
            if len(rect) != 4 or not all(isinstance(n, (int, float)) for n in rect):
                continue
            destination = _destination(str_value(action.get("URI")))
            if not destination:
                continue

            # Wrapped links can have one clickable region per line. Their
            # enclosing Rect can also cover words outside the hyperlink.
            points = list_value(annotation.get("QuadPoints"))
            if (
                points
                and len(points) % 8 == 0
                and all(isinstance(n, (int, float)) for n in points)
            ):
                for i in range(0, len(points), 8):
                    region = get_bound(
                        zip(points[i : i + 8 : 2], points[i + 1 : i + 8 : 2])
                    )
                    rectangles.append((apply_matrix_rect(matrix, region), destination))
            else:
                rectangles.append((apply_matrix_rect(matrix, tuple(rect)), destination))
        return cls(rectangles, page.mediabox[0]) if rectangles else None

    def at(self, x: float, y: float) -> str | None:
        for (left, bottom, right, top), destination in self.rectangles:
            if left <= x <= right and bottom <= y <= top:
                return destination
        return None

    def for_char(self, char: dict[str, Any]) -> str | None:
        # pdfplumber adds the MediaBox's horizontal offset to its LTChar data.
        return self.at(
            (char["x0"] + char["x1"]) / 2 - self.x_offset,
            (char["y0"] + char["y1"]) / 2,
        )

    def render_words(self, words: list[dict[str, Any]]) -> str:
        def parts() -> Iterator[tuple[str, str | None]]:
            for i, word in enumerate(words):
                if i:
                    yield " ", None
                for char in word["chars"]:
                    text = char["text"]
                    yield LIGATURES.get(text, text), self.for_char(char)

        return render_linked_text(parts())


def render_linked_text(parts: Iterable[tuple[str, str | None]]) -> str:
    output: list[str] = []
    label: list[str] = []
    active = None

    def finish_link() -> None:
        text = "".join(label)
        stripped = text.rstrip()
        # Escape characters that could change the label in Markdown or a table.
        escaped = re.sub(r"([\\\[\]*_`~|<>&])", r"\\\1", stripped)
        output.extend((f"[{escaped}]({active})", text[len(stripped) :]))
        label.clear()

    for text, destination in parts:
        if text.isspace():
            # A layout-inferred space can fall between two linked words.
            if active and "\n" not in text and "\f" not in text:
                label.append(text)
                continue
            destination = None
        if active and destination != active:
            finish_link()
        active = destination
        if active:
            label.append(text)
        else:
            output.append(text)
    if active:
        finish_link()
    return "".join(output)


def _text_runs(
    item: LTItem, links: PageLinks | None
) -> Iterator[tuple[str, str | None]]:
    # Follow pdfminer's TextConverter order, including the extra newline after a box.
    if isinstance(item, LTContainer):
        for child in item:
            yield from _text_runs(child, links)
        if isinstance(item, LTTextBox):
            yield "\n", None
    elif isinstance(item, LTText):
        target = None
        if links is not None and isinstance(item, LTChar):
            target = links.at((item.x0 + item.x1) / 2, (item.y0 + item.y1) / 2)
        yield item.get_text(), target


def extract_text_with_links(
    pdf_bytes: BytesIO, links_by_page: dict[int, PageLinks]
) -> str:
    output = StringIO()
    for index, page in enumerate(extract_pages(pdf_bytes)):
        output.write(render_linked_text(_text_runs(page, links_by_page.get(index))))
        output.write("\f")
    return output.getvalue()
