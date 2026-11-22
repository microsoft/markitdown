from dataclasses import dataclass, field
from typing import Any, BinaryIO, List, Mapping, NoReturn, Optional
from ._stream_info import StreamInfo


class _ReadOnlyCounts(dict):
    """
    A dict that cannot be modified after construction.

    Unlike types.MappingProxyType it can be pickled, deep-copied, passed to
    dataclasses.asdict and serialised directly with json.dumps.
    """

    def _readonly(self, *args: Any, **kwargs: Any) -> NoReturn:
        raise TypeError("ConversionWarning.counts is read-only")

    __setitem__ = _readonly
    __delitem__ = _readonly
    __ior__ = _readonly  # type: ignore[assignment]
    clear = _readonly
    pop = _readonly
    popitem = _readonly
    setdefault = _readonly
    update = _readonly

    def __reduce__(self) -> Any:
        # Rebuild through the constructor instead of item assignment.
        return (type(self), (dict(self),))

    def __deepcopy__(self, memo: Any) -> "_ReadOnlyCounts":
        return self  # immutable, so sharing is safe


@dataclass(frozen=True)
class ConversionWarning:
    """
    A diagnostic reported by a converter alongside the converted Markdown.

    Warnings describe information that the conversion may have lost or could
    not check. They never alter the Markdown itself.

    Attributes:
    - code: Stable, machine-readable identifier (e.g., "VECTOR_GRAPHICS_PRESENT").
    - severity: A standard Python ``logging`` level, such as ``logging.WARNING``
      or ``logging.INFO``. This allows ``logger.log(w.severity, w.message)``.
    - message: Human-readable description. Contains no document content.
    - page: 1-based page number the warning applies to, or None if it applies
      to the whole document.
    - counts: Optional diagnostic counts (e.g., {"curves": 3}). Stored as a
      read-only mapping. Instances are immutable but not hashable.
    """

    code: str
    severity: int
    message: str
    page: Optional[int] = None
    counts: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Copy into a read-only dict so the frozen instance cannot be mutated
        # through its counts mapping (and later caller changes don't leak in).
        object.__setattr__(self, "counts", _ReadOnlyCounts(self.counts))


class DocumentConverterResult:
    """The result of converting a document to Markdown."""

    def __init__(
        self,
        markdown: str,
        *,
        title: Optional[str] = None,
        warnings: Optional[List[ConversionWarning]] = None,
    ):
        """
        Initialize the DocumentConverterResult.

        The only required parameter is the converted Markdown text.
        The title, and any other metadata that may be added in the future, are optional.

        Parameters:
        - markdown: The converted Markdown text.
        - title: Optional title of the document.
        - warnings: Optional list of ConversionWarning diagnostics. None (the
          default) means no diagnostic was run; an empty list means diagnostics
          ran and found nothing to report.
        """
        self.markdown = markdown
        self.title = title
        self.warnings = warnings

    @property
    def text_content(self) -> str:
        """Soft-deprecated alias for `markdown`. New code should migrate to using `markdown` or __str__."""
        return self.markdown

    @text_content.setter
    def text_content(self, markdown: str):
        """Soft-deprecated alias for `markdown`. New code should migrate to using `markdown` or __str__."""
        self.markdown = markdown

    def __str__(self) -> str:
        """Return the converted Markdown text."""
        return self.markdown


class DocumentConverter:
    """Abstract superclass of all DocumentConverters."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        """
        Return a quick determination on if the converter should attempt converting the document.
        This is primarily based on `stream_info` (typically, `stream_info.mimetype`, `stream_info.extension`).
        In cases where the data is retrieved via HTTP, the `stream_info.url` might also be referenced to
        make a determination (e.g., special converters for Wikipedia, YouTube etc).
        Finally, it is conceivable that the `stream_info.filename` might be used in cases
        where the filename is well-known (e.g., `Dockerfile`, `Makefile`, etc)

        NOTE: The method signature is designed to match that of the convert() method. This provides some
        assurance that, if accepts() returns True, the convert() method will also be able to handle the document.

        IMPORTANT: In rare cases, (e.g., OutlookMsgConverter) we need to read more from the stream to make a final
        determination. Read operations inevitably advance the position in file_stream. In these cases, the position
        MUST be reset before returning. This is because the convert() method may be called immediately
        after accepts(), and will expect the file_stream to be at the original position.

        E.g.,
        cur_pos = file_stream.tell() # Save the current position
        data = file_stream.read(100) # ... peek at the first 100 bytes, etc.
        file_stream.seek(cur_pos)    # Reset the position to the original position

        Parameters:
        - file_stream: The file-like object to convert. Must support seek(), tell(), and read() methods.
        - stream_info: The StreamInfo object containing metadata about the file (mimetype, extension, charset, etc.)
        - kwargs: Additional keyword arguments for the converter.

        Returns:
        - bool: True if the converter can handle the document, False otherwise.
        """
        raise NotImplementedError(
            f"The subclass, {type(self).__name__}, must implement the accepts() method to determine if they can handle the document."
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        """
        Convert a document to Markdown text.

        Parameters:
        - file_stream: The file-like object to convert. Must support seek(), tell(), and read() methods.
        - stream_info: The StreamInfo object containing metadata about the file (mimetype, extension, charset, etc.)
        - kwargs: Additional keyword arguments for the converter.

        Returns:
        - DocumentConverterResult: The result of the conversion, which includes the title and markdown content.

        Raises:
        - FileConversionException: If the mimetype is recognized, but the conversion fails for some other reason.
        - MissingDependencyException: If the converter requires a dependency that is not installed.
        """
        raise NotImplementedError("Subclasses must implement this method")
