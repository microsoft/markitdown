import sys
import io
import os
import re
import base64
import hashlib
from warnings import warn
from typing import BinaryIO, Any

from ._html_converter import HtmlConverter
from ..converter_utils.docx.pre_process import pre_process_docx
from .._base_converter import DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

_dependency_exc_info = None
try:
    import mammoth
except ImportError:
    _dependency_exc_info = sys.exc_info()

ACCEPTED_MIME_TYPE_PREFIXES = ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
ACCEPTED_FILE_EXTENSIONS = [".docx"]

class DocxConverter(HtmlConverter):
    def __init__(self):
        super().__init__()
        self._html_converter = HtmlConverter()

    def accepts(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any) -> bool:
        extension = (stream_info.extension or "").lower()
        if extension in ACCEPTED_FILE_EXTENSIONS: return True
        mimetype = (stream_info.mimetype or "").lower()
        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix): return True
        return False

    def convert(self, file_stream: BinaryIO, stream_info: StreamInfo, **kwargs: Any) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(MISSING_DEPENDENCY_MESSAGE.format(converter=type(self).__name__, extension=".docx", feature="docx")) from _dependency_exc_info[1].with_traceback(_dependency_exc_info[2])

        # --- HYBRID IMAGE HANDLER ---
        # Yerel dosya yolunu önce 'local_path'ten, yoksa 'url'den al
        file_url = stream_info.local_path or stream_info.url or "document"
        base_name = os.path.splitext(os.path.basename(file_url))[0]
        
        # Akilli klasör ismi (Uzun isimleri buda + hash ekle)
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', base_name)
        if len(clean_name) > 20:
             short_hash = hashlib.md5(base_name.encode()).hexdigest()[:4]
             clean_name = f"{clean_name[:15]}_{short_hash}"
        
        assets_dir_name = f"{clean_name}_assets"
        
        # Kesin çözüm: Dosya yolunu mutlak (absolute) hale getir ve onun klasörünü baz al
        abs_file_path = os.path.abspath(file_url)
        base_dir = os.path.dirname(abs_file_path)
        assets_path = os.path.join(base_dir, assets_dir_name)
        
        image_counter = 0

        def convert_image(image):
            nonlocal image_counter
            image_counter += 1
            with image.open() as image_bytes:
                data = image_bytes.read()
                size_kb = len(data) / 1024
                
                # KÜÇÜK RESİM: Base64 yap (Eşik: 50 KB)
                if size_kb < 50:
                    base64_data = base64.b64encode(data).decode("ascii")
                    return {"src": f"data:{image.content_type};base64,{base64_data}"}
                
                # BÜYÜK RESİM: Klasöre çıkart
                if not os.path.exists(assets_path):
                    os.makedirs(assets_path, exist_ok=True)
                
                ext = image.content_type.split("/")[-1] if "/" in image.content_type else "png"
                img_filename = f"image_{image_counter}.{ext}"
                img_full_path = os.path.join(assets_path, img_filename)
                
                with open(img_full_path, "wb") as f:
                    f.write(data)
                
                # Markdown içinde klasör referansi ver
                return {"src": f"./{assets_dir_name}/{img_filename}"}

        style_map = kwargs.get("style_map", None)
        pre_process_stream = pre_process_docx(file_stream)
        
        # Mammoth'a bizim akilli handler'i veriyoruz
        html_result = mammoth.convert_to_html(
            pre_process_stream, 
            style_map=style_map,
            convert_image=mammoth.images.img_element(convert_image)
        )
        
        return self._html_converter.convert_string(html_result.value, **kwargs)
