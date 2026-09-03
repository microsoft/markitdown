"""
Enhanced PDF Converter with OCR support for embedded images.
Extracts images from PDFs and performs OCR while maintaining document context.
"""

import io
import sys
from typing import Any, BinaryIO, Optional

from markitdown import DocumentConverter, DocumentConverterResult, StreamInfo
from markitdown._exceptions import (
    MissingDependencyException,
    MISSING_DEPENDENCY_MESSAGE,
)
from ._ocr_service import LLMVisionOCRService

# Import dependencies
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    import pdfplumber
    from PIL import Image
except ImportError:
    _dependency_exc_info = sys.exc_info()


def _extract_images_from_page(page: Any) -> list[dict]:
    """
    Extract images from a PDF page by rendering page regions.

    Returns:
        List of dicts with 'stream', 'bbox', 'name', 'y_pos' keys
    """
    images_info = []

    try:
        # Try multiple methods to detect images
        images = []

        # Method 1: Use page.images (standard approach)
        if hasattr(page, "images") and page.images:
            images = page.images

        # Method 2: If no images found, try underlying PDF objects
        if not images and hasattr(page, "objects") and "image" in page.objects:
            images = page.objects.get("image", [])

        # Method 3: Try filtering all objects for image types
        if not images and hasattr(page, "objects"):
            all_objs = page.objects
            for obj_type in all_objs.keys():
                if "image" in obj_type.lower() or "xobject" in obj_type.lower():
                    potential_imgs = all_objs.get(obj_type, [])
                    if potential_imgs:
                        images = potential_imgs
                        break

        for i, img_dict in enumerate(images):
            try:
                # Try to get the actual image stream from the PDF
                img_stream = None
                y_pos = 0

                # Method A: If img_dict has 'stream' key, use it directly
                if "stream" in img_dict and hasattr(img_dict["stream"], "get_data"):
                    try:
                        img_bytes = img_dict["stream"].get_data()

                        # Try to open as PIL Image to validate/decode
                        pil_img = Image.open(io.BytesIO(img_bytes))

                        # Convert to RGB if needed (handle CMYK, etc.)
                        if pil_img.mode not in ("RGB", "L"):
                            pil_img = pil_img.convert("RGB")

                        # Save to stream as PNG
                        img_stream = io.BytesIO()
                        pil_img.save(img_stream, format="PNG")
                        img_stream.seek(0)

                        y_pos = img_dict.get("top", 0)
                    except Exception:
                        pass

                # Method B: Fallback to rendering page region
                if img_stream is None:
                    x0 = img_dict.get("x0", 0)
                    y0 = img_dict.get("top", 0)
                    x1 = img_dict.get("x1", 0)
                    y1 = img_dict.get("bottom", 0)
                    y_pos = y0

                    # Check if dimensions are valid
                    if x1 <= x0 or y1 <= y0:
                        continue

                    # Use pdfplumber's within_bbox to crop, then render
                    # This preserves coordinate system correctly
                    bbox = (x0, y0, x1, y1)
                    cropped_page = page.within_bbox(bbox)

                    # Render at 150 DPI (balance between quality and size)
                    page_img = cropped_page.to_image(resolution=150)

                    # Save to stream
                    img_stream = io.BytesIO()
                    page_img.original.save(img_stream, format="PNG")
                    img_stream.seek(0)

                if img_stream:
                    images_info.append(
                        {
                            "stream": img_stream,
                            "name": f"page_{page.page_number}_img_{i}",
                            "y_pos": y_pos,
                        }
                    )

            except Exception:
                continue

    except Exception:
        pass

    return images_info


def _extract_text_lines_from_page(page: Any) -> list[dict]:
    """
    Extract text lines with Y positions from a PDF page.

    Uses pdfplumber char-level data to group characters into lines
    based on their vertical position.

    Args:
        page: pdfplumber page object

    Returns:
        List of dicts with 'y' (float) and 'text' (str) keys, sorted top-to-bottom
    """
    chars = page.chars
    if not chars:
        # Fallback: use simple text extraction
        text_content = page.extract_text() or ""
        return [
            {"y": i * 10, "text": line}
            for i, line in enumerate(text_content.split("\n"))
        ]

    lines_with_y: list[dict] = []
    current_line: list[Any] = []
    current_y: float | None = None

    for char in sorted(chars, key=lambda c: (c["top"], c["x0"])):
        y = char["top"]
        if current_y is None:
            current_y = y
        elif abs(y - current_y) > 2:  # New line threshold
            if current_line:
                text = "".join([c["text"] for c in current_line])
                lines_with_y.append({"y": current_y, "text": text.strip()})
            current_line = []
            current_y = y
        current_line.append(char)

    # Add last line
    if current_line:
        text = "".join([c["text"] for c in current_line])
        lines_with_y.append({"y": current_y or 0, "text": text.strip()})

    return lines_with_y


class PdfConverterWithOCR(DocumentConverter):
    """
    Enhanced PDF Converter with OCR support for embedded images.
    Maintains document structure while extracting text from images inline.
    """

    def __init__(self, ocr_service: Optional[LLMVisionOCRService] = None):
        super().__init__()
        self.ocr_service = ocr_service

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension == ".pdf":
            return True

        if mimetype.startswith("application/pdf") or mimetype.startswith(
            "application/x-pdf"
        ):
            return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]

        # Get OCR service if available (from kwargs or instance)
        ocr_service: LLMVisionOCRService | None = (
            kwargs.get("ocr_service") or self.ocr_service
        )

        # Read PDF into BytesIO
        file_stream.seek(0)
        pdf_bytes = io.BytesIO(file_stream.read())

        markdown_content: list[str] = []

        try:
            with pdfplumber.open(pdf_bytes) as pdf:
                if ocr_service:
                    # ── Phase 1: Collect all images from all pages ──
                    # all_images: (image_stream, y_pos, page_num, img_name)
                    all_images: list[tuple[BinaryIO, float, int, str]] = []
                    # page_text_lines: page_num -> list of {y, text} dicts
                    page_text_lines: dict[int, list[dict]] = {}

                    for page_num, page in enumerate(pdf.pages, 1):
                        page_text_lines[page_num] = _extract_text_lines_from_page(page)
                        for img_info in _extract_images_from_page(page):
                            all_images.append(
                                (
                                    img_info["stream"],
                                    img_info["y_pos"],
                                    page_num,
                                    img_info["name"],
                                )
                            )

                    # ── Phase 2: Batch OCR all images in parallel ──
                    ocr_by_page: dict[int, list[tuple[float, str]]] = {}
                    if all_images:
                        ocr_results = ocr_service.extract_text_batch(
                            [(stream, None) for stream, _, _, _ in all_images]
                        )
                        for i, (_, y_pos, pg, name) in enumerate(all_images):
                            text = ocr_results[i].text.strip()
                            if text:
                                ocr_by_page.setdefault(pg, []).append((y_pos, text))

                    # ── Phase 3: Build output per page (interleave text + OCR) ──
                    for page_num, page in enumerate(pdf.pages, 1):
                        markdown_content.append(f"\n## Page {page_num}\n")

                        page_ocr = ocr_by_page.get(page_num, [])

                        if page_ocr:
                            # Build items: text lines + OCR blocks
                            content_items: list[dict] = [
                                {"y_pos": item["y"], "text": item["text"], "type": "text"}
                                for item in page_text_lines[page_num]
                                if item["text"]
                            ]
                            for y_pos, ocr_text in page_ocr:
                                content_items.append(
                                    {
                                        "y_pos": y_pos,
                                        "ocr_text": ocr_text,
                                        "type": "image",
                                    }
                                )

                            # Sort all items by Y position (top to bottom)
                            content_items.sort(key=lambda x: x["y_pos"])

                            for item in content_items:
                                if item["type"] == "text":
                                    markdown_content.append(item["text"])
                                else:
                                    markdown_content.append(
                                        f"\n\n*[Image OCR]\n{item['ocr_text']}\n[End OCR]*\n"
                                    )
                        else:
                            # No images on this page — just extract text
                            text_content = page.extract_text() or ""
                            if text_content.strip():
                                markdown_content.append(text_content.strip())
                else:
                    # No OCR — simple text extraction
                    for page_num, page in enumerate(pdf.pages, 1):
                        markdown_content.append(f"\n## Page {page_num}\n")
                        text_content = page.extract_text() or ""
                        if text_content.strip():
                            markdown_content.append(text_content.strip())

                # Build final markdown
                markdown = "\n\n".join(markdown_content).strip()

                # Fallback to pdfminer if empty
                if not markdown:
                    pdf_bytes.seek(0)
                    markdown = pdfminer.high_level.extract_text(pdf_bytes)

        except Exception:
            # Fallback to pdfminer
            try:
                pdf_bytes.seek(0)
                markdown = pdfminer.high_level.extract_text(pdf_bytes)
            except Exception:
                markdown = ""

        # Final fallback: If output is empty or contains only page-number
        # headers (scanned PDF with no extractable text), use full-page OCR.
        if ocr_service:
            # Strip out page-header boilerplate to test for real content
            import re as _re  # local import — only used here

            _real_content = _re.sub(
                r"\s*## Page \d+\s*", "", markdown
            ).strip()
            if not _real_content:
                pdf_bytes.seek(0)
                ocr_dpi = kwargs.get("ocr_dpi", 300)
                markdown = self._ocr_full_pages(pdf_bytes, ocr_service, ocr_dpi=ocr_dpi)

        return DocumentConverterResult(markdown=markdown)

    def _ocr_full_pages(
        self, pdf_bytes: io.BytesIO, ocr_service: LLMVisionOCRService,
        ocr_dpi: int = 300,
    ) -> str:
        """
        Fallback for scanned PDFs: render pages to images and OCR them.

        Uses a streaming pipeline: each page is submitted for OCR the moment
        its render finishes. Rendering and OCR run concurrently, so total
        time ≈ max(render_all, ocr_all) instead of render_all + ocr_all.
        """
        from concurrent.futures import ThreadPoolExecutor as _TPE, as_completed as _ac
        from ._ocr_service import OCRResult

        markdown_parts: list[str] = []
        ocr_results: dict[int, str] = {}  # page_num -> text

        try:
            pdf_bytes.seek(0)
            with pdfplumber.open(pdf_bytes) as pdf:
                n_pages = len(pdf.pages)
                if n_pages == 0:
                    return ""

                # ── Single-page fast path (no thread overhead) ──
                if n_pages == 1:
                    try:
                        pg = pdf.pages[0]
                        pg_img = pg.to_image(resolution=ocr_dpi)
                        buf = io.BytesIO()
                        pg_img.original.save(buf, format="PNG")
                        buf.seek(0)
                        result = ocr_service.extract_text(buf)
                        if result.text.strip():
                            ocr_results[1] = result.text.strip()
                    except Exception:
                        pass
                else:
                    # ── Multi-page streaming pipeline ──
                    render_workers = min(4, n_pages)
                    ocr_workers = ocr_service.max_workers

                    def _render_page(pg_num: int) -> tuple[int, BinaryIO | None]:
                        try:
                            pg = pdf.pages[pg_num - 1]
                            pg_img = pg.to_image(resolution=ocr_dpi)
                            buf = io.BytesIO()
                            pg_img.original.save(buf, format="PNG")
                            buf.seek(0)
                            return pg_num, buf
                        except Exception:
                            return pg_num, None

                    def _ocr_one(img_stream: BinaryIO) -> OCRResult:
                        try:
                            return ocr_service.extract_text(img_stream)
                        except Exception as e:
                            return OCRResult(text="", error=str(e))

                    with _TPE(max_workers=render_workers) as render_pool:
                        ocr_futures: dict = {}
                        render_futures = {
                            render_pool.submit(_render_page, i): i
                            for i in range(1, n_pages + 1)
                        }
                        with _TPE(max_workers=ocr_workers) as ocr_pool:
                            for render_future in _ac(render_futures):
                                pg_num, buf = render_future.result()
                                if buf is not None:
                                    ocr_futures[
                                        ocr_pool.submit(_ocr_one, buf)
                                    ] = pg_num
                            for ocr_future in _ac(ocr_futures):
                                pg_num = ocr_futures[ocr_future]
                                result = ocr_future.result()
                                if result.text.strip():
                                    ocr_results[pg_num] = result.text.strip()

            # ── Assemble output in page order ──
            for pg_num in sorted(ocr_results):
                markdown_parts.append(f"\n## Page {pg_num}\n")
                markdown_parts.append(
                    f"*[Image OCR]\n{ocr_results[pg_num]}\n[End OCR]*"
                )
            # Pages that failed to produce text
            for pg_num in range(1, n_pages + 1):
                if pg_num not in ocr_results:
                    markdown_parts.append(f"\n## Page {pg_num}\n")
                    markdown_parts.append(
                        "*[No text could be extracted from this page]*"
                    )

        except Exception:
            # pdfplumber failed — try PyMuPDF with same streaming pipeline
            markdown_parts = []
            ocr_results = {}
            try:
                import fitz  # PyMuPDF

                pdf_bytes.seek(0)
                doc = fitz.open(stream=pdf_bytes.read(), filetype="pdf")
                n_pages = doc.page_count
                if n_pages == 0:
                    doc.close()
                    return ""

                # ── Single-page fast path ──
                if n_pages == 1:
                    try:
                        pg = doc[0]
                        mat = fitz.Matrix(ocr_dpi / 72, ocr_dpi / 72)
                        pix = pg.get_pixmap(matrix=mat)
                        buf = io.BytesIO(pix.tobytes("png"))
                        buf.seek(0)
                        result = ocr_service.extract_text(buf)
                        if result.text.strip():
                            ocr_results[1] = result.text.strip()
                    except Exception:
                        pass
                else:
                    # ── Multi-page streaming pipeline ──
                    render_workers = min(4, n_pages)
                    ocr_workers = ocr_service.max_workers

                    def _render_mupdf(pg_num: int) -> tuple[int, BinaryIO | None]:
                        try:
                            pg = doc[pg_num - 1]
                            mat = fitz.Matrix(ocr_dpi / 72, ocr_dpi / 72)
                            pix = pg.get_pixmap(matrix=mat)
                            buf = io.BytesIO(pix.tobytes("png"))
                            buf.seek(0)
                            return pg_num, buf
                        except Exception:
                            return pg_num, None

                    def _ocr_one_mupdf(img_stream: BinaryIO) -> OCRResult:
                        try:
                            return ocr_service.extract_text(img_stream)
                        except Exception as e:
                            return OCRResult(text="", error=str(e))

                    with _TPE(max_workers=render_workers) as render_pool:
                        ocr_futures = {}
                        render_futures = {
                            render_pool.submit(_render_mupdf, i): i
                            for i in range(1, n_pages + 1)
                        }
                        with _TPE(max_workers=ocr_workers) as ocr_pool:
                            for render_future in _ac(render_futures):
                                pg_num, buf = render_future.result()
                                if buf is not None:
                                    ocr_futures[
                                        ocr_pool.submit(_ocr_one_mupdf, buf)
                                    ] = pg_num
                            for ocr_future in _ac(ocr_futures):
                                pg_num = ocr_futures[ocr_future]
                                result = ocr_future.result()
                                if result.text.strip():
                                    ocr_results[pg_num] = result.text.strip()
                doc.close()

                for pg_num in sorted(ocr_results):
                    markdown_parts.append(f"\n## Page {pg_num}\n")
                    markdown_parts.append(
                        f"*[Image OCR]\n{ocr_results[pg_num]}\n[End OCR]*"
                    )
                for pg_num in range(1, n_pages + 1):
                    if pg_num not in ocr_results:
                        markdown_parts.append(f"\n## Page {pg_num}\n")
                        markdown_parts.append(
                            "*[No text could be extracted from this page]*"
                        )

            except Exception:
                return "*[Error: Could not process scanned PDF]*"

        return "\n\n".join(markdown_parts).strip()
