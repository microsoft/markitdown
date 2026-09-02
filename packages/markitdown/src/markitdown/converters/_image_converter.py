from typing import BinaryIO, Any, Union
import base64
import mimetypes
import os
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
        extract_only = kwargs.get("extract_only", False)

        # --- Extract-only mode: save image to disk, return path reference ---
        if extract_only:
            return self._extract_only(file_stream, stream_info, **kwargs)

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

        # Try describing the image with GPT
        llm_client = kwargs.get("llm_client")
        llm_model = kwargs.get("llm_model")
        if llm_client is not None and llm_model is not None:
            llm_description = self._get_llm_description(
                file_stream,
                stream_info,
                client=llm_client,
                model=llm_model,
                prompt=kwargs.get("llm_prompt"),
            )

            if llm_description is not None:
                md_content += "\n# Description:\n" + llm_description.strip() + "\n"

        return DocumentConverterResult(
            markdown=md_content,
        )

    def _extract_only(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        """Extract image to disk and return a markdown reference with metadata."""
        import tempfile
        import uuid

        # Determine output directory
        image_output_dir = kwargs.get("image_output_dir")
        if image_output_dir is None:
            image_output_dir = tempfile.mkdtemp(prefix="markitdown_images_")

        os.makedirs(image_output_dir, exist_ok=True)

        # Determine file extension
        extension = stream_info.extension or ""
        if not extension:
            ext = mimetypes.guess_extension(stream_info.mimetype or "") or ".png"
        else:
            ext = extension if extension.startswith(".") else "." + extension

        # Generate unique filename
        unique_id = uuid.uuid4().hex[:12]
        filename = f"img_{unique_id}{ext}"
        file_path = os.path.join(image_output_dir, filename)

        # Read image data and collect metadata
        cur_pos = file_stream.tell()
        try:
            image_data = file_stream.read()
        finally:
            file_stream.seek(cur_pos)

        size_bytes = len(image_data)

        # Get image dimensions if possible
        width, height = self._get_image_dimensions(image_data, ext)

        # Write image to disk
        with open(file_path, "wb") as f:
            f.write(image_data)

        # Build markdown output with metadata comment
        md_parts = []
        if width and height:
            md_parts.append(f"<!-- image: {width}x{height}, {size_bytes // 1024}KB -->")
        else:
            md_parts.append(f"<!-- image: {size_bytes // 1024}KB -->")
        md_parts.append(f"![image]({file_path})")

        return DocumentConverterResult(
            markdown="\n".join(md_parts),
        )

    def _get_image_dimensions(
        self, image_data: bytes, ext: str
    ) -> tuple:
        """Try to get image dimensions without external dependencies."""
        try:
            from PIL import Image
            img = Image.open(__import__("io").BytesIO(image_data))
            return img.size  # (width, height)
        except ImportError:
            pass

        # Fallback: try to parse PNG/JPEG headers
        if ext.lower() in (".png",) and len(image_data) >= 24:
            import struct
            try:
                w, h = struct.unpack(">II", image_data[16:24])
                return (w, h)
            except Exception:
                pass

        if ext.lower() in (".jpg", ".jpeg") and len(image_data) > 10:
            try:
                import struct
                idx = 2
                while idx < len(image_data) - 9:
                    if image_data[idx] != 0xFF:
                        break
                    marker = image_data[idx + 1]
                    if marker in (0xC0, 0xC1, 0xC2):
                        h, w = struct.unpack(">HH", image_data[idx + 5:idx + 9])
                        return (w, h)
                    length = struct.unpack(">H", image_data[idx + 2:idx + 4])[0]
                    idx += 2 + length
            except Exception:
                pass

        return (None, None)

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
            content_type, _ = mimetypes.guess_type(
                "_dummy" + (stream_info.extension or "")
            )
        if not content_type:
            content_type = "application/octet-stream"

        # Convert to base64
        cur_pos = file_stream.tell()
        try:
            base64_image = base64.b64encode(file_stream.read()).decode("utf-8")
        except Exception as e:
            return None
        finally:
            file_stream.seek(cur_pos)

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

        # Call the OpenAI API
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content
