# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "markitdown[all]==0.1.9",
#   "markitdown-ocr==0.1.2",
#   "markitdown-sample-plugin==0.1.0a1",
#   "openai>=1.0",
# ]
#
# [tool.uv]
# prerelease = "allow"
# ///
"""Convert files, folders and URLs to Markdown with MarkItDown.

Complements the markitdown MCP server: converts many inputs in one call,
writes .md files to disk, and can run LLM-vision OCR (markitdown-ocr) on
images embedded in PDF/DOCX/PPTX/XLSX when OPENAI_API_KEY is set.

Run with:  uv run <this file> [options] INPUT [INPUT ...]
"""

import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from markitdown import MarkItDown

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".xls",
    ".csv",
    ".json",
    ".xml",
    ".html",
    ".htm",
    ".epub",
    ".ipynb",
    ".msg",
    ".rtf",
    ".txt",
    ".jpg",
    ".jpeg",
    ".png",
    ".mp3",
    ".m4a",
    ".wav",
    ".zip",
}


def is_url(value: str) -> bool:
    return urlparse(value).scheme in ("http", "https", "file", "data")


def collect_files(path: Path, recursive: bool) -> list[Path]:
    if path.is_file():
        return [path]
    pattern = "**/*" if recursive else "*"
    return sorted(
        p
        for p in path.glob(pattern)
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def md_name(src: Path) -> str:
    # Keep the source extension so report.pdf and report.docx don't collide.
    return f"{src.name}.md"


def url_output_name(url: str) -> str:
    parsed = urlparse(url)
    stem = Path(parsed.path).stem or parsed.netloc or "document"
    return f"{stem}.md"


def build_converter(args: argparse.Namespace) -> MarkItDown:
    kwargs: dict = {"enable_plugins": True}
    if args.ocr:
        if not os.getenv("OPENAI_API_KEY"):
            sys.exit("--ocr needs the OPENAI_API_KEY environment variable.")
        from openai import OpenAI

        kwargs["llm_client"] = OpenAI()
        kwargs["llm_model"] = args.model
        if args.prompt:
            kwargs["llm_prompt"] = args.prompt
    return MarkItDown(**kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("inputs", nargs="+", help="Files, folders or URLs")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Write .md files here (default: next to each source file)",
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recurse into folders"
    )
    parser.add_argument(
        "--stdout", action="store_true", help="Print Markdown instead of writing files"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Replace existing .md files"
    )
    parser.add_argument(
        "--ocr",
        action="store_true",
        help="OCR embedded images with an LLM (needs OPENAI_API_KEY)",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MARKITDOWN_LLM_MODEL", "gpt-4o"),
        help="Vision model for --ocr (default: gpt-4o or $MARKITDOWN_LLM_MODEL)",
    )
    parser.add_argument("--prompt", help="Custom OCR prompt")
    parser.add_argument(
        "--keep-data-uris", action="store_true", help="Keep base64 images in the output"
    )
    args = parser.parse_args()

    converter = build_converter(args)

    jobs: list[tuple[str, Path | None]] = []
    for item in args.inputs:
        if is_url(item):
            out_dir = args.output_dir or Path.cwd()
            jobs.append((item, out_dir / url_output_name(item)))
            continue
        path = Path(item).expanduser()
        if not path.exists():
            print(f"FAILED  {item}: not found", file=sys.stderr)
            jobs.append((item, None))
            continue
        for src in collect_files(path, args.recursive):
            if args.output_dir:
                base = path if path.is_dir() else src.parent
                rel = src.relative_to(base)
                dest = args.output_dir / rel.parent / md_name(src)
            else:
                dest = src.parent / md_name(src)
            jobs.append((str(src), dest))

    converted = skipped = failed = 0
    for source, dest in jobs:
        if dest is None:
            failed += 1
            continue
        if not args.stdout and dest.exists() and not args.overwrite:
            print(f"SKIPPED {source}: {dest} exists (use --overwrite)", file=sys.stderr)
            skipped += 1
            continue
        try:
            if is_url(source):
                result = converter.convert_uri(
                    source, keep_data_uris=args.keep_data_uris
                )
            else:
                result = converter.convert(source, keep_data_uris=args.keep_data_uris)
        except Exception as exc:  # report and keep going with the rest of the batch
            print(f"FAILED  {source}: {type(exc).__name__}: {exc}", file=sys.stderr)
            failed += 1
            continue
        if args.stdout:
            print(f"<!-- {source} -->\n{result.markdown}\n")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(result.markdown, encoding="utf-8")
            print(f"OK      {source} -> {dest}", file=sys.stderr)
        converted += 1

    print(
        f"\nconverted={converted} skipped={skipped} failed={failed}",
        file=sys.stderr,
    )
    return 1 if failed and not converted else 0


if __name__ == "__main__":
    sys.exit(main())
