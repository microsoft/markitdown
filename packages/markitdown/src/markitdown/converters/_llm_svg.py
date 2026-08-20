"""Utility helpers for converting SVG diagrams to Mermaid via LLM.

This module is used by the HTML conversion pipeline to translate inline SVG
content into Mermaid diagrams when a supported LLM client is configured.
The conversion is intentionally narrow: the model is instructed to return only
raw Mermaid source, and to return SKIP if the SVG is decorative or cannot be
expressed as a diagram.
"""

import re
from typing import Any, BinaryIO, Union

from .._stream_info import StreamInfo

_MAX_SVG_CHARS = 12_000
MAX_RESPONSE_TOKENS = 2048


def llm_svg(
    file_stream: BinaryIO,
    stream_info: StreamInfo,
    *,
    client: Any,
    model: str,
    prompt: Union[str, None] = None,
) -> Union[None, str]:
    """Convert streamed SVG content into Mermaid source using an LLM."""

    if prompt is None or prompt.strip() == "":
        prompt = (
            "You are a diagram-analysis assistant. "
            "Your task is to read an SVG element and convert it into a Mermaid "
            "diagram that faithfully represents the same visual structure. "
            "Reply with ONLY the raw Mermaid source. Do not include markdown fences or explanations."
            'Start your reply with the Mermaid diagram type keyword (e.g. "flowchart LR", "sequenceDiagram"). '
            "If the SVG is decorative and has no logical diagram structure, reply with exactly: SKIP"
        )

    # Preserve the stream position so this helper is non-destructive to the caller
    encoding = stream_info.charset or "utf-8"
    cur_pos = file_stream.tell()
    try:
        raw = file_stream.read()
    finally:
        file_stream.seek(cur_pos)

    svg_text = raw.decode(encoding, errors="replace")
    if not svg_text.strip():
        return None

    # Truncate large SVGs to keep the token count within reasonable limits
    truncated = len(svg_text) > _MAX_SVG_CHARS
    payload = svg_text[:_MAX_SVG_CHARS]
    if truncated:
        payload += "\n<!-- SVG truncated for brevity -->"

    messages = [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": "Convert the following SVG to Mermaid:\n\n" + payload,
        },
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=MAX_RESPONSE_TOKENS,
    )

    raw_reply: str = response.choices[0].message.content or ""
    result = _clean_mermaid_response(raw_reply)

    # Return None if the LLM explicitly skipped the image or returned an empty response
    if not result or result.upper() == "SKIP":
        return None

    return result


def _clean_mermaid_response(text: str) -> str:
    """Extract the raw Mermaid code from Markdown fences, or return text as is."""
    text = text.strip()
    match = re.search(r"```(?:mermaid)?\s*\n?(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text
