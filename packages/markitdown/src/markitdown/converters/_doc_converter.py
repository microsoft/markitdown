# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

import sys
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import unword
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/msword",
    "application/vnd.ms-word",
]

ACCEPTED_FILE_EXTENSIONS = [".doc"]


class DocConverter(DocumentConverter):
    """
    Converts legacy DOC files (OLE/CFB format) to Markdown using the unword library.
    No external dependencies such as LibreOffice or MS Word are required.
    """

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
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".doc",
                    feature="doc",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        data = file_stream.read()
        doc = unword.parse_doc(data)

        # Combine body text and textbox content
        markdown_parts = []
        if doc.body_text:
            markdown_parts.append(doc.body_text.strip())

        if doc.textboxes:
            for textbox in doc.textboxes:
                text = textbox.strip()
                if text:
                    markdown_parts.append(text)

        markdown = "\n\n".join(markdown_parts)

        return DocumentConverterResult(markdown=markdown)
