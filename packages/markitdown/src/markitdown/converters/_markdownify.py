import re
import markdownify

from typing import Any, Optional
from urllib.parse import quote, unquote, urlparse, urlunparse


class _CustomMarkdownify(markdownify.MarkdownConverter):
    """
    A custom version of markdownify's MarkdownConverter. Changes include:

    - Altering the default heading style to use '#', '##', etc.
    - Removing javascript hyperlinks.
    - Truncating images with large data:uri sources.
    - Ensuring URIs are properly escaped, and do not conflict with Markdown syntax
    """

    def __init__(self, **options: Any):
        options["heading_style"] = options.get("heading_style", markdownify.ATX)
        options["keep_data_uris"] = options.get("keep_data_uris", False)
        options["url"] = options.get("url", None)
        # Explicitly cast options to the expected type if necessary
        super().__init__(**options)

    def convert_hn(
            self,
            n: int,
            el: Any,
            text: str,
            convert_as_inline: Optional[bool] = False,
            **kwargs,
    ) -> str:
        """Same as usual, but be sure to start with a new line"""
        if not convert_as_inline:
            if not re.search(r"^\n", text):
                return "\n" + super().convert_hn(n, el, text, convert_as_inline)  # type: ignore

        return super().convert_hn(n, el, text, convert_as_inline)  # type: ignore

    def convert_a(
            self,
            el: Any,
            text: str,
            convert_as_inline: Optional[bool] = False,
            **kwargs,
    ):
        """Same as usual converter, but removes Javascript links and escapes URIs."""
        prefix, suffix, text = markdownify.chomp(text)  # type: ignore
        if not text:
            return ""

        if el.find_parent("pre") is not None:
            return text

        href = el.get("href")
        href = self.convert_relative_to_absolute_path(href)
        title = el.get("title")

        # Escape URIs and skip non-http or file schemes
        if href:
            try:
                parsed_url = urlparse(href)  # type: ignore
                if parsed_url.scheme and parsed_url.scheme.lower() not in ["http", "https", "file"]:  # type: ignore
                    return "%s%s%s" % (prefix, text, suffix)
                href = urlunparse(parsed_url._replace(path=quote(unquote(parsed_url.path))))  # type: ignore
            except ValueError:  # It's not clear if this ever gets thrown
                return "%s%s%s" % (prefix, text, suffix)

        # For the replacement see #29: text nodes underscores are escaped
        if (
                self.options["autolinks"]
                and text.replace(r"\_", "_") == href
                and not title
                and not self.options["default_title"]
        ):
            # Shortcut syntax
            return "<%s>" % href
        if self.options["default_title"] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        return (
            "%s[%s](%s%s)%s" % (prefix, text, href, title_part, suffix)
            if href
            else text
        )

    def convert_img(
            self,
            el: Any,
            text: str,
            convert_as_inline: Optional[bool] = False,
            **kwargs,
    ) -> str:
        """Same as usual converter, but removes data URIs"""

        alt = el.attrs.get("alt", None) or ""
        src = el.attrs.get("src", None) or ""
        title = el.attrs.get("title", None) or ""
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        if (
                convert_as_inline
                and el.parent.name not in self.options["keep_inline_images_in"]
        ):
            return alt

        # Remove dataURIs
        if src.startswith("data:") and not self.options["keep_data_uris"]:
            src = src.split(",")[0] + "..."

        src = self.convert_relative_to_absolute_path(src)

        return "![%s](%s%s)" % (alt, src, title_part)

    def convert_relative_to_absolute_path(self, path: str) -> str:
        """
        Convert a relative path to an absolute path based on the current URL.
        """
        if not path or not self.options["url"]:
            return path

        try:
            parsed_url = urlparse(path)
            if parsed_url.netloc:
                return path

            parsed_base = urlparse(self.options["url"])
            if path.startswith("/"):
                new_path = path
            else:
                base_path = parsed_base.path.rsplit("/", 1)[0] if parsed_base.path else ""
                new_path = f"{base_path}/{path}"

            # Handle path normalization: remove redundant slashes and dots
            normalized_path = re.sub(r'(?<!:)/{2,}', '/', new_path.replace("\\", "/"))
            
            # Security note: Consider validating or sanitizing normalized_path before use
            # in case of path traversal attempts (e.g., ../../etc/passwd)
            
            return parsed_base._replace(path=normalized_path).geturl()
        except Exception as e:
            # Improve logging with specific error type and message for easier debugging
            # Example: logging.warning(f"Path conversion error: {type(e).__name__}: {str(e)}")
            return path

    def convert_soup(self, soup: Any) -> str:
        return super().convert_soup(soup)  # type: ignore
