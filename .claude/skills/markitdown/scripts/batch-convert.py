#!/usr/bin/env python3
"""
Batch convert documents to Markdown using MarkItDown.

Usage:
    python batch-convert.py ./documents ./output
    python batch-convert.py ./documents ./output --extensions pdf,docx,pptx
    python batch-convert.py ./documents ./output --workers 8
"""

import argparse
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

try:
    from markitdown import MarkItDown
except ImportError:
    print("Error: markitdown not installed. Run: pip install 'markitdown[all]'")
    sys.exit(1)

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False


def convert_file(
    md: MarkItDown,
    input_file: Path,
    output_dir: Path
) -> tuple[Path, bool, str]:
    """Convert a single file and return status."""
    try:
        result = md.convert(str(input_file))
        output_file = output_dir / f"{input_file.stem}.md"
        output_file.write_text(result.text_content, encoding="utf-8")
        return input_file, True, ""
    except Exception as e:
        return input_file, False, str(e)


def batch_convert(
    input_dir: Path,
    output_dir: Path,
    extensions: Optional[list[str]] = None,
    max_workers: int = 4,
    recursive: bool = False,
    enable_plugins: bool = False
) -> dict:
    """
    Convert all matching files in directory.

    Args:
        input_dir: Source directory
        output_dir: Destination directory
        extensions: File extensions to process (None = all)
        max_workers: Number of parallel workers
        recursive: Search subdirectories
        enable_plugins: Enable MarkItDown plugins

    Returns:
        Dictionary with success and failed lists
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    md = MarkItDown(enable_plugins=enable_plugins)

    # Collect files
    files = []
    if extensions:
        for ext in extensions:
            pattern = f"**/*.{ext}" if recursive else f"*.{ext}"
            files.extend(input_dir.glob(pattern))
    else:
        if recursive:
            files = [f for f in input_dir.rglob("*") if f.is_file()]
        else:
            files = [f for f in input_dir.iterdir() if f.is_file()]

    if not files:
        print(f"No files found in {input_dir}")
        return {"success": [], "failed": []}

    results = {"success": [], "failed": []}

    # Process with progress bar if tqdm available
    if HAS_TQDM:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(convert_file, md, f, output_dir): f
                for f in files
            }

            for future in tqdm(as_completed(futures), total=len(files), desc="Converting"):
                file_path, success, error = future.result()
                if success:
                    results["success"].append(str(file_path))
                else:
                    results["failed"].append({"file": str(file_path), "error": error})
                    tqdm.write(f"Failed: {file_path.name} - {error}")
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(convert_file, md, f, output_dir): f
                for f in files
            }

            for i, future in enumerate(as_completed(futures), 1):
                file_path, success, error = future.result()
                if success:
                    results["success"].append(str(file_path))
                    print(f"[{i}/{len(files)}] Converted: {file_path.name}")
                else:
                    results["failed"].append({"file": str(file_path), "error": error})
                    print(f"[{i}/{len(files)}] Failed: {file_path.name} - {error}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert documents to Markdown using MarkItDown"
    )
    parser.add_argument("input_dir", type=Path, help="Input directory")
    parser.add_argument("output_dir", type=Path, help="Output directory")
    parser.add_argument(
        "-e", "--extensions",
        type=str,
        help="Comma-separated file extensions (e.g., pdf,docx,pptx)"
    )
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=4,
        help="Number of parallel workers (default: 4)"
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Search subdirectories recursively"
    )
    parser.add_argument(
        "--plugins",
        action="store_true",
        help="Enable MarkItDown plugins"
    )

    args = parser.parse_args()

    if not args.input_dir.exists():
        print(f"Error: Input directory does not exist: {args.input_dir}")
        sys.exit(1)

    extensions = None
    if args.extensions:
        extensions = [ext.strip().lstrip(".") for ext in args.extensions.split(",")]

    print(f"Input: {args.input_dir}")
    print(f"Output: {args.output_dir}")
    if extensions:
        print(f"Extensions: {', '.join(extensions)}")
    print(f"Workers: {args.workers}")
    print(f"Recursive: {args.recursive}")
    print()

    results = batch_convert(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        extensions=extensions,
        max_workers=args.workers,
        recursive=args.recursive,
        enable_plugins=args.plugins
    )

    print()
    print(f"Successfully converted: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")

    if results["failed"]:
        print("\nFailed files:")
        for item in results["failed"]:
            print(f"  - {item['file']}: {item['error']}")

    sys.exit(0 if not results["failed"] else 1)


if __name__ == "__main__":
    main()
