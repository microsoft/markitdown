from typing import Optional, List, Any


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


class UnsupportedFormatException(MarkItDownException):
    """
    Thrown when no suitable converter was found for the given file.
    """

    pass


class FailedConversionAttempt(object):
    """
    Represents an a single attempt to convert a file.
    """

    def __init__(self, converter: Any, exc_info: Optional[tuple] = None):
        self.converter = converter
        self.exc_info = exc_info


class FileConversionException(MarkItDownException):
    """
    Thrown when a suitable converter was found, but the conversion
    process fails for any reason.
    """

    def __init__(
        self,
        message: Optional[str] = None,
        attempts: Optional[List[FailedConversionAttempt]] = None,
    ):
        self.attempts = attempts

        if message is None:
            if attempts is None:
                message = "File conversion failed."
            else:
                message = f"File conversion failed after {len(attempts)} attempts:\n"
                for attempt in attempts:
                    message += f" - {type(attempt.converter).__name__} threw {attempt.exc_info[0].__name__} with message: {attempt.exc_info[1]}\n"

        super().__init__(message)
