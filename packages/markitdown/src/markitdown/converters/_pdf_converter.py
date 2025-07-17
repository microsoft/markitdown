import sys
import io
from typing import BinaryIO, Any
from PIL import Image
from io import BytesIO
import fitz  # type: ignore[import-untyped]
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

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
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore

        assert isinstance(file_stream, io.IOBase)

        # Extract text
        text = pdfminer.high_level.extract_text(file_stream)

        # Reset stream and load PDF with fitz
        file_stream.seek(0)
        file_bytes = file_stream.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")

        # Prepare image descriptions
        inline_captions = []
        llm_client = kwargs.get("llm_client")
        llm_model = kwargs.get("llm_model", "gpt-4o")  # Default model fallback

        for page_index, page in enumerate(doc):
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                width = base_image.get("width", 0)
                height = base_image.get("height", 0)

                # Skip small images
                if width < 100 or height < 100:
                    continue

                image_stream = BytesIO(image_bytes)

                if llm_client:
                    try:
                        # Assuming llm_client has a method describe_image; if not, modify accordingly
                        response = llm_client.chat.completions.create(
                            model=llm_model,
                            messages=[
                                {
                                    "role": "system",
                                    "content": "You are a helpful assistant that describes images.",
                                },
                                {
                                    "role": "user",
                                    "content": "Describe the image in detail.",
                                },
                            ],
                        )
                        description = response.choices[0].message.content
                    except Exception as e:
                        description = f"Image description failed: {e}"
                else:
                    description = "No LLM client provided for image description."

                caption = f"\n_Image on page {page_index + 1}: {description}_\n"
                inline_captions.append(caption)

        # Combine text and captions
        markdown = text.strip() + "\n\n" + "\n".join(inline_captions)

        return DocumentConverterResult(markdown=markdown)
