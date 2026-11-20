"""Shared validation for Office image-rendering hooks."""

from typing import Optional

from bs4 import BeautifulSoup, Doctype


def _parse_image_html(fragment: Optional[str]) -> Optional[BeautifulSoup]:
    if fragment is not None and not isinstance(fragment, str):
        raise TypeError("_image_to_html must return an HTML string or None")
    if fragment is None or not fragment.strip():
        return None

    soup = BeautifulSoup(fragment, "html.parser")
    if soup.find(["html", "head", "body"]) or any(
        isinstance(node, Doctype) for node in soup.descendants
    ):
        raise ValueError("_image_to_html must return a fragment, not a document")
    return soup
