#!/usr/bin/env python3 -m pytest
import os
import time
import pytest
import codecs


if __name__ == "__main__":
    from _test_vectors import GENERAL_TEST_VECTORS
else:
    from ._test_vectors import GENERAL_TEST_VECTORS

from markitdown import (
    MarkItDown,
    UnsupportedFormatException,
    FileConversionException,
    StreamInfo,
)

skip_remote = (
    True if os.environ.get("GITHUB_ACTIONS") else False
)  # Don't run these tests in CI

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
TEST_FILES_URL = "https://raw.githubusercontent.com/microsoft/markitdown/refs/heads/main/packages/markitdown/tests/test_files"


@pytest.mark.parametrize("test_vector", GENERAL_TEST_VECTORS)
def test_guess_stream_info(test_vector):
    """Test the ability to guess stream info."""
    markitdown = MarkItDown()

    local_path = os.path.join(TEST_FILES_DIR, test_vector.filename)
    expected_extension = os.path.splitext(test_vector.filename)[1]

    with open(local_path, "rb") as stream:
        guesses = markitdown._get_stream_info_guesses(
            stream,
            base_guess=StreamInfo(
                filename=os.path.basename(test_vector.filename),
                local_path=local_path,
                extension=expected_extension,
            ),
        )

        # For some limited exceptions, we can't guarantee the exact
        # mimetype or extension, so we'll special-case them here.
        if test_vector.filename in ["test_outlook_msg.msg"]:
            return

        assert guesses[0].mimetype == test_vector.mimetype
        assert guesses[0].extension == expected_extension
        assert _normalize_charset(guesses[0].charset) == _normalize_charset(
            test_vector.charset
        )


@pytest.mark.parametrize("test_vector", GENERAL_TEST_VECTORS)
def test_convert_local(test_vector):
    """Test the conversion of a local file."""
    markitdown = MarkItDown()

    result = markitdown.convert(
        os.path.join(TEST_FILES_DIR, test_vector.filename), url=test_vector.url
    )
    for string in test_vector.must_include:
        assert string in result.markdown
    for string in test_vector.must_not_include:
        assert string not in result.markdown


@pytest.mark.parametrize("test_vector", GENERAL_TEST_VECTORS)
def test_convert_stream_with_hints(test_vector):
    """Test the conversion of a stream with full stream info."""
    markitdown = MarkItDown()

    stream_info = StreamInfo(
        extension=os.path.splitext(test_vector.filename)[1],
        mimetype=test_vector.mimetype,
        charset=test_vector.charset,
    )

    with open(os.path.join(TEST_FILES_DIR, test_vector.filename), "rb") as stream:
        result = markitdown.convert(
            stream, stream_info=stream_info, url=test_vector.url
        )
        for string in test_vector.must_include:
            assert string in result.markdown
        for string in test_vector.must_not_include:
            assert string not in result.markdown


@pytest.mark.parametrize("test_vector", GENERAL_TEST_VECTORS)
def test_convert_stream_without_hints(test_vector):
    """Test the conversion of a stream with no stream info."""
    markitdown = MarkItDown()

    with open(os.path.join(TEST_FILES_DIR, test_vector.filename), "rb") as stream:
        result = markitdown.convert(stream, url=test_vector.url)
        for string in test_vector.must_include:
            assert string in result.markdown
        for string in test_vector.must_not_include:
            assert string not in result.markdown


@pytest.mark.skipif(
    skip_remote,
    reason="do not run tests that query external urls",
)
@pytest.mark.parametrize("test_vector", GENERAL_TEST_VECTORS)
def test_convert_url(test_vector):
    """Test the conversion of a stream with no stream info."""
    markitdown = MarkItDown()

    time.sleep(1)  # Ensure we don't hit rate limits

    result = markitdown.convert(
        TEST_FILES_URL + "/" + test_vector.filename,
        url=test_vector.url,  # Mock where this file would be found
    )
    for string in test_vector.must_include:
        assert string in result.markdown
    for string in test_vector.must_not_include:
        assert string not in result.markdown


def _normalize_charset(charset: str | None) -> str | None:
    """
    Normalize a charset string to a canonical form.
    """
    if charset is None:
        return None

    try:
        return codecs.lookup(charset).name
    except LookupError:
        return charset


if __name__ == "__main__":
    import sys

    """Runs this file's tests from the command line."""
    for test_function in [
        test_guess_stream_info,
        test_convert_local,
        test_convert_stream_with_hints,
        test_convert_stream_without_hints,
        test_convert_url,
    ]:
        for test_vector in GENERAL_TEST_VECTORS:
            print(
                f"Running {test_function.__name__} on {test_vector.filename}...", end=""
            )
            test_function(test_vector)
            print("OK")
    print("All tests passed!")
