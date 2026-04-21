import base64
import io
import mimetypes
import os
import posixpath
import re
import zipfile
from defusedxml import minidom
from xml.dom.minidom import Document

from bs4 import BeautifulSoup
from typing import BinaryIO, Any, Dict, List

from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverterResult
from ..converter_utils.images import resolve_images_dir
from .._stream_info import StreamInfo

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

            # Extract manifest items (ID → href mapping)
            manifest = {
                item.getAttribute("id"): item.getAttribute("href")
                for item in opf_dom.getElementsByTagName("item")
            }

            # Extract spine order (ID refs)
            spine_items = opf_dom.getElementsByTagName("itemref")
            spine_order = [item.getAttribute("idref") for item in spine_items]

            # Convert spine order to actual file paths
            base_path = "/".join(
                opf_path.split("/")[:-1]
            )  # Get base directory of content.opf
            spine = [
                f"{base_path}/{manifest[item_id]}" if base_path else manifest[item_id]
                for item_id in spine_order
                if item_id in manifest
            ]

            # Extract and convert the content
            # images_dir: optional base directory where images will be saved.
            # A subdirectory image_{stem} is created inside it per file, so
            # converting multiple files into the same dir never mixes images.
            # When omitted, images are embedded inline as base64 data URIs.
            save_images = kwargs.get("save_images", False)
            actual_images_dir: str | None = None
            md_images_prefix: str | None = None
            if save_images:
                actual_images_dir, md_images_prefix = resolve_images_dir(
                    save_images, stream_info, "epub"
                )

            namelist_set = set(z.namelist())
            markdown_content: List[str] = []
            for file in spine:
                if file in namelist_set:
                    with z.open(file) as f:
                        html_bytes = f.read()

                    # Resolve relative image src attributes so that images survive
                    # the conversion to Markdown.
                    html_bytes = self._resolve_images(
                        html_bytes, file, z, namelist_set,
                        actual_images_dir, md_images_prefix,
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
                        keep_data_uris=actual_images_dir is None,
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

    def _resolve_images(
        self,
        html_bytes: bytes,
        html_path: str,
        z: zipfile.ZipFile,
        namelist_set: set,
        images_dir: str | None,
        md_images_prefix: str | None,
    ) -> bytes:
        """Rewrite <img src> attributes so images survive HTML-to-Markdown conversion.

        If *images_dir* is given, each image is extracted there and the src is
        replaced with *md_images_prefix*/filename (a path relative to the markdown
        file).  Otherwise the image is embedded as a base64 data URI.
        """
        soup = BeautifulSoup(html_bytes, "html.parser")
        changed = False
        html_dir = posixpath.dirname(html_path)

        for img in soup.find_all("img"):
            src = img.get("src", "")
            if not src or src.startswith("data:") or src.startswith("http"):
                continue
            resolved = posixpath.normpath(posixpath.join(html_dir, src))
            if resolved not in namelist_set:
                continue
            img_bytes = z.read(resolved)
            if images_dir:
                img_filename = os.path.basename(resolved)
                with open(os.path.join(images_dir, img_filename), "wb") as out:
                    out.write(img_bytes)
                img["src"] = f"{md_images_prefix}/{img_filename}"
            else:
                mime, _ = mimetypes.guess_type(resolved)
                mime = mime or "image/jpeg"
                b64 = base64.b64encode(img_bytes).decode("ascii")
                img["src"] = f"data:{mime};base64,{b64}"
            changed = True

        return soup.encode("utf-8") if changed else html_bytes

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
