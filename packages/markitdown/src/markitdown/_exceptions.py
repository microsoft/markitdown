class MarkItDownException(BaseException):
    """
    Base exception class for MarkItDown.
    """

    pass


class MissingOptionalDependencyException(MarkItDownException):
    """
    Converters shipped with MarkItDown may depend on optional
    dependencies. This exception is thrown when a converter's
    convert() method is called, but the required dependency is not
    installed. This is not necessarily a fatal error, as the converter
    will simply be skipped (an error will bubble up only if no other
    suitable converter is found).

    Error messages should clearly indicate which dependency is missing.
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
