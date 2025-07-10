import sys
import io

from typing import BinaryIO, Any


from ._html_converter import HtmlConverter
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
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        assert isinstance(file_stream, io.IOBase)  # for mypy
        try:
            import base64
            from PIL import Image

            import pdfplumber
            import markdownify

            def extract_text_from_pdf(pdf_path):
                markdown_text = ""
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            markdown_text += (
                                markdownify.markdownify(text, heading_style="ATX")
                                + "\n\n"
                            )
                return markdown_text

            def extract_images_from_pdf(pdf_path):
                image_list = []
                with pdfplumber.open(pdf_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        for img in page.images:
                            bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                            cropped_image = page.to_image(resolution=150)
                            image_list.append((i + 1, cropped_image))
                return image_list

            def describe_image_with_llm(image: Image.Image, **kwargs) -> str:
                try:
                    llm_client = kwargs.get("llm_client")
                    llm_model = kwargs.get("llm_model")
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_b64 = base64.b64encode(buffered.getvalue()).decode()

                    response = llm_client.chat.completions.create(
                        model=llm_model,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Write a detailed caption for this image.",
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{img_b64}"
                                        },
                                    },
                                ],
                            }
                        ],
                    )
                    return response.choices[0].message.content
                except Exception:
                    pass

            def convert_pdf_to_markdown_with_images(pdf_path, **kwargs):
                md_text = extract_text_from_pdf(pdf_path)
                images = extract_images_from_pdf(pdf_path)

                for idx, (page_num, image) in enumerate(images):
                    description = describe_image_with_llm(image, **kwargs)
                    md_text += (
                        f"\n\n![Image{idx+1} - Page {page_num}]\n\n> {description}\n"
                    )

                return md_text

            return DocumentConverterResult(
                markdown=convert_pdf_to_markdown_with_images(file_stream, **kwargs)
            )

        except Exception as e:
            return DocumentConverterResult(
                markdown=pdfminer.high_level.extract_text(file_stream),
            )
