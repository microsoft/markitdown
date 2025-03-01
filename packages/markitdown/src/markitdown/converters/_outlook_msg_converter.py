import sys
from typing import Any, Union
from ._base import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import olefile
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


class OutlookMsgConverter(DocumentConverter):
    """Converts Outlook .msg files to markdown by extracting email metadata and content.

    Uses the olefile package to parse the .msg file structure and extract:
    - Email headers (From, To, Subject)
    - Email body content
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(
        self, local_path: str, **kwargs: Any
    ) -> Union[None, DocumentConverterResult]:
        # Bail if not a MSG file
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".msg":
            return None

        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".msg",
                    feature="outlook",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # Restore the original traceback

        try:
            msg = olefile.OleFileIO(local_path)
            # Extract email metadata
            md_content = "# Email Message\n\n"

            # Get headers
            headers = {
                "From": self._get_stream_data(msg, "__substg1.0_0C1F001F"),
                "To": self._get_stream_data(msg, "__substg1.0_0E04001F"),
                "Subject": self._get_stream_data(msg, "__substg1.0_0037001F"),
            }

            # Add headers to markdown
            for key, value in headers.items():
                if value:
                    md_content += f"**{key}:** {value}\n"

            md_content += "\n## Content\n\n"

            # Get email body
            body = self._get_stream_data(msg, "__substg1.0_1000001F")
            if body:
                md_content += body

            msg.close()

            return DocumentConverterResult(
                title=headers.get("Subject"), text_content=md_content.strip()
            )

        except Exception as e:
            raise FileConversionException(
                f"Could not convert MSG file '{local_path}': {str(e)}"
            )

    def _get_stream_data(self, msg: Any, stream_path: str) -> Union[str, None]:
        """Helper to safely extract and decode stream data from the MSG file."""
        assert isinstance(
            msg, olefile.OleFileIO
        )  # Ensure msg is of the correct type (type hinting is not possible with the optional olefile package)

        try:
            if msg.exists(stream_path):
                data = msg.openstream(stream_path).read()
                # Try UTF-16 first (common for .msg files)
                try:
                    return data.decode("utf-16-le").strip()
                except UnicodeDecodeError:
                    # Fall back to UTF-8
                    try:
                        return data.decode("utf-8").strip()
                    except UnicodeDecodeError:
                        # Last resort - ignore errors
                        return data.decode("utf-8", errors="ignore").strip()
        except Exception:
            pass
        return None
