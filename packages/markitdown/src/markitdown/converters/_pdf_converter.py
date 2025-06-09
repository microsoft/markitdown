import sys

from typing import BinaryIO, Any


from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE
from ._llm_caption import llm_caption

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf"]


class PdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown. Most style information is ignored, so the results are essentially plain-text.
    """

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

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Check the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        cur_pos = file_stream.tell()
        markdown = pdfminer.high_level.extract_text(file_stream)
        if markdown.strip() == "":
            # Try to leverage LLM OCR capabilities when PDF is not searchable
            llm_client = kwargs.get("llm_client")
            llm_model = kwargs.get("llm_model")
            if llm_client and llm_model:
                file_stream.seek(cur_pos)
                llm_prompt = """You are an advanced document extraction AI. Your task is to analyze the provided
                document, understand its content and context, and produce a perfectly structured Markdown document
                from the text within it. Do not translate neither generate new text. Retain the structure of the
                original content, ensuring that sections, titles, headers and important details are clearly separated.
                If the image contains any tables, lists and code snippets format them correctly to preserve their
                original meaning. Only a valid Markdown-formatted output is allowed."""
                markdown = llm_caption(
                    file_stream,
                    stream_info,
                    client=llm_client,
                    model=llm_model,
                    prompt=llm_prompt,
                )

        return DocumentConverterResult(markdown=str(markdown))
