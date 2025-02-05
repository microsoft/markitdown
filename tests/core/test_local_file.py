import os
from pathlib import Path

import pytest

from markitdown import MarkItDown
from tests.helpers.utils import validate_strings

TEST_FILES_DIR = Path(__file__).parent.parent / "test_files"

XLSX_TEST_STRINGS = [
    "## 09060124-b5e7-4717-9d07-3c046eb",
    "6ff4173b-42a5-4784-9b19-f49caff4d93d",
    "affc7dad-52dc-4b98-9b5d-51e65d8a8ad0",
]

DOCX_TEST_STRINGS = [
    "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
    "49e168b7-d2ae-407f-a055-2167576f39a1",
    "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
    "# Abstract",
    "# Introduction",
    "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
]

DOCX_COMMENT_TEST_STRINGS = [
    "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
    "49e168b7-d2ae-407f-a055-2167576f39a1",
    "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
    "# Abstract",
    "# Introduction",
    "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
    "This is a test comment. 12df-321a",
    "Yet another comment in the doc. 55yiyi-asd09",
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

BLOG_TEST_URL = "https://microsoft.github.io/autogen/blog/2023/04/21/LLM-tuning-math"
BLOG_TEST_STRINGS = [
    "Large language models (LLMs) are powerful tools that can generate natural language texts for various applications, such as chatbots, summarization, translation, and more. GPT-4 is currently the state of the art LLM in the world. Is model selection irrelevant? What about inference parameters?",
    "an example where high cost can easily prevent a generic complex",
]


RSS_TEST_STRINGS = [
    "The Official Microsoft Blog",
    "In the case of AI, it is absolutely true that the industry is moving incredibly fast",
]


WIKIPEDIA_TEST_URL = "https://en.wikipedia.org/wiki/Microsoft"
WIKIPEDIA_TEST_STRINGS = [
    "Microsoft entered the operating system (OS) business in 1980 with its own version of [Unix]",
    'Microsoft was founded by [Bill Gates](/wiki/Bill_Gates "Bill Gates")',
]
WIKIPEDIA_TEST_EXCLUDES = [
    "You are encouraged to create an account and log in",
    "154 languages",
    "move to sidebar",
]

SERP_TEST_URL = "https://www.bing.com/search?q=microsoft+wikipedia"
SERP_TEST_STRINGS = [
    "](https://en.wikipedia.org/wiki/Microsoft",
    "Microsoft Corporation is **an American multinational corporation and technology company headquartered** in Redmond",
    "1995–2007: Foray into the Web, Windows 95, Windows XP, and Xbox",
]
SERP_TEST_EXCLUDES = [
    "https://www.bing.com/ck/a?!&&p=",
    "data:image/svg+xml,%3Csvg%20width%3D",
]

CSV_CP932_TEST_STRINGS = [
    "名前,年齢,住所",
    "佐藤太郎,30,東京",
    "三木英子,25,大阪",
    "髙橋淳,35,名古屋",
]

common_case = {
    "xlsx": ("test.xlsx", XLSX_TEST_STRINGS, None, {}),
    "pptx": ("test.pptx", PPTX_TEST_STRINGS, None, {}),
    "blog": ("test_blog.html", BLOG_TEST_STRINGS, None, {"url": BLOG_TEST_URL}),
    "zip": ("test_files.zip", XLSX_TEST_STRINGS, None, {}),
    "wikipedia": (
        "test_wikipedia.html",
        WIKIPEDIA_TEST_STRINGS,
        WIKIPEDIA_TEST_EXCLUDES,
        {"url": WIKIPEDIA_TEST_URL},
    ),
    "serp": (
        "test_serp.html",
        SERP_TEST_STRINGS,
        SERP_TEST_EXCLUDES,
        {"url": SERP_TEST_URL},
    ),
    "rss": ("test_rss.xml", RSS_TEST_STRINGS, None, {}),
    "mskanji": ("test_mskanji.csv", CSV_CP932_TEST_STRINGS, None, {}),
}


@pytest.fixture
def markitdown() -> MarkItDown:
    return MarkItDown()


@pytest.mark.parametrize(
    "filename, expected_strings, exclude_strings, kwargs",
    common_case.values(),
    ids=common_case.keys(),
)
def test_common(
    markitdown: MarkItDown,
    filename: str,
    expected_strings: list,
    exclude_strings: list,
    kwargs,
) -> None:
    source = TEST_FILES_DIR / filename
    result = markitdown.convert(source, **kwargs)
    validate_strings(result, expected_strings, exclude_strings)


def test_docx() -> None:
    markitdown = MarkItDown()
    # Test DOCX processing
    result = markitdown.convert(os.path.join(TEST_FILES_DIR, "test.docx"))
    validate_strings(result, DOCX_TEST_STRINGS)

    # Test DOCX processing, with comments
    result = markitdown.convert(
        os.path.join(TEST_FILES_DIR, "test_with_comment.docx"),
        style_map="comment-reference => ",
    )
    validate_strings(result, DOCX_COMMENT_TEST_STRINGS)

    # Test DOCX processing, with comments and setting style_map on init
    markitdown_with_style_map = MarkItDown(style_map="comment-reference => ")
    result = markitdown_with_style_map.convert(
        os.path.join(TEST_FILES_DIR, "test_with_comment.docx")
    )
    validate_strings(result, DOCX_COMMENT_TEST_STRINGS)
