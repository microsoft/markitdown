"""
Enhanced PDF Converter with OCR support for embedded images.
Extracts images from PDFs and performs OCR while maintaining document context.
"""

import io
import sys
from typing import Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MISSING_DEPENDENCY_MESSAGE, MissingDependencyException
from .._stream_info import StreamInfo
from ._ocr_service import MultiBackendOCRService

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


class PdfConverterWithOCR(DocumentConverter):
    """
    Enhanced PDF Converter with OCR support for embedded images.
    Maintains document structure while extracting text from images inline.
    """

    def __init__(self):
        super().__init__()

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

        # Get OCR service if available
        ocr_service: MultiBackendOCRService | None = kwargs.get("ocr_service")

        # Read PDF into BytesIO
        file_stream.seek(0)
        pdf_bytes = io.BytesIO(file_stream.read())

        markdown_content = []

        try:
            with pdfplumber.open(pdf_bytes) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    markdown_content.append(f"\n## Page {page_num}\n")

                    # If OCR is enabled, interleave text and images by position
                    if ocr_service:
                        images_on_page = self._extract_page_images(pdf_bytes, page_num)

                        if images_on_page:
                            # Extract text lines with Y positions
                            chars = page.chars
                            if chars:
                                # Group chars into lines based on Y position
                                lines_with_y = []
                                current_line = []
                                current_y = None

                                for char in sorted(
                                    chars, key=lambda c: (c["top"], c["x0"])
                                ):
                                    y = char["top"]
                                    if current_y is None:
                                        current_y = y
                                    elif abs(y - current_y) > 2:  # New line threshold
                                        if current_line:
                                            text = "".join(
                                                [c["text"] for c in current_line]
                                            )
                                            lines_with_y.append(
                                                {"y": current_y, "text": text.strip()}
                                            )
                                        current_line = []
                                        current_y = y
                                    current_line.append(char)

                                # Add last line
                                if current_line:
                                    text = "".join([c["text"] for c in current_line])
                                    lines_with_y.append(
                                        {"y": current_y, "text": text.strip()}
                                    )
                            else:
                                # Fallback: use simple text extraction
                                text_content = page.extract_text() or ""
                                lines_with_y = [
                                    {"y": i * 10, "text": line}
                                    for i, line in enumerate(text_content.split("\n"))
                                ]

                            # OCR all images
                            image_data = []
                            for img_info in images_on_page:
                                ocr_result = ocr_service.extract_text(
                                    img_info["stream"]
                                )
                                if ocr_result.text.strip():
                                    image_data.append(
                                        {
                                            "y_pos": img_info["y_pos"],
                                            "name": img_info["name"],
                                            "ocr_text": ocr_result.text,
                                            "backend": ocr_result.backend_used,
                                            "type": "image",
                                        }
                                    )

                            # Add text items
                            content_items = [
                                {
                                    "y_pos": item["y"],
                                    "text": item["text"],
                                    "type": "text",
                                }
                                for item in lines_with_y
                                if item["text"]
                            ]
                            content_items.extend(image_data)

                            # Sort all items by Y position (top to bottom)
                            content_items.sort(key=lambda x: x["y_pos"])

                            # Build markdown by interleaving text and images
                            for item in content_items:
                                if item["type"] == "text":
                                    markdown_content.append(item["text"])
                                else:  # image
                                    # Use consistent OCR format
                                    img_marker = f"\n\n[Image OCR: {item['name']}]\n"
                                    img_marker += f"{item['ocr_text']}\n"
                                    img_marker += "[End Image OCR]\n"
                                    markdown_content.append(img_marker)
                        else:
                            # No images detected - just extract regular text
                            text_content = page.extract_text() or ""
                            if text_content.strip():
                                markdown_content.append(text_content.strip())
                    else:
                        # No OCR, just extract text
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
            pdf_bytes.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Final fallback: If still empty/whitespace and OCR is available,
        # treat as scanned PDF and OCR full pages
        if ocr_service and (not markdown or not markdown.strip()):
            pdf_bytes.seek(0)
            markdown = self._ocr_full_pages(pdf_bytes, ocr_service)

        return DocumentConverterResult(markdown=markdown)

    def _extract_page_images(self, pdf_bytes: io.BytesIO, page_num: int) -> list[dict]:
        """
        Extract images from a PDF page using pdfplumber.

        Args:
            pdf_bytes: PDF file as BytesIO
            page_num: Page number (1-indexed)

        Returns:
            List of image info dicts with 'stream', 'bbox', 'name', 'y_pos'
        """
        images = []

        try:
            pdf_bytes.seek(0)
            with pdfplumber.open(pdf_bytes) as pdf:
                if page_num <= len(pdf.pages):
                    page = pdf.pages[page_num - 1]  # 0-indexed
                    images = _extract_images_from_page(page)
        except Exception:
            pass

        # Sort by vertical position (top to bottom)
        images.sort(key=lambda x: x["y_pos"])

        return images

    def _ocr_full_pages(
        self, pdf_bytes: io.BytesIO, ocr_service: MultiBackendOCRService
    ) -> str:
        """
        Fallback for scanned PDFs: Convert entire pages to images and OCR them.
        Used when text extraction returns empty/whitespace results.

        Args:
            pdf_bytes: PDF file as BytesIO
            ocr_service: OCR service to use

        Returns:
            Markdown text extracted from OCR of full pages
        """
        markdown_parts = []

        try:
            pdf_bytes.seek(0)
            with pdfplumber.open(pdf_bytes) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        markdown_parts.append(f"\n## Page {page_num}\n")

                        # Render page to image at high resolution for better OCR
                        page_img = page.to_image(resolution=300)
                        img_stream = io.BytesIO()
                        page_img.original.save(img_stream, format="PNG")
                        img_stream.seek(0)

                        # Run OCR on the full page image
                        ocr_result = ocr_service.extract_text(img_stream)

                        if ocr_result.text.strip():
                            # Use consistent OCR format for scanned pages
                            markdown_parts.append(
                                f"[Image OCR: page_{page_num}_fullpage]\n"
                            )
                            markdown_parts.append(ocr_result.text.strip())
                            markdown_parts.append("\n[End Image OCR]\n")
                        else:
                            markdown_parts.append(
                                "*[No text could be extracted from this page]*"
                            )

                    except Exception as e:
                        markdown_parts.append(
                            f"*[Error processing page {page_num}: {str(e)}]*"
                        )
                        continue

        except Exception:
            return "*[Error: Could not process scanned PDF]*"

        return "\n\n".join(markdown_parts).strip()
