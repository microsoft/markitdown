from typing import BinaryIO, Any, Union, Callable
import base64
import mimetypes
from ._exiftool import exiftool_metadata
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_MIME_TYPE_PREFIXES = [
    "image/jpeg",
    "image/png",
]

ACCEPTED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


class ImageConverter(DocumentConverter):
    """
    Converts images to markdown via extraction of metadata (if `exiftool` is installed), and description via a multimodal LLM.
    The LLM interaction can be customized by passing a callback function.
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
        metadata = exiftool_metadata(
            file_stream, exiftool_path=kwargs.get("exiftool_path")
        )

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

        # Try describing the image with an LLM
        llm_describber = kwargs.get("llm_describber")
        llm_client = kwargs.get("llm_client")
        llm_model = kwargs.get("llm_model")
        llm_prompt = kwargs.get("llm_prompt")
        llm_description = None

        if llm_describber is not None:
            # New, flexible path using a callback
            llm_description = self._get_llm_description_from_callback(
                file_stream,
                stream_info,
                describber=llm_describber,
                prompt=llm_prompt,
            )
        elif llm_client is not None and llm_model is not None:
            # Legacy path for backward compatibility with OpenAI client
            llm_description = self._get_llm_description_openai(
                file_stream,
                stream_info,
                client=llm_client,
                model=llm_model,
                prompt=llm_prompt,
            )

        if llm_description:
            md_content += "\n# Description:\n" + llm_description.strip() + "\n"

        return DocumentConverterResult(
            markdown=md_content,
        )

    def _prepare_data_uri(
        self, file_stream: BinaryIO, stream_info: StreamInfo
    ) -> Union[str, None]:
        """Prepares a data URI from a file stream."""
        # Get the content type
        content_type = stream_info.mimetype
        if not content_type:
            content_type, _ = mimetypes.guess_type(
                "_dummy" + (stream_info.extension or "")
            )
        if not content_type:
            content_type = "application/octet-stream"

        # Convert to base64
        cur_pos = file_stream.tell()
        try:
            base64_image = base64.b64encode(file_stream.read()).decode("utf-8")
        except Exception:
            return None
        finally:
            file_stream.seek(cur_pos)

        return f"data:{content_type};base64,{base64_image}"

    def _get_llm_description_from_callback(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        *,
        describber: Callable[..., Union[str, None]],
        prompt: Union[str, None],
    ) -> Union[str, None]:
        """Gets image description from a user-provided callback function."""
        if prompt is None or prompt.strip() == "":
            prompt = "Write a detailed caption for this image."

        data_uri = self._prepare_data_uri(file_stream, stream_info)
        if not data_uri:
            return None

        try:
            # The callback is responsible for the actual LLM call
            return describber(data_uri=data_uri, prompt=prompt)
        except Exception:
            # Broad exception to safeguard against errors in user-provided code
            return None

    def _get_llm_description_openai(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        *,
        client: Any,
        model: str,
        prompt: Union[str, None],
    ) -> Union[str, None]:
        """Gets image description using the OpenAI client (legacy method)."""
        if prompt is None or prompt.strip() == "":
            prompt = "Write a detailed caption for this image."

        data_uri = self._prepare_data_uri(file_stream, stream_info)
        if not data_uri:
            return None

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

        # Call the OpenAI API
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content
