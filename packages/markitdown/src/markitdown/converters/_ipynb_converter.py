from typing import BinaryIO, Any
import json

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import FileConversionException
from .._stream_info import StreamInfo

CANDIDATE_MIME_TYPE_PREFIXES = [
    "application/json",
]

ACCEPTED_FILE_EXTENSIONS = [".ipynb"]


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
                    return self._looks_like_notebook(notebook_content)
                except (ValueError, LookupError):
                    return False
                finally:
                    file_stream.seek(cur_pos)

        return False

    def _looks_like_notebook(self, text: str) -> bool:
        """Decide from the text itself whether it is a notebook.

        A plain JSON file can mention ``nbformat``/``nbformat_minor`` anywhere
        (a docs snippet, a config sample, ...), and latching onto that made us
        return an empty conversion for it. So look at the actual top-level
        keys instead of the raw text.
        """
        # Editors and Windows tooling prepend a BOM, which json rejects
        text = text.lstrip("\ufeff")

        try:
            data = json.loads(text)
        except (ValueError, RecursionError):
            # Not JSON, or nested too deeply for the parser - not a notebook
            return False

        if not isinstance(data, dict):
            return False
        return (
            "nbformat" in data
            and "nbformat_minor" in data
            and isinstance(data.get("cells"), list)
        )

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
                    md_output.append(f"```python\n{''.join(source_lines)}\n```")
                elif cell_type == "raw":
                    md_output.append(f"```\n{''.join(source_lines)}\n```")

            md_text = "\n\n".join(md_output)

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
