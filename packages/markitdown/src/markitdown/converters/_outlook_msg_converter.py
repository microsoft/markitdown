"""Outlook .msg converter — extracts email metadata and body from Outlook message files via olefile."""

import sys
from typing import Any, Union, BinaryIO
from .._stream_info import StreamInfo
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
olefile = None
try:
    import olefile  # type: ignore[no-redef]
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.ms-outlook",
]

ACCEPTED_FILE_EXTENSIONS = [".msg"]


class OutlookMsgConverter(DocumentConverter):
    """Converts Outlook .msg files to markdown by extracting email metadata and content.

    Uses the olefile package to parse the .msg file structure and extract:
    - Email headers (From, To, Subject)
    - Email body content
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        # Check the extension and mimetype
        if self._accepted_by_mime_or_ext(
            stream_info, ACCEPTED_MIME_TYPE_PREFIXES, ACCEPTED_FILE_EXTENSIONS
        ):
            return True

        if olefile is None:
            return False

        # Brute force, check if we have an OLE file and it looks like an Outlook message
        cur_pos = file_stream.tell()
        try:
            if not olefile.isOleFile(file_stream):
                return False
            msg = olefile.OleFileIO(file_stream)
            toc = "\n".join([str(stream) for stream in msg.listdir()])
            return (
                "__properties_version1.0" in toc
                and "__recip_version1.0_#00000000" in toc
            )
        except (OSError, RuntimeError):
            return False
        finally:
            file_stream.seek(cur_pos)

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".msg",
                    feature="outlook",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        assert (
            olefile is not None
        )  # If we made it this far, olefile should be available
        msg = olefile.OleFileIO(file_stream)

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
            markdown=md_content.strip(),
            title=headers.get("Subject"),
        )

    def _get_stream_data(self, msg: Any, stream_path: str) -> Union[str, None]:
        """Helper to safely extract and decode stream data from the MSG file."""
        assert olefile is not None
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
        except (AttributeError, OSError, IndexError, RuntimeError):
            pass
        return None
