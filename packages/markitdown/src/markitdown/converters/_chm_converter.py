import io
import os
import tempfile
from typing import Any, BinaryIO, Optional

# This converter requires an optional CHM parsing library (e.g., 'pychm', 'chm-py').
# The converter will be disabled if the library is not installed.
try:
    import chm
except ImportError:
    chm = None

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._html_converter import HtmlConverter

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.ms-htmlhelp",
    "application/x-chm",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".chm",
]

class ChmConverter(DocumentConverter):
    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        """Checks for .chm extension or MIME type and if the CHM library is installed."""
        if chm is None:
            return False

        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        """Converts a CHM file to Markdown by processing its internal HTML files."""
        if chm is None:
            raise RuntimeError("CHM parsing library is not installed (e.g., 'pychm').")

        # Create a temporary file because some CHM readers require a file path.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".chm") as tmp_file:
            tmp_file.write(file_stream.read())
            tmp_path = tmp_file.name

        try:
            # This is the core logic that reuses the HtmlConverter.
            return self._process_chm_file(tmp_path, stream_info, **kwargs)
        finally:
            # Ensure the temporary file is always deleted.
            os.remove(tmp_path)

    def _process_chm_file(
        self, file_path: str, stream_info: StreamInfo, **kwargs: Any
    ) -> DocumentConverterResult:
        """Helper function to process the CHM file and convert its contents."""
        html_converter = HtmlConverter()
        markdown_parts = []
        doc_title = None

        chm_file = chm.CHMFile(file_path)

        # Get all file paths and sort them for consistent output.
        # The API for listing files might differ (e.g., chm_file.files).
        object_paths = sorted([path.decode(errors='ignore') for path in chm_file.get_objects()])

        for path in object_paths:
            if not path.lower().endswith((".html", ".htm")):
                continue

            try:
                # The API for reading files might differ (e.g., chm_file.read_file(path)).
                _chm_object_info, chm_object_data = chm_file.retrieve_object(path)

                # Decode the HTML content, trying utf-8 then a fallback.
                try:
                    html_content = chm_object_data.decode("utf-8")
                except UnicodeDecodeError:
                    html_content = chm_object_data.decode("cp1252", errors="ignore")

                if not html_content.strip():
                    continue

                # Construct a representative URL for the internal file.
                base_url = stream_info.url
                full_url = f"{base_url}!/{path.lstrip('/')}" if base_url else None

                # REUSE HtmlConverter instead of re-implementing logic.
                result = html_converter.convert_string(
                    html_content, url=full_url, **kwargs
                )

                if result.markdown:
                    markdown_parts.append(result.markdown)

                if doc_title is None and result.title:
                    doc_title = result.title

            except Exception:
                # Skip any individual files that fail to process.
                continue

        full_markdown = "\n\n---\n\n".join(markdown_parts)

        return DocumentConverterResult(
            markdown=full_markdown.strip(),
            title=doc_title,
        )

    def convert_bytes(
        self, chm_bytes: bytes, *, url: Optional[str] = None, **kwargs
    ) -> DocumentConverterResult:
        """Convenience method to convert CHM file bytes to markdown."""
        return self.convert(
            file_stream=io.BytesIO(chm_bytes),
            stream_info=StreamInfo(
                mimetype="application/vnd.ms-htmlhelp",
                extension=".chm",
                url=url,
            ),
            **kwargs,
        )
