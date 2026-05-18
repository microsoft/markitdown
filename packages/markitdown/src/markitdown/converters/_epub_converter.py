import os
import logging
import zipfile
from defusedxml import minidom
from xml.dom.minidom import Document

from typing import BinaryIO, Any, Dict, List

from ._html_converter import HtmlConverter
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import FileConversionException

logger = logging.getLogger(__name__)

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
        return self._accepted_by_mime_or_ext(
            stream_info, ACCEPTED_MIME_TYPE_PREFIXES, ACCEPTED_FILE_EXTENSIONS
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        try:
            with zipfile.ZipFile(file_stream, "r") as z:
                # Locate content.opf
                try:
                    container_dom = minidom.parse(z.open("META-INF/container.xml"))
                    rootfiles = container_dom.getElementsByTagName("rootfile")
                    if not rootfiles:
                        raise FileConversionException(
                            "EpubConverter: no rootfile found in container.xml"
                        )
                    opf_path = rootfiles[0].getAttribute("full-path")
                except (KeyError, zipfile.BadZipFile, OSError) as e:
                    logger.warning("EPUB container.xml parsing failed: %s", e)
                    raise FileConversionException(
                        f"EpubConverter: invalid EPUB structure: {e}"
                    ) from e

                # Parse content.opf
                try:
                    opf_dom = minidom.parse(z.open(opf_path))
                except (KeyError, zipfile.BadZipFile, OSError) as e:
                    logger.warning("EPUB content.opf parsing failed: %s", e)
                    raise FileConversionException(
                        f"EpubConverter: unable to read {opf_path}: {e}"
                    ) from e

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
                markdown_content: List[str] = []
                for file in spine:
                    if file not in z.namelist():
                        logger.debug("EPUB spine file not found in archive: %s", file)
                        continue
                    try:
                        with z.open(file) as f:
                            filename = os.path.basename(file)
                            extension = os.path.splitext(filename)[1].lower()
                            mimetype = MIME_TYPE_MAPPING.get(extension)
                            converted_content = self._html_converter.convert(
                                f,
                                StreamInfo(
                                    mimetype=mimetype,
                                    extension=extension,
                                    filename=filename,
                                ),
                            )
                            markdown_content.append(converted_content.markdown.strip())
                    except Exception as e:
                        logger.warning("EPUB chapter conversion failed for %s: %s", file, e)
                        # Continue with remaining chapters instead of failing entirely
                        markdown_content.append(f"[Conversion failed for {file}: {e}]")
                        continue

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
        except zipfile.BadZipFile as e:
            logger.warning("EPUB file is not a valid ZIP: %s", e)
            raise FileConversionException(
                f"EpubConverter: file is not a valid EPUB/ZIP archive: {e}"
            ) from e
        except FileConversionException:
            raise
        except Exception as e:
            logger.warning("EPUB conversion failed: %s", e)
            raise FileConversionException(
                f"EpubConverter: conversion failed: {e}"
            ) from e

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
