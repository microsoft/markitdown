from collections.abc import Callable
from typing import Final

import pytest
from bs4 import Tag

from markitdown.converters import HtmlConverter


@pytest.mark.parametrize(
    ("strip_pre", "expected"),
    [
        pytest.param("strip", "```\none\n```", id="strip"),
        pytest.param("strip_one", "```\n\none\n```", id="strip-one"),
        pytest.param(None, "```\n\n\none\n\n\n```", id="preserve"),
    ],
)
def test_html_code_trimming(strip_pre: str | None, expected: str) -> None:
    assert (
        HtmlConverter()
        .convert_string("<pre><code>\n\none\n\n</code></pre>", strip_pre=strip_pre)
        .markdown
        == expected
    )


def test_html_code_default_trimming() -> None:
    assert (
        HtmlConverter().convert_string("<pre><code>\n\none\n\n</code></pre>").markdown
        == "```\none\n```"
    )


def test_html_code_default_language() -> None:
    assert (
        HtmlConverter()
        .convert_string("<pre>one</pre>", code_language="python linenums")
        .markdown
        == "```python linenums\none\n```"
    )


@pytest.mark.parametrize(
    "language",
    [pytest.param("ruby", id="override"), pytest.param("", id="disable")],
)
def test_html_code_explicit_language_overrides_class(language: str) -> None:
    assert (
        HtmlConverter()
        .convert_string(
            '<pre><code class="language-python">one</code></pre>',
            code_language=language,
        )
        .markdown
        == f"```{language}\none\n```"
    )


def test_html_inline_symbols_keep_separate_wrappers() -> None:
    assert (
        HtmlConverter()
        .convert_string(
            "<p>H<sub>2</sub>O and x<sup>2</sup></p>",
            sub_symbol="~",
            sup_symbol="<sup>",
        )
        .markdown
        == "H~2~O and x<sup>2</sup>"
    )


def test_html_code_invalid_trimming() -> None:
    with pytest.raises(ValueError, match="Invalid value for strip_pre: unknown"):
        HtmlConverter().convert_string("<pre>one</pre>", strip_pre="unknown")


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        pytest.param("<pre></pre>", "", id="empty"),
        pytest.param("<pre> </pre>", "```\n```", id="whitespace"),
        pytest.param("<pre><code>```</code></pre>", "````\n```\n````", id="backticks"),
        pytest.param(
            "<pre><code><ul><li>one</li><li>two</li></ul></code></pre>",
            "```\none\ntwo\n```",
            id="malformed-blocks",
        ),
        pytest.param(
            "<table><tr><td><pre>one\ntwo</pre></td></tr></table>",
            "|  |\n| --- |\n| `one two` |",
            id="table-cell",
        ),
        pytest.param(
            "<ul><li><pre>one\ntwo</pre></li></ul>",
            "* \n  ```\n  one\n  two\n  ```",
            id="list-item",
        ),
        pytest.param(
            '<pre><code class="language-python">one</code></pre>',
            "```python\none\n```",
            id="class-language",
        ),
    ],
)
def test_html_code_layout(html: str, expected: str) -> None:
    assert HtmlConverter().convert_string(html).markdown == expected


@pytest.mark.parametrize(
    ("callback", "expected"),
    [
        pytest.param(lambda tag: "python", "```python\none\n```", id="override"),
        pytest.param(lambda tag: None, "```default\none\n```", id="fallback-none"),
        pytest.param(lambda tag: "", "```default\none\n```", id="fallback-empty"),
        pytest.param(
            lambda tag: "python linenums",
            "```python linenums\none\n```",
            id="info-string",
        ),
    ],
)
def test_html_code_language_callback(
    callback: Callable[[Tag], str | None], expected: str
) -> None:
    assert (
        HtmlConverter()
        .convert_string(
            '<pre><code class="language-html">one</code></pre>',
            code_language="default",
            code_language_callback=callback,
        )
        .markdown
        == expected
    )


def test_html_code_callback_receives_tag_context() -> None:
    def language(tag: Tag) -> str:
        code: Final = tag.find("code")
        section: Final = tag.find_parent("section")
        html: Final = tag.find_parent("html")
        assert isinstance(code, Tag)
        assert isinstance(section, Tag)
        assert isinstance(html, Tag)
        return f"{html['data-prefix']}-{section['id']}-{code['class'][0]}"

    assert (
        HtmlConverter()
        .convert_string(
            '<html data-prefix="notes"><body><section id="garden"><pre><code class="python">one</code></pre></section></body></html>',
            code_language_callback=language,
        )
        .markdown
        == "```notes-garden-python\none\n```"
    )


def test_html_code_callback_handles_multiple_blocks() -> None:
    def language(tag: Tag) -> str:
        return str(tag["data-language"])

    assert (
        HtmlConverter()
        .convert_string(
            '<pre data-language="python">one</pre><pre data-language="ruby">two</pre>',
            code_language_callback=language,
        )
        .markdown
        == "```python\none\n```\n\n```ruby\ntwo\n```"
    )


@pytest.mark.parametrize(
    ("option", "expected", "calls"),
    [
        pytest.param("strip", "one", [], id="strip"),
        pytest.param("convert", "one", [], id="convert"),
        pytest.param("default", "```python\none\n```", ["one"], id="default"),
    ],
)
def test_html_code_filtered_pre_does_not_call_callback(
    option: str,
    expected: str,
    calls: list[str],
) -> None:
    actual_calls: Final[list[str]] = []

    def language(tag: Tag) -> str:
        actual_calls.append(tag.get_text())
        return "python"

    assert (
        HtmlConverter()
        .convert_string(
            "<pre>one</pre>",
            code_language_callback=language,
            strip=["pre"] if option == "strip" else None,
            convert=["p"] if option == "convert" else None,
        )
        .markdown,
        actual_calls,
    ) == (expected, calls)


@pytest.mark.parametrize(
    ("content", "expected", "calls"),
    [
        pytest.param("", "", [], id="empty"),
        pytest.param("one", "```python\none\n```", ["one"], id="text"),
    ],
)
def test_html_code_empty_pre_does_not_call_callback(
    content: str, expected: str, calls: list[str]
) -> None:
    actual_calls: Final[list[str]] = []

    def language(tag: Tag) -> str:
        actual_calls.append(tag.get_text())
        return "python"

    assert (
        HtmlConverter()
        .convert_string(f"<pre>{content}</pre>", code_language_callback=language)
        .markdown,
        actual_calls,
    ) == (expected, calls)
