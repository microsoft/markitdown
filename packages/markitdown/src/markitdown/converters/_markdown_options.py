from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from bs4 import Tag

_OPTION_VALUE = TypeVar("_OPTION_VALUE")


class _MarkdownOptions(TypedDict, total=False):
    code_language: str
    code_language_callback: Callable[[Tag], str | None]
    strip_pre: str | None
    keep_data_uris: bool
    autolinks: bool
    default_title: bool
    strong_em_symbol: str
    sub_symbol: str
    sup_symbol: str
    strip: Sequence[str] | None
    convert: Sequence[str] | None
    heading_style: str
    bullets: str
    table_infer_header: bool
    escape_misc: bool
    escape_asterisks: bool
    escape_underscores: bool
    wrap_width: int
    wrap: bool
    newline_style: str
    strip_document: Literal["strip", "lstrip", "rstrip"] | None
    strict: bool


__all__ = ["_OPTION_VALUE", "_MarkdownOptions"]
