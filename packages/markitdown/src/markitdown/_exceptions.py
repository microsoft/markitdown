class MarkItDownException(BaseException):
    """
    Base exception class for MarkItDown.
    """

    pass


class ConverterPrerequisiteException(MarkItDownException):
    """
    Thrown when instantiating a DocumentConverter in cases where
    a required library or dependency is not installed, an API key
    is not set, or some other prerequisite is not met.

    This is not necessarily a fatal error. If thrown during
    MarkItDown's plugin loading phase, the converter will simply be
    skipped, and a warning will be issued.
    """

    pass


class FileConversionException(MarkItDownException):
    """
    Thrown when a suitable converter was found, but the conversion
    process fails for any reason.
    """

    pass


class UnsupportedFormatException(MarkItDownException):
    """
    Thrown when no suitable converter was found for the given file.
    """

    pass
