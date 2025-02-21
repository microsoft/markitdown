from typing import Any, Union
from bs4 import BeautifulSoup

from ._base import DocumentConverter, DocumentConverterResult
from ._markdownify import _CustomMarkdownify
from ._converter_input import ConverterInput


class HtmlConverter(DocumentConverter):
    """Anything with content type text/html"""

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_GENERIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(
        self, input: ConverterInput, **kwargs: Any
    ) -> Union[None, DocumentConverterResult]:
        # Bail if not html
        extension = kwargs.get("file_extension", "")
        if extension.lower() not in [".html", ".htm"]:
            return None

        result = None
        file_obj = input.read_file(mode="rt", encoding="utf-8")
        result = self._convert(file_obj.read())
        file_obj.close()

        return result

    def _convert(self, html_content: str) -> Union[None, DocumentConverterResult]:
        """Helper function that converts an HTML string."""

        # Parse the string
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove javascript and style blocks
        for script in soup(["script", "style"]):
            script.extract()

        # Print only the main content
        body_elm = soup.find("body")
        webpage_text = ""
        if body_elm:
            webpage_text = _CustomMarkdownify().convert_soup(body_elm)
        else:
            webpage_text = _CustomMarkdownify().convert_soup(soup)

        assert isinstance(webpage_text, str)

        # remove leading and trailing \n
        webpage_text = webpage_text.strip()

        return DocumentConverterResult(
            title=None if soup.title is None else soup.title.string,
            text_content=webpage_text,
        )
