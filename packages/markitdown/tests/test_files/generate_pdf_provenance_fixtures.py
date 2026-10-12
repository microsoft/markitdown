"""Build small synthetic PDFs for page provenance tests using only stdlib.

All text and PDF objects are created here. No source documents are copied.
Run this script from any directory to regenerate the six sibling PDFs.
"""

from pathlib import Path


def _stream(data: bytes) -> bytes:
    return b"<< /Length %d >>\nstream\n" % len(data) + data + b"\nendstream"


def _text(value: str, x: int = 72, y: int = 720) -> bytes:
    return f"BT /F1 12 Tf {x} {y} Td ({value}) Tj ET\n".encode("ascii")


def _pdf(contents: list[bytes]) -> bytes:
    # Page labels deliberately disagree with physical positions: i, ii, 27...
    page_ids = [5 + 2 * index for index in range(len(contents))]
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R /PageLabels "
        b"<< /Nums [0 << /S /r >> 2 << /S /D /St 27 >>] >> >>",
        b"<< /Type /Pages /Count %d /Kids [%s] >>"
        % (len(contents), b" ".join(f"{n} 0 R".encode() for n in page_ids)),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
        b"/Encoding /WinAnsiEncoding /ToUnicode 4 0 R >>",
        _stream(
            b"/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n"
            b"/CIDSystemInfo << /Registry (Synthetic) /Ordering (Test) /Supplement 0 >> def\n"
            b"/CMapName /Synthetic def\n/CMapType 2 def\n"
            b"1 begincodespacerange\n<00> <FF>\nendcodespacerange\n"
            b"1 beginbfchar\n<01> <000C>\nendbfchar\n"
            b"endcmap\nCMapName currentdict /CMap defineresource pop\nend\nend"
        ),
    ]
    for page_id, content in zip(page_ids, contents):
        objects.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>"
            % (page_id + 1)
        )
        objects.append(_stream(content))

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    )
    return bytes(output)


def main() -> None:
    directory = Path(__file__).resolve().parent
    cover = _text("Synthetic cover. Printed page i.")
    table = b"".join(
        _text(cell, x, y)
        for y, row in zip(
            (720, 700, 680),
            (("Item", "Count", "Cost"), ("ALPHA", "2", "10"), ("BETA", "3", "15")),
        )
        for x, cell in zip((72, 220, 380), row)
    )
    prose = (
        _text("Synthetic prose. Printed page 28.")
        + _text(".1", y=680)
        + _text("Keep this numbered text together.", y=660)
    )
    fixtures = {
        "pdf_provenance_mixed.pdf": [cover, b"", table, prose, b""],
        "pdf_provenance_plain.pdf": [
            cover + _text(r"Before\001After", y=680),
            b"",
            _text("Last physical page. Printed page 27.")
            + _text(".1", y=680)
            + _text("Keep this numbered text together.", y=660),
        ],
        "pdf_provenance_empty.pdf": [b"", b"", b""],
        "pdf_provenance_repeated.pdf": [cover, b"", cover, b""],
        "pdf_provenance_edges.pdf": [b"", cover, b"", table, prose, b""],
        "pdf_provenance_boundaries.pdf": [
            _text("End of first physical page.") + _text(".1", y=680),
            _text("continuation on next physical page."),
            _text(".2")
            + _text("This continuation is on the same page.", y=700)
            + _text("unfinished-", y=660),
            _text("lowercase continuation stays on the fourth page."),
        ],
    }
    for name, pages in fixtures.items():
        (directory / name).write_bytes(_pdf(pages))


if __name__ == "__main__":
    main()
