import re
from typing import Any, BinaryIO

from bs4 import BeautifulSoup, Tag

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._markdownify import _CustomMarkdownify

ACCEPTED_MIME_TYPE_PREFIXES = [
    "text/html",
    "application/xhtml",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".html",
    ".htm",
]


class WeChatConverter(DocumentConverter):
    """Handle WeChat public account articles, focusing on the article content."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        url = stream_info.url or ""
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if re.search(r"^https?://mp\.weixin\.qq\.com/s/", url):
            return True

        is_html = extension in ACCEPTED_FILE_EXTENSIONS or any(
            mimetype.startswith(prefix) for prefix in ACCEPTED_MIME_TYPE_PREFIXES
        )
        if not is_html:
            return False

        cur_pos = file_stream.tell()
        try:
            preview = file_stream.read(65536)
        finally:
            file_stream.seek(cur_pos)

        if not isinstance(preview, bytes):
            return False
        preview_text = preview.decode("utf-8", errors="ignore")

        return bool(
            re.search(r"id=[\"']js_content[\"']", preview_text)
            and (
                "rich_media_content" in preview_text
                or re.search(r"id=[\"']activity-name[\"']", preview_text)
                or re.search(r"id=[\"']img-content[\"']", preview_text)
            )
        )

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset
        soup = BeautifulSoup(file_stream, "html.parser", from_encoding=encoding)
        content_source = soup.find(id="js_content")
        if not isinstance(content_source, Tag):
            raise ValueError("Could not find WeChat article content.")

        for tag in soup(["script", "style", "noscript", "template", "iframe", "form"]):
            tag.extract()

        title = self._text(soup.find(id="activity-name")) or self._meta_content(
            soup, 'meta[property="og:title"]', 'meta[name="twitter:title"]'
        )
        author = self._text(soup.find(id="js_author_name"))
        account = self._text(soup.find(id="js_name"))
        publish_time = self._text(soup.find(id="publish_time"))
        cover_url = self._meta_content(
            soup, 'meta[property="og:image"]', 'meta[name="twitter:image"]'
        )

        content_soup = BeautifulSoup(str(content_source), "html.parser")
        content = content_soup.find(id="js_content") or content_soup

        self._remove_elements_by_selector(
            content,
            (
                ".novel-card",
                ".qr_code_pc",
                ".wx_follow_context",
                ".wx_stream_article_slide_tip",
                ".weui-dialog",
                ".article-tag__error-tips",
                "[id^='js_minipro_dialog']",
                "[id^='js_pc_qr_code']",
            ),
        )
        self._remove_blocks_containing_text(
            content,
            (
                "因微信平台规则调整",
                "建议您将本公众号设为星标",
                "预览时标签不可点",
            ),
        )
        self._truncate_children_from_markers(
            content,
            (
                "点击下方“阅读原文”",
                '点击下方"阅读原文"',
                "相关阅读",
            ),
        )
        self._normalize_lazy_images(content)

        article_soup = BeautifulSoup(
            "<!doctype html><html><head></head><body><article></article></body></html>",
            "html.parser",
        )
        article = article_soup.article
        assert article is not None

        if title:
            title_tag = article_soup.new_tag("title")
            title_tag.string = title
            assert article_soup.head is not None
            article_soup.head.append(title_tag)

        if cover_url:
            cover = article_soup.new_tag("img", src=cover_url)
            cover["alt"] = "cover_image"
            article.append(cover)

        if title:
            h1 = article_soup.new_tag("h1")
            h1.string = title
            article.append(h1)

        metadata = self._metadata(
            author=author, account=account, publish_time=publish_time
        )
        if metadata:
            metadata_tag = article_soup.new_tag("p")
            metadata_tag.string = metadata
            article.append(metadata_tag)

        body_fragment = BeautifulSoup(str(content), "html.parser")
        body = body_fragment.find(id="js_content") or body_fragment
        for child in list(body.children):
            article.append(child)

        webpage_text = _CustomMarkdownify(**kwargs).convert_soup(article).strip()

        return DocumentConverterResult(
            markdown=webpage_text,
            title=title,
        )

    def _text(self, element: Tag | None) -> str | None:
        if not element:
            return None
        text = element.get_text(" ", strip=True)
        return text or None

    def _meta_content(self, soup: BeautifulSoup, *selectors: str) -> str | None:
        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get("content"):
                return str(element["content"]).strip()
        return None

    def _metadata(
        self, *, author: str | None, account: str | None, publish_time: str | None
    ) -> str | None:
        parts = []
        if author:
            parts.append(f"Author: {author}")
        if account and account != author:
            parts.append(f"Account: {account}")
        if publish_time:
            parts.append(f"Published: {publish_time}")
        if not parts:
            return None
        return " | ".join(dict.fromkeys(parts))

    def _remove_elements_by_selector(
        self, root: Tag | BeautifulSoup, selectors: tuple[str, ...]
    ) -> None:
        for selector in selectors:
            for element in root.select(selector):
                element.extract()

    def _remove_blocks_containing_text(
        self, root: Tag | BeautifulSoup, markers: tuple[str, ...]
    ) -> None:
        matches = []
        for node in root.find_all(string=True):
            text = str(node)
            if any(marker in text for marker in markers):
                block = self._nearest_small_block(root, node.parent)
                if block and block not in matches:
                    matches.append(block)
        for block in matches:
            block.extract()

    def _nearest_small_block(
        self, root: Tag | BeautifulSoup, element: Tag | None
    ) -> Tag | None:
        current = element
        while current and current is not root:
            if current.name in {"p", "li", "blockquote"}:
                return current
            current = current.parent if isinstance(current.parent, Tag) else None

        current = element
        while current and current is not root:
            if current.name in {"section", "div"}:
                return current
            current = current.parent if isinstance(current.parent, Tag) else None
        return None

    def _truncate_children_from_markers(
        self, root: Tag | BeautifulSoup, markers: tuple[str, ...]
    ) -> None:
        children = [child for child in root.children if isinstance(child, Tag)]
        truncate_at = None
        for index, child in enumerate(children):
            text = child.get_text(" ", strip=True)
            if any(marker in text for marker in markers):
                truncate_at = index
                break
        if truncate_at is None:
            return
        for child in children[truncate_at:]:
            child.extract()

    def _normalize_lazy_images(self, root: Tag | BeautifulSoup) -> None:
        for image in root.find_all("img"):
            data_src = (
                image.get("data-src")
                or image.get("data-original")
                or image.get("data-lazy-src")
            )
            if data_src and not image.get("src"):
                image["src"] = data_src
            for attr in ("data-src", "data-original", "data-lazy-src"):
                if image.has_attr(attr):
                    del image[attr]
