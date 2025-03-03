from typing import Any, Union, BinaryIO, Optional


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


class BaseDocumentConverter:
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

    def convert(
        self,
        file_stream,
        *,
        mime_type: str = "application/octet-stream",
        file_extension: Optional[str] = None,
        charset: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[None, DocumentConverterResult]:
        """
        Convert a document to Markdown text, or return None if the converter
        cannot handle the document (causing the next converter to be tried).

        The determination of whether a converter can handle a document is primarily based on
        the provided MIME type. The file extension can serve as a secondary check if the
        MIME type is not sufficiently specific (e.g., application/octet-stream). Finally, the
        chatset is used to determine the encoding of the file content in cases of text/*

        Prameters:
        - file_stream: The file-like object to convert. Must support seek(), tell(), and read() methods.
        - mime_type: The MIME type of the file. Default is "application/octet-stream".
        - file_extension: The file extension of the file. Default is None.
        - charset: The character set of the file. Default is None.
        - kwargs: Additional keyword arguments for the converter.

        Returns:
        - DocumentConverterResult: The result of the conversion, which includes the title and markdown content.
        or
        - None: If the converter cannot handle the document.

        Raises:
        - FileConversionException: If the mimetype is recognized, but the conversion fails for some other reason.
        - MissingDependencyException: If the converter requires a dependency that is not installed.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @property
    def priority(self) -> float:
        """Priority of the converter in markitdown's converter list. Higher priority values are tried first."""
        return self._priority

    @priority.setter
    def priority(self, value: float):
        self._priority = value
