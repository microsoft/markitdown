import io
import os
import re
import urllib.request
import warnings
from typing import Any, Optional
from urllib.parse import quote, unquote, urlparse, urlunparse

import markdownify

from .._stream_info import StreamInfo
from ._llm_svg import llm_svg


class _CustomMarkdownify(markdownify.MarkdownConverter):
    """
    A custom version of markdownify's MarkdownConverter. Changes include:

    - Altering the default heading style to use '#', '##', etc.
    - Removing javascript hyperlinks.
    - Truncating images with large data:uri sources.
    - Ensuring URIs are properly escaped, and do not conflict with Markdown syntax
    - Supporting optional local image downloading and sequential renaming.
    - Converting inline <svg> elements to Mermaid diagrams via an LLM (if configured).
    """

    def __init__(self, **options: Any):
        options["heading_style"] = options.get("heading_style", markdownify.ATX)
        options["keep_data_uris"] = options.get("keep_data_uris", False)

        # Options for downloading images locally
        self.download_images: bool = options.pop("download_images", False)
        self.output_dir: str = options.pop("output_dir", ".")
        self.image_folder: str = options.pop("image_folder", "images")
        self.image_counter: int = 0

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
        """Same as usual converter, but removes JavaScript links and escapes URIs."""
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
        """Same as usual converter, but removes data URIs and handles auto-downloading"""

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

        # Remove dataURIs
        if src.startswith("data:") and not self.options["keep_data_uris"]:
            src = src.split(",")[0] + "..."

        # Download remote images locally and assign a sequential filename if enabled
        if self.download_images and src.startswith(("http://", "https://")):
            try:
                self.image_counter += 1

                # Safe extension extraction and validation
                parsed_path = urlparse(src).path
                ext = os.path.splitext(parsed_path)[1].lower() or ".png"

                ALLOWED_EXTENSIONS = {
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".webp",
                    ".gif",
                    ".svg",
                    ".bmp",
                    ".ico",
                }
                if ext not in ALLOWED_EXTENSIONS:
                    ext = ".png"

                new_filename = f"figure-{self.image_counter:03d}{ext}"

                # Build target directory for physical save
                target_dir = (
                    os.path.join(self.output_dir, self.image_folder)
                    if self.image_folder
                    else self.output_dir
                )
                os.makedirs(target_dir, exist_ok=True)
                full_save_path = os.path.join(target_dir, new_filename)

                req = urllib.request.Request(
                    src,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
                    },
                )
                # Download with timeout to prevent indefinite blocking
                with (
                    urllib.request.urlopen(req, timeout=15) as response,
                    open(full_save_path, "wb") as out_file,
                ):
                    out_file.write(response.read())

                # Build cross-platform relative path for Markdown link
                if self.image_folder:
                    src = os.path.join(self.image_folder, new_filename).replace(
                        "\\", "/"
                    )
                else:
                    src = new_filename
            except Exception as e:
                warnings.warn(
                    f"Could not download image {src}: {e}",
                    RuntimeWarning,
                )

        return "![%s](%s%s)" % (alt, src, title_part)

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

    def convert_svg(
        self,
        el: Any,
        text: str,
        convert_as_inline: Optional[bool] = False,
        **kwargs,
    ) -> str:
        """Convert an inline <svg> element via an LLM to a Mermaid diagram, if configured."""
        llm_client = self.options.get("llm_client")
        llm_model = self.options.get("llm_model")
        svg_source = str(el)

        if llm_client is not None and llm_model is not None:
            stream = io.BytesIO(svg_source.encode("utf-8"))
            stream_info = StreamInfo(
                mimetype="image/svg+xml", extension=".svg", charset="utf-8"
            )
            try:
                mermaid = llm_svg(
                    stream,
                    stream_info,
                    client=llm_client,
                    model=llm_model,
                    prompt=self.options.get("llm_prompt"),
                )
            except Exception:
                mermaid = None

            if mermaid:
                return f"\n\n```mermaid\n{mermaid}\n```\n\n"

        # Fallback: preserve the original inline SVG source when Mermaid extraction fails
        return f"\n\n```xml\n{svg_source.strip()}\n```\n\n"

    def convert_soup(self, soup: Any) -> str:
        return super().convert_soup(soup)  # type: ignore
