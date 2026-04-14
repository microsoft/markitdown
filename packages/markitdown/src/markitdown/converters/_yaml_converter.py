import sys
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from .._stream_info import StreamInfo

_dependency_exc_info = None
try:
    import yaml
except ImportError:
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/yaml",
    "text/yaml",
    "text/x-yaml",
    "application/x-yaml",
]

ACCEPTED_FILE_EXTENSIONS = [".yaml", ".yml"]


def _render_value(value, depth: int = 0) -> str:
    """Recursively render a YAML value to Markdown."""
    indent = "  " * depth
    lines = []
    if isinstance(value, dict):
        for k, v in value.items():
            if isinstance(v, dict):
                lines.append(f"{indent}- **{k}:**")
                lines.append(_render_value(v, depth + 1))
            elif isinstance(v, list):
                lines.append(f"{indent}- **{k}:**")
                lines.append(_render_value(v, depth + 1))
            else:
                lines.append(f"{indent}- **{k}:** {v}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                lines.append(_render_value(item, depth))
            else:
                lines.append(f"{indent}- {item}")
    else:
        lines.append(f"{indent}{value}")
    return "\n".join(lines)


def _yaml_to_markdown(data: Any, title: str = None) -> str:
    """Convert parsed YAML data to Markdown."""
    lines = []
    if title:
        lines.append(f"# {title}\n")

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"\n## {key}\n")
                lines.append(_render_value(value, 0))
            elif isinstance(value, list):
                lines.append(f"\n## {key}\n")
                lines.append(_render_value(value, 0))
            else:
                lines.append(f"- **{key}:** {value}")
    elif isinstance(data, list):
        for item in data:
            lines.append(_render_value(item, 0))
    else:
        lines.append(str(data))

    return "\n".join(lines)


class YamlConverter(DocumentConverter):
    """Converts YAML (.yaml/.yml) files to structured Markdown."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
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
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".yaml",
                    feature="yaml",
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        encoding = stream_info.charset or "utf-8"
        content = file_stream.read().decode(encoding)
        data = yaml.safe_load(content)

        filename = stream_info.filename or ""
        title = filename if filename else None

        markdown = _yaml_to_markdown(data, title=title)
        return DocumentConverterResult(markdown=markdown, title=title)
