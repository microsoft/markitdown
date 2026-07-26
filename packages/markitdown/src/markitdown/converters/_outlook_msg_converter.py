import io
import sys
from typing import Any, Union, BinaryIO

from charset_normalizer import from_bytes

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


class OutlookMsgConverter(DocumentConverter):
    """Converts Outlook .msg files to markdown by extracting email metadata and content.

    Uses the olefile package to parse the .msg file structure and extract:
    - Email headers (From, To, Subject)
    - Email body content
    """

    def __init__(self):
        super().__init__()
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
            "From": self._get_sender(msg),
            "To": self._get_stream_data(msg, "__substg1.0_0E04001F"),
            "Subject": self._get_stream_data(msg, "__substg1.0_0037001F"),
        }

        # Add headers to markdown
        for key, value in headers.items():
            if value:
                md_content += f"**{key}:** {value}\n"

        md_content += "\n## Content\n\n"

        # Get email body. HTML-only messages leave PR_BODY empty and carry
        # their content in PR_HTML instead.
        body = self._get_stream_data(msg, "__substg1.0_1000001F")
        if not body:
            body = self._get_html_body(msg)
        if body:
            md_content += body

        msg.close()

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=headers.get("Subject"),
        )

    def _get_sender(self, msg: Any) -> Union[str, None]:
        """Helper to resolve the sender's address, preferring SMTP over an Exchange DN.

        PR_SENDER_EMAIL_ADDRESS (0x0C1F) only holds an email address when
        PR_SENDER_ADDRTYPE (0x0C1E) is "SMTP". Messages sent through Exchange
        set the address type to "EX" and store a Distinguished Name there
        instead (e.g. "/O=EXCHANGELABS/OU=.../CN=RECIPIENTS/CN=..."), keeping
        the real address in PR_SENDER_SMTP_ADDRESS (0x5D01).
        """
        # PR_SENDER_SMTP_ADDRESS, then PR_SENT_REPRESENTING_SMTP_ADDRESS.
        for address_stream in ("__substg1.0_5D01001F", "__substg1.0_5D02001F"):
            address = self._get_stream_data(msg, address_stream)
            if address:
                return address

        # PR_SENDER_EMAIL_ADDRESS / PR_SENT_REPRESENTING_EMAIL_ADDRESS, each
        # usable only when its address type is not the Exchange DN form.
        for address_stream, addrtype_stream in (
            ("__substg1.0_0C1F001F", "__substg1.0_0C1E001F"),
            ("__substg1.0_0065001F", "__substg1.0_0064001F"),
        ):
            address = self._get_stream_data(msg, address_stream)
            addrtype = self._get_stream_data(msg, addrtype_stream) or ""
            if address and addrtype.upper() != "EX":
                return address

        # Nothing better on file: report the DN rather than dropping the header.
        return self._get_stream_data(msg, "__substg1.0_0C1F001F")

    def _get_html_body(self, msg: Any) -> Union[str, None]:
        """Helper to convert the HTML body (PR_HTML, 0x1013) to markdown.

        Used for messages that carry no plain-text body, where reading only
        PR_BODY would silently drop the entire message content.
        """
        charset: Union[str, None] = None

        # PR_HTML is normally a binary stream; some clients write the string variant.
        html_bytes = self._read_stream(msg, "__substg1.0_10130102")
        if html_bytes is None:
            html = self._get_stream_data(msg, "__substg1.0_1013001F")
            if not html:
                return None
            html_bytes = html.encode("utf-8")
            charset = "utf-8"
        else:
            # The stream carries no encoding of its own, so detect it rather
            # than assuming UTF-8 and mangling non-ASCII text.
            detected = from_bytes(html_bytes).best()
            if detected is not None:
                charset = detected.encoding

        return self._html_converter.convert(
            io.BytesIO(html_bytes),
            StreamInfo(mimetype="text/html", extension=".html", charset=charset),
        ).markdown

    def _get_stream_data(self, msg: Any, stream_path: str) -> Union[str, None]:
        """Helper to safely extract and decode stream data from the MSG file."""
        data = self._read_stream(msg, stream_path)
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

    def _read_stream(self, msg: Any, stream_path: str) -> Union[bytes, None]:
        """Helper to safely read the raw bytes of a stream from the MSG file.

        Binary properties (such as PR_HTML) must not go through
        `_get_stream_data`: arbitrary bytes rarely fail a UTF-16 decode, so
        they would come back as mojibake instead of raising.
        """
        assert olefile is not None
        assert isinstance(
            msg, olefile.OleFileIO
        )  # Ensure msg is of the correct type (type hinting is not possible with the optional olefile package)

        try:
            if msg.exists(stream_path):
                data: bytes = msg.openstream(stream_path).read()
                return data
        except Exception:
            pass
        return None
