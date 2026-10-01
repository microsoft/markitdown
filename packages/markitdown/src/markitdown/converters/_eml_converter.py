from typing import Any, BinaryIO, List, Tuple

from email import policy
from email.parser import BytesParser
from email.utils import getaddresses

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo


ACCEPTED_MIME_TYPE_PREFIXES = [
    "message/",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".eml",
]


class EmlConverter(DocumentConverter):
    """Converts EML (email) files to Markdown. Preserves headers, body, and attachments info."""

    def accepts(
        self,
        file_stream: BinaryIO,  # noqa: ARG002 - required by interface
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

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,  # noqa: ARG002 - kept for interface compatibility
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        """Convert an EML message to markdown."""
        _ = kwargs  # Currently unused

        # Read the full message from the binary stream and parse it
        raw_bytes = file_stream.read()
        msg = BytesParser(policy=policy.default).parsebytes(raw_bytes)

        # Build markdown content
        md_parts: List[str] = []

        # Add email headers
        md_parts.append("## Email Headers\n")

        # Helper to format address headers that can contain multiple addresses
        def _format_address_header(header_name: str) -> Tuple[str, str]:
            raw_values = msg.get_all(header_name, [])
            if not raw_values:
                return header_name, ""

            addresses = getaddresses(raw_values)
            formatted = []
            for name, addr in addresses:
                if name and addr:
                    formatted.append(f"{name} <{addr}>")
                elif addr:
                    formatted.append(addr)
            return header_name, ", ".join(formatted)

        # From, To, Cc, Bcc in a readable format
        for header in ["From", "To", "Cc", "Bcc"]:
            key, value = _format_address_header(header)
            if value:
                md_parts.append(f"**{key}:** {value}")

        # Other common headers
        subject = msg.get("Subject", "")
        if subject:
            md_parts.append(f"**Subject:** {subject}")

        date = msg.get("Date", "")
        if date:
            md_parts.append(f"**Date:** {date}")

        md_parts.append("\n## Email Content\n")

        # Prefer plain text body; fall back to HTML if no plain text part exists
        body_text: List[str] = []
        has_text_plain = False

        if msg.is_multipart():
            # First pass: check if there is any text/plain part
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    has_text_plain = True
                    break

            for part in msg.walk():
                content_type = part.get_content_type()
                disposition = part.get_content_disposition()

                # Skip attachments when extracting the main body
                if disposition == "attachment":
                    continue

                if content_type == "text/plain":
                    body_text.append(part.get_content())
                elif content_type == "text/html" and not has_text_plain:
                    # If we have HTML content but no plain text, fall back to HTML
                    body_text.append(part.get_content())
        else:
            # Single-part message
            content_type = msg.get_content_type()
            if content_type in ("text/plain", "text/html", "text/rfc822-headers"):
                body_text.append(msg.get_content())

        if body_text:
            md_parts.append("\n".join(body_text))

        # List attachments, if any
        attachments: List[str] = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()
                    if filename:
                        try:
                            payload = part.get_content()
                            size = len(payload) if isinstance(payload, (bytes, str)) else 0
                        except Exception:
                            size = 0
                        mime_type = part.get_content_type()
                        attachments.append(
                            f"- {filename} ({mime_type}, {size:,} bytes)"
                        )

        if attachments:
            md_parts.append("\n## Attachments\n")
            md_parts.extend(attachments)

        markdown = "\n".join(md_parts).strip()

        return DocumentConverterResult(
            markdown=markdown,
            title=subject or None,
        )