"""
.env / dotenv File Converter for MarkItDown
New feature: Convert .env files to a redacted Markdown table (values are masked for security).
Author: Maishad Hassan (maishad777)
"""
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_FILE_EXTENSIONS = [".env", ".env.example", ".env.sample", ".env.local"]


class EnvConverter(DocumentConverter):
    """
    Converts .env / dotenv files to a Markdown table.
    Values are masked by default to prevent secrets from leaking into LLM context.
    Pass `show_values=True` as a kwarg to reveal values.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        extension = (stream_info.extension or "").lower()
        filename = (stream_info.filename or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        # Match filenames like .env, .env.local etc.
        for ext in ACCEPTED_FILE_EXTENSIONS:
            if filename.endswith(ext):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        show_values = kwargs.get("show_values", False)
        raw = file_stream.read().decode("utf-8", errors="replace")
        lines = raw.splitlines()

        rows = []
        comments = []

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                if stripped.startswith("#"):
                    comments.append(stripped[1:].strip())
                continue

            if "=" in stripped:
                key, _, value = stripped.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                masked = value if show_values else ("*" * min(len(value), 8) if value else "_(empty)_")
                rows.append((key, masked))

        if not rows:
            return DocumentConverterResult(markdown="*No environment variables found.*")

        filename = stream_info.filename or ".env"
        md_lines = [f"# Environment Variables: `{filename}`\n"]

        if not show_values:
            md_lines.append("> ⚠️ Values are masked for security. Pass `show_values=True` to reveal.\n")

        if comments:
            md_lines.append("**File description:** " + " ".join(comments[:3]) + "\n")

        md_lines.append("| Variable | Value |")
        md_lines.append("|---|---|")
        for key, val in rows:
            md_lines.append(f"| `{key}` | `{val}` |")

        return DocumentConverterResult(
            markdown="\n".join(md_lines),
            title=f"Env: {filename}",
        )
