"""YAML document converter for MarkItDown."""

import io
from typing import Any, Union

from markitdown._base_converter import DocumentConverter, DocumentConverterResult
from markitdown._stream_info import StreamInfo


class YamlConverter(DocumentConverter):
    """Converts YAML files to Markdown with syntax highlighting."""

    SUPPORTED_EXTENSIONS = (".yaml", ".yml")

    def accepts(
        self,
        file_stream: io.IOBase,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        """Accept YAML files based on extension."""
        return stream_info.extension in self.SUPPORTED_EXTENSIONS

    def convert(
        self,
        file_stream: io.IOBase,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        """Convert YAML content to Markdown with a fenced code block."""
        content = file_stream.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")

        title = stream_info.filename or "document.yaml"
        markdown = f"# {title}\n\n```yaml\n{content}\n```\n"

        return DocumentConverterResult(title=title, text_content=markdown)


def _parse_yaml_frontmatter(text: str) -> dict[str, Any]:
    """Extract YAML frontmatter from a Markdown-style document."""
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    try:
        import yaml
        return yaml.safe_load(text[3:end]) or {}
    except Exception:
        return {}
