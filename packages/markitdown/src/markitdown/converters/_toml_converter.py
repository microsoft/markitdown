"""
TOML Converter for MarkItDown
New feature: Convert TOML config/data files to structured Markdown.
Author: Maishad Hassan (maishad777)
"""
import tomllib
import io
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/toml",
    "text/toml",
]

ACCEPTED_FILE_EXTENSIONS = [".toml"]


class TomlConverter(DocumentConverter):
    """
    Converts TOML files (e.g., pyproject.toml, Cargo.toml, config.toml)
    to structured, human-readable Markdown.
    """

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
        raw = file_stream.read()
        try:
            data = tomllib.loads(raw.decode("utf-8"))
        except Exception as e:
            return DocumentConverterResult(
                markdown=f"*Error parsing TOML: {e}*"
            )

        filename = (stream_info.filename or "TOML File").replace(".toml", "")
        md_lines = [f"# {filename}\n"]
        md_lines.extend(self._render_dict(data, level=2))

        return DocumentConverterResult(
            markdown="\n".join(md_lines),
            title=filename,
        )

    def _render_dict(self, data: dict, level: int = 2) -> list:
        lines = []
        hdr = "#" * min(level, 6)

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"\n{hdr} {key}\n")
                lines.extend(self._render_dict(value, level + 1))
            elif isinstance(value, list):
                lines.append(f"\n**{key}:**")
                for item in value:
                    if isinstance(item, dict):
                        lines.append("")
                        for k, v in item.items():
                            lines.append(f"  - **{k}:** {v}")
                    else:
                        lines.append(f"- {item}")
            else:
                lines.append(f"- **{key}:** {value}")

        return lines
