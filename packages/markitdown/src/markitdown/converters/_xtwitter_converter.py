"""
X (Twitter) 推文转换器

支持类型：
- 普通推文（纯文字 / 带图片）
- 长文 (X Article)
- 视频推文

数据来源：FXTwitter API (https://api.fxtwitter.com)
"""

import hashlib
import os
import re
from typing import Any, BinaryIO, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

# X / Twitter URL 匹配模式
_TWITTER_URL_PATTERN = re.compile(
    r"^https?://(www\.)?(twitter\.com|x\.com)/\w+/status/(\d+)"
)

# 请求头
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}


class XTwitterConverter(DocumentConverter):
    """X (Twitter) 推文转换器，通过 FXTwitter API 获取结构化数据。"""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        url = stream_info.url or ""
        return bool(_TWITTER_URL_PATTERN.match(url))

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        url = stream_info.url or ""

        # 从 URL 提取 screen_name 和 tweet_id
        match = _TWITTER_URL_PATTERN.match(url)
        if not match:
            return DocumentConverterResult(markdown="")

        screen_name = url.split("/")[-3]
        tweet_id = match.group(3)

        # 通过 FXTwitter API 获取推文数据
        tweet_data = self._fetch_tweet(screen_name, tweet_id)
        if not tweet_data:
            return DocumentConverterResult(
                markdown=f"Failed to fetch tweet: {url}"
            )

        # 根据类型分发
        if tweet_data.get("article"):
            markdown = self._convert_article(tweet_data, url)
        else:
            markdown = self._convert_tweet(tweet_data, url)

        title = self._extract_title(tweet_data)

        return DocumentConverterResult(
            markdown=markdown,
            title=title,
        )

    # ------------------------------------------------------------------
    # 数据获取
    # ------------------------------------------------------------------

    @staticmethod
    def _fetch_tweet(screen_name: str, tweet_id: str) -> Optional[Dict]:
        """通过 FXTwitter API 获取推文数据。"""
        api_url = f"https://api.fxtwitter.com/{screen_name}/status/{tweet_id}"
        try:
            resp = requests.get(api_url, headers=_HEADERS, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            return data.get("tweet")
        except Exception:
            return None

    # ------------------------------------------------------------------
    # 普通推文 / 图片推文 / 视频推文
    # ------------------------------------------------------------------

    def _convert_tweet(
        self, tweet: Dict, url: str
    ) -> str:
        """转换普通推文、图片推文、视频推文。"""
        author = tweet.get("author", {})
        author_name = author.get("name", "")
        author_handle = author.get("screen_name", "")
        text = tweet.get("text", "")
        created_at = tweet.get("created_at", "")
        likes = tweet.get("likes", 0)
        retweets = tweet.get("retweets", 0)
        replies = tweet.get("replies", 0)
        views = tweet.get("views", 0)
        bookmarks = tweet.get("bookmarks", 0)

        # 拼接头部
        header = f"# {author_name} 的推文\n\n"
        header += f"**作者**: {author_name} (@{author_handle})\n"
        if created_at:
            header += f"**时间**: {created_at}\n"
        header += f"**原文链接**: {url}\n"
        header += f"\n---\n\n"

        # 正文
        body = text + "\n\n"

        # 处理图片
        media = tweet.get("media", {})
        image_dir = os.path.join(os.getcwd(), "images")
        if image_dir is None:
            image_dir = os.path.join(os.getcwd(), "images")

        images = media.get("all", [])
        for idx, img in enumerate(images, start=1):
            if img.get("type") == "photo":
                img_url = img.get("url", "")
                if img_url:
                    local_name = self._download_image(
                        img_url, image_dir, idx
                    )
                    if local_name:
                        folder = os.path.basename(image_dir)
                        path = f"{folder}/{local_name}".replace("\\", "/")
                        body += f"![图片{idx}]({path})\n\n"

        # 处理视频
        videos = media.get("videos", [])
        if videos:
            for idx, vid in enumerate(videos, start=1):
                video_url = vid.get("url", "")
                duration = vid.get("duration", 0)
                thumb_url = vid.get("thumbnail_url", "")
                minutes = int(duration // 60)
                seconds = int(duration % 60)

                body += f"**[视频{idx}]** 时长 {minutes:02d}:{seconds:02d}\n\n"

                # 下载缩略图
                if thumb_url:
                    thumb_name = self._download_image(
                        thumb_url, image_dir, idx, prefix="thumb"
                    )
                    if thumb_name:
                        folder = os.path.basename(image_dir)
                        path = f"{folder}/{thumb_name}".replace("\\", "/")
                        body += f"![视频缩略图{idx}]({path})\n\n"

                if video_url:
                    body += f"视频下载链接: {video_url}\n\n"

        # 互动数据
        stats = (
            f"---\n\n"
            f"| 浏览 | 点赞 | 转发 | 收藏 | 评论 |\n"
            f"|------|------|------|------|------|\n"
            f"| {self._fmt_num(views)} | {self._fmt_num(likes)} "
            f"| {self._fmt_num(retweets)} | {self._fmt_num(bookmarks)} "
            f"| {self._fmt_num(replies)} |\n"
        )
        body += stats

        return header + body

    # ------------------------------------------------------------------
    # 长文 (X Article)
    # ------------------------------------------------------------------

    def _convert_article(
        self, tweet: Dict, url: str
    ) -> str:
        """转换长文推文 (X Article)。"""
        author = tweet.get("author", {})
        author_name = author.get("name", "")
        author_handle = author.get("screen_name", "")
        article = tweet.get("article", {})
        title = article.get("title", "")
        preview = article.get("preview_text", "")
        cover = article.get("cover_media", {})
        created_at = tweet.get("created_at", "")

        # 拼接头部
        header = f"# {title}\n\n"
        header += f"**作者**: {author_name} (@{author_handle})\n"
        if created_at:
            header += f"**时间**: {created_at}\n"
        header += f"**原文链接**: {url}\n"
        header += f"\n---\n\n"

        # 下载封面图
        image_dir = os.path.join(os.getcwd(), "images")
        if image_dir is None:
            image_dir = os.path.join(os.getcwd(), "images")

        body = ""
        cover_url = ""
        if cover:
            media_info = cover.get("media_info", {})
            cover_url = media_info.get("original_img_url", "")
            if cover_url:
                cover_name = self._download_image(
                    cover_url, image_dir, 0, prefix="cover"
                )
                if cover_name:
                    folder = os.path.basename(image_dir)
                    path = f"{folder}/{cover_name}".replace("\\", "/")
                    body += f"![封面]({path})\n\n"

        # 解析文章内容（Draft.js 块格式）
        content = article.get("content", {})
        blocks = content.get("blocks", [])
        entity_map = content.get("entityMap", [])
        media_entities = article.get("media_entities", [])

        # 建立 entityMap 索引
        entity_lookup = {}
        if isinstance(entity_map, list):
            for entry in entity_map:
                key = str(entry.get("key", ""))
                entity_lookup[key] = entry.get("value", entry)
        elif isinstance(entity_map, dict):
            entity_lookup = entity_map

        # 建立 media_entities 索引 (media_id -> img_url)
        media_lookup = {}
        if isinstance(media_entities, list):
            for me in media_entities:
                mid = me.get("media_id", "")
                mi = me.get("media_info", {})
                img_url = mi.get("original_img_url", "")
                if mid and img_url:
                    media_lookup[mid] = img_url
        elif isinstance(media_entities, dict):
            for mid, me in media_entities.items():
                mi = me.get("media_info", {})
                img_url = mi.get("original_img_url", "")
                if img_url:
                    media_lookup[mid] = img_url

        img_idx = 0
        for block in blocks:
            block_type = block.get("type", "unstyled")
            text = block.get("text", "")
            entity_ranges = block.get("entityRanges", [])
            inline_styles = block.get("inlineStyleRanges", [])

            # 处理图片 / 媒体块
            if block_type == "atomic" and entity_ranges:
                for er in entity_ranges:
                    entity_key = str(er.get("key", ""))
                    entity = entity_lookup.get(entity_key, {})
                    etype = entity.get("type", "")
                    edata = entity.get("data", {})

                    if etype == "MEDIA":
                        # 从 mediaItems 找到 media_id -> img_url
                        for mi in edata.get("mediaItems", []):
                            media_id = mi.get("mediaId", "")
                            img_url = media_lookup.get(media_id, "")
                            if img_url:
                                img_idx += 1
                                local_name = self._download_image(
                                    img_url, image_dir, img_idx
                                )
                                if local_name:
                                    folder = os.path.basename(image_dir)
                                    path = f"{folder}/{local_name}".replace(
                                        "\\", "/"
                                    )
                                    body += f"\n![图片{img_idx}]({path})\n\n"

                    elif etype == "MARKDOWN":
                        md_text = edata.get("markdown", "")
                        if md_text:
                            body += f"\n{md_text}\n\n"
                continue

            # 应用内联样式（加粗）
            text = self._apply_inline_styles(text, inline_styles)

            # 处理链接实体
            if entity_ranges:
                for er in entity_ranges:
                    entity_key = str(er.get("key", ""))
                    entity = entity_lookup.get(entity_key, {})
                    etype = entity.get("type", "")
                    if etype == "LINK":
                        link_url = entity.get("data", {}).get("url", "")
                        if link_url:
                            offset = er.get("offset", 0)
                            length = er.get("length", 0)
                            link_text = text[offset : offset + length]
                            if link_text and link_text != link_url:
                                replacement = f"[{link_text}]({link_url})"
                                text = text[:offset] + replacement + text[offset + length :]

            # 根据块类型输出
            if block_type == "header-two":
                body += f"\n## {text}\n\n"
            elif block_type == "header-three":
                body += f"\n### {text}\n\n"
            elif block_type == "blockquote":
                lines = text.split("\n")
                for line in lines:
                    body += f"> {line}\n"
                body += "\n"
            elif block_type == "unordered-list-item":
                body += f"- {text.rstrip()}\n"
            elif block_type == "ordered-list-item":
                # Draft.js 的有序列表块没有自带序号，简单处理
                body += f"1. {text.rstrip()}\n"
            elif block_type == "code-block":
                body += f"\n```\n{text}\n```\n\n"
            else:
                # unstyled 或其他
                if text.strip():
                    body += f"{text}\n\n"

        # 互动数据
        likes = tweet.get("likes", 0)
        retweets = tweet.get("retweets", 0)
        replies = tweet.get("replies", 0)
        views = tweet.get("views", 0)
        bookmarks = tweet.get("bookmarks", 0)

        stats = (
            f"---\n\n"
            f"| 浏览 | 点赞 | 转发 | 收藏 | 评论 |\n"
            f"|------|------|------|------|------|\n"
            f"| {self._fmt_num(views)} | {self._fmt_num(likes)} "
            f"| {self._fmt_num(retweets)} | {self._fmt_num(bookmarks)} "
            f"| {self._fmt_num(replies)} |\n"
        )
        body += stats

        return header + body

    # ------------------------------------------------------------------
    # 辅助方法
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_title(tweet: Dict) -> str:
        """提取标题：优先用文章标题，否则用作者名。"""
        article = tweet.get("article", {})
        if article:
            title = article.get("title", "")
            if title:
                return title
        author = tweet.get("author", {})
        name = author.get("name", "")
        if name:
            return f"{name} 的推文"
        return "Tweet"

    @staticmethod
    def _apply_inline_styles(text: str, styles: List[Dict]) -> str:
        """应用内联样式（加粗等）到文本。"""
        if not styles:
            return text

        # 按偏移量倒序排列，避免位置偏移
        sorted_styles = sorted(styles, key=lambda s: s.get("offset", 0), reverse=True)

        for style in sorted_styles:
            offset = style.get("offset", 0)
            length = style.get("length", 0)
            style_name = style.get("style", "")

            if style_name == "Bold" and offset + length <= len(text):
                text = text[:offset] + "**" + text[offset : offset + length] + "**" + text[offset + length :]

        return text

    @staticmethod
    def _download_image(
        url: str, image_dir: str, index: int, prefix: str = "img"
    ) -> Optional[str]:
        """下载图片到本地，返回文件名。"""
        try:
            os.makedirs(image_dir, exist_ok=True)
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
            ext = _guess_image_ext(url)
            filename = f"tw_{prefix}_{index:03d}_{url_hash}{ext}"
            filepath = os.path.join(image_dir, filename)

            if os.path.exists(filepath):
                return filename

            resp = requests.get(url, headers=_HEADERS, timeout=30, stream=True)
            resp.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            return filename
        except Exception:
            return None

    @staticmethod
    def _fmt_num(n: Any) -> str:
        """格式化数字：1200 -> 1.2K。"""
        try:
            n = int(n)
        except (ValueError, TypeError):
            return str(n)
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M"
        if n >= 1_000:
            return f"{n / 1_000:.1f}K"
        return str(n)


def _guess_image_ext(url: str) -> str:
    """从 URL 路径推断图片扩展名。"""
    from urllib.parse import urlparse
    path = urlparse(url).path
    for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"):
        if path.lower().endswith(ext):
            return ext
    return ".jpg"
