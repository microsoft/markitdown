import email
import email.policy
import io
import os
from typing import BinaryIO, Any, TYPE_CHECKING

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import UnsupportedFormatException, FileConversionException

if TYPE_CHECKING:
    from .._markitdown import MarkItDown

ACCEPTED_MIME_TYPE_PREFIXES = [
    "message/rfc822",
]

ACCEPTED_FILE_EXTENSIONS = [".eml"]


class EmlConverter(DocumentConverter):
    """Converts .eml files to markdown by extracting headers, body content, and recursively converting attachments.
    """

    def __init__(
        self,
        *,
        markitdown: "MarkItDown",
    ):
        super().__init__()
        self._markitdown = markitdown

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # Parse email bytes using default policy
        msg = email.message_from_bytes(file_stream.read(), policy=email.policy.default)

        # Get headers
        headers = {}
        for h in ["From", "To", "Subject", "Date"]:
            headers[h] = msg.get(h)

        md_content = "# Email Message\n\n"
        for key, value in headers.items():
            if value:
                md_content += f"**{key}:** {value}\n"

        md_content += "\n## Content\n\n"

        # Extract email body
        body_text = ""
        body_html = ""

        for part in msg.walk():
            content_type = part.get_content_type()
            # Skip attachments, handle separately
            if part.is_multipart() or part.get_filename():
                continue
            try:
                content = part.get_content()
                if content_type == "text/plain":
                    body_text += content + "\n"
                elif content_type == "text/html":
                    body_html += content + "\n"
            except Exception:
                pass

        if body_html:
            html_stream = io.BytesIO(body_html.encode("utf-8"))
            html_stream_info = StreamInfo(mimetype="text/html", extension=".html")
            try:
                res = self._markitdown.convert_stream(html_stream, html_stream_info)
                md_content += res.markdown + "\n\n"
            except Exception:
                if body_text:
                    md_content += body_text + "\n\n"
        elif body_text:
            md_content += body_text + "\n\n"

        # Handle attachments
        for part in msg.iter_attachments():
            filename = part.get_filename()
            if not filename:
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue

            att_stream = io.BytesIO(payload)
            att_stream_info = StreamInfo(
                extension=os.path.splitext(filename)[1],
                filename=filename,
            )
            try:
                result = self._markitdown.convert_stream(
                    stream=att_stream,
                    stream_info=att_stream_info,
                )
                if result is not None:
                    md_content += f"## Attachment: {filename}\n\n"
                    md_content += result.markdown + "\n\n"
            except (UnsupportedFormatException, FileConversionException):
                pass
            except Exception:
                pass

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=headers.get("Subject"),
        )
