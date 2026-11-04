"""Image conversion, captions, and media metadata."""

import io
import os
import re
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any, BinaryIO, Optional
from unittest.mock import MagicMock

import pytest

import markitdown.converters._image_converter as image_module
from markitdown import (
    DocumentConverterResult,
    FileConversionException,
    MarkItDown,
    StreamInfo,
)
from markitdown.converters import ImageConverter

# Image captions

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
    monkeypatch.setattr(image_module, "llm_caption", description)

    result = ImageConverter().convert(
        io.BytesIO(IMAGE_FILE.read_bytes()),
        StreamInfo(extension=".jpg", mimetype="image/jpeg"),
    )

    assert result.markdown == ("Title: Image title\n" if metadata else "")
    description.assert_not_called()


def test_image_converter_uses_shared_llm_caption() -> None:
    from markitdown.converters import _llm_caption, _pptx_converter

    assert image_module.llm_caption is _llm_caption.llm_caption
    assert image_module.llm_caption is _pptx_converter.llm_caption
    assert not hasattr(ImageConverter, "_get_llm_description")


@pytest.mark.parametrize("prompt", [None, "Describe the chart."])
def test_image_converter_delegates_to_llm_caption(
    prompt: Optional[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(image_module, "exiftool_metadata", MagicMock(return_value={}))
    caption = MagicMock(return_value="  Shared caption.  ")
    monkeypatch.setattr(image_module, "llm_caption", caption)
    client = MagicMock()
    stream = io.BytesIO(IMAGE_FILE.read_bytes())
    stream_info = StreamInfo(extension=".jpg", mimetype="image/jpeg")

    kwargs: dict[str, Any] = {"llm_client": client, "llm_model": "test-model"}
    if prompt is not None:
        kwargs["llm_prompt"] = prompt
    result = ImageConverter().convert(stream, stream_info, **kwargs)

    assert result.markdown == "\n# Description:\nShared caption.\n"
    caption.assert_called_once_with(
        stream, stream_info, client=client, model="test-model", prompt=prompt
    )
    client.chat.completions.create.assert_not_called()


def test_image_converter_skips_description_when_llm_caption_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        image_module,
        "exiftool_metadata",
        MagicMock(return_value={"Title": "Image title"}),
    )
    caption = MagicMock(return_value=None)
    monkeypatch.setattr(image_module, "llm_caption", caption)

    result = ImageConverter().convert(
        io.BytesIO(IMAGE_FILE.read_bytes()),
        StreamInfo(extension=".jpg", mimetype="image/jpeg"),
        llm_client=MagicMock(),
        llm_model="test-model",
    )

    assert result.markdown == "Title: Image title\n"
    caption.assert_called_once()


@pytest.mark.parametrize(
    "llm_kwargs",
    [{"llm_client": MagicMock()}, {"llm_model": "test-model"}],
)
def test_image_converter_requires_client_and_model_for_caption(
    llm_kwargs: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(image_module, "exiftool_metadata", MagicMock(return_value={}))
    caption = MagicMock(return_value="unused")
    monkeypatch.setattr(image_module, "llm_caption", caption)

    result = ImageConverter().convert(
        io.BytesIO(IMAGE_FILE.read_bytes()),
        StreamInfo(extension=".jpg", mimetype="image/jpeg"),
        **llm_kwargs,
    )

    assert result.markdown == ""
    caption.assert_not_called()


@pytest.mark.parametrize("prompt", [None, "", "   "])
def test_image_converter_default_prompt_via_llm_caption(
    prompt: Optional[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(image_module, "exiftool_metadata", MagicMock(return_value={}))
    client = MagicMock()
    client.chat.completions.create.return_value.choices[0].message.content = "ok"

    ImageConverter().convert(
        io.BytesIO(IMAGE_FILE.read_bytes()),
        StreamInfo(extension=".jpg", mimetype="image/jpeg"),
        llm_client=client,
        llm_model="test-model",
        llm_prompt=prompt,
    )

    messages = client.chat.completions.create.call_args.kwargs["messages"]
    assert messages[0]["content"][0] == {
        "type": "text",
        "text": "Write a detailed caption for this image.",
    }


@pytest.mark.parametrize(
    "stream_info, expected_type",
    [
        (StreamInfo(mimetype="image/png", extension=".jpg"), "image/png"),
        (StreamInfo(extension=".jpg"), "image/jpeg"),
        (StreamInfo(), "application/octet-stream"),
    ],
)
def test_llm_caption_builds_data_uri_and_restores_stream(
    stream_info: StreamInfo, expected_type: str
) -> None:
    import base64

    from markitdown.converters._llm_caption import llm_caption

    client = MagicMock()
    client.chat.completions.create.return_value.choices[0].message.content = "cap"
    prefix = b"prefix"
    payload = b"image-bytes"
    stream = io.BytesIO(prefix + payload)
    stream.seek(len(prefix))

    result = llm_caption(
        stream, stream_info, client=client, model="m", prompt="Custom prompt"
    )

    assert result == "cap"
    assert stream.tell() == len(prefix)
    call = client.chat.completions.create.call_args
    assert call.kwargs["model"] == "m"
    content = call.kwargs["messages"][0]["content"]
    assert content[0] == {"type": "text", "text": "Custom prompt"}
    assert content[1]["image_url"]["url"] == (
        f"data:{expected_type};base64," + base64.b64encode(payload).decode("utf-8")
    )


# Conversion regressions

# Skip exiftool tests if not installed
skip_exiftool = shutil.which("exiftool") is None

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

JPG_TEST_EXIFTOOL = {
    "Author": "AutoGen Authors",
    "Title": "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
    "Description": "AutoGen enables diverse LLM-based applications",
    "ImageSize": "1615x1967",
    "DateTimeOriginal": "2024:03:14 22:10:00",
}

MP3_TEST_EXIFTOOL = {
    "Title": "f67a499e-a7d0-4ca3-a49b-358bd934ae3e",
    "Artist": "Artist Name Test String",
    "Album": "Album Name Test String",
    "SampleRate": "48000",
}


@pytest.mark.skipif(
    skip_exiftool,
    reason="do not run if exiftool is not installed",
)
def test_markitdown_exiftool(monkeypatch: pytest.MonkeyPatch) -> None:
    import speech_recognition as sr

    # Decode audio locally, but avoid the remote speech service in metadata tests.
    monkeypatch.setattr(sr.Recognizer, "recognize_google", lambda *args, **kwargs: "")
    which_exiftool = shutil.which("exiftool")
    assert which_exiftool is not None

    # Test explicitly setting the location of exiftool
    markitdown = MarkItDown(exiftool_path=which_exiftool)
    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "test.jpg"))
    for key in JPG_TEST_EXIFTOOL:
        target = f"{key}: {JPG_TEST_EXIFTOOL[key]}"
        assert target in result.text_content

    # Test setting the exiftool path through an environment variable
    monkeypatch.setenv("EXIFTOOL_PATH", which_exiftool)
    markitdown = MarkItDown()
    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "test.jpg"))
    for key in JPG_TEST_EXIFTOOL:
        target = f"{key}: {JPG_TEST_EXIFTOOL[key]}"
        assert target in result.text_content

    # Test some other media types
    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "test.mp3"))
    for key in MP3_TEST_EXIFTOOL:
        target = f"{key}: {MP3_TEST_EXIFTOOL[key]}"
        assert target in result.text_content


# ---------------------------------------------------------------------------
# Regression test for issue #1960:
# exiftool_path pointing to a nonexistent binary used to leak a raw
# FileNotFoundError. It should now be wrapped in RuntimeError with a
# message that includes the path.
# ---------------------------------------------------------------------------


def test_exiftool_metadata_with_nonexistent_binary():
    """#1960: nonexistent exiftool_path raises RuntimeError, not FileNotFoundError."""
    from markitdown.converters._exiftool import exiftool_metadata

    exiftool_path = "/this/does/not/exist/exiftool"
    with pytest.raises(
        RuntimeError,
        match=re.escape(f"Failed to invoke exiftool at {exiftool_path}"),
    ):
        exiftool_metadata(io.BytesIO(b""), exiftool_path=exiftool_path)


def test_exiftool_metadata_with_no_path():
    """Sanity check: exiftool_path=None still returns {} (early return)."""
    from markitdown.converters._exiftool import exiftool_metadata

    assert exiftool_metadata(io.BytesIO(b""), exiftool_path=None) == {}


def test_exiftool_metadata_invocation_oserror():
    """#1960: an OSError while running exiftool is wrapped, and the stream is restored."""
    from unittest.mock import patch

    from markitdown.converters._exiftool import exiftool_metadata

    def fake_run(args, **kwargs):
        # The version check succeeds ...
        if "-ver" in args:
            return SimpleNamespace(stdout="12.24\n")
        # ... but the actual metadata invocation fails.
        raise OSError("exiftool vanished")

    exiftool_path = "/usr/bin/exiftool"
    file_stream = io.BytesIO(b"0123456789")
    file_stream.seek(4)

    with patch("markitdown.converters._exiftool.subprocess.run", side_effect=fake_run):
        with pytest.raises(
            RuntimeError,
            match=re.escape(f"Failed to invoke exiftool at {exiftool_path}"),
        ):
            exiftool_metadata(file_stream, exiftool_path=exiftool_path)

    assert file_stream.tell() == 4


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
