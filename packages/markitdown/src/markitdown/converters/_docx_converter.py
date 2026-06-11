import sys
import io
import os
import re
import zipfile
from warnings import warn

from typing import BinaryIO, Any

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    import mammoth

except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

ACCEPTED_FILE_EXTENSIONS = [".docx"]


class DocxConverter(HtmlConverter):
    """
    Converts DOCX files to Markdown. Style information (e.g.m headings) and tables are preserved where possible.
    """

    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

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
        # Check: the dependencies
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".docx",
                    feature="docx",
                )
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        extract_images = kwargs.get("extract_images", False)
        media_files: list[str] = []

        # ① 提取阶段：从 ZIP 获取原图（按文档中出现顺序）
        if extract_images:
            file_stream.seek(0)
            zip_bytes = io.BytesIO(file_stream.read())

            with zipfile.ZipFile(zip_bytes) as z:
                media_files = self._get_media_in_doc_order(z)

                if media_files:
                    images_dir = kwargs["images_dir"]
                    os.makedirs(images_dir, exist_ok=True)

                    for i, media_file in enumerate(media_files, 1):
                        ext = os.path.splitext(media_file)[1]
                        if ext.lower() == ".jpeg":
                            ext = ".jpg"
                        if not ext:
                            data = z.read(media_file)
                            ext = self._detect_ext(data)
                        filename = f"image_{i}{ext}"
                        with open(os.path.join(images_dir, filename), "wb") as f:
                            f.write(z.read(media_file))

            file_stream.seek(0)

        # ② mammoth 转 HTML
        style_map = kwargs.get("style_map", None)
        pre_process_stream = pre_process_docx(file_stream)
        html_value = mammoth.convert_to_html(
            pre_process_stream, style_map=style_map
        ).value

        # ③ 替换 base64 → 相对路径
        if extract_images and media_files:
            images_rel = kwargs.get("images_rel_dir", "images")
            for i, media_file in enumerate(media_files, 1):
                ext = os.path.splitext(media_file)[1]
                if ext.lower() == ".jpeg":
                    ext = ".jpg"
                filename = f"image_{i}{ext}"
                # 替换 mammoth 生成的 data: URI 为文件路径
                html_value = re.sub(
                    r'<img([^>]*)src="data:image/[^"]+"',
                    f'<img\\1src="{images_rel}/{filename}"',
                    html_value,
                    count=1,
                )

        # ④ HTML → Markdown
        return self._html_converter.convert_string(html_value, **kwargs)

    @staticmethod
    def _get_media_in_doc_order(z: zipfile.ZipFile) -> list[str]:
        """从 DOCX 的 document.xml.rels 和 document.xml 解析图片在文档中的出现顺序"""
        from xml.etree.ElementTree import fromstring

        try:
            # 1. rels: rId -> media 路径
            rels_xml = z.read("word/_rels/document.xml.rels")
            rels_root = fromstring(rels_xml)
            rid_to_media: dict[str, str] = {}
            for rel in rels_root:
                target = rel.get("Target", "")
                if target.startswith("media/"):
                    rid_to_media[rel.get("Id", "")] = target

            # 2. document.xml: 按出现顺序收集 rId
            doc_xml = z.read("word/document.xml")
            doc_root = fromstring(doc_xml)
            ns_a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
            ns_r = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"

            ordered_media: list[str] = []
            for blip in doc_root.iter(f"{ns_a}blip"):
                rid = blip.get(f"{ns_r}embed")
                if rid and rid in rid_to_media:
                    ordered_media.append(f"word/{rid_to_media[rid]}")

            return ordered_media
        except Exception:
            # fallback: 按文件名数字自然排序
            raw = [f for f in z.namelist() if f.startswith("word/media/") and not f.endswith("/")]
            return sorted(raw, key=lambda p: int("".join(c for c in os.path.basename(p) if c.isdigit()) or "0"))

    @staticmethod
    def _detect_ext(data: bytes) -> str:
        """根据文件头 magic bytes 检测图片格式"""
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            return ".png"
        if data[:2] == b"\xff\xd8":
            return ".jpg"
        if data[:4] == b"GIF8":
            return ".gif"
        if data[:4] == b"RIFF" and len(data) > 12 and data[8:12] == b"WEBP":
            return ".webp"
        if data[:2] == b"BM":
            return ".bmp"
        if data[:4] == b"\x00\x00\x01\x00":
            return ".ico"
        return ".png"  # 默认
