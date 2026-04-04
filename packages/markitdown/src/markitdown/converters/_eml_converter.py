import email
import email.message
import email.policy
import io
import os
import re
import warnings
from typing import TYPE_CHECKING, Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import FileConversionException, UnsupportedFormatException
from .._stream_info import StreamInfo

if TYPE_CHECKING:
    from .._markitdown import MarkItDown

ACCEPTED_MIME_TYPE_PREFIXES = [
    "message/rfc822",
]

ACCEPTED_FILE_EXTENSIONS = [".eml"]


class EmlConverter(DocumentConverter):
    """Converts EML (RFC 822) email files to markdown.

    Extracts email headers, body content, and optionally converts attachments
    by passing them back through the MarkItDown converter pipeline.

    Attachment conversion requires a MarkItDown instance, which is injected
    automatically when the converter is registered via ``enable_builtins()``.
    If no MarkItDown instance is provided, attachments are listed by filename
    without being converted.

    Example output::

        # Email Message

        **From:** sender@example.com
        **To:** recipient@example.com
        **Subject:** Q1 Report

        ## Content

        Please find the Q1 report attached.

        ## Attachments

        ### Q1_Report.xlsx

        ## Sheet1
        | Quarter | Revenue |
        |---------|---------|
        | Q1 2026 | 1.2M    |
    """

    def __init__(self, *, markitdown: "MarkItDown | None" = None) -> None:
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

        attachments = self._get_attachments(msg)
        if attachments:
            md_content += "\n\n## Attachments\n\n"
            for filename, content in attachments:
                md_content += f"### {filename}\n\n"
                md_content += content + "\n\n"

        return DocumentConverterResult(
            markdown=md_content.strip(),
            title=headers.get("Subject") or None,
        )

    def _get_body(self, msg: email.message.Message) -> str:
        """Extract the body from the email message.

        Prefers text/plain. Falls back to text/html with HTML tag stripping.
        Skips parts that are attachments.
        """
        if msg.is_multipart():
            plain_part = None
            html_part = None
            for part in msg.walk():
                # Skip attachments
                disposition = part.get("Content-Disposition", "")
                if "attachment" in disposition.lower():
                    continue

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

    def _get_attachments(self, msg: email.message.Message) -> list[tuple[str, str]]:
        """Extract and convert email attachments.

        Iterates over all MIME parts with Content-Disposition: attachment.
        If a MarkItDown instance is available, each attachment is passed through
        the converter pipeline. If not, the attachment is listed by filename with
        a note that conversion requires a MarkItDown instance.

        Returns a list of (filename, markdown_content) tuples.
        """
        results: list[tuple[str, str]] = []

        if not msg.is_multipart():
            return results

        for part in msg.walk():
            disposition = part.get("Content-Disposition", "")
            if "attachment" not in disposition.lower():
                continue

            filename = part.get_filename() or "attachment"
            payload = part.get_payload(decode=True)

            if payload is None:
                continue

            if self._markitdown is None:
                results.append(
                    (
                        filename,
                        "*Attachment present but not converted. "
                        "Pass a MarkItDown instance to EmlConverter to enable attachment conversion.*",
                    )
                )
                continue

            ext = os.path.splitext(filename)[1].lower()
            try:
                attachment_stream = io.BytesIO(payload)
                attachment_info = StreamInfo(
                    extension=ext,
                    filename=filename,
                )
                result = self._markitdown.convert_stream(
                    stream=attachment_stream,
                    stream_info=attachment_info,
                )
                if result is not None and result.markdown:
                    results.append((filename, result.markdown))
                else:
                    results.append(
                        (filename, "*Attachment converted but produced no content.*")
                    )
            except UnsupportedFormatException:
                results.append(
                    (
                        filename,
                        f"*Attachment not converted: unsupported format (`{ext}`).*",
                    )
                )
            except FileConversionException as e:
                results.append((filename, f"*Attachment not converted: {e}*"))
            except Exception as e:
                warnings.warn(
                    f"Unexpected error converting attachment '{filename}': {e}",
                    stacklevel=2,
                )
                results.append(
                    (filename, "*Attachment not converted due to an unexpected error.*")
                )

        return results

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
