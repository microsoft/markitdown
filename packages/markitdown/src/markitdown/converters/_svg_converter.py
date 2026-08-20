from typing import Any, BinaryIO

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ._llm_svg import llm_svg

ACCEPTED_MIME_TYPE_PREFIXES = [
    "image/svg+xml",
    "image/svg",
]

ACCEPTED_FILE_EXTENSIONS = [".svg"]


class SvgConverter(DocumentConverter):
    """
    Converts SVG files to Markdown.
    When an LLM client is configured, attempts to produce a Mermaid diagram.
    Falls back to a fenced xml code block to preserve the SVG source.
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
        llm_client = kwargs.get("llm_client")
        llm_model = kwargs.get("llm_model")

        if llm_client is not None and llm_model is not None:
            try:
                mermaid = llm_svg(
                    file_stream,
                    stream_info,
                    client=llm_client,
                    model=llm_model,
                    prompt=kwargs.get("llm_prompt"),
                )
            except Exception:
                mermaid = None

            if mermaid:
                return DocumentConverterResult(markdown=f"```mermaid\n{mermaid}\n```")

        # Fallback: preserve the SVG source in a fenced xml block
        encoding = stream_info.charset or "utf-8"
        cur_pos = file_stream.tell()
        try:
            svg_text = file_stream.read().decode(encoding, errors="replace")
        finally:
            file_stream.seek(cur_pos)

        return DocumentConverterResult(markdown=f"```xml\n{svg_text.strip()}\n```")
