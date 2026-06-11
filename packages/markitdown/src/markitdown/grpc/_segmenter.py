"""Best-effort segmentation of Markdown into structured document blocks.

This module backs the ConvertDocumentStream RPC. It performs a line-based
pass over converted Markdown and groups lines into typed blocks (headings,
paragraphs, tables, lists, code blocks, images, block quotes, and horizontal
rules). It is intentionally conservative: anything that does not match a
known block type is emitted as a paragraph, so no content is ever dropped.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterator, List, Optional, Union

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_FENCE_RE = re.compile(r"^(```+|~~~+)\s*(\S*)\s*$")
_TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
_TABLE_DELIMITER_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
_UNORDERED_ITEM_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
_ORDERED_ITEM_RE = re.compile(r"^(\s*)\d{1,9}[.)]\s+(.*)$")
_BLOCK_QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
_HORIZONTAL_RULE_RE = re.compile(r"^\s*((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})$")
_IMAGE_BLOCK_RE = re.compile(
    r"""^!\[(?P<alt>[^\]]*)\]\(\s*(?P<url><[^>]*>|[^\s)]+)(?:\s+"(?P<title>[^"]*)")?\s*\)$"""
)


@dataclass
class HeadingBlock:
    level: int
    text: str


@dataclass
class ParagraphBlock:
    text: str


@dataclass
class TableBlock:
    markdown: str
    rows: List[List[str]] = field(default_factory=list)


@dataclass
class ListBlock:
    markdown: str
    ordered: bool
    items: List[str] = field(default_factory=list)


@dataclass
class CodeBlock:
    language: str
    code: str


@dataclass
class ImageBlock:
    alt_text: str
    url: str
    title: Optional[str] = None


@dataclass
class BlockQuoteBlock:
    text: str


@dataclass
class HorizontalRuleBlock:
    pass


DocumentBlock = Union[
    HeadingBlock,
    ParagraphBlock,
    TableBlock,
    ListBlock,
    CodeBlock,
    ImageBlock,
    BlockQuoteBlock,
    HorizontalRuleBlock,
]


def segment_markdown(markdown: str) -> Iterator[DocumentBlock]:
    """Yield typed blocks for the given Markdown, in document order."""
    lines = markdown.split("\n")
    index = 0
    total = len(lines)

    while index < total:
        line = lines[index]

        if not line.strip():
            index += 1
            continue

        fence_match = _FENCE_RE.match(line)
        if fence_match:
            block, index = _consume_code_block(lines, index, fence_match)
            yield block
            continue

        heading_match = _HEADING_RE.match(line)
        if heading_match:
            yield HeadingBlock(
                level=len(heading_match.group(1)), text=heading_match.group(2)
            )
            index += 1
            continue

        if _HORIZONTAL_RULE_RE.match(line):
            yield HorizontalRuleBlock()
            index += 1
            continue

        if _TABLE_ROW_RE.match(line) and _is_table_start(lines, index):
            block, index = _consume_table(lines, index)
            yield block
            continue

        if _BLOCK_QUOTE_RE.match(line):
            block, index = _consume_block_quote(lines, index)
            yield block
            continue

        list_match = _UNORDERED_ITEM_RE.match(line) or _ORDERED_ITEM_RE.match(line)
        if list_match and not list_match.group(1):
            block, index = _consume_list(lines, index)
            yield block
            continue

        image_match = _IMAGE_BLOCK_RE.match(line.strip())
        if image_match and _is_block_end(lines, index + 1):
            url = image_match.group("url")
            if url.startswith("<") and url.endswith(">"):
                url = url[1:-1]
            yield ImageBlock(
                alt_text=image_match.group("alt"),
                url=url,
                title=image_match.group("title"),
            )
            index += 1
            continue

        block, index = _consume_paragraph(lines, index)
        yield block


def _is_block_end(lines: List[str], index: int) -> bool:
    return index >= len(lines) or not lines[index].strip()


def _is_table_start(lines: List[str], index: int) -> bool:
    return index + 1 < len(lines) and bool(_TABLE_DELIMITER_RE.match(lines[index + 1]))


def _consume_code_block(
    lines: List[str], index: int, fence_match: "re.Match[str]"
) -> tuple[CodeBlock, int]:
    fence = fence_match.group(1)
    language = fence_match.group(2)
    code_lines: List[str] = []
    index += 1
    while index < len(lines):
        if lines[index].strip().startswith(fence[0] * 3):
            index += 1
            break
        code_lines.append(lines[index])
        index += 1
    return CodeBlock(language=language, code="\n".join(code_lines)), index


def _split_table_row(line: str) -> List[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    # Split on pipes that are not escaped with a backslash.
    cells = re.split(r"(?<!\\)\|", stripped)
    return [cell.replace("\\|", "|").strip() for cell in cells]


def _consume_table(lines: List[str], index: int) -> tuple[TableBlock, int]:
    start = index
    rows: List[List[str]] = [_split_table_row(lines[index])]
    index += 2  # Skip past the header and delimiter rows.
    while index < len(lines) and _TABLE_ROW_RE.match(lines[index]):
        rows.append(_split_table_row(lines[index]))
        index += 1
    markdown = "\n".join(lines[start:index])
    return TableBlock(markdown=markdown, rows=rows), index


def _consume_block_quote(lines: List[str], index: int) -> tuple[BlockQuoteBlock, int]:
    quoted: List[str] = []
    while index < len(lines):
        match = _BLOCK_QUOTE_RE.match(lines[index])
        if not match:
            break
        quoted.append(match.group(1))
        index += 1
    return BlockQuoteBlock(text="\n".join(quoted)), index


def _consume_list(lines: List[str], index: int) -> tuple[ListBlock, int]:
    start = index
    ordered = _ORDERED_ITEM_RE.match(lines[index]) is not None

    items: List[str] = []
    current_item: List[str] = []

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            # A blank line ends the list unless it is followed by indented
            # continuation or another top-level item of the same list type.
            next_index = index + 1
            if next_index < len(lines) and (
                _is_same_type_item(lines[next_index], ordered)
                or _is_indented(lines[next_index])
            ):
                current_item.append("")
                index += 1
                continue
            break

        item_match = _UNORDERED_ITEM_RE.match(line) or _ORDERED_ITEM_RE.match(line)
        if item_match and not item_match.group(1):
            # An adjacent top-level list of the other type starts a new block.
            if (_ORDERED_ITEM_RE.match(line) is not None) != ordered:
                break
            if current_item:
                items.append("\n".join(current_item).rstrip())
            current_item = [item_match.group(2)]
        elif item_match or _is_indented(line):
            # Nested item or indented continuation stays with its parent.
            current_item.append(line.strip())
        else:
            break
        index += 1

    if current_item:
        items.append("\n".join(current_item).rstrip())

    markdown = "\n".join(lines[start:index]).rstrip()
    return ListBlock(markdown=markdown, ordered=ordered, items=items), index


def _is_same_type_item(line: str, ordered: bool) -> bool:
    match = _UNORDERED_ITEM_RE.match(line) or _ORDERED_ITEM_RE.match(line)
    if match is None or match.group(1):
        return False
    return (_ORDERED_ITEM_RE.match(line) is not None) == ordered


def _is_indented(line: str) -> bool:
    return line.startswith(("    ", "\t", "  "))


def _consume_paragraph(lines: List[str], index: int) -> tuple[ParagraphBlock, int]:
    paragraph: List[str] = []
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            break
        # Stop if a new structured block begins mid-paragraph.
        if (
            _HEADING_RE.match(line)
            or _FENCE_RE.match(line)
            or _HORIZONTAL_RULE_RE.match(line)
            or (_TABLE_ROW_RE.match(line) and _is_table_start(lines, index))
            or _BLOCK_QUOTE_RE.match(line)
        ) and paragraph:
            break
        item_match = _UNORDERED_ITEM_RE.match(line) or _ORDERED_ITEM_RE.match(line)
        if item_match and not item_match.group(1) and paragraph:
            break
        paragraph.append(line)
        index += 1
    return ParagraphBlock(text="\n".join(paragraph).strip()), index
