#!/usr/bin/env python3
"""
Convert Jupyter notebooks to Markdown with optional code extraction.

Usage:
    python convert-jupyter.py notebook.ipynb
    python convert-jupyter.py notebook.ipynb -o output.md
    python convert-jupyter.py notebook.ipynb --code-only
    python convert-jupyter.py ./notebooks/ --batch
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    print("Error: markitdown not installed. Run: pip install 'markitdown[all]'")
    sys.exit(1)


def extract_code_cells(markdown_content: str) -> list[str]:
    """Extract Python code blocks from markdown content."""
    return re.findall(r"```python\n(.*?)```", markdown_content, re.DOTALL)


def convert_notebook(
    input_path: Path,
    output_path: Path | None = None,
    code_only: bool = False,
) -> str:
    """Convert a single Jupyter notebook to markdown."""
    md = MarkItDown()
    result = md.convert(str(input_path))
    content = result.text_content

    if code_only:
        code_blocks = extract_code_cells(content)
        content = "\n\n".join(
            f"# Cell {i}\n{block}" for i, block in enumerate(code_blocks, 1)
        )

    if output_path:
        output_path.write_text(content)
        print(f"Converted: {input_path.name} -> {output_path.name}")
    else:
        print(content)

    return content


def batch_convert(
    input_dir: Path,
    output_dir: Path | None = None,
    code_only: bool = False,
) -> dict:
    """Convert all notebooks in a directory."""
    if output_dir is None:
        output_dir = input_dir

    output_dir.mkdir(parents=True, exist_ok=True)
    results = {"success": [], "failed": []}

    for notebook in input_dir.glob("*.ipynb"):
        suffix = ".py" if code_only else ".md"
        output_path = output_dir / f"{notebook.stem}{suffix}"
        try:
            convert_notebook(notebook, output_path, code_only)
            results["success"].append(str(notebook))
        except Exception as e:
            results["failed"].append({"file": str(notebook), "error": str(e)})
            print(f"Failed: {notebook.name} - {e}", file=sys.stderr)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to Markdown"
    )
    parser.add_argument("input", help="Notebook file or directory")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument(
        "--code-only",
        action="store_true",
        help="Extract only code cells",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all notebooks in directory",
    )

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)

    if args.batch or input_path.is_dir():
        output_dir = Path(args.output) if args.output else None
        results = batch_convert(input_path, output_dir, args.code_only)
        print(f"\nConverted: {len(results['success'])}")
        print(f"Failed: {len(results['failed'])}")
    else:
        output_path = Path(args.output) if args.output else None
        convert_notebook(input_path, output_path, args.code_only)


if __name__ == "__main__":
    main()
