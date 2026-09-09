import email
import email.policy
import re
from typing import Any, BinaryIO
from .._stream_info import StreamInfo
from .._base_converter import DocumentConverter, DocumentConverterResult

ACCEPTED_MIME_TYPE_PREFIXES = [
    "message/rfc822",
]

ACCEPTED_FILE_EXTENSIONS = [".eml"]


class EmlConverter(DocumentConverter):
    """Converts EML (RFC 822) email files to markdown by extracting headers and body content.

    Uses Python's built-in email module to parse the message and extract:
    - Email headers (From, To, Cc, Subject, Date)
    - Email body content (prefers text/plain, falls back to text/html with tag stripping)
    """

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
        raw_bytes = file_stream.read()
        msg = email.message_from_bytes(raw_bytes, policy=email.policy.default)

        md_content = "# Email Message\n\n"

        headers = {
            "From": msg.get("From", ""),
            "To": msg.get("To", ""),
            "Cc": msg.get("Cc", ""),
            "Subject": msg.get("Subject", ""),
            "Date": msg.get("Date", ""),
        }

        for key, value in headers.items():
            if value:
                md_content += f"**{key}:** {value}\n"

        md_content += "\n## Content\n\n"

        body = self._get_body(msg)
        if body:
            md_content += body

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=headers.get("Subject") or None,
        )

    def _get_body(self, msg: email.message.Message) -> str:
        """Extract the body from the email message.

        Prefers text/plain. Falls back to text/html with HTML tag stripping.
        """
        if msg.is_multipart():
            plain_part = None
            html_part = None
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain" and plain_part is None:
                    plain_part = part
                elif content_type == "text/html" and html_part is None:
                    html_part = part

            if plain_part is not None:
                return self._decode_part(plain_part)
            elif html_part is not None:
                return self._strip_html(self._decode_part(html_part))
        else:
            content_type = msg.get_content_type()
            body = self._decode_payload(msg)
            if content_type == "text/html":
                return self._strip_html(body)
            return body

        return ""

    def _decode_part(self, part: email.message.Message) -> str:
        """Decode a MIME part's payload to a string."""
        payload = part.get_payload(decode=True)
        if payload is None:
            return ""
        charset = part.get_content_charset() or "utf-8"
        try:
            return payload.decode(charset).strip()
        except (UnicodeDecodeError, LookupError):
            return payload.decode("utf-8", errors="ignore").strip()

    def _decode_payload(self, msg: email.message.Message) -> str:
        """Decode a non-multipart message payload to a string."""
        payload = msg.get_payload(decode=True)
        if payload is None:
            return ""
        charset = msg.get_content_charset() or "utf-8"
        try:
            return payload.decode(charset).strip()
        except (UnicodeDecodeError, LookupError):
            return payload.decode("utf-8", errors="ignore").strip()

    def _strip_html(self, html: str) -> str:
        """Strip HTML tags to extract plain text."""
        text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
        text = re.sub(r"</?p\s*/?>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"&amp;", "&", text)
        text = re.sub(r"&lt;", "<", text)
        text = re.sub(r"&gt;", ">", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
