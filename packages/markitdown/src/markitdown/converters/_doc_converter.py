import sys
import subprocess
import tempfile
import os
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
    "application/vnd.ms-word",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]

_TOOLS = ["antiword", "catdoc"]


def _get_available_tool() -> str | None:
    """Return the first available command-line tool for .doc conversion."""
    for tool in _TOOLS:
        try:
            subprocess.run(
                [tool, "--help"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
            return tool
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


class DocConverter(DocumentConverter):
    """
    Converts legacy .doc (Word 97-2003) files to Markdown plain text.

    Requires one of the following system tools to be installed:
      - antiword  (https://www.winfield.demon.nl/)
      - catdoc    (https://www.wagner.pp.ru/~vitus/software/catdoc/)

    On macOS: ``brew install antiword`` or ``brew install catdoc``
    On Ubuntu/Debian: ``apt install antiword`` or ``apt install catdoc``
    """

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
        tool = _get_available_tool()
        if tool is None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc",
                )
                + "\n\nInstall antiword or catdoc:\n"
                "  macOS:          brew install antiword\n"
                "  Ubuntu/Debian:  apt install antiword"
            )

        # Write the stream to a temporary file (antiword/catdoc require a path)
        suffix = stream_info.extension or ".doc"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_stream.read())
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                [tool, tmp_path],
                capture_output=True,
                text=True,
                timeout=30,
            )
            text = result.stdout.strip()
            if not text and result.returncode != 0:
                raise ValueError(
                    f"{tool} failed (exit {result.returncode}): {result.stderr.strip()}"
                )
        finally:
            os.unlink(tmp_path)

        return DocumentConverterResult(markdown=text or "")
