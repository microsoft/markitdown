import subprocess
import io
import os
import tempfile
from typing import BinaryIO, Any, Optional

from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE


# Track antiword availability at import time
_antiword_available = False
try:
    subprocess.run(["antiword", "--help"], capture_output=True, timeout=5)
    _antiword_available = True
except (FileNotFoundError, subprocess.TimeoutExpired):
    _antiword_available = False


ACCEPTED_DOC_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocumentConverter):
    """
    Converts DOC files to Markdown using antiword.

    Antiword is a command-line tool that converts Microsoft Word .doc files
    to plain text. The output is then wrapped in simple HTML and converted
    to Markdown using the existing HTML converter.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: Any,
        **kwargs: Any,
    ) -> bool:
        extension = (stream_info.extension or "").lower()
        if extension in ACCEPTED_DOC_FILE_EXTENSIONS:
            return True
        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: Any,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Check dependencies
        if not _antiword_available:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc",
                )
            )

        # Save current position
        cur_pos = file_stream.tell()

        try:
            file_stream.seek(0)
            doc_data = file_stream.read()

            # Write to temp file and run antiword
            with tempfile.NamedTemporaryFile(suffix=".doc", delete=False) as tmp:
                tmp.write(doc_data)
                tmp_path = tmp.name

            try:
                result = subprocess.run(
                    ["antiword", tmp_path],
                    capture_output=True,
                    timeout=30,
                )
                if result.returncode == 0 and result.stdout:
                    text = result.stdout.decode("utf-8", errors="replace")
                else:
                    text = ""
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

            # Convert the text to markdown
            # Wrap in simple HTML paragraphs
            paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
            if paragraphs:
                html_parts = ["<p>" + "</p><p>".join(paragraphs) + "</p>"]
                html = "".join(html_parts)
            else:
                html = "<p></p>"

            markdown = self._html_converter.convert_string(html, **kwargs).markdown

            return DocumentConverterResult(markdown=markdown.strip())

        except Exception:
            raise
        finally:
            try:
                file_stream.seek(cur_pos)
            except Exception:
                pass


_doc_converter_instance = DocConverter()

