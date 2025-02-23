from xml.dom import minidom
from typing import Union
from bs4 import BeautifulSoup

from ._markdownify import _CustomMarkdownify
from ._base import DocumentConverter, DocumentConverterResult


class RssConverter(DocumentConverter):
    """Convert RSS / Atom type to markdown"""

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(
        self, local_path: str, **kwargs
    ) -> Union[None, DocumentConverterResult]:
        # Bail if not RSS type
        extension = kwargs.get("file_extension", "")
        if extension.lower() not in [".xml", ".rss", ".atom"]:
            return None
        try:
            doc = minidom.parse(local_path)
        except BaseException as _:
            return None
        result = None
        if doc.getElementsByTagName("rss"):
            # A RSS feed must have a root element of <rss>
            result = self._parse_rss_type(doc)
        elif doc.getElementsByTagName("feed"):
            root = doc.getElementsByTagName("feed")[0]
            if root.getElementsByTagName("entry"):
                # An Atom feed must have a root element of <feed> and at least one <entry>
                result = self._parse_atom_type(doc)
            else:
                return None
        else:
            # not rss or atom
            return None

        return result

    def _parse_atom_type(
        self, doc: minidom.Document
    ) -> Union[None, DocumentConverterResult]:
        """Parse the type of an Atom feed.

        Returns None if the feed type is not recognized or something goes wrong.
        """
        try:
            root = doc.getElementsByTagName("feed")[0]
            title = self._get_data_by_tag_name(root, "title")
            subtitle = self._get_data_by_tag_name(root, "subtitle")
            entries = root.getElementsByTagName("entry")
            md_text = f"# {title}\n"
            if subtitle:
                md_text += f"{subtitle}\n"
            for entry in entries:
                entry_title = self._get_data_by_tag_name(entry, "title")
                entry_summary = self._get_data_by_tag_name(entry, "summary")
                entry_updated = self._get_data_by_tag_name(entry, "updated")
                entry_content = self._get_data_by_tag_name(entry, "content")

                if entry_title:
                    md_text += f"\n## {entry_title}\n"
                if entry_updated:
                    md_text += f"Updated on: {entry_updated}\n"
                if entry_summary:
                    md_text += self._parse_content(entry_summary)
                if entry_content:
                    md_text += self._parse_content(entry_content)

            return DocumentConverterResult(
                title=title,
                text_content=md_text,
            )
        except BaseException as _:
            return None

    def _parse_rss_type(
        self, doc: minidom.Document
    ) -> Union[None, DocumentConverterResult]:
        """Parse the type of an RSS feed.

        Returns None if the feed type is not recognized or something goes wrong.
        """
        try:
            root = doc.getElementsByTagName("rss")[0]
            channel = root.getElementsByTagName("channel")
            if not channel:
                return None
            channel = channel[0]
            channel_title = self._get_data_by_tag_name(channel, "title")
            channel_description = self._get_data_by_tag_name(channel, "description")
            items = channel.getElementsByTagName("item")
            if channel_title:
                md_text = f"# {channel_title}\n"
            if channel_description:
                md_text += f"{channel_description}\n"
            if not items:
                items = []
            for item in items:
                title = self._get_data_by_tag_name(item, "title")
                description = self._get_data_by_tag_name(item, "description")
                pubDate = self._get_data_by_tag_name(item, "pubDate")
                content = self._get_data_by_tag_name(item, "content:encoded")

                if title:
                    md_text += f"\n## {title}\n"
                if pubDate:
                    md_text += f"Published on: {pubDate}\n"
                if description:
                    md_text += self._parse_content(description)
                if content:
                    md_text += self._parse_content(content)

            return DocumentConverterResult(
                title=channel_title,
                text_content=md_text,
            )
        except BaseException as _:
            print(traceback.format_exc())
            return None

    def _parse_content(self, content: str) -> str:
        """Parse the content of an RSS feed item"""
        try:
            # using bs4 because many RSS feeds have HTML-styled content
            soup = BeautifulSoup(content, "html.parser")
            return _CustomMarkdownify().convert_soup(soup)
        except BaseException as _:
            return content

    def _get_data_by_tag_name(
        self, element: minidom.Element, tag_name: str
    ) -> Union[str, None]:
        """Get data from first child element with the given tag name.
        Returns None when no such element is found.
        """
        nodes = element.getElementsByTagName(tag_name)
        if not nodes:
            return None
        fc = nodes[0].firstChild
        if fc:
            return fc.data
        return None
