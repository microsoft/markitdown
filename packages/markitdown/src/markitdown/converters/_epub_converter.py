import base64
import io
import mimetypes
import os
import posixpath
import zipfile
from defusedxml import minidom
from xml.dom.minidom import Document

from typing import BinaryIO, Any, Dict, List, Optional
from urllib.parse import urlsplit, unquote

from bs4 import BeautifulSoup

from markitdown.converters._html_converter import HtmlConverter
from markitdown._base_converter import DocumentConverterResult
from markitdown._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/epub",
    "application/epub+zip",
    "application/x-epub+zip",
]

ACCEPTED_FILE_EXTENSIONS = [".epub"]

MIME_TYPE_MAPPING = {
    ".html": "text/html",
    ".xhtml": "application/xhtml+xml",
}


class EpubConverter(HtmlConverter):
    """
    Converts EPUB files to Markdown. Style information (e.g.m headings) and tables are preserved where possible.
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
            **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        with zipfile.ZipFile(file_stream, "r") as z:
            # Extracts metadata (title, authors, language, publisher, date, description, cover) from an EPUB file."""

            # Locate content.opf
            container_dom = minidom.parse(z.open("META-INF/container.xml"))
            opf_path = container_dom.getElementsByTagName("rootfile")[0].getAttribute(
                "full-path"
            )

            # Parse content.opf
            opf_dom = minidom.parse(z.open(opf_path))
            metadata: Dict[str, Any] = {
                "title": self._get_text_from_node(opf_dom, "dc:title"),
                "authors": self._get_all_texts_from_nodes(opf_dom, "dc:creator"),
                "language": self._get_text_from_node(opf_dom, "dc:language"),
                "publisher": self._get_text_from_node(opf_dom, "dc:publisher"),
                "date": self._get_text_from_node(opf_dom, "dc:date"),
                "description": self._get_text_from_node(opf_dom, "dc:description"),
                "identifier": self._get_text_from_node(opf_dom, "dc:identifier"),
            }

            # Extract spine order (ID refs)
            spine_items = opf_dom.getElementsByTagName("itemref")
            spine_order = [item.getAttribute("idref") for item in spine_items]

            # Convert spine order to actual file paths
            base_path = "/".join(
                opf_path.split("/")[:-1]
            )  # Get base directory of content.opf

            # Extract manifest items (ID → href mapping), and a path → media-type map.
            manifest: Dict[str, str] = {}
            media_type_by_path: Dict[str, str] = {}
            for item in opf_dom.getElementsByTagName("item"):
                item_id = item.getAttribute("id")
                href = item.getAttribute("href")
                if item_id and href:
                    manifest[item_id] = href
                    full_path = f"{base_path}/{href}" if base_path else href
                    media_type = item.getAttribute("media-type")
                    if media_type:
                        media_type_by_path[full_path] = media_type
            spine = [
                f"{base_path}/{manifest[item_id]}" if base_path else manifest[item_id]
                for item_id in spine_order
                if item_id in manifest
            ]

            # Extract and convert the content
            markdown_content: List[str] = []
            keep_data_uris = kwargs.get("keep_data_uris", False)
            for file in spine:
                if file in z.namelist():
                    with z.open(file) as f:
                        html_bytes = f.read()

                    if keep_data_uris:
                        html_bytes = self._inline_images(
                            html_bytes, file, z, media_type_by_path
                        )

                    filename = os.path.basename(file)
                    extension = os.path.splitext(filename)[1].lower()
                    mimetype = MIME_TYPE_MAPPING.get(extension)
                    converted_content = self._html_converter.convert(
                        io.BytesIO(html_bytes),
                        StreamInfo(
                            mimetype=mimetype,
                            extension=extension,
                            filename=filename,
                        ),
                        **kwargs,
                    )
                    markdown_content.append(converted_content.markdown.strip())

            # Format and add the metadata
            metadata_markdown = []
            for key, value in metadata.items():
                if isinstance(value, list):
                    value = ", ".join(value)
                if value:
                    metadata_markdown.append(f"**{key.capitalize()}:** {value}")

            markdown_content.insert(0, "\n".join(metadata_markdown))

            return DocumentConverterResult(
                markdown="\n\n".join(markdown_content), title=metadata["title"]
            )

    def _get_text_from_node(self, dom: Document, tag_name: str) -> str | None:
        """Convenience function to extract a single occurrence of a tag (e.g., title)."""
        texts = self._get_all_texts_from_nodes(dom, tag_name)
        if len(texts) > 0:
            return texts[0]
        else:
            return None

    def _get_all_texts_from_nodes(self, dom: Document, tag_name: str) -> List[str]:
        """Helper function to extract all occurrences of a tag (e.g., multiple authors)."""
        texts: List[str] = []
        for node in dom.getElementsByTagName(tag_name):
            if node.firstChild and hasattr(node.firstChild, "nodeValue"):
                texts.append(node.firstChild.nodeValue.strip())
        return texts

    def _inline_images(
            self,
            html_bytes: bytes,
            html_path: str,
            zip_file: zipfile.ZipFile,
            media_type_by_path: Dict[str, str],
    ) -> bytes:
        soup = BeautifulSoup(html_bytes, "html.parser")
        updated = False
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if not src:
                continue

            if src.startswith("data:"):
                continue

            parsed = urlsplit(src)
            if parsed.scheme or parsed.netloc:
                continue

            img_path = self._resolve_epub_path(html_path, unquote(parsed.path))
            if not img_path or img_path not in zip_file.namelist():
                continue

            with zip_file.open(img_path) as img_f:
                data = img_f.read()

            content_type = media_type_by_path.get(img_path)
            if not content_type:
                content_type, _ = mimetypes.guess_type(img_path)
            if not content_type:
                content_type = "application/octet-stream"

            b64 = base64.b64encode(data).decode("ascii")
            img["src"] = f"data:{content_type};base64,{b64}"
            updated = True

        if not updated:
            return html_bytes

        return str(soup).encode("utf-8")

    def _resolve_epub_path(self, html_path: str, resource_path: str) -> Optional[str]:
        if not resource_path:
            return None

        if resource_path.startswith("/"):
            return resource_path.lstrip("/")

        base_dir = posixpath.dirname(html_path)
        return posixpath.normpath(posixpath.join(base_dir, resource_path))
