"""Rebuild copied PDF fixtures with PyMuPDF (already used by the OCR package).

Run from packages/markitdown with: python tests/test_files/generate_pdf_cleanup_fixtures.py
The existing source PDFs are opened read-only; only pdf_cleanup_*.pdf is written.
"""

from pathlib import Path

import pymupdf


FIXTURES = Path(__file__).resolve().parent


def main() -> None:
    with pymupdf.open(FIXTURES / "test.pdf") as plain, pymupdf.open(
        FIXTURES / "REPAIR-2022-INV-001_multipage.pdf"
    ) as form:
        for name, pages in (
            ("plain", [plain, plain, plain]),
            ("form", [form, form, form]),
            ("mixed", [form, plain, form]),
        ):
            with pymupdf.open() as copied:
                for source in pages:
                    copied.insert_pdf(source, from_page=0, to_page=0)
                copied.save(FIXTURES / f"pdf_cleanup_{name}.pdf", deflate=True)


if __name__ == "__main__":
    main()
