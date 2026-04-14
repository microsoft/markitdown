import subprocess
import sys
import tempfile
import io

from typing import BinaryIO, Any
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


def _check_antiword() -> None:
    """Check if antiword is available on the system."""
    try:
        subprocess.run(
            ["antiword"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except FileNotFoundError:
        msg = (
            f"DOCConverter recognized the input as a potential .doc file, "
            "but the 'antiword' tool is not installed. "
            "On Debian/Ubuntu, install it with: sudo apt install antiword"
        )
        raise MissingDependencyException(msg)
    except subprocess.CalledProcessError as e:
        msg = (
            f"DOCConverter recognized the input as a potential .doc file, "
            "but the 'antiword' tool is not installed. "
            "On Debian/Ubuntu, install it with: sudo apt install antiword"
        )
        raise MissingDependencyException(msg) from e


class DocConverter(DocumentConverter):
    """
    Converts legacy DOC files (not DOCX) to Markdown using antiword.
    DOC is the older binary format that was used before Office Open XML (DOCX).
    """

    def __init__(self):
        super().__init__()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        mimetype = (stream_info.mimetype or "").lower()
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
        # Check if antiword is available
        _check_antiword()

        # Write stream to temp file
        with tempfile.NamedTemporaryFile(suffix=".doc", delete=False) as tmp:
            tmp.write(file_stream.read())
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                ["antiword", "-w", "0", tmp_path],
                capture_output=True,
                text=True,
                check=True,
            )
            text_content = result.stdout
        except subprocess.CalledProcessError as e:
            text_content = e.stdout if e.stdout else ""
            text_content += f"\n\n[Warning: Conversion had errors: {e.stderr}]"

        return DocumentConverterResult(markdown=text_content)