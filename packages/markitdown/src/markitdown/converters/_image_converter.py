from typing import BinaryIO, Any, Union, Optional, Dict
import base64
import mimetypes
import io
import os
from warnings import warn
from ._exiftool import exiftool_metadata
from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ..bbox import BBoxDoc, BBoxPage, BBoxLine, BBoxWord

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
        *,
        emit_bbox: bool = False,
        ocr_lang: Optional[str] = None,
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

        bbox_doc: Optional[BBoxDoc] = None
        if emit_bbox:
            try:
                from PIL import Image
                import pytesseract
                from pytesseract import Output
            except Exception:
                warn("emit_bbox requested but pytesseract/Pillow not installed; skipping bbox output")
            else:
                cur_pos = file_stream.tell()
                file_stream.seek(0)
                img = Image.open(file_stream)
                file_stream.seek(cur_pos)
                width, height = img.size
                lang = ocr_lang or os.getenv("MARKITDOWN_OCR_LANG", "eng")
                df = pytesseract.image_to_data(img, output_type=Output.DATAFRAME, lang=lang)
                line_map: Dict[int, int] = {}
                tmp: Dict[int, Dict[str, Any]] = {}
                words: list[BBoxWord] = []
                for _, row in df[df.level == 5].iterrows():
                    text = str(row["text"]).strip()
                    if not text:
                        continue
                    left, top, w, h = int(row.left), int(row.top), int(row.width), int(row.height)
                    x1, y1, x2, y2 = left, top, left + w, top + h
                    conf = float(row.conf) if row.conf != -1 else None
                    bbox_abs = [x1, y1, x2, y2]
                    bbox_norm = [x1 / width, y1 / height, w / width, h / height]
                    key = int(row.line_num)
                    line_id = line_map.setdefault(key, len(line_map))
                    t = tmp.setdefault(
                        key,
                        {"page": 1, "words": [], "minx": x1, "miny": y1, "maxx": x2, "maxy": y2},
                    )
                    t["minx"] = min(t["minx"], x1)
                    t["miny"] = min(t["miny"], y1)
                    t["maxx"] = max(t["maxx"], x2)
                    t["maxy"] = max(t["maxy"], y2)
                    t["words"].append(text)
                    words.append(
                        BBoxWord(
                            page=1,
                            text=text,
                            bbox_norm=bbox_norm,
                            bbox_abs=bbox_abs,
                            confidence=conf,
                            line_id=line_id,
                        )
                    )
                line_list = [None] * len(line_map)
                for key, idx in line_map.items():
                    t = tmp[key]
                    x1, y1, x2, y2 = t["minx"], t["miny"], t["maxx"], t["maxy"]
                    bbox_abs = [x1, y1, x2, y2]
                    bbox_norm = [
                        x1 / width,
                        y1 / height,
                        (x2 - x1) / width,
                        (y2 - y1) / height,
                    ]
                    text_line = " ".join(t["words"]).strip()
                    line_list[idx] = BBoxLine(
                        page=1,
                        text=text_line,
                        bbox_norm=bbox_norm,
                        bbox_abs=bbox_abs,
                        confidence=None,
                        md_span={"start": None, "end": None},
                    )
                bbox_doc = BBoxDoc(
                    source=stream_info.filename or "",
                    pages=[BBoxPage(page=1, width=width, height=height)],
                    lines=line_list,
                    words=words,
                )

        return DocumentConverterResult(markdown=md_content, bbox=bbox_doc)

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
