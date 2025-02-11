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
