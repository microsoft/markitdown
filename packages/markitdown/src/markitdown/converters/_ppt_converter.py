import sys
import os
import io
import tempfile
import subprocess
from typing import BinaryIO, Any

from ._pptx_converter import PptxConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, FileConversionException

# Check if libreoffice is available
_ppt_libreoffice_available = None


def _check_libreoffice_available():
    """Check if libreoffice is installed and available."""
    global _ppt_libreoffice_available
    if _ppt_libreoffice_available is not None:
        return _ppt_libreoffice_available

    try:
        # Try to run libreoffice --version to check if it's available
        result = subprocess.run(
            ["libreoffice", "--version"],
            capture_output=True,
            timeout=5,
        )
        _ppt_libreoffice_available = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        _ppt_libreoffice_available = False

    return _ppt_libreoffice_available


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.ms-powerpoint",
]

ACCEPTED_FILE_EXTENSIONS = [".ppt"]


class PptConverter(DocumentConverter):
    """
    Converts old PPT (Microsoft Office 97-2003 PowerPoint) files to Markdown.
    Uses libreoffice to convert PPT to PPTX, then uses PptxConverter for the conversion.
    Supports text, tables, images with alt text, and notes.
    """

    def __init__(self):
        super().__init__()
        self._pptx_converter = PptxConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        # Only accept .ppt files if libreoffice is available
        if not _check_libreoffice_available():
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
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check if libreoffice is available
        if not _check_libreoffice_available():
            raise MissingDependencyException(
                "libreoffice is required to convert .ppt files. "
                "Please install LibreOffice and ensure 'libreoffice' command is available in your PATH."
            )

        # Create a temporary directory for conversion
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the input file temporarily
            input_ppt_path = os.path.join(temp_dir, "input.ppt")
            with open(input_ppt_path, "wb") as f:
                f.write(file_stream.read())

            # Convert PPT to PPTX using libreoffice
            output_dir = os.path.join(temp_dir, "output")
            os.makedirs(output_dir, exist_ok=True)

            try:
                # Use libreoffice in headless mode to convert to PPTX
                subprocess.run(
                    [
                        "libreoffice",
                        "--headless",
                        "--convert-to",
                        "pptx",
                        "--outdir",
                        output_dir,
                        input_ppt_path,
                    ],
                    capture_output=True,
                    timeout=300,  # 5 minutes timeout
                    check=True,
                )
            except subprocess.TimeoutExpired:
                raise FileConversionException(
                    "Timeout: libreoffice conversion of .ppt to .pptx took too long"
                )
            except subprocess.CalledProcessError as e:
                raise FileConversionException(
                    f"Failed to convert .ppt to .pptx: {e.stderr.decode('utf-8', errors='ignore')}"
                )

            # Find the converted PPTX file
            output_pptx_path = os.path.join(output_dir, "input.pptx")
            if not os.path.exists(output_pptx_path):
                raise FileConversionException(
                    "Conversion produced no output file"
                )

            # Read the converted PPTX file
            with open(output_pptx_path, "rb") as f:
                pptx_stream = io.BytesIO(f.read())

            # Use PptxConverter to convert the PPTX file
            pptx_stream_info = StreamInfo(
                extension=".pptx",
                mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )

            return self._pptx_converter.convert(pptx_stream, pptx_stream_info, **kwargs)
