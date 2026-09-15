from __future__ import annotations

import argparse
import io
from pathlib import Path

from PIL import Image

from markitdown import MarkItDown, StreamInfo
from markitdown_paddleocr import PaddleOCRService, PdfConverterWithPaddleOCR


def _image_to_pdf_bytes(path: Path) -> bytes:
    image = Image.open(path).convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, "PDF", resolution=150.0)
    return buffer.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare current MarkItDown output with PaddleOCR fallback output."
    )
    parser.add_argument("path", help="Path to an image or scanned PDF sample")
    parser.add_argument("--lang", default="ch", help="PaddleOCR language code")
    args = parser.parse_args()

    source_path = Path(args.path)
    if not source_path.exists():
        raise SystemExit(f"File not found: {source_path}")

    md = MarkItDown()
    baseline = md.convert(str(source_path)).markdown.strip()

    ocr_service = PaddleOCRService(
        lang=args.lang,
        paddleocr_kwargs={
            "use_doc_orientation_classify": False,
            "use_doc_unwarping": False,
            "use_textline_orientation": False,
        },
    )
    converter = PdfConverterWithPaddleOCR(ocr_service=ocr_service)

    if source_path.suffix.lower() == ".pdf":
        pdf_bytes = source_path.read_bytes()
    else:
        pdf_bytes = _image_to_pdf_bytes(source_path)

    plugin_result = converter.convert(
        io.BytesIO(pdf_bytes),
        StreamInfo(extension=".pdf"),
    ).markdown.strip()

    print(f"Sample: {source_path.name}")
    print(f"Baseline length: {len(baseline)}")
    print(f"PaddleOCR length: {len(plugin_result)}")
    print("\n--- Baseline ---\n")
    print(baseline[:1200] or "<empty>")
    print("\n--- PaddleOCR Fallback ---\n")
    print(plugin_result[:2400] or "<empty>")


if __name__ == "__main__":
    main()
