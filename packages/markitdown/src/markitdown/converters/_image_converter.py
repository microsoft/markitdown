from typing import BinaryIO, Any
import base64
import mimetypes
from ._exiftool import exiftool_metadata
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

ACCEPTED_MIME_TYPE_PREFIXES = [
    "image/jpeg",
    "image/png",
]

ACCEPTED_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png"]


class ImageConverter(DocumentConverter):
    """
    Converts images to markdown via extraction of metadata (if `exiftool` is installed), and description via a multimodal LLM (if an llm_client is configured).
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

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

        #        # Try describing the image with GPTV
        #        llm_client = kwargs.get("llm_client")
        #        llm_model = kwargs.get("llm_model")
        #        if llm_client is not None and llm_model is not None:
        #            md_content += (
        #                "\n# Description:\n"
        #                + self._get_llm_description(
        #                    local_path,
        #                    extension,
        #                    llm_client,
        #                    llm_model,
        #                    prompt=kwargs.get("llm_prompt"),
        #                ).strip()
        #                + "\n"
        #            )

        return DocumentConverterResult(
            markdown=md_content,
        )


#    def _get_llm_description(self, local_path, extension, client, model, prompt=None):
#        if prompt is None or prompt.strip() == "":
#            prompt = "Write a detailed caption for this image."
#
#        data_uri = ""
#        with open(local_path, "rb") as image_file:
#            content_type, encoding = mimetypes.guess_type("_dummy" + extension)
#            if content_type is None:
#                content_type = "image/jpeg"
#            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
#            data_uri = f"data:{content_type};base64,{image_base64}"
#
#        messages = [
#            {
#                "role": "user",
#                "content": [
#                    {"type": "text", "text": prompt},
#                    {
#                        "type": "image_url",
#                        "image_url": {
#                            "url": data_uri,
#                        },
#                    },
#                ],
#            }
#        ]
#
#        response = client.chat.completions.create(model=model, messages=messages)
#        return response.choices[0].message.content
