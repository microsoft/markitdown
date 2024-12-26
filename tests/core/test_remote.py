import io
import os

import pytest
import requests

from markitdown import MarkItDown

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

skip_remote = (
    True if os.environ.get("GITHUB_ACTIONS") else False
)  # Don't run these tests in CI


PDF_TEST_URL = "https://arxiv.org/pdf/2308.08155v2.pdf"
PDF_TEST_STRINGS = [
    "While there is contemporaneous exploration of multi-agent approaches"
]


@pytest.mark.skipif(
    skip_remote,
    reason="do not run tests that query external urls",
)
def test_markitdown_remote() -> None:
    markitdown = MarkItDown()

    # By URL
    result = markitdown.convert(PDF_TEST_URL)
    for test_string in PDF_TEST_STRINGS:
        assert test_string in result.text_content

    # By stream
    response = requests.get(PDF_TEST_URL)
    result = markitdown.convert_stream(
        io.BytesIO(response.content), file_extension=".pdf", url=PDF_TEST_URL
    )
    for test_string in PDF_TEST_STRINGS:
        assert test_string in result.text_content

    # Youtube
    # TODO: This test randomly fails for some reason. Haven't been able to repro it yet. Disabling until I can debug the issue
    # result = markitdown.convert(YOUTUBE_TEST_URL)
    # for test_string in YOUTUBE_TEST_STRINGS:
    #     assert test_string in result.text_content
