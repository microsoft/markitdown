import sys
import os
import re
import base64
import hashlib
import unicodedata
from typing import BinaryIO, Any, Dict, List, Tuple
from io import BytesIO
import json
from bs4 import BeautifulSoup

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

ACCEPTED_FILE_EXTENSIONS = [".docx"]


class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown. Style information (e.g., headings) and tables are preserved where possible.
    Extracts images from documents and saves them to document-specific subfolders.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename by removing or replacing problematic characters.

        Args:
            filename: The original filename

        Returns:
            A sanitized filename safe for filesystem use
        """
        # Step 1: Normalize unicode characters
        filename = unicodedata.normalize("NFKD", filename)

        # Step 2: Remove invalid characters and replace spaces with underscores
        # Keep alphanumeric characters, underscores, hyphens, and periods
        sanitized = re.sub(r"[^\w\-\.]", "_", filename)

        # Step 3: Collapse multiple underscores
        sanitized = re.sub(r"_+", "_", sanitized)

        # Step 4: Remove leading/trailing underscores
        sanitized = sanitized.strip("_")

        # Step 5: Ensure we have a valid filename (default if empty)
        if not sanitized:
            sanitized = "unnamed"

        return sanitized

    def _get_document_name(self, stream_info: StreamInfo) -> str:
        """
        Extract document name from StreamInfo and sanitize it
        """
        # First try to extract from filename attribute
        if stream_info.filename:
            basename = os.path.basename(stream_info.filename)
            name, _ = os.path.splitext(basename)
            if name:
                return self._sanitize_filename(name)

        # If local_path exists, try to extract from local path
        if stream_info.local_path:
            basename = os.path.basename(stream_info.local_path)
            name, _ = os.path.splitext(basename)
            if name:
                return name

        # Default name
        return "docx_document"

    def _extract_and_save_images(
        self, html_content: str, doc_folder: str, assets_folder: str = "assets"
    ) -> str:
        """
        Extract base64 images from HTML content, save them to filesystem, and update HTML with new image paths

        Args:
            html_content: The HTML content containing images
            doc_folder: The document-specific folder name
            assets_folder: The base folder for assets

        Returns:
            Updated HTML content with image references pointing to saved files
        """
        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all images
        images = soup.find_all("img")
        if not images:
            return html_content

        # Create output directory
        output_dir = os.path.join(assets_folder, doc_folder)
        os.makedirs(output_dir, exist_ok=True)

        # Process each image
        for img in images:
            src = img.get("src", "") or img.get("data-src", "")
            if not src or not src.startswith("data:image"):
                continue

            try:
                # Parse image data
                mime_type = src.split(";")[0].replace("data:", "")

                # Get file extension
                ext = {
                    "image/png": ".png",
                    "image/jpeg": ".jpg",
                    "image/jpg": ".jpg",
                    "image/gif": ".gif",
                }.get(mime_type, ".png")

                # Extract base64 data
                encoded_data = src.split(",", 1)[1]
                image_data = base64.b64decode(encoded_data)

                # Generate unique filename
                hashname = hashlib.sha256(image_data).hexdigest()[:8]
                filename = f"image_{hashname}{ext}"

                # Save file
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(image_data)

                # Update image src in HTML
                new_src = os.path.join(output_dir, filename).replace("\\", "/")
                img["src"] = new_src

                # Add alt text if empty
                if not img.get("alt"):
                    img["alt"] = f"image_{hashname}"

            except Exception as e:
                continue

        # Return updated HTML
        return str(soup)

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".docx",
                    feature="docx",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        # Get document name
        doc_name = kwargs.get("conversion_name") or self._get_document_name(stream_info)
        if hasattr(self, "sanitize_filename"):
            doc_name = self.sanitize_filename(doc_name)

        # Get assets folder
        assets_folder = kwargs.get("image_output_dir", "assets")

        # Convert DOCX to HTML
        style_map = kwargs.get("style_map", None)
        pre_process_stream = pre_process_docx(file_stream)
        html_content = mammoth.convert_to_html(
            pre_process_stream, style_map=style_map
        ).value

        # Extract and save images, getting updated HTML with correct image references
        processed_html = self._extract_and_save_images(
            html_content, doc_name, assets_folder
        )

        # Create a new StreamInfo for the HTML converter
        html_stream_info = stream_info.copy_and_update(
            mimetype="text/html", extension=".html"
        )

        # Use the standard HTML converter to convert to Markdown
        # We don't need to pass conversion_name because images are already extracted
        html_kwargs = {k: v for k, v in kwargs.items() if k != "conversion_name"}

        return self._html_converter.convert(
            file_stream=BytesIO(processed_html.encode("utf-8")),
            stream_info=html_stream_info,
            **html_kwargs,
        )
