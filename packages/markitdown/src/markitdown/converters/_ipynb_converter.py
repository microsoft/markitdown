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

    def _convert(self, notebook_content: dict) -> DocumentConverterResult:
        """Helper function that converts notebook JSON content to Markdown."""
        try:
            md_output = []
            title = None

            for cell in notebook_content.get("cells", []):
                cell_type = cell.get("cell_type", "")
                # nbformat's `multiline_string` is a string *or* a list of lines, and
                # both are valid; `nbformat.reads` keeps whichever the file used.
                # Joining the list and taking the string as-is give the same text.
                source = cell.get("source", [])
                source_text = source if isinstance(source, str) else "".join(source)

                if cell_type == "markdown":
                    md_output.append(source_text)

                    # Extract the first # heading as title if not already found.
                    # Split the text rather than walking the raw value: a string
                    # source would otherwise be iterated one character at a time,
                    # and a list entry holding several lines would hide a heading
                    # that is not on its first one.
                    if title is None:
                        for line in source_text.split("\n"):
                            if line.startswith("# "):
                                title = line.removeprefix("# ").strip()
                                break

                elif cell_type == "code":
                    # Code cells are wrapped in Markdown code blocks
                    md_output.append(f"```python\n{source_text}\n```")
                elif cell_type == "raw":
                    md_output.append(f"```\n{source_text}\n```")

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
