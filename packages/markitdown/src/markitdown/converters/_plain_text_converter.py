import mimetypes

from charset_normalizer import from_path
from typing import Any, Union

from ._base import DocumentConverter, DocumentConverterResult


# Mimetypes to ignore (commonly confused extensions)
IGNORE_MIMETYPES = [
    "text/vnd.in3d.spot",  # .spo wich is confused with xls, doc, etc.
    "text/vnd.graphviz",  # .dot which is confused with xls, doc, etc.
]


class PlainTextConverter(DocumentConverter):
    """Anything with content type text/plain"""

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_GENERIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(
        self, local_path: str, **kwargs: Any
    ) -> Union[None, DocumentConverterResult]:
        # Guess the content type from any file extension that might be around
        content_type, _ = mimetypes.guess_type(
            "__placeholder" + kwargs.get("file_extension", "")
        )

        # Ignore common false positives
        if content_type in IGNORE_MIMETYPES:
            content_type = None

        # Only accept text files
        if content_type is None:
            return None
        elif all(
            not content_type.lower().startswith(type_prefix)
            for type_prefix in ["text/", "application/json"]
        ):
            return None

        text_content = str(from_path(local_path).best())
        return DocumentConverterResult(
            title=None,
            text_content=text_content,
        )
