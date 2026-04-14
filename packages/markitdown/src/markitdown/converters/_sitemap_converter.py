"""
Sitemap XML Converter for MarkItDown
New feature: Convert XML sitemaps to structured Markdown link lists.
Author: Maishad Hassan (maishad777)
"""
from defusedxml import minidom
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/xml",
    "application/xml",
]

ACCEPTED_FILE_EXTENSIONS = [".xml"]


class SitemapConverter(DocumentConverter):
    """
    Converts XML sitemaps (sitemap.xml) to a structured Markdown list of URLs.
    Supports standard sitemaps and sitemap index files.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()
        url = (stream_info.url or "").lower()

        if "sitemap" in url and (
            extension in ACCEPTED_FILE_EXTENSIONS
            or any(mimetype.startswith(p) for p in ACCEPTED_MIME_TYPE_PREFIXES)
        ):
            return True

        # Check XML content for sitemap tags
        if extension in ACCEPTED_FILE_EXTENSIONS or any(
            mimetype.startswith(p) for p in ACCEPTED_MIME_TYPE_PREFIXES
        ):
            cur_pos = file_stream.tell()
            try:
                doc = minidom.parse(file_stream)
                if doc.getElementsByTagName("urlset") or doc.getElementsByTagName(
                    "sitemapindex"
                ):
                    return True
            except Exception:
                pass
            finally:
                file_stream.seek(cur_pos)

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        doc = minidom.parse(file_stream)

        # Sitemap index (collection of sitemaps)
        if doc.getElementsByTagName("sitemapindex"):
            return self._convert_sitemap_index(doc)

        # Standard urlset sitemap
        if doc.getElementsByTagName("urlset"):
            return self._convert_urlset(doc)

        return DocumentConverterResult(markdown="*No sitemap content found.*")

    def _convert_urlset(self, doc: Any) -> DocumentConverterResult:
        urls = doc.getElementsByTagName("url")
        md_lines = ["# Sitemap URLs\n"]

        for url_elem in urls:
            loc_nodes = url_elem.getElementsByTagName("loc")
            lastmod_nodes = url_elem.getElementsByTagName("lastmod")
            priority_nodes = url_elem.getElementsByTagName("priority")
            changefreq_nodes = url_elem.getElementsByTagName("changefreq")

            if not loc_nodes:
                continue

            loc = loc_nodes[0].firstChild.data.strip() if loc_nodes[0].firstChild else ""
            lastmod = (
                lastmod_nodes[0].firstChild.data.strip()
                if lastmod_nodes and lastmod_nodes[0].firstChild
                else None
            )
            priority = (
                priority_nodes[0].firstChild.data.strip()
                if priority_nodes and priority_nodes[0].firstChild
                else None
            )
            changefreq = (
                changefreq_nodes[0].firstChild.data.strip()
                if changefreq_nodes and changefreq_nodes[0].firstChild
                else None
            )

            line = f"- [{loc}]({loc})"
            meta = []
            if lastmod:
                meta.append(f"last modified: {lastmod}")
            if priority:
                meta.append(f"priority: {priority}")
            if changefreq:
                meta.append(f"changefreq: {changefreq}")
            if meta:
                line += f" _{' | '.join(meta)}_"
            md_lines.append(line)

        return DocumentConverterResult(
            markdown="\n".join(md_lines),
            title="Sitemap",
        )

    def _convert_sitemap_index(self, doc: Any) -> DocumentConverterResult:
        sitemaps = doc.getElementsByTagName("sitemap")
        md_lines = ["# Sitemap Index\n"]

        for sitemap in sitemaps:
            loc_nodes = sitemap.getElementsByTagName("loc")
            lastmod_nodes = sitemap.getElementsByTagName("lastmod")

            if not loc_nodes:
                continue

            loc = loc_nodes[0].firstChild.data.strip() if loc_nodes[0].firstChild else ""
            lastmod = (
                lastmod_nodes[0].firstChild.data.strip()
                if lastmod_nodes and lastmod_nodes[0].firstChild
                else None
            )

            line = f"- [{loc}]({loc})"
            if lastmod:
                line += f" _(last modified: {lastmod})_"
            md_lines.append(line)

        return DocumentConverterResult(
            markdown="\n".join(md_lines),
            title="Sitemap Index",
        )
