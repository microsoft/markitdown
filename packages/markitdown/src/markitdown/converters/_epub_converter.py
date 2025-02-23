# type: ignore
from typing import Any

from ebooklib import epub, ITEM_DOCUMENT

from ._base import DocumentConverter, DocumentConverterResult
from ._html_converter import HtmlConverter

class EpubConverter(DocumentConverter):
    """Converts EPUB files to Markdown. Preserves chapter structure and metadata."""

    def convert(self, local_path: str, **kwargs: Any) -> DocumentConverterResult:
        """Convert an EPUB file to markdown.

        Args:
            local_path: Path to the EPUB file
            **kwargs: Additional arguments (unused)

        Returns:
            DocumentConverterResult containing the converted markdown

        Raises:
            FileConversionException: If the file is not an EPUB file
        """
        # Check if this is an EPUB file
        file_ext = kwargs.get("file_extension", "").lower()
        if not file_ext.endswith(".epub"):
            return None

        book = epub.read_epub(local_path)

        # Initialize result with book title
        result = DocumentConverterResult(
            title=(
                book.get_metadata("DC", "title")[0][0]
                if book.get_metadata("DC", "title")
                else None
            )
        )

        # Start with metadata
        metadata_md = []
        if book.get_metadata("DC", "creator"):
            metadata_md.append(f"Author: {book.get_metadata('DC', 'creator')[0][0]}")
        if book.get_metadata("DC", "description"):
            metadata_md.append(f"\n{book.get_metadata('DC', 'description')[0][0]}")

        # Convert content
        content_md = []
        for item in book.get_items():
            if item.get_type() == ITEM_DOCUMENT:
                content = item.get_content().decode("utf-8")
                html_result = HtmlConverter()._convert(content)
                if html_result and html_result.text_content:
                    content_md.append(html_result.text_content)

        # Combine all parts
        result.text_content = "\n\n".join(metadata_md + content_md)

        return result
