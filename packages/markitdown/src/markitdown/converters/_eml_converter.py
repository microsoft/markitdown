from typing import Any
from ._base import DocumentConverter, DocumentConverterResult
from email import policy
from email.parser import Parser
from email.utils import parseaddr

class EmlConverter(DocumentConverter):
    """Converts EML (email) files to Markdown. Preserves headers, body, and attachments info."""

    def convert(self, local_path: str, **kwargs: Any) -> DocumentConverterResult:
        """Convert an EML file to markdown.
        Args:
            local_path: Path to the EML file
            **kwargs: Additional arguments (unused)
        Returns:
            DocumentConverterResult containing the converted markdown
        """
        # Check if this is an EML file
        file_ext = kwargs.get("file_extension", "").lower()
        if not file_ext.endswith(".eml"):
            return None

        with open(local_path, "r", encoding="utf-8") as fp:
            # Use policy=default to handle RFC compliant emails
            msg = Parser(policy=policy.default).parse(fp)

        # Initialize result with email subject as title
        result = DocumentConverterResult(title=msg.get("subject", "Untitled Email"))

        # Build markdown content
        md_parts = []

        # Add email headers
        md_parts.append("## Email Headers\n")

        # From and To in a more readable format
        from_name, from_email = parseaddr(msg.get("from", ""))
        to_name, to_email = parseaddr(msg.get("to", ""))

        md_parts.append(
            f"**From:** {from_name} <{from_email}>"
            if from_name
            else f"**From:** {from_email}"
        )
        md_parts.append(
            f"**To:** {to_name} <{to_email}>" if to_name else f"**To:** {to_email}"
        )
        md_parts.append(f"**Subject:** {msg.get('subject', '')}")
        md_parts.append(f"**Date:** {msg.get('date', '')}")

        # Add CC if present
        if msg.get("cc"):
            md_parts.append(f"**CC:** {msg.get('cc')}")

        md_parts.append("\n## Email Content\n")

        # Handle the email body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    md_parts.append(part.get_content())
                elif part.get_content_type() == "text/html":
                    # If we have HTML content but no plain text, we could convert HTML to markdown here
                    # For now, we'll just note it's HTML content
                    if not any(
                        p.get_content_type() == "text/plain" for p in msg.walk()
                    ):
                        md_parts.append(part.get_content())
        else:
            md_parts.append(msg.get_content())

        # List attachments if any
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_disposition() == "attachment":
                    filename = part.get_filename()
                    if filename:
                        size = len(part.get_content())
                        mime_type = part.get_content_type()
                        attachments.append(
                            f"- {filename} ({mime_type}, {size:,} bytes)"
                        )

        if attachments:
            md_parts.append("\n## Attachments\n")
            md_parts.extend(attachments)

        # Combine all parts
        result.text_content = "\n".join(md_parts)

        return result