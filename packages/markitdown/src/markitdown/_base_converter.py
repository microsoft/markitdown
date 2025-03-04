import os
import tempfile
from warnings import warn
from typing import Any, Union, BinaryIO, Optional, List
from ._stream_info import StreamInfo

# Avoid printing the same warning multiple times
_WARNED: List[str] = []


class DocumentConverterResult:
    """The result of converting a document to Markdown."""

    def __init__(
        self,
        markdown: str,
        *,
        title: Optional[str] = None,
    ):
        """
        Initialize the DocumentConverterResult.

        The only required parameter is the converted Markdown text.
        The title, and any other metadata that may be added in the future, are optional.

        Parameters:
        - markdown: The converted Markdown text.
        - title: Optional title of the document.
        """
        self.markdown = markdown
        self.title = title

    @property
    def text_content(self) -> str:
        """Soft-deprecated alias for `markdown`. New code should migrate to using `markdown` or __str__."""
        return self.markdown

    @text_content.setter
    def text_content(self, markdown: str):
        """Soft-deprecated alias for `markdown`. New code should migrate to using `markdown` or __str__."""
        self.markdown = markdown

    def __str__(self) -> str:
        """Return the Markdown content."""
        return self.markdown


class DocumentConverter:
    """Abstract superclass of all DocumentConverters."""

    # Lower priority values are tried first.
    PRIORITY_SPECIFIC_FILE_FORMAT = (
        0.0  # e.g., .docx, .pdf, .xlsx, Or specific pages, e.g., wikipedia
    )
    PRIORITY_GENERIC_FILE_FORMAT = (
        10.0  # Near catch-all converters for mimetypes like text/*, etc.
    )

    def __init__(self, priority: float = PRIORITY_SPECIFIC_FILE_FORMAT):
        """
        Initialize the DocumentConverter with a given priority.

        Priorities work as follows: By default, most converters get priority
        DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT (== 0). The exception
        is the PlainTextConverter, which gets priority PRIORITY_SPECIFIC_FILE_FORMAT (== 10),
        with lower values being tried first (i.e., higher priority).

        Just prior to conversion, the converters are sorted by priority, using
        a stable sort. This means that converters with the same priority will
        remain in the same order, with the most recently registered converters
        appearing first.

        We have tight control over the order of built-in converters, but
        plugins can register converters in any order. A converter's priority
        field reasserts some control over the order of converters.

        Plugins can register converters with any priority, to appear before or
        after the built-ins. For example, a plugin with priority 9 will run
        before the PlainTextConverter, but after the built-in converters.
        """
        self._priority = priority

    def convert_stream(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> Union[None, DocumentConverterResult]:
        """
        Convert a document to Markdown text, or return None if the converter
        cannot handle the document (causing the next converter to be tried).

        The determination of whether a converter can handle a document is primarily based on
        the provided `stream_info.mimetype`. The field `stream_info.extension` can serve as
        a secondary check if the MIME type is not sufficiently specific
        (e.g., application/octet-stream). In the case of data retreived via HTTP, the
        `steam_info.url` might also be referenced to guide conversion (e.g., special-handling
        for Wikipedia). Finally, the `stream_info.chatset` is used to determine the encoding
        of the file content in cases of text/*

        Prameters:
        - file_stream: The file-like object to convert. Must support seek(), tell(), and read() methods.
        - stream_info: The StreamInfo object containing metadata about the file (mimetype, extension, charset, set)
        - kwargs: Additional keyword arguments for the converter.

        Returns:
        - DocumentConverterResult: The result of the conversion, which includes the title and markdown content.
        or
        - None: If the converter cannot handle the document.

        Raises:
        - FileConversionException: If the mimetype is recognized, but the conversion fails for some other reason.
        - MissingDependencyException: If the converter requires a dependency that is not installed.
        """

        # Default implementation ensures backward compatibility with the legacy convert() method, and
        # should absolutely be overridden in subclasses. This behavior is deprecated and will be removed
        # in the future.
        result = None
        used_legacy = False

        if stream_info.local_path is not None and os.path.exists(
            stream_info.local_path
        ):
            # If the stream is backed by a local file, pass it to the legacy convert() method
            try:
                result = self.convert(stream_info.local_path, **kwargs)
                used_legacy = True
            except (
                NotImplementedError
            ):  # If it wasn't implemented, rethrow the error, but with this as the stack trace
                raise NotImplementedError(
                    "Subclasses must implement the convert_stream method."
                )
        else:
            # Otherwise, we need to read the stream into a temporary file. There is potential for
            # thrashing here if there are many converters or conversion attempts
            cur_pos = file_stream.tell()
            temp_fd, temp_path = tempfile.mkstemp()
            try:
                with os.fdopen(temp_fd, "wb") as temp_file:
                    temp_file.write(file_stream.read())
                try:
                    result = self.convert(temp_path, **kwargs)
                    used_legacy = True
                except NotImplementedError:
                    raise NotImplementedError(
                        "Subclasses must implement the convert_stream method."
                    )
            finally:
                os.remove(temp_path)
                file_stream.seek(0)

        if used_legacy:
            message = f"{type(self).__name__} uses the legacy convert() method, which is deprecated."
            if message not in _WARNED:
                warn(message, DeprecationWarning)
                _WARNED.append(message)

        return result

    def convert(
        self, local_path: str, **kwargs: Any
    ) -> Union[None, DocumentConverterResult]:
        """
        Legacy, and deprecated method to convert a document to Markdown text.
        This method reads from the file at `local_path` and returns the converted Markdown text.
        This method is deprecated in favor of `convert_stream`, which uses a file-like object.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @property
    def priority(self) -> float:
        """Priority of the converter in markitdown's converter list. Higher priority values are tried first."""
        return self._priority

    @priority.setter
    def priority(self, value: float):
        self._priority = value
