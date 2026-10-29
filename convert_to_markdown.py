#!/usr/bin/env python3
"""Convert files to Markdown using MarkItDown (any format it supports)."""

import sys
from pathlib import Path

from markitdown import MarkItDown


def convert_file(md: MarkItDown, path: Path) -> None:
    output_path = path.with_suffix(".md")
    try:
        result = md.convert(str(path))
    except Exception as e:
        print(f"FAILED  {path.name}: {e}")
        return
    output_path.write_text(result.text_content, encoding="utf-8")
    print(f"OK      {path.name} -> {output_path.name}")


def main() -> None:
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("Enter path to folder or file: ").strip()

    target_path = Path(target).expanduser()

    if not target_path.exists():
        print(f"Path not found: {target_path}")
        sys.exit(1)

    md = MarkItDown()

    if target_path.is_file():
        convert_file(md, target_path)
        return

    files = sorted(p for p in target_path.iterdir() if p.is_file())

    if not files:
        print("No files found in folder.")
        return

    for path in files:
        convert_file(md, path)


if __name__ == "__main__":
    main()
