from typing import Any, Union


class DocumentConverterResult:
    """The result of converting a document to text."""

    def __init__(self, title: Union[str, None] = None, text_content: str = ""):
        self.title: Union[str, None] = title
        self.text_content: str = text_content


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

    def convert(
        self, local_path: str, **kwargs: Any
    ) -> Union[None, DocumentConverterResult]:
        raise NotImplementedError("Subclasses must implement this method")

    @property
    def priority(self) -> float:
        """Priority of the converter in markitdown's converter list. Higher priority values are tried first."""
        return self._priority

    @priority.setter
    def radius(self, value: float):
        self._priority = value

    @priority.deleter
    def radius(self):
        raise AttributeError("Cannot delete the priority attribute")
