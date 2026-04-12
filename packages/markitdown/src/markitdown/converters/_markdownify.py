import re
from typing import Any
from urllib.parse import quote, unquote, urlparse, urlunparse

import markdownify


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
        # Explicitly cast options to the expected type if necessary
        super().__init__(**options)

    def convert_hn(
        self,
        n: int,
        el: Any,
        text: str,
        convert_as_inline: bool | None = False,
        **kwargs,
    ) -> str:
        """Same as usual, but be sure to start with a new line"""
        if not convert_as_inline and not re.search(r"^\n", text):
            return "\n" + super().convert_hn(n, el, text, convert_as_inline)  # type: ignore

        return super().convert_hn(n, el, text, convert_as_inline)  # type: ignore

    def convert_a(
        self,
        el: Any,
        text: str,
        convert_as_inline: bool | None = False,
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
                if parsed_url.scheme and parsed_url.scheme.lower() not in [
                    "http",
                    "https",
                    "file",
                ]:  # type: ignore
                    return f"{prefix}{text}{suffix}"
                href = urlunparse(
                    parsed_url._replace(path=quote(unquote(parsed_url.path)))
                )  # type: ignore
            except ValueError:  # It's not clear if this ever gets thrown
                return f"{prefix}{text}{suffix}"

        # For the replacement see #29: text nodes underscores are escaped
        if (
            self.options["autolinks"]
            and text.replace(r"\_", "_") == href
            and not title
            and not self.options["default_title"]
        ):
            # Shortcut syntax
            return f"<{href}>"
        if self.options["default_title"] and not title:
            title = href
        escaped_title = title.replace('"', r"\"")
        title_part = f' "{escaped_title}"' if title else ""
        return f"{prefix}[{text}]({href}{title_part}{suffix})" if href else text

    def convert_img(
        self,
        el: Any,
        text: str,
        convert_as_inline: bool | None = False,
        **kwargs,
    ) -> str:
        """Same as usual converter, but removes data URIs"""

        alt = el.attrs.get("alt", None) or ""
        src = el.attrs.get("src", None) or el.attrs.get("data-src", None) or ""
        title = el.attrs.get("title", None) or ""
        escaped_title = title.replace('"', r"\"")
        title_part = f' "{escaped_title}"' if title else ""
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

        return f"![{alt}]({src}{title_part})"

    def convert_input(
        self,
        el: Any,
        text: str,
        convert_as_inline: bool | None = False,
        **kwargs,
    ) -> str:
        """Convert checkboxes to Markdown [x]/[ ] syntax."""

        if el.get("type") == "checkbox":
            return "[x] " if el.has_attr("checked") else "[ ] "
        return ""

    def convert_soup(self, soup: Any) -> str:
        return super().convert_soup(soup)  # type: ignore
