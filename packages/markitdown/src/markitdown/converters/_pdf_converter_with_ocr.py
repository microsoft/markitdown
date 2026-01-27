"""
Enhanced PDF Converter with OCR support for embedded images.
Extracts images from PDFs and performs OCR while maintaining document context.
"""

import sys
import io
from typing import BinaryIO, Any, Optional

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from ._ocr_service import MultiBackendOCRService, OCRResult

# Import dependencies
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    import pdfplumber
    from PIL import Image
    import fitz  # PyMuPDF for high-quality image extraction
except ImportError:
    _dependency_exc_info = sys.exc_info()


def _extract_images_from_page(page: Any) -> list[dict]:
    """
    Extract images from a PDF page with position information.

    Returns:
        List of dicts with 'stream', 'bbox', 'name' keys
    """
    images_info = []

    try:
        # Get images from page
        images = page.images

        for i, img_dict in enumerate(images):
            try:
                # Get image data
                x0, y0, x1, y1 = (
                    img_dict["x0"],
                    img_dict["top"],
                    img_dict["x1"],
                    img_dict["bottom"],
                )

                # Extract image from page
                # We need to crop the image from the page
                bbox = (x0, y0, x1, y1)

                # Get the image object
                # pdfplumber images don't directly give us the PIL image
                # We need to extract it differently

                # Try to get the image stream
                # This is a workaround - we'll extract using the page object
                try:
                    # Get the PDF page object
                    page_obj = page.page_obj

                    # Navigate to resources
                    if "/XObject" in page_obj["/Resources"]:
                        xobjects = page_obj["/Resources"]["/XObject"].get_object()

                        for obj_name in xobjects:
                            obj = xobjects[obj_name]

                            if obj["/Subtype"] == "/Image":
                                # Extract image data
                                size = (obj["/Width"], obj["/Height"])
                                data = obj.get_data()

                                # Create PIL Image
                                try:
                                    if "/ColorSpace" in obj:
                                        cs = obj["/ColorSpace"]
                                        if cs == "/DeviceRGB":
                                            mode = "RGB"
                                        elif cs == "/DeviceGray":
                                            mode = "L"
                                        else:
                                            mode = "RGB"
                                    else:
                                        mode = "RGB"

                                    img = Image.frombytes(mode, size, data)
                                    img_stream = io.BytesIO()
                                    img.save(img_stream, format="PNG")
                                    img_stream.seek(0)

                                    images_info.append(
                                        {
                                            "stream": img_stream,
                                            "bbox": bbox,
                                            "name": f"page_{page.page_number}_img_{i}",
                                            "y_pos": y0,  # For sorting
                                        }
                                    )
                                except Exception:
                                    # Try alternative extraction
                                    pass

                except Exception:
                    pass

            except Exception:
                continue

    except Exception:
        pass

    return images_info


def _extract_images_using_pymupdf(pdf_bytes: io.BytesIO, page_num: int) -> list[dict]:
    """
    Extract images using PyMuPDF for high-quality direct extraction.
    This extracts the actual embedded image data without rendering.

    Args:
        pdf_bytes: PDF file as BytesIO
        page_num: Page number (1-indexed)

    Returns:
        List of dicts with 'stream', 'bbox', 'name', 'y_pos' keys
    """
    images_info = []

    try:
        # Open PDF with PyMuPDF
        pdf_bytes.seek(0)
        doc = fitz.open(stream=pdf_bytes.read(), filetype="pdf")
        page = doc[page_num - 1]  # PyMuPDF uses 0-indexed pages

        # Get list of images
        image_list = page.get_images()

        for img_index, img_info in enumerate(image_list):
            try:
                xref = img_info[0]  # xref number

                # Extract the actual embedded image
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Load as PIL Image
                pil_img = Image.open(io.BytesIO(image_bytes))

                # Save to stream
                img_stream = io.BytesIO()
                pil_img.save(img_stream, format="PNG")
                img_stream.seek(0)

                # Get image position on page (for sorting)
                # Get image instances on this page
                img_rects = page.get_image_rects(xref)
                y_pos = img_rects[0].y0 if img_rects else 0

                images_info.append(
                    {
                        "stream": img_stream,
                        "bbox": (
                            0,
                            0,
                            pil_img.width,
                            pil_img.height,
                        ),  # Image dimensions
                        "name": f"page_{page_num}_img_{img_index}",
                        "y_pos": y_pos,
                    }
                )

            except Exception:
                continue

        doc.close()

    except Exception:
        pass

    return images_info


def _extract_images_using_pdfplumber(page: Any) -> list[dict]:
    """
    Alternative method to extract images using pdfplumber's to_image.
    NOTE: This method renders the page as a screenshot, which degrades quality.
    Use _extract_images_using_pymupdf() for better results.

    Returns:
        List of dicts with 'stream', 'bbox', 'name' keys
    """
    images_info = []

    try:
        # Get list of images from page
        images = page.images

        for i, img_dict in enumerate(images):
            try:
                x0 = img_dict.get("x0", 0)
                y0 = img_dict.get("top", 0)
                x1 = img_dict.get("x1", 0)
                y1 = img_dict.get("bottom", 0)

                # Check if dimensions are valid
                if x1 <= x0 or y1 <= y0:
                    continue

                # Render the page region as an image
                page_img = page.to_image(resolution=150)

                # Crop to the specific region
                cropped = page_img.original.crop((x0, y0, x1, y1))

                # Save to stream
                img_stream = io.BytesIO()
                cropped.save(img_stream, format="PNG")
                img_stream.seek(0)

                images_info.append(
                    {
                        "stream": img_stream,
                        "bbox": (x0, y0, x1, y1),
                        "name": f"page_{page.page_number}_img_{i}",
                        "y_pos": y0,
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
        ocr_service: Optional[MultiBackendOCRService] = kwargs.get("ocr_service")

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
                                    img_marker = f"\n\n[Image: {item['name']}]\n"
                                    img_marker += f"{item['ocr_text']}\n"
                                    if item.get("backend"):
                                        img_marker += f"(OCR: {item['backend']})\n"
                                    img_marker += "[End Image]\n"
                                    markdown_content.append(img_marker)
                        else:
                            # No images, just add text
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

        return DocumentConverterResult(markdown=markdown)

    def _extract_page_images(self, pdf_bytes: io.BytesIO, page_num: int) -> list[dict]:
        """
        Extract images from a PDF page using PyMuPDF for high quality.

        Args:
            pdf_bytes: PDF file as BytesIO
            page_num: Page number (1-indexed)

        Returns:
            List of image info dicts with 'stream', 'bbox', 'name', 'y_pos'
        """
        # Use PyMuPDF for high-quality direct image extraction
        images = _extract_images_using_pymupdf(pdf_bytes, page_num)

        # Sort by vertical position (top to bottom)
        images.sort(key=lambda x: x["y_pos"])

        return images
