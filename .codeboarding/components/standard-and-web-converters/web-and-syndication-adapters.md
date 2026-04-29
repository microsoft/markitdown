---
component_id: 2.1
component_name: Web & Syndication Adapters
---

# Web & Syndication Adapters

## Component Description

Handles the extraction of content from dynamic and structured web sources, including HTML pages, Wikipedia articles, and RSS/Atom feeds. It performs initial DOM cleaning using BeautifulSoup and metadata extraction (e.g., titles, feed entries) before passing content to the transformation engine.

---

## Key References:

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converters/_html_converter.py (lines 21-110)
```
class HtmlConverter(DocumentConverter):
    """Anything with content type text/html"""

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
        # Pop our own keyword before forwarding the rest to markdownify.
        # strict=True raises RecursionError instead of falling back to plain text.
        strict: bool = kwargs.pop("strict", False)

        # Parse the stream
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        soup = BeautifulSoup(file_stream, "html.parser", from_encoding=encoding)

        # Remove javascript and style blocks
        for script in soup(["script", "style"]):
            script.extract()

        # Print only the main content
        body_elm = soup.find("body")
        webpage_text = ""
        try:
            if body_elm:
                webpage_text = _CustomMarkdownify(**kwargs).convert_soup(body_elm)
            else:
                webpage_text = _CustomMarkdownify(**kwargs).convert_soup(soup)
        except RecursionError:
            if strict:
                raise
            # Large or deeply-nested HTML can exceed Python's recursion limit
            # during markdownify's recursive DOM traversal.  Fall back to
            # BeautifulSoup's iterative get_text() so the caller still gets
            # usable plain-text content instead of raw HTML.
            warnings.warn(
                "HTML document is too deeply nested for markdown conversion "
                "(RecursionError). Falling back to plain-text extraction.",
                stacklevel=2,
            )
            target = body_elm if body_elm else soup
            webpage_text = target.get_text("\n", strip=True)

        assert isinstance(webpage_text, str)

        # remove leading and trailing \n
        webpage_text = webpage_text.strip()

        return DocumentConverterResult(
            markdown=webpage_text,
            title=None if soup.title is None else soup.title.string,
        )

    def convert_string(
        self, html_content: str, *, url: Optional[str] = None, **kwargs
    ) -> DocumentConverterResult:
        """
        Non-standard convenience method to convert a string to markdown.
        Given that many converters produce HTML as intermediate output, this
        allows for easy conversion of HTML to markdown.
        """
        return self.convert(
            file_stream=io.BytesIO(html_content.encode("utf-8")),
            stream_info=StreamInfo(
                mimetype="text/html",
                extension=".html",
                charset="utf-8",
                url=url,
            ),
            **kwargs,
        )
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converters/_wikipedia_converter.py (lines 20-87)
```
class WikipediaConverter(DocumentConverter):
    """Handle Wikipedia pages separately, focusing only on the main document content."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        """
        Make sure we're dealing with HTML content *from* Wikipedia.
        """

        url = stream_info.url or ""
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if not re.search(r"^https?:\/\/[a-zA-Z]{2,3}\.wikipedia.org\/", url):
            # Not a Wikipedia URL
            return False

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        # Not HTML content
        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Parse the stream
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        soup = bs4.BeautifulSoup(file_stream, "html.parser", from_encoding=encoding)

        # Remove javascript and style blocks
        for script in soup(["script", "style"]):
            script.extract()

        # Print only the main content
        body_elm = soup.find("div", {"id": "mw-content-text"})
        title_elm = soup.find("span", {"class": "mw-page-title-main"})

        webpage_text = ""
        main_title = None if soup.title is None else soup.title.string

        if body_elm:
            # What's the title
            if title_elm and isinstance(title_elm, bs4.Tag):
                main_title = title_elm.string

            # Convert the page
            webpage_text = f"# {main_title}\n\n" + _CustomMarkdownify(
                **kwargs
            ).convert_soup(body_elm)
        else:
            webpage_text = _CustomMarkdownify(**kwargs).convert_soup(soup)

        return DocumentConverterResult(
            markdown=webpage_text,
            title=main_title,
        )
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converters/_rss_converter.py (lines 29-192)
```
class RssConverter(DocumentConverter):
    """Convert RSS / Atom type to markdown"""

    def __init__(self):
        super().__init__()
        self._kwargs = {}

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        # Check for precise mimetypes and file extensions
        if extension in PRECISE_FILE_EXTENSIONS:
            return True

        for prefix in PRECISE_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        # Check for precise mimetypes and file extensions
        if extension in CANDIDATE_FILE_EXTENSIONS:
            return self._check_xml(file_stream)

        for prefix in CANDIDATE_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return self._check_xml(file_stream)

        return False

    def _check_xml(self, file_stream: BinaryIO) -> bool:
        cur_pos = file_stream.tell()
        try:
            doc = minidom.parse(file_stream)
            return self._feed_type(doc) is not None
        except BaseException as _:
            pass
        finally:
            file_stream.seek(cur_pos)
        return False

    def _feed_type(self, doc: Any) -> str | None:
        if doc.getElementsByTagName("rss"):
            return "rss"
        elif doc.getElementsByTagName("feed"):
            root = doc.getElementsByTagName("feed")[0]
            if root.getElementsByTagName("entry"):
                # An Atom feed must have a root element of <feed> and at least one <entry>
                return "atom"
        return None

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        self._kwargs = kwargs
        doc = minidom.parse(file_stream)
        feed_type = self._feed_type(doc)

        if feed_type == "rss":
            return self._parse_rss_type(doc)
        elif feed_type == "atom":
            return self._parse_atom_type(doc)
        else:
            raise ValueError("Unknown feed type")

    def _parse_atom_type(self, doc: Document) -> DocumentConverterResult:
        """Parse the type of an Atom feed.

        Returns None if the feed type is not recognized or something goes wrong.
        """
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
            markdown=md_text,
            title=title,
        )

    def _parse_rss_type(self, doc: Document) -> DocumentConverterResult:
        """Parse the type of an RSS feed.

        Returns None if the feed type is not recognized or something goes wrong.
        """
        root = doc.getElementsByTagName("rss")[0]
        channel_list = root.getElementsByTagName("channel")
        if not channel_list:
            raise ValueError("No channel found in RSS feed")
        channel = channel_list[0]
        channel_title = self._get_data_by_tag_name(channel, "title")
        channel_description = self._get_data_by_tag_name(channel, "description")
        items = channel.getElementsByTagName("item")
        if channel_title:
            md_text = f"# {channel_title}\n"
        if channel_description:
            md_text += f"{channel_description}\n"
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
            markdown=md_text,
            title=channel_title,
        )

    def _parse_content(self, content: str) -> str:
        """Parse the content of an RSS feed item"""
        try:
            # using bs4 because many RSS feeds have HTML-styled content
            soup = BeautifulSoup(content, "html.parser")
            return _CustomMarkdownify(**self._kwargs).convert_soup(soup)
        except BaseException as _:
            return content

    def _get_data_by_tag_name(
        self, element: Element, tag_name: str
    ) -> Union[str, None]:
        """Get data from first child element with the given tag name.
        Returns None when no such element is found.
        """
        nodes = element.getElementsByTagName(tag_name)
        if not nodes:
            return None
        fc = nodes[0].firstChild
        if fc:
            if hasattr(fc, "data"):
                return fc.data
        return None
```


## Source Files:

- `packages/markitdown/src/markitdown/_base_converter.py`
- `packages/markitdown/src/markitdown/_exceptions.py`
- `packages/markitdown/src/markitdown/converters/_bing_serp_converter.py`
- `packages/markitdown/src/markitdown/converters/_csv_converter.py`
- `packages/markitdown/src/markitdown/converters/_epub_converter.py`
- `packages/markitdown/src/markitdown/converters/_html_converter.py`
- `packages/markitdown/src/markitdown/converters/_ipynb_converter.py`
- `packages/markitdown/src/markitdown/converters/_markdownify.py`
- `packages/markitdown/src/markitdown/converters/_plain_text_converter.py`
- `packages/markitdown/src/markitdown/converters/_rss_converter.py`

