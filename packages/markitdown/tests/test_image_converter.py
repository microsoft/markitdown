import io
from pathlib import Path
from typing import Any, BinaryIO, Optional
from unittest.mock import MagicMock

import pytest

from markitdown import (
    DocumentConverterResult,
    FileConversionException,
    MarkItDown,
    StreamInfo,
)
from markitdown.converters import ImageConverter
import markitdown.converters._image_converter as image_module

IMAGE_FILE = Path(__file__).parent / "test_files" / "test.jpg"


@pytest.mark.parametrize("metadata", [{}, {"Title": "Image title"}])
@pytest.mark.parametrize("use_dispatcher", [False, True])
def test_image_caption_errors_propagate(
    metadata: dict[str, str],
    use_dispatcher: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        image_module, "exiftool_metadata", MagicMock(return_value=metadata)
    )
    error = RuntimeError("Caption request failed after client retries")
    client = MagicMock()
    client.chat.completions.create.side_effect = error

    if use_dispatcher:
        md = MarkItDown(llm_client=client, llm_model="test-model")
        with pytest.raises(FileConversionException, match=str(error)) as conversion_exc:
            md.convert(IMAGE_FILE)

        attempts = conversion_exc.value.attempts
        assert attempts is not None
        assert any(
            isinstance(attempt.converter, ImageConverter)
            and attempt.exc_info is not None
            and attempt.exc_info[1] is error
            for attempt in attempts
        )
    else:
        prefix = b"ignored prefix"
        stream = io.BytesIO(prefix + IMAGE_FILE.read_bytes())
        stream.seek(len(prefix))
        with pytest.raises(RuntimeError) as caption_exc:
            ImageConverter().convert(
                stream,
                StreamInfo(extension=".jpg", mimetype="image/jpeg"),
                llm_client=client,
                llm_model="test-model",
            )

        assert caption_exc.value is error
        assert stream.tell() == len(prefix)
        client.chat.completions.create.assert_called_once()


def test_image_caption_error_allows_fallback() -> None:
    client = MagicMock()
    client.chat.completions.create.side_effect = RuntimeError("Caption request failed")
    image = IMAGE_FILE.read_bytes()

    class FallbackImageConverter(ImageConverter):
        def convert(
            self,
            file_stream: BinaryIO,
            stream_info: StreamInfo,
            **kwargs: Any,
        ) -> DocumentConverterResult:
            assert client.chat.completions.create.called
            assert file_stream.read() == image
            return DocumentConverterResult(markdown="Fallback image description")

    md = MarkItDown(llm_client=client, llm_model="test-model", exiftool_path="")
    md.register_converter(FallbackImageConverter(), priority=10)
    prefix = b"ignored prefix"
    stream = io.BytesIO(prefix + image)
    stream.seek(len(prefix))

    result = md.convert_stream(
        stream, stream_info=StreamInfo(extension=".jpg", mimetype="image/jpeg")
    )

    assert result.markdown == "Fallback image description"
    assert stream.tell() == len(prefix)


@pytest.mark.parametrize("metadata", [{}, {"Title": "Image title"}])
@pytest.mark.parametrize("caption", [None, "  Image caption.  "])
def test_image_successful_caption_response_is_unchanged(
    metadata: dict[str, str],
    caption: Optional[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        image_module, "exiftool_metadata", MagicMock(return_value=metadata)
    )
    client = MagicMock()
    client.chat.completions.create.return_value.choices[0].message.content = caption

    result = ImageConverter().convert(
        io.BytesIO(IMAGE_FILE.read_bytes()),
        StreamInfo(extension=".jpg", mimetype="image/jpeg"),
        llm_client=client,
        llm_model="test-model",
    )

    expected = "Title: Image title\n" if metadata else ""
    if caption is not None:
        expected += "\n# Description:\nImage caption.\n"
    assert result.markdown == expected
    client.chat.completions.create.assert_called_once()


@pytest.mark.parametrize("metadata", [{}, {"Title": "Image title"}])
def test_image_without_llm_is_unchanged(
    metadata: dict[str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        image_module, "exiftool_metadata", MagicMock(return_value=metadata)
    )
    description = MagicMock()
    monkeypatch.setattr(ImageConverter, "_get_llm_description", description)

    result = ImageConverter().convert(
        io.BytesIO(IMAGE_FILE.read_bytes()),
        StreamInfo(extension=".jpg", mimetype="image/jpeg"),
    )

    assert result.markdown == ("Title: Image title\n" if metadata else "")
    description.assert_not_called()
