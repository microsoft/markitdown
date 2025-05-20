import dataclasses
from typing import List


@dataclasses.dataclass(frozen=True, kw_only=True)
class FileTestVector(object):
    filename: str
    mimetype: str | None
    charset: str | None
    url: str | None
    must_include: List[str]
    must_not_include: List[str]


GENERAL_TEST_VECTORS = [
    FileTestVector(
        filename="test.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        charset=None,
        url=None,
        must_include=[
            "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
            "49e168b7-d2ae-407f-a055-2167576f39a1",
            "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
            "# Abstract",
            "# Introduction",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
            "data:image/png;base64...",
        ],
        must_not_include=[
            "data:image/png;base64,iVBORw0KGgoAAAANSU",
        ],
    ),
    FileTestVector(
        filename="test.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        charset=None,
        url=None,
        must_include=[
            "## 09060124-b5e7-4717-9d07-3c046eb",
            "6ff4173b-42a5-4784-9b19-f49caff4d93d",
            "affc7dad-52dc-4b98-9b5d-51e65d8a8ad0",
        ],
        must_not_include=[],
    ),
    FileTestVector(
        filename="test.xls",
        mimetype="application/vnd.ms-excel",
        charset=None,
        url=None,
        must_include=[
            "## 09060124-b5e7-4717-9d07-3c046eb",
            "6ff4173b-42a5-4784-9b19-f49caff4d93d",
            "affc7dad-52dc-4b98-9b5d-51e65d8a8ad0",
        ],
        must_not_include=[],
    ),
    FileTestVector(
        filename="test.pptx",
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        charset=None,
        url=None,
        must_include=[
            "2cdda5c8-e50e-4db4-b5f0-9722a649f455",
            "04191ea8-5c73-4215-a1d3-1cfb43aaaf12",
            "44bf7d06-5e7a-4a40-a2e1-a2e42ef28c8a",
            "1b92870d-e3b5-4e65-8153-919f4ff45592",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
            "a3f6004b-6f4f-4ea8-bee3-3741f4dc385f",  # chart title
            "2003",  # chart value
            "![This phrase of the caption is Human-written.](Picture4.jpg)",
        ],
        must_not_include=["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE"],
    ),
    FileTestVector(
        filename="test_outlook_msg.msg",
        mimetype="application/vnd.ms-outlook",
        charset=None,
        url=None,
        must_include=[
            "# Email Message",
            "**From:** test.sender@example.com",
            "**To:** test.recipient@example.com",
            "**Subject:** Test Email Message",
            "## Content",
            "This is the body of the test email message",
        ],
        must_not_include=[],
    ),
    FileTestVector(
        filename="test.pdf",
        mimetype="application/pdf",
        charset=None,
        url=None,
        must_include=[
            "While there is contemporaneous exploration of multi-agent approaches"
        ],
        must_not_include=[],
    ),
    FileTestVector(
        filename="test_blog.html",
        mimetype="text/html",
        charset="utf-8",
        url="https://microsoft.github.io/autogen/blog/2023/04/21/LLM-tuning-math",
        must_include=[
            "Large language models (LLMs) are powerful tools that can generate natural language texts for various applications, such as chatbots, summarization, translation, and more. GPT-4 is currently the state of the art LLM in the world. Is model selection irrelevant? What about inference parameters?",
            "an example where high cost can easily prevent a generic complex",
        ],
        must_not_include=[],
    ),
    FileTestVector(
        filename="test_wikipedia.html",
        mimetype="text/html",
        charset="utf-8",
        url="https://en.wikipedia.org/wiki/Microsoft",
        must_include=[
            "Microsoft entered the operating system (OS) business in 1980 with its own version of [Unix]",
            'Microsoft was founded by [Bill Gates](/wiki/Bill_Gates "Bill Gates")',
        ],
        must_not_include=[
            "You are encouraged to create an account and log in",
            "154 languages",
            "move to sidebar",
        ],
    ),
    FileTestVector(
        filename="test_serp.html",
        mimetype="text/html",
        charset="utf-8",
        url="https://www.bing.com/search?q=microsoft+wikipedia",
        must_include=[
            "](https://en.wikipedia.org/wiki/Microsoft",
            "Microsoft Corporation is **an American multinational corporation and technology company headquartered** in Redmond",
            "1995–2007: Foray into the Web, Windows 95, Windows XP, and Xbox",
        ],
        must_not_include=[
            "https://www.bing.com/ck/a?!&&p=",
            "data:image/svg+xml,%3Csvg%20width%3D",
        ],
    ),
    FileTestVector(
        filename="test_mskanji.csv",
        mimetype="text/csv",
        charset="cp932",
        url=None,
        must_include=[
            "| 名前 | 年齢 | 住所 |",
            "| --- | --- | --- |",
            "| 佐藤太郎 | 30 | 東京 |",
            "| 三木英子 | 25 | 大阪 |",
            "| 髙橋淳 | 35 | 名古屋 |",
        ],
        must_not_include=[],
    ),
    FileTestVector(
        filename="test.json",
        mimetype="application/json",
        charset="ascii",
        url=None,
        must_include=[
            "5b64c88c-b3c3-4510-bcb8-da0b200602d8",
            "9700dc99-6685-40b4-9a3a-5e406dcb37f3",
        ],
        must_not_include=[],
    ),
    FileTestVector(
        filename="test_rss.xml",
        mimetype="text/xml",
        charset="utf-8",
        url=None,
        must_include=[
            "# The Official Microsoft Blog",
            "## Ignite 2024: Why nearly 70% of the Fortune 500 now use Microsoft 365 Copilot",
            "In the case of AI, it is absolutely true that the industry is moving incredibly fast",
        ],
        must_not_include=["<rss", "<feed"],
    ),
    FileTestVector(
        filename="test_notebook.ipynb",
        mimetype="application/json",
        charset="ascii",
        url=None,
        must_include=[
            "# Test Notebook",
            "```python",
            'print("markitdown")',
            "```",
            "## Code Cell Below",
        ],
        must_not_include=[
            "nbformat",
            "nbformat_minor",
        ],
    ),
    FileTestVector(
        filename="test_files.zip",
        mimetype="application/zip",
        charset=None,
        url=None,
        must_include=[
            "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
            "49e168b7-d2ae-407f-a055-2167576f39a1",
            "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
            "# Abstract",
            "# Introduction",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
            "2cdda5c8-e50e-4db4-b5f0-9722a649f455",
            "04191ea8-5c73-4215-a1d3-1cfb43aaaf12",
            "44bf7d06-5e7a-4a40-a2e1-a2e42ef28c8a",
            "1b92870d-e3b5-4e65-8153-919f4ff45592",
            "## 09060124-b5e7-4717-9d07-3c046eb",
            "6ff4173b-42a5-4784-9b19-f49caff4d93d",
            "affc7dad-52dc-4b98-9b5d-51e65d8a8ad0",
            "Microsoft entered the operating system (OS) business in 1980 with its own version of [Unix]",
            'Microsoft was founded by [Bill Gates](/wiki/Bill_Gates "Bill Gates")',
        ],
        must_not_include=[],
    ),
    FileTestVector(
        filename="test.epub",
        mimetype="application/epub+zip",
        charset=None,
        url=None,
        must_include=[
            "**Authors:** Test Author",
            "A test EPUB document for MarkItDown testing",
            "# Chapter 1: Test Content",
            "This is a **test** paragraph with some formatting",
            "* A bullet point",
            "* Another point",
            "# Chapter 2: More Content",
            "*different* style",
            "> This is a blockquote for testing",
        ],
        must_not_include=[],
    ),
]


DATA_URI_TEST_VECTORS = [
    FileTestVector(
        filename="test.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        charset=None,
        url=None,
        must_include=[
            "314b0a30-5b04-470b-b9f7-eed2c2bec74a",
            "49e168b7-d2ae-407f-a055-2167576f39a1",
            "## d666f1f7-46cb-42bd-9a39-9a39cf2a509f",
            "# Abstract",
            "# Introduction",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
            "data:image/png;base64,iVBORw0KGgoAAAANSU",
        ],
        must_not_include=[
            "data:image/png;base64...",
        ],
    ),
    FileTestVector(
        filename="test.pptx",
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        charset=None,
        url=None,
        must_include=[
            "2cdda5c8-e50e-4db4-b5f0-9722a649f455",
            "04191ea8-5c73-4215-a1d3-1cfb43aaaf12",
            "44bf7d06-5e7a-4a40-a2e1-a2e42ef28c8a",
            "1b92870d-e3b5-4e65-8153-919f4ff45592",
            "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
            "a3f6004b-6f4f-4ea8-bee3-3741f4dc385f",  # chart title
            "2003",  # chart value
            "![This phrase of the caption is Human-written.]",  # image caption
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQE",
        ],
        must_not_include=[
            "![This phrase of the caption is Human-written.](Picture4.jpg)",
        ],
    ),
]
