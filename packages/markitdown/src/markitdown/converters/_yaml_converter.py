import io
from typing import BinaryIO, Any

import yaml
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_FILE_EXTENSIONS = [".yaml", ".yml"]


class YamlConverter(DocumentConverter):
    """Converts YAML files to Markdown."""

    def __init__(self):
        super().__init__()

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        extension = (stream_info.extension or "").lower()
        return extension in ACCEPTED_FILE_EXTENSIONS

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        content = file_stream.read().decode("utf-8")

        try:
            docs = list(yaml.safe_load_all(content))
        except yaml.YAMLError:
            return DocumentConverterResult(markdown="")

        if len(docs) == 1:
            markdown = self._render_value(docs[0])
        else:
            parts = []
            for i, doc in enumerate(docs, 1):
                parts.append(f"---\n\n**Document {i}:**\n\n{self._render_value(doc)}")
            markdown = "\n\n".join(parts)

        return DocumentConverterResult(markdown=markdown.strip())

    def _render_value(self, value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            return self._render_list(value)
        if isinstance(value, dict):
            return self._render_dict(value)
        return str(value)

    def _render_dict(self, data: dict) -> str:
        if not data:
            return ""

        if self._is_table_data(data):
            return self._render_table(data)

        lines = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"**{key}:**")
                lines.append(self._render_value(value))
            else:
                lines.append(f"**{key}:** {self._render_value(value)}")
        return "\n\n".join(lines)

    def _render_list(self, items: list) -> str:
        if not items:
            return ""

        if items and isinstance(items[0], dict):
            if self._is_uniform_dicts(items):
                return self._render_list_table(items)

        lines = []
        for item in items:
            lines.append(f"- {self._render_value(item)}")
        return "\n".join(lines)

    def _is_table_data(self, data: Any) -> bool:
        if isinstance(data, dict):
            values = list(data.values())
            if values and isinstance(values[0], list):
                if values[0] and isinstance(values[0][0], dict):
                    return True
        return False

    def _is_uniform_dicts(self, items: list) -> bool:
        if not items or not isinstance(items[0], dict):
            return False
        keys = set(items[0].keys())
        return len(keys) > 0 and all(isinstance(i, dict) and set(i.keys()) == keys for i in items)

    def _render_table(self, data: dict) -> str:
        headers = list(data.keys())
        rows = list(zip(*[data[h] for h in headers]))

        header_line = "| " + " | ".join(str(h) for h in headers) + " |"
        separator = "| " + " | ".join("---" for _ in headers) + " |"
        data_lines = []
        for row in rows:
            data_lines.append("| " + " | ".join(str(v) for v in row) + " |")

        return "\n".join([header_line, separator] + data_lines)

    def _render_list_table(self, items: list) -> str:
        if not items:
            return ""

        headers = list(items[0].keys())
        header_line = "| " + " | ".join(str(h) for h in headers) + " |"
        separator = "| " + " | ".join("---" for _ in headers) + " |"
        data_lines = []
        for item in items:
            row = [str(item.get(h, "")) for h in headers]
            data_lines.append("| " + " | ".join(row) + " |")

        return "\n".join([header_line, separator] + data_lines)
