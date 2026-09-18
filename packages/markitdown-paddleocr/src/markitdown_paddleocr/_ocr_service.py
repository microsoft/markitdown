import tempfile
from dataclasses import dataclass
from typing import Any, BinaryIO


@dataclass
class OCRResult:
    text: str
    backend_used: str | None = None
    error: str | None = None


class PaddleOCRService:
    """Lazy PaddleOCR wrapper used by the plugin."""

    def __init__(
        self,
        *,
        lang: str = "ch",
        paddleocr_kwargs: dict[str, Any] | None = None,
        ocr_instance: Any | None = None,
    ) -> None:
        self._lang = lang
        self._paddleocr_kwargs = paddleocr_kwargs or {}
        self._ocr_instance = ocr_instance

    def _get_ocr_instance(self) -> Any:
        if self._ocr_instance is None:
            from paddleocr import PaddleOCR

            init_kwargs = {"lang": self._lang}
            init_kwargs.update(self._paddleocr_kwargs)
            self._ocr_instance = PaddleOCR(**init_kwargs)
        return self._ocr_instance

    def extract_text(self, image_stream: BinaryIO) -> OCRResult:
        cur_pos = image_stream.tell()
        try:
            image_stream.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
                tmp.write(image_stream.read())
                tmp.flush()
                raw_result = self._get_ocr_instance().predict(tmp.name)
            text = self._result_to_text(raw_result)
            return OCRResult(text=text, backend_used="paddleocr")
        except Exception as exc:
            return OCRResult(text="", backend_used="paddleocr", error=str(exc))
        finally:
            image_stream.seek(cur_pos)

    def _result_to_text(self, raw_result: Any) -> str:
        lines = self._extract_text_lines(raw_result)
        cleaned = [line.strip() for line in lines if isinstance(line, str) and line.strip()]
        return "\n".join(cleaned)

    def _extract_text_lines(self, node: Any) -> list[str]:
        if node is None:
            return []

        if isinstance(node, str):
            return [node]

        if isinstance(node, dict):
            if "rec_texts" in node and isinstance(node["rec_texts"], list):
                return [str(item) for item in node["rec_texts"]]
            if "rec_text" in node and node["rec_text"]:
                return [str(node["rec_text"])]
            lines: list[str] = []
            for value in node.values():
                lines.extend(self._extract_text_lines(value))
            return lines

        if hasattr(node, "res"):
            return self._extract_text_lines(node.res)

        if isinstance(node, (list, tuple)):
            lines: list[str] = []
            for item in node:
                lines.extend(self._extract_text_lines(item))
            return lines

        return []
