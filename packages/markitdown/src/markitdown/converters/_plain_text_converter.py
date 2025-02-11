import mimetypes

from charset_normalizer import from_path
from typing import Any, Union

from ._base import DocumentConverter, DocumentConverterResult


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
