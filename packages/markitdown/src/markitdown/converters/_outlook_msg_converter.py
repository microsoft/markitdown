import sys
from typing import Any, Union, BinaryIO
from charset_normalizer import from_bytes
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
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        # Check the extension and mimetype
        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        # Brute force, check if we have an OLE file
        cur_pos = file_stream.tell()
        try:
            if olefile and not olefile.isOleFile(file_stream):
                return False
        finally:
            file_stream.seek(cur_pos)

        # Brute force, check if it's an Outlook file
        try:
            if olefile is not None:
                msg = olefile.OleFileIO(file_stream)
                toc = "\n".join([str(stream) for stream in msg.listdir()])
                return (
                    "__properties_version1.0" in toc
                    and "__recip_version1.0_#00000000" in toc
                )
        except Exception as e:
            pass
        finally:
            file_stream.seek(cur_pos)

        return False

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
            "From": self._get_property_data(msg, "0C1F"),  # PR_SENDER_EMAIL_ADDRESS
            "To": self._get_property_data(msg, "0E04"),  # PR_DISPLAY_TO
            "Subject": self._get_property_data(msg, "0037"),  # PR_SUBJECT
        }

        # Add headers to markdown
        for key, value in headers.items():
            if value:
                md_content += f"**{key}:** {value}\n"

        md_content += "\n## Content\n\n"

        # Get email body
        body = self._get_property_data(msg, "1000")  # PR_BODY
        if body:
            md_content += body

        msg.close()

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=headers.get("Subject"),
        )

    def _get_property_data(self, msg: Any, property_tag: str) -> Union[str, None]:
        """Helper to read a MAPI string property, whichever string type is used.

        Outlook stores each string property either as PT_UNICODE (stream type
        001F, UTF-16LE) or as PT_STRING8 (stream type 001E, the message's 8-bit
        code page), depending on whether the message was saved in Unicode or in
        the legacy non-Unicode format. A message carries one or the other, so
        reading only 001F returns nothing at all for a non-Unicode .msg.
        """
        value = self._get_stream_data(msg, "__substg1.0_%s001F" % property_tag)
        if value:
            return value
        return self._get_ansi_stream_data(msg, "__substg1.0_%s001E" % property_tag)

    def _get_ansi_stream_data(self, msg: Any, stream_path: str) -> Union[str, None]:
        """Helper to extract and decode a PT_STRING8 stream from the MSG file.

        These streams record no encoding of their own -- they are written in
        the message's code page -- so the charset has to be detected, as is
        done elsewhere for other 8-bit sources.
        """
        assert olefile is not None
        assert isinstance(msg, olefile.OleFileIO)

        try:
            if not msg.exists(stream_path):
                return None
            data = msg.openstream(stream_path).read()
        except Exception:
            return None

        if not data:
            return None

        detected = from_bytes(data).best()
        if detected is not None:
            return str(detected).strip()
        return data.decode("utf-8", errors="ignore").strip()

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
        except Exception:
            pass
        return None
