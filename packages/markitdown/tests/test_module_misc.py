"""Library infrastructure, cross-format options, and remaining format regressions."""

import io
import json
import ntpath
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from charset_normalizer import from_bytes

import markitdown._uri_utils as uri_utils
from markitdown import (
    FileConversionException,
    MarkItDown,
    StreamInfo,
    UnsupportedFormatException,
)
from markitdown._markitdown import (
    _get_content_disposition_filename,
    _read_charset_sample,
)
from markitdown._uri_utils import (
    _is_unc_or_device_path,
    file_uri_to_path,
    parse_data_uri,
)


# Library behavior and remaining formats

skip_remote = (
    True if os.environ.get("GITHUB_ACTIONS") else False
)  # Don't run these tests in CI

# Don't run the llm tests without a key and the client library
skip_llm = False if os.environ.get("OPENAI_API_KEY") else True

try:
    import openai
except ModuleNotFoundError:
    skip_llm = True

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

LLM_TEST_STRINGS = [
    "5bda1dd6",
]

PPTX_TEST_STRINGS = [
    "2cdda5c8-e50e-4db4-b5f0-9722a649f455",
    "04191ea8-5c73-4215-a1d3-1cfb43aaaf12",
    "44bf7d06-5e7a-4a40-a2e1-a2e42ef28c8a",
    "1b92870d-e3b5-4e65-8153-919f4ff45592",
    "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
    "a3f6004b-6f4f-4ea8-bee3-3741f4dc385f",  # chart title
    "2003",  # chart value
]


# --- Helper Functions ---
def validate_strings(result, expected_strings, exclude_strings=None):
    """Validate presence or absence of specific strings."""
    text_content = result.text_content.replace("\\", "")
    for string in expected_strings:
        assert string in text_content
    if exclude_strings:
        for string in exclude_strings:
            assert string not in text_content


def test_stream_info_operations() -> None:
    """Test operations performed on StreamInfo objects."""

    stream_info_original = StreamInfo(
        mimetype="mimetype.1",
        extension="extension.1",
        charset="charset.1",
        filename="filename.1",
        local_path="local_path.1",
        url="url.1",
    )

    # Check updating all attributes by keyword
    keywords = ["mimetype", "extension", "charset", "filename", "local_path", "url"]
    for keyword in keywords:
        updated_stream_info = stream_info_original.copy_and_update(
            **{keyword: f"{keyword}.2"}
        )

        # Make sure the targeted attribute is updated
        assert getattr(updated_stream_info, keyword) == f"{keyword}.2"

        # Make sure the other attributes are unchanged
        for k in keywords:
            if k != keyword:
                assert getattr(stream_info_original, k) == getattr(
                    updated_stream_info, k
                )

    # Check updating all attributes by passing a new StreamInfo object
    keywords = ["mimetype", "extension", "charset", "filename", "local_path", "url"]
    for keyword in keywords:
        updated_stream_info = stream_info_original.copy_and_update(
            StreamInfo(**{keyword: f"{keyword}.2"})
        )

        # Make sure the targeted attribute is updated
        assert getattr(updated_stream_info, keyword) == f"{keyword}.2"

        # Make sure the other attributes are unchanged
        for k in keywords:
            if k != keyword:
                assert getattr(stream_info_original, k) == getattr(
                    updated_stream_info, k
                )

    # Check mixing and matching
    updated_stream_info = stream_info_original.copy_and_update(
        StreamInfo(extension="extension.2", filename="filename.2"),
        mimetype="mimetype.3",
        charset="charset.3",
    )
    assert updated_stream_info.extension == "extension.2"
    assert updated_stream_info.filename == "filename.2"
    assert updated_stream_info.mimetype == "mimetype.3"
    assert updated_stream_info.charset == "charset.3"
    assert updated_stream_info.local_path == "local_path.1"
    assert updated_stream_info.url == "url.1"

    # Check multiple StreamInfo objects
    updated_stream_info = stream_info_original.copy_and_update(
        StreamInfo(extension="extension.4", filename="filename.5"),
        StreamInfo(mimetype="mimetype.6", charset="charset.7"),
    )
    assert updated_stream_info.extension == "extension.4"
    assert updated_stream_info.filename == "filename.5"
    assert updated_stream_info.mimetype == "mimetype.6"
    assert updated_stream_info.charset == "charset.7"
    assert updated_stream_info.local_path == "local_path.1"
    assert updated_stream_info.url == "url.1"


def test_data_uris() -> None:
    # Test basic parsing of data URIs
    data_uri = "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="
    mime_type, attributes, data = parse_data_uri(data_uri)
    assert mime_type == "text/plain"
    assert len(attributes) == 0
    assert data == b"Hello, World!"

    data_uri = "data:base64,SGVsbG8sIFdvcmxkIQ=="
    mime_type, attributes, data = parse_data_uri(data_uri)
    assert mime_type is None
    assert len(attributes) == 0
    assert data == b"Hello, World!"

    data_uri = "data:text/plain;charset=utf-8;base64,SGVsbG8sIFdvcmxkIQ=="
    mime_type, attributes, data = parse_data_uri(data_uri)
    assert mime_type == "text/plain"
    assert len(attributes) == 1
    assert attributes["charset"] == "utf-8"
    assert data == b"Hello, World!"

    data_uri = "data:text/plain;CHARSET=utf-8;BASE64,SGVsbG8sIFdvcmxkIQ=="
    mime_type, attributes, data = parse_data_uri(data_uri)
    assert mime_type == "text/plain"
    assert len(attributes) == 1
    assert attributes["charset"] == "utf-8"
    assert data == b"Hello, World!"

    data_uri = "data:,Hello%2C%20World%21"
    mime_type, attributes, data = parse_data_uri(data_uri)
    assert mime_type is None
    assert len(attributes) == 0
    assert data == b"Hello, World!"

    data_uri = "data:text/plain,Hello%2C%20World%21"
    mime_type, attributes, data = parse_data_uri(data_uri)
    assert mime_type == "text/plain"
    assert len(attributes) == 0
    assert data == b"Hello, World!"

    data_uri = "data:text/plain;charset=utf-8,Hello%2C%20World%21"
    mime_type, attributes, data = parse_data_uri(data_uri)
    assert mime_type == "text/plain"
    assert len(attributes) == 1
    assert attributes["charset"] == "utf-8"
    assert data == b"Hello, World!"


def test_file_uris() -> None:
    expected_path = os.path.abspath("/path/to/file.txt")

    # Test file URI with an empty host
    file_uri = "file:///path/to/file.txt"
    netloc, path = file_uri_to_path(file_uri)
    assert netloc is None
    assert path == expected_path

    # Test file URI with no host
    file_uri = "file:/path/to/file.txt"
    netloc, path = file_uri_to_path(file_uri)
    assert netloc is None
    assert path == expected_path

    # Test file URI with localhost
    file_uri = "file://localhost/path/to/file.txt"
    netloc, path = file_uri_to_path(file_uri)
    assert netloc == "localhost"
    assert path == expected_path

    # URI schemes are case-insensitive
    file_uri = "FILE:///path/to/file.txt"
    netloc, path = file_uri_to_path(file_uri)
    assert netloc is None
    assert path == expected_path


def test_convert_case_insensitive_uri_schemes(tmp_path) -> None:
    markitdown = MarkItDown()
    expected_path = os.path.abspath("/path/to/file.txt")

    data_result = markitdown.convert("DATA:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")
    assert data_result.markdown == "Hello, World!"

    text_file = tmp_path / "hello.txt"
    text_file.write_text("Hello from file", encoding="utf-8")

    file_result = markitdown.convert(text_file.as_uri().replace("file:", "FILE:", 1))
    assert file_result.markdown == "Hello from file"

    # Test file URI with query parameters
    file_uri = "file:///path/to/file.txt?param=value"
    netloc, path = file_uri_to_path(file_uri)
    assert netloc is None
    assert path == expected_path

    # Test file URI with fragment
    file_uri = "file:///path/to/file.txt#fragment"
    netloc, path = file_uri_to_path(file_uri)
    assert netloc is None
    assert path == expected_path


def test_file_uri_with_percent_encoded_windows_drive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from nturl2path import url2pathname as windows_url2pathname

    monkeypatch.setattr(uri_utils, "os", SimpleNamespace(name="nt", path=ntpath))
    monkeypatch.setattr(uri_utils, "url2pathname", windows_url2pathname)

    netloc, path = uri_utils.file_uri_to_path("file:///C%3A/Temp/example.md")

    assert netloc is None
    assert path == r"C:\Temp\example.md"


def test_input_as_strings() -> None:
    markitdown = MarkItDown()

    # Test input from a stream
    input_data = b"<html><body><h1>Test</h1></body></html>"
    result = markitdown.convert_stream(io.BytesIO(input_data))
    assert "# Test" in result.text_content

    # Test input with leading blank characters
    input_data = b"   \n\n\n<html><body><h1>Test</h1></body></html>"
    result = markitdown.convert_stream(io.BytesIO(input_data))
    assert "# Test" in result.text_content


def test_plain_text_charset_guessed_from_prefix() -> None:
    # Charset is guessed from only the first 4096 bytes of the stream. If
    # that prefix happens to be pure ASCII but a multi-byte UTF-8 character
    # (e.g. an em dash) appears later, the charset would previously be
    # mis-detected as "ascii" and decoding the full content would raise
    # UnicodeDecodeError. See PlainTextConverter.convert.
    markitdown = MarkItDown()
    input_data = ("a" * 4096 + "em dash — end").encode("utf-8")
    result = markitdown.convert_stream(io.BytesIO(input_data), file_extension=".txt")
    assert "em dash — end" in result.text_content
def _mock_response(content_disposition: str) -> MagicMock:
    response = MagicMock()
    response.headers = {"content-disposition": content_disposition}
    response.url = "https://example.com/download"
    response.iter_content.return_value = [b"name,value\nalpha,beta\n"]
    response.raise_for_status.return_value = None
    return response


def test_convert_response_uses_rfc5987_content_disposition_filename() -> None:
    markitdown = MarkItDown()
    result = markitdown.convert_response(
        _mock_response("attachment; filename*=UTF-8''data.csv")
    )

    assert result.markdown == "\n".join(
        [
            "| name | value |",
            "| --- | --- |",
            "| alpha | beta |",
        ]
    )


def test_convert_response_prefers_extended_content_disposition_filename() -> None:
    markitdown = MarkItDown()
    result = markitdown.convert_response(
        _mock_response("attachment; filename=fallback.txt; filename*=UTF-8''data.csv")
    )

    assert result.markdown == "\n".join(
        [
            "| name | value |",
            "| --- | --- |",
            "| alpha | beta |",
        ]
    )


def test_get_content_disposition_filename_decodes_rfc5987() -> None:
    assert (
        _get_content_disposition_filename(
            "attachment; filename=fallback.txt; "
            "filename*=UTF-8''d%C3%A1t%C3%A1%2Ecsv"
        )
        == "d\u00e1t\u00e1.csv"
    )


# Youtube
# result = markitdown.convert(YOUTUBE_TEST_URL)
# for test_string in YOUTUBE_TEST_STRINGS:
#    assert test_string in result.text_content


@pytest.mark.skipif(
    skip_remote,
    reason="do not run remotely run speech transcription tests",
)
def test_speech_transcription() -> None:
    markitdown = MarkItDown()

    # Test WAV files, MP3 and M4A files
    for file_name in ["test.wav", "test.mp3", "test.m4a"]:
        result = markitdown.convert(os.path.join(TEST_FILES_DIR, file_name))
        result_lower = result.text_content.lower()
        assert (
            ("1" in result_lower or "one" in result_lower)
            and ("2" in result_lower or "two" in result_lower)
            and ("3" in result_lower or "three" in result_lower)
            and ("4" in result_lower or "four" in result_lower)
            and ("5" in result_lower or "five" in result_lower)
        )


def test_exceptions() -> None:
    # Check that an exception is raised when trying to convert an unsupported format
    markitdown = MarkItDown()
    with pytest.raises(UnsupportedFormatException):
        markitdown.convert(os.path.join(TEST_FILES_DIR, "random.bin"))

    # Check that an exception is raised when trying to convert a file that is corrupted
    with pytest.raises(FileConversionException) as exc_info:
        markitdown.convert(
            os.path.join(TEST_FILES_DIR, "random.bin"), file_extension=".pptx"
        )
    assert len(exc_info.value.attempts) == 1
    assert type(exc_info.value.attempts[0].converter).__name__ == "PptxConverter"


def test_markitdown_llm_parameters() -> None:
    """Test that LLM parameters are correctly passed to the client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="Test caption with red circle and blue square 5bda1dd6"
            )
        )
    ]
    mock_client.chat.completions.create.return_value = mock_response

    test_prompt = "You are a professional test prompt."
    markitdown = MarkItDown(
        llm_client=mock_client, llm_model="gpt-4o", llm_prompt=test_prompt
    )

    # Test image file
    markitdown.convert(os.path.join(TEST_FILES_DIR, "test_llm.jpg"))

    # Verify the prompt was passed to the OpenAI API
    assert mock_client.chat.completions.create.called
    call_args = mock_client.chat.completions.create.call_args
    messages = call_args[1]["messages"]
    assert len(messages) == 1
    assert messages[0]["content"][0]["text"] == test_prompt

    # Reset the mock for the next test
    mock_client.chat.completions.create.reset_mock()

    # TODO: may only use one test after the llm caption method duplicate has been removed:
    # https://github.com/microsoft/markitdown/pull/1254
    # Test PPTX file
    markitdown.convert(os.path.join(TEST_FILES_DIR, "test.pptx"))

    # Verify the prompt was passed to the OpenAI API for PPTX images too
    assert mock_client.chat.completions.create.called
    call_args = mock_client.chat.completions.create.call_args
    messages = call_args[1]["messages"]
    assert len(messages) == 1
    assert messages[0]["content"][0]["text"] == test_prompt


@pytest.mark.skipif(
    skip_llm,
    reason="do not run llm tests without a key",
)
def test_markitdown_llm() -> None:
    client = openai.OpenAI()
    markitdown = MarkItDown(llm_client=client, llm_model="gpt-4o")

    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "test_llm.jpg"))
    for test_string in LLM_TEST_STRINGS:
        assert test_string in result.text_content

    # This is not super precise. It would also accept "red square", "blue circle",
    # "the square is not blue", etc. But it's sufficient for this test.
    for test_string in ["red", "circle", "blue", "square"]:
        assert test_string in result.text_content.lower()

    # Images embedded in PPTX files
    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "test.pptx"))
    # LLM Captions are included
    for test_string in LLM_TEST_STRINGS:
        assert test_string in result.text_content
    # Standard alt text is included
    validate_strings(result, PPTX_TEST_STRINGS)


def test_ipynb_heading_title_preserves_leading_hash() -> None:
    """Heading marker removal must not eat a leading '#' from the title text.

    Regression for https://github.com/microsoft/markitdown/issues/2367
    """
    from markitdown.converters._ipynb_converter import IpynbConverter

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": [
            {
                "cell_type": "markdown",
                "source": ["# #hashtag campaign results\n"],
                "metadata": {},
            }
        ],
    }
    result = IpynbConverter()._convert(notebook)
    assert result.title == "#hashtag campaign results"


_UTF8_BOM = b"\xef\xbb\xbf"

_BOM_NOTEBOOK = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {},
    "cells": [
        {"cell_type": "markdown", "source": ["# Quarterly notes\n"], "metadata": {}},
        {"cell_type": "code", "source": ["print('hello')\n"], "metadata": {}},
    ],
}


def test_ipynb_with_a_utf8_bom_is_still_converted() -> None:
    """A leading BOM must not stop the notebook from being parsed."""
    from markitdown.converters._ipynb_converter import IpynbConverter

    data = _UTF8_BOM + json.dumps(_BOM_NOTEBOOK).encode("utf-8")

    result = IpynbConverter().convert(
        io.BytesIO(data), StreamInfo(extension=".ipynb", charset="utf-8")
    )

    assert "# Quarterly notes" in result.markdown
    assert "```python\nprint('hello')" in result.markdown
    assert result.title == "Quarterly notes"


def test_ipynb_with_a_utf8_bom_is_not_emitted_as_raw_json() -> None:
    """The whole stack must not fall through to the plain-text converter."""
    data = _UTF8_BOM + json.dumps(_BOM_NOTEBOOK).encode("utf-8")

    result = MarkItDown().convert_stream(
        io.BytesIO(data), stream_info=StreamInfo(extension=".ipynb")
    )

    assert result.markdown.startswith("# Quarterly notes")
    assert "nbformat" not in result.markdown


def test_ipynb_without_a_bom_is_unchanged() -> None:
    """The case that already worked must produce exactly the same markdown."""
    from markitdown.converters._ipynb_converter import IpynbConverter

    data = json.dumps(_BOM_NOTEBOOK).encode("utf-8")

    result = IpynbConverter().convert(
        io.BytesIO(data), StreamInfo(extension=".ipynb", charset="utf-8")
    )

    assert result.markdown == "# Quarterly notes\n\n\n```python\nprint('hello')\n\n```"


def test_ipynb_utf8_sig_charset_still_works() -> None:
    """A charset that already consumes the BOM must not be double-stripped."""
    from markitdown.converters._ipynb_converter import IpynbConverter

    data = _UTF8_BOM + json.dumps(_BOM_NOTEBOOK).encode("utf-8")

    result = IpynbConverter().convert(
        io.BytesIO(data), StreamInfo(extension=".ipynb", charset="utf-8-sig")
    )

    assert "# Quarterly notes" in result.markdown


def test_ipynb_accepts_non_ascii() -> None:
    """IpynbConverter.accepts() must not raise on non-ASCII binary content."""
    from markitdown.converters._ipynb_converter import IpynbConverter

    converter = IpynbConverter()

    # Binary content that is not valid UTF-8 (simulates non-ASCII file)
    binary_data = b"\x80\x81\x82\x83"
    stream_info = StreamInfo(mimetype="application/json", charset="utf-8")

    # Should return False without raising
    result = converter.accepts(io.BytesIO(binary_data), stream_info)
    assert result is False

    # French PDF content (UTF-8 bytes that would crash if decoded as ASCII)
    french_bytes = "lettre d'information sur l'événement".encode("utf-8")
    stream_info_ascii = StreamInfo(mimetype="application/json", charset="ascii")

    result = converter.accepts(io.BytesIO(french_bytes), stream_info_ascii)
    assert result is False

    # Valid notebook content should still be accepted
    notebook_bytes = b'{"nbformat": 4, "nbformat_minor": 5, "cells": []}'
    stream_info_json = StreamInfo(mimetype="application/json", charset="utf-8")

    result = converter.accepts(io.BytesIO(notebook_bytes), stream_info_json)
    assert result is True


# File URI validation

UNC_URI_PATHS = [
    "//server.example/share/x.txt",
    "///server.example/share/x.txt",
    "////server.example/share/x.txt",
    r"/\server.example/share/x.txt",
    r"\/server.example/share/x.txt",
    r"\\server.example\share\x.txt",
    "/%2Fserver.example/share/x.txt",
    "/%2fserver.example/share/x.txt",
    "/%5Cserver.example/share/x.txt",
    "/%5cserver.example/share/x.txt",
    "%2F%2Fserver.example/share/x.txt",
    "%5C%5Cserver.example%5Cshare%5Cx.txt",
    "/%5C%3F%5CUNC%5Cserver.example%5Cshare%5Cx.txt",
    "/%5C.%5CUNC%5Cserver.example%5Cshare%5Cx.txt",
    "/%5C%3F%5CC:%5CTemp%5Cx.txt",
    "/%5C.%5CPhysicalDrive0",
]

BLOCKED_URIS = (
    [
        f"file://{authority}{path}"
        for authority in ("", "localhost")
        for path in UNC_URI_PATHS
        # An authority must be followed by a slash to introduce its path.
        if path.startswith("/")
    ]
    + [f"file:{path}" for path in UNC_URI_PATHS if not path.startswith("/")]
    + [
        "FILE:////server.example/share/x.txt",
        "file:////C:/Temp/x.txt",
    ]
)


@pytest.mark.parametrize("uri", BLOCKED_URIS)
def test_file_uri_rejects_unc_or_device_path(uri: str) -> None:
    with pytest.raises(ValueError, match="UNC"):
        file_uri_to_path(uri)


class _NoFileAccessMarkItDown(MarkItDown):
    def convert_local(self, *args, **kwargs):
        pytest.fail("Rejected file URIs must not reach convert_local()")


@pytest.fixture(scope="module")
def no_file_access_markitdown() -> MarkItDown:
    return _NoFileAccessMarkItDown(enable_builtins=False)


@pytest.mark.parametrize("method", ["convert", "convert_uri"])
@pytest.mark.parametrize("uri", BLOCKED_URIS + ["file://server.example/share/x.txt"])
def test_convert_rejects_remote_file_uri_before_file_access(
    no_file_access_markitdown: MarkItDown, method: str, uri: str
) -> None:
    with pytest.raises(ValueError, match="Unsupported file URI"):
        getattr(no_file_access_markitdown, method)(uri)


@pytest.mark.parametrize(
    "path, blocked",
    [
        (r"\\server\share\x.txt", True),
        ("//server/share/x.txt", True),
        (r"/\server/share/x.txt", True),
        (r"\/server/share/x.txt", True),
        (r"\\?\UNC\server\share\x.txt", True),
        (r"\\?\C:\Temp\x.txt", True),
        (r"\\.\PhysicalDrive0", True),
        (r"C:\Temp\x.txt", False),
        ("C:/Temp/x.txt", False),
        ("/home/user/x.txt", False),
        ("relative.txt", False),
    ],
)
def test_resolved_path_validation(path: str, blocked: bool) -> None:
    assert _is_unc_or_device_path(path) is blocked


def test_file_uri_rejects_unc_after_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    # Check the final guard independently of the URI prefix check. Replace only
    # the helper's converter binding, leaving the stdlib functions unchanged.
    monkeypatch.setattr(
        uri_utils, "url2pathname", lambda _: "//server.example/share/x.txt"
    )

    with pytest.raises(ValueError, match="UNC"):
        file_uri_to_path("file:///local.txt")


@pytest.mark.parametrize("filename", ["notes.txt", "notes café.txt", "%5C%5Cx.txt"])
@pytest.mark.parametrize("authority", ["", "localhost"])
def test_local_file_uri_conversion(
    tmp_path: Path, filename: str, authority: str
) -> None:
    local_file = tmp_path / filename
    local_file.write_text("Local file contents", encoding="utf-8")
    uri = local_file.as_uri().replace("file://", f"file://{authority}", 1)

    netloc, path = file_uri_to_path(uri)

    assert netloc == (authority or None)
    assert path == str(local_file)
    markitdown = MarkItDown()
    assert markitdown.convert(uri).markdown == "Local file contents"
    assert markitdown.convert(str(local_file)).markdown == "Local file contents"


@pytest.mark.skipif(os.name != "nt", reason="Requires native Windows path conversion")
@pytest.mark.parametrize("authority", ["", "localhost"])
@pytest.mark.parametrize(
    "uri_path, expected",
    [
        ("/C:/Temp/notes.txt", r"C:\Temp\notes.txt"),
        ("/C%3A/Temp/notes.txt", r"C:\Temp\notes.txt"),
        ("/C%3a/Temp/notes.txt", r"C:\Temp\notes.txt"),
        ("/C:/Temp/notes%20caf%C3%A9.txt", "C:\\Temp\\notes café.txt"),
        ("/C:/Temp/%255C%255Cx.txt", r"C:\Temp\%5C%5Cx.txt"),
    ],
)
def test_windows_local_drive_uri(authority: str, uri_path: str, expected: str) -> None:
    netloc, path = file_uri_to_path(f"file://{authority}{uri_path}")

    assert netloc == (authority or None)
    assert path == expected


# Charset sampling

_SAMPLE_SIZE = 65536

_SPLIT_CHARACTERS = [
    (character, split)
    for character in ("\u00e9", "\u65e5", "\U0001f600")
    for split in range(1, len(character.encode("utf-8")))
]


def _split_utf8_json(character: str, split: int) -> bytes:
    prefix = '{"name":"r\u00e9sum\u00e9","notes":"'.encode("utf-8")
    return (
        prefix
        + b"a" * (_SAMPLE_SIZE - split - len(prefix))
        + (character + '"}').encode("utf-8")
    )


@pytest.fixture(scope="module")
def markitdown() -> MarkItDown:
    return MarkItDown()


@pytest.mark.parametrize("character,split", _SPLIT_CHARACTERS)
def test_charset_sample_completes_only_the_split_character(
    character: str, split: int
) -> None:
    data = _split_utf8_json(character, split)
    stream = io.BytesIO(data)
    expected_size = _SAMPLE_SIZE + len(character.encode("utf-8")) - split

    sample = _read_charset_sample(stream)

    assert sample == data[:expected_size]
    assert stream.tell() == expected_size
    assert expected_size <= _SAMPLE_SIZE + 3
    sample.decode("utf-8")


@pytest.mark.parametrize("character,split", _SPLIT_CHARACTERS)
def test_split_utf8_json_preserves_content(
    markitdown: MarkItDown, character: str, split: int
) -> None:
    data = _split_utf8_json(character, split)
    stream = io.BytesIO(data)

    guesses = markitdown._get_stream_info_guesses(stream, StreamInfo())
    assert guesses[0].charset == "utf-8"
    assert stream.tell() == 0

    result = markitdown.convert_stream(stream)

    assert result.markdown == data.decode("utf-8")


@pytest.mark.parametrize(
    "sample,tail",
    [
        (b"", b""),
        (b"ordinary text", b""),
        (b"short incomplete \xc3", b""),
        (b"a" * _SAMPLE_SIZE, b"\xc3\xa9"),
        (b"a" * (_SAMPLE_SIZE - 2) + b"\xc3\xa9", b"\xf0\x9f\x98\x80"),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xc3", b""),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xf0", b"\x9f"),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xc3", b"x"),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xe0", b"\x80\x80"),
        (b"a" * (_SAMPLE_SIZE - 1) + b"\xed", b"\xa0\x80"),
        (b"\xff" + b"a" * (_SAMPLE_SIZE - 2) + b"\xc3", b"\xa9"),
    ],
    ids=[
        "empty",
        "short",
        "short-incomplete",
        "ascii",
        "complete-utf8",
        "incomplete-at-eof",
        "incomplete-after-lookahead",
        "invalid-continuation",
        "overlong",
        "surrogate",
        "non-utf8-prefix",
    ],
)
def test_other_charset_samples_are_unchanged(sample: bytes, tail: bytes) -> None:
    stream = io.BytesIO(sample + tail)

    assert _read_charset_sample(stream) == sample
    assert stream.tell() <= _SAMPLE_SIZE + 3


def test_charset_guesses_restore_nonzero_stream_position(
    markitdown: MarkItDown,
) -> None:
    stream = io.BytesIO(b"prefix" + _split_utf8_json("\U0001f600", 1))
    stream.seek(len(b"prefix"))

    markitdown._get_stream_info_guesses(stream, StreamInfo())

    assert stream.tell() == len(b"prefix")


def test_explicit_charset_still_takes_precedence(markitdown: MarkItDown) -> None:
    data = _split_utf8_json("\u00e9", 1)

    result = markitdown.convert_stream(
        io.BytesIO(data),
        stream_info=StreamInfo(extension=".json", charset="cp1252"),
    )

    assert result.markdown == data.decode("cp1252")


# Undetectable charsets

# Tests for bytes no charset decodes.
#
# ``charset_normalizer.from_bytes(data).best()`` returns ``None`` when nothing
# decodes the bytes, and ``str(None)`` is the four-character string ``"None"``,
# so a binary file handed over with a text extension became a document whose
# entire content was the word "None" -- four characters that were never in the
# file.

# Random bytes: no charset claims them, which is what makes `best()` answer None.
# Fixed rather than generated, so the test does not depend on chance.
UNDECODABLE = bytes((7 * i * i + 251 * i + 193) % 256 for i in range(4096))


def test_the_fixture_really_is_undecodable() -> None:
    """Guards the guard: if some charset claimed these bytes the rest would pass
    for the wrong reason."""
    assert from_bytes(UNDECODABLE).best() is None


def test_binary_with_a_text_extension_is_not_the_word_none() -> None:
    markitdown = MarkItDown()
    for extension in (".txt", ".md"):
        result = markitdown.convert_stream(
            io.BytesIO(UNDECODABLE), file_extension=extension
        )
        assert result.markdown != "None"


def test_binary_with_a_csv_extension_is_not_a_table_of_none() -> None:
    markitdown = MarkItDown()
    result = markitdown.convert_stream(io.BytesIO(UNDECODABLE), file_extension=".csv")
    assert result.markdown != "| None |\n| --- |"


def test_ordinary_text_is_unchanged() -> None:
    """The fallback only runs when detection fails; everything else is as it was."""
    markitdown = MarkItDown()

    text = markitdown.convert_stream(
        io.BytesIO(b"hello, world\n"), file_extension=".txt"
    )
    assert text.markdown == "hello, world\n"

    table = markitdown.convert_stream(io.BytesIO(b"a,b\n1,2\n"), file_extension=".csv")
    assert table.markdown == "| a | b |\n| --- | --- |\n| 1 | 2 |"


def test_text_containing_the_word_none_survives() -> None:
    """The bug was a whole document reading "None", not the word appearing in
    one."""
    markitdown = MarkItDown()
    result = markitdown.convert_stream(
        io.BytesIO(b"value,note\nNone,missing\n"), file_extension=".csv"
    )
    assert result.markdown == "| value | note |\n| --- | --- |\n| None | missing |"


def test_a_declared_charset_still_wins() -> None:
    """`stream_info.charset` short-circuits detection and is untouched."""
    markitdown = MarkItDown()
    body = "名称,代码\n浦发银行,600000\n".encode("gb18030")
    result = markitdown.convert_stream(
        io.BytesIO(body),
        stream_info=StreamInfo(extension=".csv", charset="gb18030"),
    )
    assert "浦发银行" in result.markdown


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
