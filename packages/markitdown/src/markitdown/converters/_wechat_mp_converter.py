"""
微信公众号文章转换器

将 mp.weixin.qq.com 的公众号文章转为 Markdown，并下载图片到本地。
"""

import hashlib
import io
import os
import re
from typing import Any, BinaryIO, Dict, Optional
from urllib.parse import urljoin

import requests
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

# 公众号反爬验证页面的关键词
_CAPTCHA_INDICATORS = ["环境异常", "captcha", "appmsgcaptcha", "验证后即可继续"]


class WeChatMPConverter(DocumentConverter):
    """微信公众号文章转换器，提取标题/作者/正文/图片，图片下载到本地。"""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        url = stream_info.url or ""
        if not re.search(r"^https?://mp\.weixin\.qq\.com/", url):
            return False

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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        encoding = "utf-8" if stream_info.charset is None else stream_info.charset

        # 先读取内容，检测是否被反爬拦截
        cur_pos = file_stream.tell()
        raw_bytes = file_stream.read()
        file_stream.seek(cur_pos)

        # 如果检测到验证页面，尝试用更好的 headers 重新请求
        html_text = raw_bytes.decode(encoding, errors="replace")
        original_url = stream_info.url
        if self._is_captcha_page(html_text) and stream_info.url:
            raw_bytes = self._refetch(stream_info.url)
            if raw_bytes is not None:
                html_text = raw_bytes.decode("utf-8", errors="replace")

        soup = BeautifulSoup(html_text, "html.parser")

        # 提取元信息
        title = self._extract_title(soup)
        account = self._extract_account(soup)
        author = self._extract_author(soup)
        date = self._extract_date(soup)

        # 提取正文
        content = soup.find("div", id="js_content")
        if not content:
            # 回退：尝试 class 匹配
            content = soup.find("div", class_="rich_media_content")
        if not content:
            # 最终回退：用整个 body
            content = soup.find("body") or soup

        # 下载图片并替换路径
        image_dir = kwargs.get("wechat_image_dir", None)
        if image_dir is None:
            # 默认在当前工作目录下创建 images 文件夹
            image_dir = os.path.join(os.getcwd(), "images")
        self._download_images(content, image_dir, stream_info.url)

        # 转换为 Markdown
        md_body = _CustomMarkdownify(**kwargs).convert_soup(content)
        md_body = md_body.strip()

        # 拼接头部元信息
        header = f"# {title}\n\n"
        meta_lines = []
        if account:
            meta_lines.append(f"**公众号**: {account}")
        if author and author != account:
            meta_lines.append(f"**作者**: {author}")
        if date:
            meta_lines.append(f"**发布时间**: {date}")
        # 原文链接：优先用原始 URL，如果被重定向到验证页则从中提取
        display_url = original_url or ""
        if "appmsgcaptcha" in display_url and "target_url=" in display_url:
            from urllib.parse import parse_qs, urlparse
            params = parse_qs(urlparse(display_url).query)
            if "target_url" in params:
                display_url = params["target_url"][0]
        if display_url:
            meta_lines.append(f"**原文链接**: {display_url}")
        if meta_lines:
            header += "\n".join(meta_lines) + "\n\n---\n\n"

        markdown = header + md_body

        return DocumentConverterResult(
            markdown=markdown,
            title=title,
        )

    # ------------------------------------------------------------------
    # 反爬处理
    # ------------------------------------------------------------------

    @staticmethod
    def _is_captcha_page(html: str) -> bool:
        """检测 HTML 是否是验证页面。"""
        html_lower = html.lower()
        return any(kw in html_lower for kw in _CAPTCHA_INDICATORS)

    @staticmethod
    def _refetch(url: str) -> Optional[bytes]:
        """用移动端 User-Agent 重新请求，尝试绕过反爬。"""
        # 如果当前 URL 是验证页，从中提取原始 URL
        original_url = url
        if "appmsgcaptcha" in url and "target_url=" in url:
            from urllib.parse import parse_qs, urlparse
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            if "target_url" in params:
                original_url = params["target_url"][0]

        headers_list = [
            {
                "User-Agent": (
                    "Mozilla/5.0 (Linux; Android 13; Pixel 7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Mobile Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Referer": "https://mp.weixin.qq.com/",
            },
            {
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/17.0 Mobile/15E148 Safari/604.1"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Referer": "https://mp.weixin.qq.com/",
            },
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Referer": "https://www.weixin.qq.com/",
            },
        ]
        for hdrs in headers_list:
            try:
                session = requests.Session()
                resp = session.get(original_url, headers=hdrs, timeout=30)
                resp.raise_for_status()
                content = resp.content
                # 验证新页面不是验证页
                text = content.decode("utf-8", errors="replace").lower()
                if not any(kw in text for kw in _CAPTCHA_INDICATORS):
                    return content
            except Exception:
                continue
        return None

    # ------------------------------------------------------------------
    # 元信息提取
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
        el = soup.find("h1", id="activity-name")
        if el:
            return el.get_text(strip=True)
        el = soup.find("h1", class_="rich_media_title")
        if el:
            return el.get_text(strip=True)
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        return "Untitled"

    @staticmethod
    def _extract_account(soup: BeautifulSoup) -> str:
        el = soup.find("a", id="js_name")
        if el:
            return el.get_text(strip=True)
        el = soup.find("span", class_="rich_media_meta_nickname")
        if el:
            return el.get_text(strip=True)
        return ""

    @staticmethod
    def _extract_author(soup: BeautifulSoup) -> str:
        el = soup.find("span", id="js_author_name")
        if el:
            return el.get_text(strip=True)
        el = soup.find("span", class_="rich_media_meta_text")
        if el:
            return el.get_text(strip=True)
        return ""

    @staticmethod
    def _extract_date(soup: BeautifulSoup) -> str:
        el = soup.find("em", id="publish_time")
        if el:
            text = el.get_text(strip=True)
            if text:
                return text
        # 回退：从 meta 标签提取
        meta = soup.find("meta", {"property": "article:published_time"})
        if meta and meta.get("content"):
            return meta["content"][:10]
        return ""

    # ------------------------------------------------------------------
    # 图片处理
    # ------------------------------------------------------------------

    def _download_images(
        self,
        content: Tag,
        image_dir: str,
        page_url: Optional[str],
    ) -> None:
        """
        找到正文中的所有 <img>，下载到 image_dir，并将 src/data-src
        替换为本地相对路径。
        """
        images = content.find_all("img")
        if not images:
            return

        os.makedirs(image_dir, exist_ok=True)

        # 图片文件夹的名称，用于生成相对路径
        image_folder_name = os.path.basename(image_dir)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": page_url or "https://mp.weixin.qq.com/",
        }

        for idx, img in enumerate(images, start=1):
            # 优先用 data-src（公众号懒加载），其次 src
            img_url = img.get("data-src") or img.get("src") or ""
            if not img_url or img_url.startswith("data:"):
                continue

            # 补全相对路径
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            elif not img_url.startswith("http"):
                img_url = urljoin(page_url or "", img_url)

            # 下载图片
            local_path = self._download_one(
                img_url, image_dir, idx, headers
            )
            if local_path:
                # 替换为相对路径
                relative_path = os.path.join(image_folder_name, local_path)
                # 统一用正斜杠，兼容 Markdown 渲染
                relative_path = relative_path.replace("\\", "/")
                img["src"] = relative_path
                # 清掉 data-src，避免 markdownify 二次处理
                if img.get("data-src"):
                    del img["data-src"]

    @staticmethod
    def _download_one(
        url: str,
        image_dir: str,
        index: int,
        headers: Dict[str, str],
    ) -> Optional[str]:
        """下载单张图片，返回文件名；失败返回 None。"""
        try:
            resp = requests.get(url, headers=headers, timeout=30, stream=True)
            resp.raise_for_status()

            # 从 Content-Type 或 URL 推断扩展名
            ext = _guess_extension(resp.headers.get("Content-Type", ""), url)

            # 用 URL 的 md5 做文件名，避免重复下载
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
            filename = f"img_{index:03d}_{url_hash}{ext}"
            filepath = os.path.join(image_dir, filename)

            # 如果文件已存在，跳过下载
            if os.path.exists(filepath):
                return filename

            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            return filename

        except Exception:
            return None


def _guess_extension(content_type: str, url: str) -> str:
    """从 Content-Type 或 URL 路径推断图片扩展名。"""
    ct_map = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/svg+xml": ".svg",
        "image/bmp": ".bmp",
    }
    ct_lower = content_type.lower().split(";")[0].strip()
    if ct_lower in ct_map:
        return ct_map[ct_lower]

    # 从 URL 路径猜测
    from urllib.parse import urlparse
    path = urlparse(url).path
    for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"):
        if path.lower().endswith(ext):
            return ext

    # 公众号默认大多是 jpg
    return ".jpg"
