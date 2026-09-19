from typing import BinaryIO, Any
import json

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import FileConversionException
from .._stream_info import StreamInfo

CANDIDATE_MIME_TYPE_PREFIXES = [
    "application/json",
]

ACCEPTED_FILE_EXTENSIONS = [".ipynb"]


def _fence_for(text: str) -> str:
    """Pick a backtick fence longer than any backtick run in text.

    A fixed triple-backtick fence breaks when the content itself contains
    a ``` run (a printed markdown example, say): it closes early and the
    rest of the output leaks out as prose.
    """
    longest = 0
    run = 0
    for ch in text:
        if ch == "`":
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return "`" * max(3, longest + 1)


class IpynbConverter(DocumentConverter):
    """Converts Jupyter Notebook (.ipynb) files to Markdown."""

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in CANDIDATE_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                # Read further to see if it's a notebook
                cur_pos = file_stream.tell()
                try:
                    encoding = stream_info.charset or "utf-8"
                    notebook_content = file_stream.read().decode(encoding)
                    return (
                        "nbformat" in notebook_content
                        and "nbformat_minor" in notebook_content
                    )
                except (ValueError, LookupError):
                    return False
                finally:
                    file_stream.seek(cur_pos)

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Parse and convert the notebook
        encoding = stream_info.charset or "utf-8"
        notebook_content = file_stream.read().decode(encoding=encoding)

        # Editors and Windows tooling prepend a UTF-8 BOM, which json rejects
        # outright; strip it so the notebook is read as a notebook.
        notebook_content = notebook_content.lstrip("\ufeff")

        return self._convert(json.loads(notebook_content))



    @staticmethod
    def _render_outputs(outputs: list) -> str:
        """Render a code cell's outputs as markdown, text-bearing ones only."""
        parts: list[str] = []
        for out in outputs:
            if not isinstance(out, dict):
                continue
            out_type = out.get("output_type", "")
            if out_type == "stream":
                text = "".join(out.get("text", []) or [])
                if text.strip():
                    lang = "text" if out.get("name", "stdout") != "stderr" else ""
                    fence = _fence_for(text)
                    parts.append(f"{fence}{lang}\n{text.rstrip()}\n{fence}")
            elif out_type == "error":
                lines = out.get("traceback") or []
                header = f"{out.get('ename', 'Error')}: {out.get('evalue', '')}".rstrip(": ")
                body = "\n".join(lines) if lines else header
                fence = _fence_for(body)
                parts.append(f"{fence}\n{body}\n{fence}")
            elif out_type in ("execute_result", "display_data"):
                data = out.get("data", {}) or {}
                text = "".join(data.get("text/plain", []) or [])
                if text.strip():
                    fence = _fence_for(text)
                    parts.append(f"{fence}\n{text.rstrip()}\n{fence}")
        return "\n\n".join(parts)

    def _convert(self, notebook_content: dict) -> DocumentConverterResult:
        """Helper function that converts notebook JSON content to Markdown."""
        try:
            md_output = []
            title = None

            for cell in notebook_content.get("cells", []):
                cell_type = cell.get("cell_type", "")
                source_lines = cell.get("source", [])

                if cell_type == "markdown":
                    md_output.append("".join(source_lines))

                    # Extract the first # heading as title if not already found
                    if title is None:
                        for line in source_lines:
                            if line.startswith("# "):
                                title = line.removeprefix("# ").strip()
                                break

                elif cell_type == "code":
                    # Code cells are wrapped in Markdown code blocks
                    src = ''.join(source_lines)
                    fence = _fence_for(src)
                    md_output.append(f"{fence}python\n{src}\n{fence}")
                    # Text-bearing outputs (stdout/stderr streams, error
                    # tracebacks, text results) follow their cell so the
                    # notebook's recorded results survive conversion (#2285).
                    md_output.append(self._render_outputs(cell.get("outputs", [])))
                elif cell_type == "raw":
                    src = ''.join(source_lines)
                    fence = _fence_for(src)
                    md_output.append(f"{fence}\n{src}\n{fence}")

            md_text = "\n\n".join(part for part in md_output if part.strip())

            # Check for title in notebook metadata
            title = notebook_content.get("metadata", {}).get("title", title)

            return DocumentConverterResult(
                markdown=md_text,
                title=title,
            )

        except Exception as e:
            raise FileConversionException(
                f"Error converting .ipynb file: {str(e)}"
            ) from e
