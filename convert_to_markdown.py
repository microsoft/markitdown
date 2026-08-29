#!/usr/bin/env python3
"""Convert files to Markdown using MarkItDown (any format it supports)."""

import sys
from pathlib import Path

from markitdown import MarkItDown


def prompt(message: str) -> str:
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input required.")


def convert_file(md: MarkItDown, path: Path, output_path: Path) -> str:
    try:
        result = md.convert(str(path))
    except Exception as e:
        print(f"FAILED  {path.name}: {e}")
        return "failed"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result.text_content, encoding="utf-8")
    print(f"OK      {path.name} -> {output_path}")
    return "ok"


def ask_output_location(source_root: Path) -> tuple[Path | None, bool]:
    """Returns (output_dir, flatten). output_dir=None means next to original."""
    choice = prompt(
        "Save .md files next to originals, or in a specific location? [next/specific] "
    ).lower()

    if choice not in ("specific", "s"):
        return None, False

    dest = prompt("Enter destination folder: ")
    output_dir = Path(dest).expanduser()

    structure_choice = prompt(
        "Keep same subfolder structure as originals, or put all .md files flat "
        "in one location? [structure/flat] "
    ).lower()

    flatten = structure_choice in ("flat", "f")
    return output_dir, flatten


def print_summary(ok_count: int, failed_count: int, skipped_count: int) -> None:
    total = ok_count + failed_count + skipped_count
    print("---")
    print(
        f"Summary: {total} file(s) - {ok_count} converted, "
        f"{failed_count} failed, {skipped_count} skipped"
    )


def resolve_output_path(
    source_path: Path,
    source_root: Path,
    output_dir: Path | None,
    flatten: bool,
) -> Path:
    if output_dir is None:
        return source_path.with_suffix(".md")

    if flatten:
        return output_dir / (source_path.stem + ".md")

    rel = source_path.relative_to(source_root)
    return (output_dir / rel).with_suffix(".md")


def main() -> None:
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = prompt("Enter path to folder or file: ")

    target_path = Path(target).expanduser()

    if not target_path.exists():
        print(f"Path not found: {target_path}")
        sys.exit(1)

    md = MarkItDown()

    if target_path.is_file():
        if target_path.suffix.lower() == ".md":
            print(f"SKIP    {target_path.name}: already Markdown")
            print_summary(0, 0, 1)
            return
        output_dir, flatten = ask_output_location(target_path.parent)
        output_path = resolve_output_path(
            target_path, target_path.parent, output_dir, flatten
        )
        status = convert_file(md, target_path, output_path)
        print_summary(1 if status == "ok" else 0, 1 if status == "failed" else 0, 0)
        return

    all_files = sorted(p for p in target_path.rglob("*") if p.is_file())
    files = [p for p in all_files if p.suffix.lower() != ".md"]
    skipped = len(all_files) - len(files)

    for path in all_files:
        if path.suffix.lower() == ".md":
            print(f"SKIP    {path.name}: already Markdown")

    if not all_files:
        print("No files found in folder.")
        return

    if not files:
        print_summary(0, 0, skipped)
        return

    output_dir, flatten = ask_output_location(target_path)

    ok_count = 0
    failed_count = 0
    for path in files:
        output_path = resolve_output_path(path, target_path, output_dir, flatten)
        status = convert_file(md, path, output_path)
        if status == "ok":
            ok_count += 1
        else:
            failed_count += 1

    print_summary(ok_count, failed_count, skipped)


if __name__ == "__main__":
    main()
