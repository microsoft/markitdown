"""Structure-aware XLSX -> Markdown renderer.

For each sheet, splits contiguous non-empty regions into separate Markdown
tables, promotes single-cell header rows to ### headings, trims unused
leading/trailing columns per block, and skips header-only blocks.
"""
import openpyxl


def cell_to_md(value) -> str:
    if value is None:
        return ""
    return str(value).strip().replace("|", "\\|").replace("\n", "<br>")


def used_col_range(rows):
    lo, hi = None, 0
    for row in rows:
        for i, v in enumerate(row):
            if v not in (None, ""):
                if lo is None or i < lo:
                    lo = i
                if i + 1 > hi:
                    hi = i + 1
    return (lo or 0, hi)


def is_empty_row(row, n):
    return all(c in (None, "") for c in row[:n])


def non_empty_count(row, n):
    return sum(1 for c in row[:n] if c not in (None, ""))


def render_table(block, n):
    lines = ["| " + " | ".join(cell_to_md(c) for c in block[0][:n]) + " |"]
    lines.append("| " + " | ".join(["---"] * n) + " |")
    for row in block[1:]:
        lines.append("| " + " | ".join(cell_to_md(c) for c in row[:n]) + " |")
    return "\n".join(lines)


def render_paragraphs(block, n):
    out = []
    for row in block:
        for c in row[:n]:
            if c not in (None, ""):
                out.append(cell_to_md(c))
                break
    return "\n\n".join(out)


def render_sheet(ws) -> str:
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    _, max_col = used_col_range(rows)
    if max_col == 0:
        return f"## {ws.title}\n\n_(empty)_"

    blocks, cur = [], []
    for row in rows:
        if is_empty_row(row, max_col):
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(row)
    if cur:
        blocks.append(cur)

    parts = [f"## {ws.title}"]
    for block in blocks:
        lo, hi = used_col_range(block)
        block = [row[lo:hi] for row in block]
        n = hi - lo
        if n <= 1:
            parts.append(render_paragraphs(block, n))
            continue
        if non_empty_count(block[0], n) == 1 and len(block) > 1:
            heading = next(
                (cell_to_md(c) for c in block[0][:n] if c not in (None, "")), ""
            )
            parts.append(f"### {heading}")
            block = block[1:]
        if len(block) <= 1:
            parts.append(render_paragraphs(block, n))
        else:
            parts.append(render_table(block, n))
    return "\n\n".join(parts)


def render_workbook(source) -> str:
    wb = openpyxl.load_workbook(source, data_only=True)
    return "\n\n".join(render_sheet(ws) for ws in wb.worksheets) + "\n"
