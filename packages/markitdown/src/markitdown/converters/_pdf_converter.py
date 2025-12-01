import io
import os
import sys
from typing import Any, BinaryIO, Dict, Optional
from warnings import warn


from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from ..bbox import BBoxDoc, BBoxPage, BBoxLine, BBoxWord
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
        *,
        emit_bbox: bool = False,
        ocr_lang: Optional[str] = None,
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

        data = file_stream.read()
        markdown = pdfminer.high_level.extract_text(io.BytesIO(data))

        bbox_doc: Optional[BBoxDoc] = None
        if emit_bbox:
            try:
                import pdfplumber  # type: ignore
            except Exception:
                warn(
                    "emit_bbox requested but pdfplumber is not installed; skipping bbox output",
                )
                emit_bbox = False

        if emit_bbox:
            with pdfplumber.open(io.BytesIO(data)) as doc:
                pages: list[BBoxPage] = []
                lines: list[BBoxLine] = []
                words: list[BBoxWord] = []
                plain_lines: list[str] = []

                for pno, page in enumerate(doc.pages):
                    wlist = page.extract_words(use_text_flow=True)
                    base_line_id = len(lines)

                    if len(wlist) == 0:
                        try:
                            from PIL import Image
                            import pytesseract
                            from pytesseract import Output
                        except Exception:
                            warn(
                                "emit_bbox requested but pytesseract/Pillow not available; skipping bbox output",
                            )
                            continue
                        img = page.to_image(resolution=200).original
                        width, height = img.width, img.height
                        pages.append(BBoxPage(page=pno + 1, width=width, height=height))
                        lang = ocr_lang or os.getenv("MARKITDOWN_OCR_LANG", "eng")
                        df = pytesseract.image_to_data(
                            img, output_type=Output.DATAFRAME, lang=lang
                        )
                        line_map: Dict[int, int] = {}
                        tmp: Dict[int, Dict[str, Any]] = {}
                        for _, row in df[df.level == 5].iterrows():
                            text = str(row["text"]).strip()
                            if not text:
                                continue
                            left, top, widthw, heighth = (
                                int(row.left),
                                int(row.top),
                                int(row.width),
                                int(row.height),
                            )
                            conf = float(row.conf) if row.conf != -1 else None
                            x1, y1, x2, y2 = left, top, left + widthw, top + heighth
                            bbox_abs = [x1, y1, x2, y2]
                            bbox_norm = [
                                x1 / width,
                                y1 / height,
                                widthw / width,
                                heighth / height,
                            ]
                            key = int(row.line_num)
                            line_id = line_map.setdefault(
                                key, base_line_id + len(line_map)
                            )
                            t = tmp.setdefault(
                                line_id,
                                {
                                    "page": pno + 1,
                                    "words": [],
                                    "minx": x1,
                                    "miny": y1,
                                    "maxx": x2,
                                    "maxy": y2,
                                },
                            )
                            t["minx"] = min(t["minx"], x1)
                            t["miny"] = min(t["miny"], y1)
                            t["maxx"] = max(t["maxx"], x2)
                            t["maxy"] = max(t["maxy"], y2)
                            t["words"].append(text)
                            words.append(
                                BBoxWord(
                                    page=pno + 1,
                                    text=text,
                                    bbox_norm=bbox_norm,
                                    bbox_abs=bbox_abs,
                                    confidence=conf,
                                    line_id=line_id,
                                )
                            )
                        for idx in sorted(tmp.keys()):
                            t = tmp[idx]
                            x1, y1, x2, y2 = (
                                t["minx"],
                                t["miny"],
                                t["maxx"],
                                t["maxy"],
                            )
                            bbox_abs = [x1, y1, x2, y2]
                            bbox_norm = [
                                x1 / width,
                                y1 / height,
                                (x2 - x1) / width,
                                (y2 - y1) / height,
                            ]
                            text_line = " ".join(t["words"]).strip()
                            lines.append(
                                BBoxLine(
                                    page=pno + 1,
                                    text=text_line,
                                    bbox_norm=bbox_norm,
                                    bbox_abs=bbox_abs,
                                    confidence=None,
                                    md_span={"start": None, "end": None},
                                )
                            )
                            plain_lines.append(text_line)
                    else:
                        width, height = float(page.width), float(page.height)
                        pages.append(
                            BBoxPage(page=pno + 1, width=width, height=height)
                        )
                        sorted_words = sorted(
                            wlist, key=lambda w: (float(w["top"]), float(w["x0"]))
                        )
                        tmp: Dict[int, Dict[str, Any]] = {}
                        current_line_id: Optional[int] = None
                        current_top: Optional[float] = None
                        line_tol = 2.0
                        for w in sorted_words:
                            text = str(w.get("text", "")).strip()
                            if not text:
                                continue
                            x0 = float(w["x0"])
                            top = float(w["top"])
                            x1 = float(w["x1"])
                            bottom = float(w["bottom"])
                            if current_top is None or abs(top - current_top) > line_tol:
                                current_line_id = base_line_id + len(tmp)
                                tmp[current_line_id] = {
                                    "page": pno + 1,
                                    "words": [],
                                    "minx": x0,
                                    "miny": top,
                                    "maxx": x1,
                                    "maxy": bottom,
                                }
                                current_top = top
                            t = tmp[current_line_id]
                            t["minx"] = min(t["minx"], x0)
                            t["miny"] = min(t["miny"], top)
                            t["maxx"] = max(t["maxx"], x1)
                            t["maxy"] = max(t["maxy"], bottom)
                            t["words"].append(text)
                            bbox_abs = [x0, top, x1, bottom]
                            bbox_norm = [
                                x0 / width,
                                top / height,
                                (x1 - x0) / width,
                                (bottom - top) / height,
                            ]
                            words.append(
                                BBoxWord(
                                    page=pno + 1,
                                    text=text,
                                    bbox_norm=bbox_norm,
                                    bbox_abs=bbox_abs,
                                    confidence=None,
                                    line_id=current_line_id,
                                )
                            )
                        for idx in sorted(tmp.keys()):
                            t = tmp[idx]
                            x1, y1, x2, y2 = (
                                t["minx"],
                                t["miny"],
                                t["maxx"],
                                t["maxy"],
                            )
                            bbox_abs = [x1, y1, x2, y2]
                            bbox_norm = [
                                x1 / width,
                                y1 / height,
                                (x2 - x1) / width,
                                (y2 - y1) / height,
                            ]
                            text_line = " ".join(t["words"]).strip()
                            lines.append(
                                BBoxLine(
                                    page=pno + 1,
                                    text=text_line,
                                    bbox_norm=bbox_norm,
                                    bbox_abs=bbox_abs,
                                    confidence=None,
                                    md_span={"start": None, "end": None},
                                )
                            )
                            plain_lines.append(text_line)

                bbox_doc = BBoxDoc(
                    source=stream_info.filename or "",
                    pages=pages,
                    lines=lines,
                    words=words,
                )
                if not markdown.strip():
                    markdown = "\n".join(plain_lines)

        return DocumentConverterResult(markdown=markdown, bbox=bbox_doc)
