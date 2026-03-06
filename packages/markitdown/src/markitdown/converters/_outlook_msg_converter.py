import io
import sys
from typing import Any, Union, BinaryIO
from .._stream_info import StreamInfo
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from ._html_converter import HtmlConverter

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
HTML_BODY_BINARY_STREAM = "__substg1.0_10130102"
HTML_BODY_TEXT_STREAMS = [
    "__substg1.0_1013001F",
    "__substg1.0_1013001E",
]


class OutlookMsgConverter(DocumentConverter):
    """Converts Outlook .msg files to markdown by extracting email metadata and content.

    Uses the olefile package to parse the .msg file structure and extract:
    - Email headers (From, To, Subject)
    - Email body content
    """

    def __init__(self) -> None:
        self._html_converter = HtmlConverter()

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

        # Brue force, check if it's an Outlook file
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
            "From": self._get_stream_data(msg, "__substg1.0_0C1F001F"),
            "To": self._get_stream_data(msg, "__substg1.0_0E04001F"),
            "Subject": self._get_stream_data(msg, "__substg1.0_0037001F"),
        }

        # Add headers to markdown
        for key, value in headers.items():
            if value:
                md_content += f"**{key}:** {value}\n"

        md_content += "\n## Content\n\n"

        # Prefer the HTML body when it is present so Outlook tables survive as tables.
        body = self._get_html_body(msg, **kwargs)
        if body is None:
            body = self._get_stream_data(msg, "__substg1.0_1000001F")
        if body:
            md_content += body

        msg.close()

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=headers.get("Subject"),
        )

    def _get_html_body(self, msg: Any, **kwargs: Any) -> Union[str, None]:
        html_data = self._get_stream_bytes(msg, HTML_BODY_BINARY_STREAM)
        if html_data:
            try:
                markdown = self._html_converter.convert(
                    io.BytesIO(html_data),
                    StreamInfo(mimetype="text/html", extension=".html"),
                    **kwargs,
                ).markdown.strip()
            except Exception:
                markdown = None

            if markdown:
                return markdown

        for stream_path in HTML_BODY_TEXT_STREAMS:
            html_text = self._get_stream_data(msg, stream_path)
            if not html_text:
                continue

            try:
                markdown = self._html_converter.convert_string(
                    html_text,
                    **kwargs,
                ).markdown.strip()
            except Exception:
                markdown = None

            if markdown:
                return markdown

        return None

    def _get_stream_bytes(self, msg: Any, stream_path: str) -> Union[bytes, None]:
        """Helper to safely extract raw stream data from the MSG file."""
        assert olefile is not None
        assert isinstance(
            msg, olefile.OleFileIO
        )  # Ensure msg is of the correct type (type hinting is not possible with the optional olefile package)

        try:
            if msg.exists(stream_path):
                return msg.openstream(stream_path).read()
        except Exception:
            pass
        return None

    def _get_stream_data(self, msg: Any, stream_path: str) -> Union[str, None]:
        """Helper to safely extract and decode stream data from the MSG file."""
        data = self._get_stream_bytes(msg, stream_path)
        if data is None:
            return None

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
