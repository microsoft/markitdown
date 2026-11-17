"""
OCR Service Layer for MarkItDown
Provides LLM Vision-based image text extraction.
"""

import base64
import inspect
import re
from typing import Any, BinaryIO
from dataclasses import dataclass

from markitdown import StreamInfo


@dataclass
class OCRResult:
    """Result from OCR extraction."""

    text: str
    confidence: float | None = None
    backend_used: str | None = None
    error: str | None = None


_DEFAULT_PROMPT = (
    "Extract all text from this image. "
    "Return ONLY the extracted text, maintaining the original "
    "layout and order. Do not add any commentary or description."
)

# MiniCPM-OCR is trained on region prompts, but also handles full pages.
# A Markdown-oriented prompt preserves tables and formulas that a
# text-only prompt flattens into loose lines. This wording was checked
# against scanned reports, forms, invoices, and formulas.
_MINICPM_OCR_PROMPT = (
    "Convert this page to Markdown, preserving tables as Markdown "
    "tables and formulas as LaTeX."
)

_OTSL_BLOCK_RE = re.compile(r"<otsl>(?P<body>.*?)</otsl>", re.DOTALL)
_OTSL_TAG_RE = re.compile(r"(<fcel>|<ecel>|<lcel>|<ucel>|<xcel>|<nl>)")
_FENCED_BLOCK_RE = re.compile(
    r"```[A-Za-z0-9_-]*[ \t]*\n?(?P<body>.*?)\n?```",
    re.DOTALL,
)
_LEADING_THINK_RE = re.compile(r"^\s*<think>.*?</think>\s*", re.DOTALL | re.IGNORECASE)


class LLMVisionOCRService:
    """OCR service using LLM vision models (OpenAI-compatible)."""

    backend_used = "llm_vision"

    def __init__(
        self,
        client: Any,
        model: str,
        default_prompt: str | None = None,
    ) -> None:
        """
        Initialize LLM Vision OCR service.

        Args:
            client: OpenAI-compatible client
            model: Model name (e.g., 'gpt-4o', 'gemini-2.0-flash')
            default_prompt: Default prompt for OCR extraction
        """
        self.client = client
        self.model = model
        self.default_prompt = default_prompt or _DEFAULT_PROMPT

    def _build_messages(self, prompt: str, data_uri: str) -> list[dict[str, Any]]:
        """Build the chat messages sent to the vision model."""
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": data_uri},
                    },
                ],
            }
        ]

    def _create_completion(self, messages: list[dict[str, Any]]) -> Any:
        """Send one OCR request to the configured client."""
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

    def _postprocess(self, text: str | None) -> str:
        """Normalize the model response before it is used as OCR text."""
        return text.strip() if text else ""

    def extract_text(
        self,
        image_stream: BinaryIO,
        prompt: str | None = None,
        stream_info: StreamInfo | None = None,
        **kwargs: Any,
    ) -> OCRResult:
        """Extract text using LLM vision."""
        if self.client is None:
            return OCRResult(
                text="",
                backend_used=self.backend_used,
                error="LLM client not configured",
            )

        try:
            image_stream.seek(0)

            content_type: str | None = None
            if stream_info:
                content_type = stream_info.mimetype

            if not content_type:
                try:
                    from PIL import Image

                    image_stream.seek(0)
                    img = Image.open(image_stream)
                    fmt = img.format.lower() if img.format else "png"
                    content_type = f"image/{fmt}"
                except Exception:
                    content_type = "image/png"

            image_stream.seek(0)
            base64_image = base64.b64encode(image_stream.read()).decode("utf-8")
            data_uri = f"data:{content_type};base64,{base64_image}"

            actual_prompt = prompt or self.default_prompt
            response = self._create_completion(
                self._build_messages(actual_prompt, data_uri)
            )

            return OCRResult(
                text=self._postprocess(response.choices[0].message.content),
                backend_used=self.backend_used,
            )
        except Exception as e:
            return OCRResult(text="", backend_used=self.backend_used, error=str(e))
        finally:
            image_stream.seek(0)


class MiniCPMOCRService(LLMVisionOCRService):
    """OCR service tuned for locally served MiniCPM-OCR models."""

    backend_used = "minicpm_ocr"

    def __init__(
        self,
        client: Any,
        model: str,
        default_prompt: str | None = None,
    ) -> None:
        super().__init__(
            client=client,
            model=model,
            default_prompt=default_prompt or _MINICPM_OCR_PROMPT,
        )

    def _build_messages(self, prompt: str, data_uri: str) -> list[dict[str, Any]]:
        # MiniCPM-OCR expects the image before the instruction.
        return [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": data_uri},
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]

    def _create_completion(self, messages: list[dict[str, Any]]) -> Any:
        # Low-temperature decoding keeps OCR output stable across retries.
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.01,
            top_p=0.001,
        )

    def _postprocess(self, text: str | None) -> str:
        return _normalize_minicpm_text(text)


def _normalize_minicpm_text(text: str | None) -> str:
    """Normalize MiniCPM-OCR output, including OTSL tables."""
    if not text:
        return ""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    normalized = _LEADING_THINK_RE.sub("", normalized)
    normalized = _FENCED_BLOCK_RE.sub(_replace_fenced_otsl, normalized)
    normalized = _OTSL_BLOCK_RE.sub(_replace_otsl_block, normalized)
    return re.sub(r"\n{3,}", "\n\n", normalized).strip()


def _replace_otsl_block(match: re.Match[str]) -> str:
    """Replace one OTSL block with a table padded by blank lines."""
    return "\n\n" + _otsl_to_markdown(match.group("body")) + "\n\n"


def _replace_fenced_otsl(match: re.Match[str]) -> str:
    """Unwrap a code fence only when it contains OTSL table markup."""
    body = match.group("body")
    converted = _OTSL_BLOCK_RE.sub(_replace_otsl_block, body)
    return converted if converted != body else match.group(0)


def _escape_table_pipes(text: str) -> str:
    """Escape pipes while preserving preceding backslashes in table cells."""
    output: list[str] = []
    index = 0
    while index < len(text):
        if text[index] == "\\":
            end = index
            while end < len(text) and text[end] == "\\":
                end += 1
            run_length = end - index
            if end < len(text) and text[end] == "|":
                # A literal backslash needs two source characters, and the
                # pipe needs one more escape before it.
                output.append("\\" * (2 * run_length + 1) + "|")
                index = end + 1
            else:
                output.append(text[index:end])
                index = end
        elif text[index] == "|":
            output.append("\\|")
            index += 1
        else:
            output.append(text[index])
            index += 1
    return "".join(output)


def _otsl_to_markdown(body: str) -> str:
    """Convert MiniCPM-OCR OTSL table markup into a Markdown table."""
    rows: list[list[str]] = []
    row: list[str] = []
    cell_open = False

    for token in _OTSL_TAG_RE.split(body):
        if token == "<fcel>":
            cell_open = False
            row.append("")
            cell_open = True
        elif token in {"<ecel>", "<lcel>", "<ucel>", "<xcel>"}:
            cell_open = False
            row.append("")
        elif token == "<nl>":
            cell_open = False
            if row:
                rows.append(row)
            row = []
        elif token:
            content = token.strip()
            if not content:
                continue
            if cell_open:
                row[-1] = content
                cell_open = False
            elif row:
                row[-1] = f"{row[-1]} {content}".strip()
            else:
                row.append(content)

    if row:
        rows.append(row)
    if not rows:
        return ""

    width = max(len(item) for item in rows)
    rows = [item + [""] * (width - len(item)) for item in rows]

    def format_cell(cell: str) -> str:
        # Escape pipes that are not already escaped. This keeps LaTeX
        # delimiters such as "\|x\|" intact while protecting the table.
        escaped = _escape_table_pipes(cell)
        return escaped.replace("\n", "<br>").strip()

    header, *data_rows = rows
    lines = [
        "| " + " | ".join(format_cell(cell) for cell in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    lines.extend(
        "| " + " | ".join(format_cell(cell) for cell in data_row) + " |"
        for data_row in data_rows
    )
    return "\n".join(lines)


def _is_minicpm_ocr_model(model: str | None) -> bool:
    if not model:
        return False
    normalized = model.lower().replace("_", "-")
    # Jev is a scoring model, not an OCR model, so it keeps the generic path.
    return "minicpm-ocr" in normalized and "jev" not in normalized


def create_ocr_service(
    client: Any,
    model: str,
    default_prompt: str | None = None,
) -> LLMVisionOCRService:
    """Create the OCR service that matches the configured model name."""
    if _is_minicpm_ocr_model(model):
        return MiniCPMOCRService(client, model, default_prompt)
    return LLMVisionOCRService(client, model, default_prompt)


def _extract_text_with_metadata(
    ocr_service: LLMVisionOCRService,
    image_stream: BinaryIO,
    stream_info: StreamInfo,
) -> OCRResult:
    """Forward metadata when supported, retaining the legacy stream-only call."""
    extract_text = ocr_service.extract_text
    try:
        inspect.signature(extract_text).bind(image_stream, stream_info=stream_info)
    except (TypeError, ValueError):
        # Unsupported or uninspectable signatures keep the legacy invocation.
        return extract_text(image_stream)
    # Keep service errors outside the signature check; never retry an OCR call.
    return extract_text(image_stream, stream_info=stream_info)
