"""
Converts legacy .doc (Word 97-2003) files to Markdown.
Uses antiword or textract as the underlying conversion engine.
"""

import sys
import subprocess
import shutil
from typing import BinaryIO, Any

from ._plain_text_converter import PlainTextConverter
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional dependencies
_dependency_exc_info = None
try:
    import textract
except ImportError:
    textract = None

ACCEPTED_FILE_EXTENSIONS = [".doc"]
ACCEPTED_MIME_TYPES = [
    "application/msword",
    "application/x-msword",
]


class DocConverter(PlainTextConverter):
    """
    Converts legacy .doc (Word 97-2003) files to Markdown.
    Requires either 'antiword' system command or 'textract' Python package.
    """

    def __init__(self):
        super().__init__()
        self._has_antiword = shutil.which("antiword") is not None
        self._has_textract = textract is not None

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        if mimetype in ACCEPTED_MIME_TYPES:
            return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Check for available conversion methods
        if not self._has_antiword and not self._has_textract:
            raise MissingDependencyException(
                "The DocConverter requires either 'antiword' system command "
                "or 'textract' Python package to convert .doc files. "
                "Install with: pip install textract "
                "Or install antiword: apt-get install antiword (Debian/Ubuntu) "
                "or brew install antiword (macOS)"
            )

        # Read file content
        file_stream.seek(0)
        content = file_stream.read()

        # Try textract first (pure Python, more portable)
        if self._has_textract:
            try:
                import tempfile
                import os

                # Write to temp file since textract needs a file path
                with tempfile.NamedTemporaryFile(
                    suffix=".doc", delete=False
                ) as tmp_file:
                    tmp_file.write(content)
                    tmp_path = tmp_file.name

                try:
                    text = textract.process(tmp_path).decode("utf-8")
                    return DocumentConverterResult(markdown=text)
                finally:
                    os.unlink(tmp_path)
            except Exception:
                # Fall back to antiword if textract fails
                pass

        # Try antiword as fallback
        if self._has_antiword:
            try:
                import tempfile
                import os

                with tempfile.NamedTemporaryFile(
                    suffix=".doc", delete=False
                ) as tmp_file:
                    tmp_file.write(content)
                    tmp_path = tmp_file.name

                try:
                    result = subprocess.run(
                        ["antiword", tmp_path],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    return DocumentConverterResult(markdown=result.stdout)
                finally:
                    os.unlink(tmp_path)
            except subprocess.CalledProcessError as e:
                raise MissingDependencyException(
                    f"antiword failed to convert .doc file: {e.stderr}"
                )

        # Should not reach here, but just in case
        raise MissingDependencyException(
            "No available method to convert .doc files. "
            "Please install textract: pip install textract"
        )
