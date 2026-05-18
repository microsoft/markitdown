from typing import BinaryIO, Any, Union
import base64
import logging
import mimetypes
from ._exiftool import exiftool_metadata
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._exceptions import FileConversionException
from .._stream_info import StreamInfo

logger = logging.getLogger(__name__)

ACCEPTED_MIME_TYPE_PREFIXES = [
    "image/jpeg",
    "image/png",
]

ACCEPTED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


class ImageConverter(DocumentConverter):
    """
    Converts images to markdown via extraction of metadata (if `exiftool` is installed), and description via a multimodal LLM (if an llm_client is configured).
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
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        md_content = ""

        # Add metadata
        try:
            metadata = exiftool_metadata(
                file_stream, exiftool_path=kwargs.get("exiftool_path")
            )
        except Exception as e:
            logger.warning("ImageConverter: exiftool metadata extraction failed: %s", e)
            metadata = None

        if metadata:
            for f in [
                "ImageSize",
                "Title",
                "Caption",
                "Description",
                "Keywords",
                "Artist",
                "Author",
                "DateTimeOriginal",
                "CreateDate",
                "GPSPosition",
            ]:
                if f in metadata:
                    md_content += f"{f}: {metadata[f]}\n"

        # Try describing the image with GPT
        llm_client = kwargs.get("llm_client")
        llm_model = kwargs.get("llm_model")
        if llm_client is not None and llm_model is not None:
            try:
                llm_description = self._get_llm_description(
                    file_stream,
                    stream_info,
                    client=llm_client,
                    model=llm_model,
                    prompt=kwargs.get("llm_prompt"),
                )
            except Exception as e:
                logger.warning(
                    "ImageConverter: LLM description failed for %s: %s",
                    getattr(stream_info, "extension", "?"),
                    e,
                )
                llm_description = None

            if llm_description is not None:
                md_content += "\n# Description:\n" + llm_description.strip() + "\n"

        return DocumentConverterResult(
            markdown=md_content,
        )

    def _get_llm_description(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        *,
        client,
        model,
        prompt=None,
    ) -> Union[None, str]:
        if prompt is None or prompt.strip() == "":
            prompt = "Write a detailed caption for this image."

        # Get the content type
        content_type = stream_info.mimetype
        if not content_type:
            try:
                content_type, _ = mimetypes.guess_type(
                    "_dummy" + (stream_info.extension or "")
                )
            except Exception:
                content_type = None
        if not content_type:
            content_type = "application/octet-stream"

        # Convert to base64
        cur_pos = 0
        try:
            cur_pos = file_stream.tell()
        except (OSError, AttributeError):
            pass

        try:
            image_data = file_stream.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
        except (OSError, ValueError) as e:
            logger.warning("ImageConverter: base64 encoding failed: %s", e)
            return None
        finally:
            try:
                file_stream.seek(cur_pos)
            except (OSError, AttributeError):
                pass

        # Prepare the data-uri
        data_uri = f"data:{content_type};base64,{base64_image}"

        # Prepare the OpenAI API request
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_uri,
                        },
                    },
                ],
            }
        ]

        # Call the OpenAI API (with error handling for network/auth/rate-limit)
        try:
            response = client.chat.completions.create(model=model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(
                "ImageConverter: LLM API call failed for %s: %s",
                getattr(stream_info, "extension", "?"),
                e,
            )
            return None
