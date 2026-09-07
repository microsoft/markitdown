import io
from unittest.mock import MagicMock

import pytest
from markitdown import StreamInfo

from markitdown_ocr._ocr_service import LLMVisionOCRService


def test_extract_text_warns_when_llm_request_fails() -> None:
    client = MagicMock()
    client.chat.completions.create.side_effect = RuntimeError(
        "simulated API failure"
    )
    image_stream = io.BytesIO(b"image data")

    with pytest.warns(UserWarning, match="RuntimeError") as warning_info:
        result = LLMVisionOCRService(client, "test-model").extract_text(
            image_stream,
            stream_info=StreamInfo(mimetype="image/png"),
        )

    assert "simulated API failure" not in str(warning_info[0].message)
    assert result.text == ""
    assert result.error == "simulated API failure"
    assert image_stream.tell() == 0
