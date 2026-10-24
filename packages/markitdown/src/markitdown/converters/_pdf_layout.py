"""Conservative horizontal PDF layout and mixed-direction glyph reconstruction.

PDFs store positioned glyphs, not necessarily logical Unicode strings. Keep each
ToUnicode mapping intact (one glyph may encode a ligature) while ordering glyphs
and directional runs. This is not a general inverse of the Unicode bidi
algorithm: ambiguous untagged layouts cannot reveal the author's original order.
"""

import re
import unicodedata
from dataclasses import dataclass
from typing import Any


@dataclass
class _Line:
    chars: list[dict[str, Any]]
    baseline: float

    @property
    def size(self) -> float:
        return max(float(c["size"]) for c in self.chars)


def _has_rtl(text: str) -> bool:
    return any(unicodedata.bidirectional(c) in ("R", "AL") for c in text)


def _lines(chars: list[dict[str, Any]]) -> list[_Line]:
    """Use text-matrix baselines, independent of a font's ascent/descent."""
    lines: list[_Line] = []
    for char in sorted(chars, key=lambda c: -c["matrix"][5]):
        baseline = float(char["matrix"][5])
        if not lines or abs(lines[-1].baseline - baseline) > 3:
            lines.append(_Line([], baseline))
        lines[-1].chars.append(char)
    for line in lines:
        # Stable sorting also retains coincident combining marks and joiners.
        # PDF numeric operands are often rounded independently for a joiner
        # and its base. Treat sub-pixel differences as the same position.
        line.chars.sort(key=lambda c: round(c["x0"], 1))
    return lines


def _rtl_base(chars: list[dict[str, Any]]) -> bool:
    # The right edge distinguishes RTL prose with a long English identifier
    # from an English line containing a short RTL quotation.
    for char in reversed(chars):
        for codepoint in reversed(char["text"]):
            direction = unicodedata.bidirectional(codepoint)
            if direction in ("R", "AL", "L"):
                return direction != "L"
    return False


def _logical_line(chars: list[dict[str, Any]], rtl: bool | None = None) -> str:
    if not chars:
        return ""
    # Insert spaces only for actual gaps, not at every font/run boundary.
    glyphs: list[str] = []
    previous = None
    for char in chars:
        if previous is not None:
            gap = char["x0"] - previous["x1"]
            if gap > max(1.5, min(char["size"], previous["size"]) * 0.2):
                if not glyphs[-1].isspace() and not char["text"].isspace():
                    glyphs.append(" ")
        glyphs.append(char["text"])
        previous = char
    if not any(_has_rtl(g) for g in glyphs):
        return "".join(glyphs).strip()
    if rtl is None:
        rtl = _rtl_base(chars)

    # Assign directional runs, keeping neutral characters between LTR letters
    # and digits with the expression (URLs, dates, versions and equations).
    # Brackets at either edge retain their original ToUnicode mapping.
    strong = []
    for glyph in glyphs:
        types = {unicodedata.bidirectional(c) for c in glyph}
        strong.append(
            "R" if types & {"R", "AL"} else "L" if types & {"L", "EN", "AN"} else ""
        )
    directions = ["R" if rtl else "L"] * len(glyphs)
    seeds = [i for i, direction in enumerate(strong) if direction]
    for i in seeds:
        directions[i] = strong[i]
    for left, right in zip(seeds, seeds[1:]):
        if strong[left] == strong[right]:
            directions[left : right + 1] = [strong[left]] * (right - left + 1)

    # In an Arabic paragraph a number before a Latin unit can be displayed to
    # its right (weak type EN resolved after AL). Prefer quantity-before-unit
    # for a standalone compound-unit expression. This is an explicit heuristic,
    # not recovery of missing bidi metadata. Do not apply it to URLs or versions.
    if rtl:
        visual = "".join(glyphs)
        pattern = r"(?<![\w/])([A-Za-zµμ]+/[A-Za-zµμ]+)(\s+)(\d+(?:[.,]\d+)?)(?![\w.])"
        offsets = []
        offset = 0
        for glyph in glyphs:
            offsets.append(offset)
            offset += len(glyph)
        for match in re.finditer(pattern, visual):
            start, end = match.span(2)
            for i, offset in enumerate(offsets):
                if start <= offset < end:
                    directions[i] = "R"

    runs: list[tuple[str, list[str]]] = []
    for glyph, direction in zip(glyphs, directions):
        if not runs or runs[-1][0] != direction:
            runs.append((direction, []))
        runs[-1][1].append(glyph)
    if rtl:
        runs.reverse()
    return "".join(
        "".join(reversed(run) if direction == "R" else run) for direction, run in runs
    ).strip()


def _paragraphs(lines: list[_Line]) -> str:
    result = ""
    previous = None
    for line in lines:
        text = _logical_line(line.chars)
        if not text:
            continue
        if previous is not None:
            gap = previous.baseline - line.baseline
            result += "\n\n" if gap > max(previous.size, line.size) * 1.6 else "\n"
        result += text
        previous = line
    return result


def _columns(lines: list[_Line], page_width: float) -> list[list[_Line]] | None:
    """Recognize two separated text columns, requiring a persistent wide gutter.

    Restrict this to pages with two segments on every line and at least two
    lines. Spanning headings, narrow gutters, forms and complex layouts stay on
    the existing extraction path rather than guessing a universal column order.
    """
    if len(lines) < 2:
        return None
    pairs = []
    for line in lines:
        chars = line.chars
        gaps = [
            (chars[i + 1]["x0"] - chars[i]["x1"], i + 1) for i in range(len(chars) - 1)
        ]
        wide = [(gap, i) for gap, i in gaps if gap >= page_width * 0.2]
        if len(wide) != 1:
            return None
        _, split = wide[0]
        pairs.append((chars[:split], chars[split:]))
    if max(max(c["x1"] for c in left) for left, _ in pairs) >= min(
        min(c["x0"] for c in right) for _, right in pairs
    ):
        return None
    return [
        [_Line(pair[index], line.baseline) for pair, line in zip(pairs, lines)]
        for index in (0, 1)
    ]


def extract_ordered_content(page: Any) -> str | None:
    """Return reconstructed RTL/sparse-column content, or defer to the converter."""
    chars = page.chars
    if not chars:
        return None
    # Rotated/vertical text requires a different coordinate system.
    if any(
        not c["upright"]
        or abs(c["matrix"][1]) > 0.01
        or abs(c["matrix"][2]) > 0.01
        or c["matrix"][0] <= 0
        or c["matrix"][3] <= 0
        for c in chars
    ):
        return None
    rtl = any(_has_rtl(c["text"]) for c in chars)
    lines = _lines(chars)
    # Ruled tables have reliable cell geometry; use it rather than word-based
    # form inference, which can split a mixed-font cell across baselines.
    tables = page.find_tables() if rtl else []
    if tables:
        pieces = []
        used = set()
        for table in tables:
            table_chars = [
                c
                for c in chars
                if table.bbox[0] <= (c["x0"] + c["x1"]) / 2 < table.bbox[2]
                and table.bbox[1] <= (c["top"] + c["bottom"]) / 2 < table.bbox[3]
            ]
            header = table.rows[0]
            header_chars = [
                c
                for c in table_chars
                if any(
                    box is not None and box[1] <= (c["top"] + c["bottom"]) / 2 < box[3]
                    for box in header.cells
                )
            ]
            table_rtl = _rtl_base(sorted(header_chars, key=lambda c: c["x0"]))
            rows = []
            for row in table.rows:
                cells = []
                for box in row.cells:
                    cell_chars = (
                        []
                        if box is None
                        else [
                            c
                            for c in table_chars
                            if box[0] <= (c["x0"] + c["x1"]) / 2 < box[2]
                            and box[1] <= (c["top"] + c["bottom"]) / 2 < box[3]
                        ]
                    )
                    used.update(id(c) for c in cell_chars)
                    cells.append(_paragraphs(_lines(cell_chars)).replace("\n", " "))
                rows.append(list(reversed(cells)) if table_rtl else cells)
            if rows:
                # Escape literal pipes so cell content cannot create columns.
                rows = [[cell.replace("|", "\\|") for cell in row] for row in rows]
                output = [
                    "| " + " | ".join(rows[0]) + " |",
                    "| " + " | ".join("---" for _ in rows[0]) + " |",
                ]
                output.extend("| " + " | ".join(row) + " |" for row in rows[1:])
                pieces.append((table.bbox[1], "\n".join(output)))
        for line in _lines([c for c in chars if id(c) not in used]):
            pieces.append(
                (min(c["top"] for c in line.chars), _logical_line(line.chars))
            )
        return "\n\n".join(
            text for _, text in sorted(pieces, key=lambda piece: piece[0]) if text
        )
    # Ruled tables are not newspaper-style columns, including on LTR pages.
    columns = _columns(lines, page.width) if not page.edges else None
    if columns is not None:
        if rtl and _rtl_base(sorted(chars, key=lambda c: c["x0"])):
            columns.reverse()
        return "\n\n".join(_paragraphs(column) for column in columns)
    return _paragraphs(lines) if rtl else None
