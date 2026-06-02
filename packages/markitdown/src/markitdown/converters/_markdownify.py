import base64
import hashlib
import os
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
    - Saving data:uri images to disk when `save_images_dir` is set.
    - Ensuring URIs are properly escaped, and do not conflict with Markdown syntax
    """

    def __init__(self, **options: Any):
        options["heading_style"] = options.get("heading_style", markdownify.ATX)
        options["keep_data_uris"] = options.get("keep_data_uris", False)
        self._save_images_dir = options.pop("save_images_dir", None)
        self._image_counter = 0
        if self._save_images_dir:
            os.makedirs(self._save_images_dir, exist_ok=True)
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
        src = el.attrs.get("src", None) or el.attrs.get("data-src", None) or ""
        title = el.attrs.get("title", None) or ""
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        # Remove all line breaks from alt
        alt = alt.replace("\n", " ")
        if (
            convert_as_inline
            and el.parent.name not in self.options["keep_inline_images_in"]
        ):
            return alt

        # Handle dataURIs
        if src.startswith("data:"):
            if self._save_images_dir and not self.options["keep_data_uris"]:
                # Save image to disk with relative link
                src = self._save_data_image(src)
            elif not self.options["keep_data_uris"]:
                src = src.split(",")[0] + "..."
            
        return "![%s](%s%s)" % (alt, src, title_part)
    
    def _save_data_image(self, data_uri: str) -> str:
        """Decode a data: URI and save it to disk, returning a relative path."""
        header, encoded = data_uri.split(",", 1)
        ext = ".png"
        if "image/" in header:
            mime_type = header.split(";")[0].split(":")[1]
            ext_map = {
                "image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg",
                "image/gif": ".gif", "image/webp": ".webp", "image/svg+xml": ".svg",
                "image/bmp": ".bmp", "image/tiff": ".tiff",
            }
            ext = ext_map.get(mime_type, ".png")
        
        img_data = base64.b64decode(encoded)
        img_hash = hashlib.md5(img_data).hexdigest()[:8]
        filename = f"image_{self._image_counter}_{img_hash}{ext}"
        self._image_counter += 1
        
        filepath = os.path.join(self._save_images_dir, filename)
        with open(filepath, "wb") as f:
            f.write(img_data)
        
        return os.path.join(os.path.basename(self._save_images_dir), filename)

    def convert_input(
        self,
        el: Any,
        text: str,
        convert_as_inline: Optional[bool] = False,
        **kwargs,
    ) -> str:
        """Convert checkboxes to Markdown [x]/[ ] syntax."""

        if el.get("type") == "checkbox":
            return "[x] " if el.has_attr("checked") else "[ ] "
        return ""

    def convert_soup(self, soup: Any) -> str:
        return super().convert_soup(soup)  # type: ignore
