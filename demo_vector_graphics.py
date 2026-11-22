"""Demo: MarkItDown's opt-in PDF vector-graphics diagnostic.

Usage:
    python demo_vector_graphics.py [file.pdf ...]

With no arguments, runs against the bundled test fixtures.
"""

import logging
import sys
from pathlib import Path

from markitdown import MarkItDown

FIXTURES = Path("./packages/markitdown/tests/test_files")
DEFAULT_FILES = [
    FIXTURES / "vector_graphics_mixed.pdf",  # curves on pages 1 and 3
    FIXTURES / "vector_graphics_rule_only.pdf",  # rule + box only: not flagged
    FIXTURES / "test.pdf",  # plain text
]


def show(md: MarkItDown, path: Path) -> None:
    print(f"=== {path.name}")

    default = md.convert(str(path))
    print(f"  default run:          warnings = {default.warnings!r}  (not checked)")

    result = md.convert(str(path), detect_vector_graphics=True)
    print(f"  Markdown unchanged:   {result.markdown == default.markdown}")

    if not result.warnings:
        print("  detect run:           warnings = []  (checked, nothing found)")
    for w in result.warnings or []:
        where = f"page {w.page}" if w.page is not None else "document"
        print(
            f"  {logging.getLevelName(w.severity):<8} {w.code} on {where}: "
            f"{dict(w.counts)}"
        )
        print(f"           {w.message}")
    print()


def main() -> None:
    files = [Path(p) for p in sys.argv[1:]] or DEFAULT_FILES
    md = MarkItDown()
    for path in files:
        show(md, path)


if __name__ == "__main__":
    main()
