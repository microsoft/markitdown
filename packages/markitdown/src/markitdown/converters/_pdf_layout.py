"""Conservative horizontal PDF layout and mixed-direction glyph reconstruction.

PDFs store positioned glyphs, not necessarily logical Unicode strings. Keep each
ToUnicode mapping intact (one glyph may encode a ligature) while ordering glyphs
and directional runs. This is not a general inverse of the Unicode bidi
algorithm: ambiguous untagged layouts cannot reveal the author's original order.
"""

import bisect
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


_MIRROR = dict(
    zip("()[]{}<>\u00ab\u00bb\u2039\u203a", ")(][}{><\u00bb\u00ab\u203a\u2039")
)


def _has_rtl(text: str) -> bool:
    return any(unicodedata.bidirectional(c) in ("R", "AL") for c in text)


def _is_mark(text: str) -> bool:
    return bool(text) and all(unicodedata.category(c) == "Mn" for c in text)


def _base_letters(text: str) -> str:
    """Map Arabic Presentation Forms (shaped glyph codepoints) to base letters.

    Some producers (Chromium/Skia, for example) map shaped glyphs back to the
    contextual forms U+FB50-FDFF and U+FE70-FEFF. These are compatibility
    characters for the letters a reader would search for; ordinary letters,
    ZWNJ and digits are never altered.
    """
    if not any("\ufb50" <= c <= "\ufdff" or "\ufe70" <= c <= "\ufeff" for c in text):
        return text
    return "".join(
        (
            unicodedata.normalize("NFKC", c)
            if "\ufb50" <= c <= "\ufdff" or "\ufe70" <= c <= "\ufeff"
            else c
        )
        for c in text
    )


def _lines(chars: list[dict[str, Any]]) -> list[_Line]:
    """Use text-matrix baselines, independent of a font's ascent/descent."""
    lines: list[_Line] = []
    marks = [c for c in chars if _is_mark(c["text"])]
    bases = [c for c in chars if not _is_mark(c["text"])]
    if not bases:
        bases, marks = chars, []
    for char in sorted(bases, key=lambda c: -c["matrix"][5]):
        baseline = float(char["matrix"][5])
        if not lines or abs(lines[-1].baseline - baseline) > 3:
            lines.append(_Line([], baseline))
        lines[-1].chars.append(char)
    # Positioned marks (tanwin, hamza above, kasra) may be offset vertically by
    # GPOS. Attach each to the line whose base glyph it overlaps horizontally.
    leftovers = []
    for mark in marks:
        centre = (mark["x0"] + mark["x1"]) / 2
        height = float(mark["matrix"][5])
        reach = max(float(mark["size"]), 1) * 0.9
        near = [ln for ln in lines if abs(ln.baseline - height) <= reach]
        over = [
            ln
            for ln in near
            if any(b["x0"] - 1 <= centre <= b["x1"] + 1 for b in ln.chars)
        ]
        pool = over or near
        if pool:
            min(pool, key=lambda ln: abs(ln.baseline - height)).chars.append(mark)
        else:
            leftovers.append(mark)
    for mark in sorted(leftovers, key=lambda c: -c["matrix"][5]):
        lines.append(_Line([mark], float(mark["matrix"][5])))
    lines.sort(key=lambda line: -line.baseline)
    order = {id(c): i for i, c in enumerate(chars)}
    for line in lines:
        # Stable sorting also retains coincident combining marks and joiners.
        # PDF numeric operands are often rounded independently for a joiner
        # and its base. Treat sub-pixel differences as the same position.
        line.chars.sort(key=lambda c: (round(c["x0"], 1), order[id(c)]))
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

    # A bracket pair that encloses left-to-right text is part of that text, as in
    # UBA rule N0. Only drawn-in-order pairs match: a reversed pair (")...(")
    # is left to the run reversal below.
    stack: list[int] = []
    for i, glyph in enumerate(glyphs):
        if glyph in "([{":
            stack.append(i)
        elif (
            glyph in ")]}"
            and stack
            and "([{".index(glyphs[stack[-1]]) == ")]}".index(glyph)
        ):
            start = stack.pop()
            if not strong[start] and not strong[i]:
                if any(strong[k] == "L" for k in range(start + 1, i)):
                    directions[start] = directions[i] = "L"

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

    # Shapers draw a bracket or guillemet inside right-to-left text with its
    # mirrored glyph, so ToUnicode reports the opposite character. Restore the
    # logical one when strong right-to-left text surrounds it on both sides.
    for i, glyph in enumerate(glyphs):
        if glyph in _MIRROR and directions[i] == "R":
            before = next((strong[j] for j in range(i - 1, -1, -1) if strong[j]), "R")
            after = next(
                (strong[j] for j in range(i + 1, len(glyphs)) if strong[j]), "R"
            )
            if before == "R" and after == "R":
                glyphs[i] = _MIRROR[glyph]

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


_ITEM_MARKER = re.compile(
    r"(?:[0-9\u06f0-\u06f9\u0660-\u0669]+[.)]|[\u2022\u25e6\u25aa-])$"
)


def _starts_item(line: _Line) -> bool:
    """True when the line begins with a list marker such as "1." or a bullet."""
    marker = ""
    previous = None
    # Marker and item text are separate pieces; a list line in an RTL paragraph
    # begins at its right edge, while an LTR one begins at its left edge.
    for char in sorted(line.chars, key=lambda c: -c["x1"]):
        if char["text"].isspace() or (
            previous is not None and previous["x0"] - char["x1"] > 1.5
        ):
            break
        marker += char["text"]
        previous = char
    reading = marker.strip()
    left = ""
    previous = None
    for char in line.chars:
        if char["text"].isspace() or (
            previous is not None and char["x0"] - previous["x1"] > 1.5
        ):
            break
        left += char["text"]
        previous = char
    return bool(_ITEM_MARKER.match(reading) or _ITEM_MARKER.match(left.strip()))


def _paragraph_rtl(lines: list[_Line]) -> bool | None:
    """Base direction of a wrapped paragraph; None defers to each line's edge."""
    if len(lines) < 2:
        return None
    right = left = 0
    for line in lines:
        for char in line.chars:
            for codepoint in char["text"]:
                direction = unicodedata.bidirectional(codepoint)
                right += direction in ("R", "AL")
                left += direction == "L"
    return right >= left if right + left else None


def _paragraphs(lines: list[_Line]) -> str:
    lines = [line for line in lines if line.chars]
    # Wrapped paragraphs use a regular line pitch. A larger gap starts a new
    # paragraph, so generous line spacing is not mistaken for paragraph spacing.
    pitches = sorted(
        gap
        for first, second in zip(lines, lines[1:])
        if 0
        < (gap := first.baseline - second.baseline)
        <= max(first.size, second.size) * 2.2
    )
    pitch = pitches[len(pitches) // 2] if pitches else 0
    paragraphs: list[list[_Line]] = []
    for index, line in enumerate(lines):
        if index:
            previous = lines[index - 1]
            gap = previous.baseline - line.baseline
            resized = abs(previous.size - line.size) > 0.5
            if (
                resized
                or _starts_item(line)
                or gap > max(max(previous.size, line.size) * 1.6, pitch * 1.25)
            ):
                paragraphs.append([])
        if not paragraphs:
            paragraphs.append([])
        paragraphs[-1].append(line)
    blocks = []
    for paragraph in paragraphs:
        rtl = _paragraph_rtl(paragraph)
        texts = [_logical_line(line.chars, rtl) for line in paragraph]
        blocks.append("\n".join(text for text in texts if text))
    return "\n\n".join(block for block in blocks if block)


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


def _zero_advance_spaces(chars: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Recognize a ZWNJ that the font maps to its space glyph.

    Some fonts share one glyph between U+0020 and U+200C, so ToUnicode can only
    report a space. A real space advances the pen; the ZWNJ does not, so the
    following letter starts inside the space's nominal box. Such a glyph is
    restored to U+200C, kept ahead of that letter.
    """
    buckets: dict[int, list[float]] = {}
    for char in chars:
        if not char["text"].isspace():
            buckets.setdefault(round(char["matrix"][5] / 3), []).append(char["x0"])
    for starts in buckets.values():
        starts.sort()
    result = []
    for char in chars:
        if char["text"] == " ":
            starts = buckets.get(round(char["matrix"][5] / 3), [])
            first = bisect.bisect_left(starts, char["x0"] - 0.5)
            if first < len(starts) and starts[first] < char["x1"] - 1:
                x = char["x0"] - 0.2
                char = dict(char, text="\u200c", x0=x, x1=x)
        result.append(char)
    return result


def _gutter_columns(chars: list[dict[str, Any]], page_width: float):
    """Split RTL text pages at one clear vertical gutter shared by every line.

    Unlike the sparse form of `_columns`, this accepts ordinary wrapped columns
    with a gutter of a few line-heights. The gutter must be the only free band
    in the text area, so spanning headings, tables and justified rivers defer.
    """
    sizes = sorted(float(c["size"]) for c in chars)
    threshold = max(sizes[len(sizes) // 2], page_width * 0.02)
    spans = sorted((c["x0"], c["x1"]) for c in chars if not c["text"].isspace())
    if not spans:
        return None
    free = []
    reach = spans[0][1]
    for start, end in spans[1:]:
        if start - reach >= threshold:
            free.append((reach, start))
        reach = max(reach, end)
    if len(free) != 1:
        return None
    middle = (free[0][0] + free[0][1]) / 2
    sides = [
        [c for c in chars if (c["x0"] + c["x1"]) / 2 < middle],
        [c for c in chars if (c["x0"] + c["x1"]) / 2 >= middle],
    ]
    columns = [_lines(side) for side in sides]
    if any(len(column) < 2 for column in columns):
        return None
    return columns


def extract_ordered_content(page: Any) -> str | None:
    """Return reconstructed RTL/sparse-column content, or defer to the converter."""
    chars = page.chars
    if not chars:
        return None
    chars = [
        (
            dict(c, text=_base_letters(c["text"]))
            if _base_letters(c["text"]) != c["text"]
            else c
        )
        for c in chars
    ]
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
    if rtl:
        chars = _zero_advance_spaces(chars)
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
    reverse = (
        rtl and columns is not None and _rtl_base(sorted(chars, key=lambda c: c["x0"]))
    )
    if columns is None and rtl and not page.edges:
        columns = _gutter_columns(chars, page.width)
        reverse = bool(_paragraph_rtl(lines))
    if columns is not None:
        if reverse:
            columns.reverse()
        return "\n\n".join(_paragraphs(column) for column in columns)
    return _paragraphs(lines) if rtl else None
