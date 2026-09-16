"""Internal bridge from the DOCX image hook to document HTML."""

import mimetypes
from typing import Any, Callable, Optional
from uuid import uuid4

from bs4 import BeautifulSoup, Tag
from bs4.builder import HTMLTreeBuilder
from mammoth import html, images
from mammoth.docx.files import InvalidFileReferenceError

from ..._stream_info import StreamInfo
from .._image import _parse_image_html


_BLOCK_ELEMENTS = HTMLTreeBuilder.DEFAULT_BLOCK_ELEMENTS | {
    "details",
    "dialog",
    "hgroup",
    "menu",
    "search",
    "summary",
}
_PHRASING_CONTAINERS = set(
    "a abbr b bdi bdo cite code data del dfn em i ins kbd label mark q s samp "
    "small span strong sub sup time u var p h1 h2 h3 h4 h5 h6 pre".split()
)


def _lift_out_of_parent(node: Tag, soup: BeautifulSoup) -> None:
    """Split a paragraph/inline wrapper around generated block content."""
    parent = node.parent
    assert isinstance(parent, Tag)
    before = soup.new_tag(parent.name)
    before.attrs.update(parent.attrs)
    for sibling in list(parent.contents):
        if sibling is node:
            break
        before.append(sibling.extract())
    if before.contents:
        parent.insert_before(before)
        parent.attrs.pop("id", None)
    parent.insert_before(node.extract())
    if not parent.contents:
        if parent.has_attr("id") and not node.has_attr("id"):
            node["id"] = parent["id"]
        parent.decompose()


class _DocxImages:
    def __init__(
        self,
        render: Callable[..., Optional[str]],
        options: dict[str, Any],
    ):
        self._render = render
        self._options = options
        self._attribute = "data-markitdown-image-" + uuid4().hex
        self._fragments: dict[str, BeautifulSoup] = {}

    def convert_image(self, image: Any) -> list[Any]:
        stream_info = StreamInfo(
            mimetype=image.content_type,
            extension=(
                mimetypes.guess_extension(image.content_type)
                if image.content_type
                else None
            ),
        )
        with image.open() as image_stream:
            try:
                fragment = self._render(image_stream, stream_info, **self._options)
            except InvalidFileReferenceError as exc:
                # Mammoth swallows this exception for missing document images,
                # but an error raised by the override must reach the dispatcher.
                raise RuntimeError("_image_to_html failed") from exc
        soup = _parse_image_html(fragment)
        if soup is None:
            return images.data_uri(image)

        key = str(len(self._fragments))
        self._fragments[key] = soup
        return [html.element("img", {self._attribute: key})]

    def replace_images(self, html_content: str) -> str:
        if not self._fragments:
            return html_content

        soup = BeautifulSoup(html_content, "html.parser")
        for image in soup.find_all("img", attrs={self._attribute: True}):
            key = image[self._attribute]
            assert isinstance(key, str)
            fragment = self._fragments[key]
            blocks = fragment.find_all(_BLOCK_ELEMENTS)
            links = fragment.find_all("a")
            image.replace_with(*list(fragment.contents))

            # Only generated content is lifted, never its table cell or list item.
            for block in blocks:
                while (
                    isinstance(block.parent, Tag)
                    and block.parent.name in _PHRASING_CONTAINERS
                ):
                    _lift_out_of_parent(block, soup)
            for link in links:
                outer_link = link.find_parent("a")
                if outer_link is not None:
                    while link.parent is not outer_link:
                        _lift_out_of_parent(link, soup)
                    _lift_out_of_parent(link, soup)
        return str(soup)
