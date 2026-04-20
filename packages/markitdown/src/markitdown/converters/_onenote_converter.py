# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import sys
from typing import BinaryIO, Any
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

# Try loading the optional onenote dependency
_onenote_dependency_exc_info = None
try:
    from onenotepy import Notebook  # noqa: F401
except ImportError:
    _onenote_dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/onenote",
    "application/msonenote",
]
ACCEPTED_FILE_EXTENSIONS = [".one"]


class OneNoteConverter(DocumentConverter):
    """
    Converts Microsoft OneNote (.one) files to Markdown.

    Requires the optional dependency `onenotepy`:
        pip install onenotepy
    """

    def __init__(self):
        super().__init__()

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

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Raise an informative error if the dependency is missing
        if _onenote_dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter="OneNoteConverter",
                    extension=".one",
                    feature="onenote",
                    install_command="pip install onenotepy",
                )
            ) from _onenote_dependency_exc_info[1].with_traceback(
                _onenote_dependency_exc_info[2]
            )

        from onenotepy import Notebook

        # Write stream to a temp file because onenotepy needs a file path
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(
            suffix=".one", delete=False
        ) as tmp:
            tmp.write(file_stream.read())
            tmp_path = tmp.name

        try:
            notebook = Notebook(tmp_path)
            md_parts = []

            for section in notebook.sections:
                md_parts.append(f"## {section.name}")
                for page in section.pages:
                    md_parts.append(f"### {page.title}")
                    # Extract plain text content from page
                    content = page.get_content()
                    if content:
                        md_parts.append(content.strip())

            markdown = "\n\n".join(md_parts)
        finally:
            os.unlink(tmp_path)

        return DocumentConverterResult(markdown=markdown)
