import os
from pathlib import Path
from warnings import catch_warnings, resetwarnings

import pytest

from markitdown import MarkItDown

TEST_FILES_DIR = Path(__file__).parent.parent / "test_files"

# Don't run the llm tests without a key and the client library
skip_llm = False if os.environ.get("OPENAI_API_KEY") else True
try:
    import openai
except ModuleNotFoundError:
    skip_llm = True

LLM_TEST_STRINGS = [
    "5bda1dd6",
]


def test_markitdown_deprecation() -> None:
    try:
        with catch_warnings(record=True) as w:
            test_client = object()
            markitdown = MarkItDown(mlm_client=test_client)
            assert len(w) == 1
            assert w[0].category is DeprecationWarning
            assert markitdown._llm_client == test_client
    finally:
        resetwarnings()

    try:
        with catch_warnings(record=True) as w:
            markitdown = MarkItDown(mlm_model="gpt-4o")
            assert len(w) == 1
            assert w[0].category is DeprecationWarning
            assert markitdown._llm_model == "gpt-4o"
    finally:
        resetwarnings()

    try:
        test_client = object()
        markitdown = MarkItDown(mlm_client=test_client, llm_client=test_client)
        assert False
    except ValueError:
        pass

    try:
        markitdown = MarkItDown(mlm_model="gpt-4o", llm_model="gpt-4o")
        assert False
    except ValueError:
        pass


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
