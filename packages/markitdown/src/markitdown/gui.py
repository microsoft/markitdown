from __future__ import annotations

from pathlib import Path
from typing import Protocol

from ._base_converter import DocumentConverterResult
from ._markitdown import MarkItDown


class Converter(Protocol):
    def convert(self, path: Path) -> DocumentConverterResult:
        ...


def convert_file_to_markdown(
    input_path: str | Path,
    output_path: str | Path,
    *,
    converter: Converter | None = None,
) -> None:
    source = Path(input_path) if input_path else None
    destination = Path(output_path) if output_path else None

    if source is None or not source.exists():
        raise ValueError("Input file does not exist.")
    if not source.is_file():
        raise ValueError("Input path is not a file.")
    if destination is None:
        raise ValueError("Output path is required.")
    if not destination.parent.exists():
        raise ValueError("Output directory does not exist.")

    active_converter = converter or MarkItDown(enable_plugins=False)
    result = active_converter.convert(source)
    destination.write_text(result.markdown, encoding="utf-8")
