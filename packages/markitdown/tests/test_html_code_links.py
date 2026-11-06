import pytest

from markitdown.converters._html_converter import HtmlConverter


@pytest.mark.parametrize("tag", ["code", "kbd", "samp"])
@pytest.mark.parametrize(
    "content, expected",
    [
        ('<a href="Action.html">Action</a>', "Action"),
        ('<span><a href="/Client">Client </a></span>value', "Client value"),
    ],
)
def test_inline_code_links_remain_literal(
    tag: str, content: str, expected: str
) -> None:
    result = HtmlConverter().convert_string(f"<p>Use <{tag}>{content}</{tag}>.</p>")

    assert result.markdown == f"Use `{expected}`."


@pytest.mark.parametrize(
    "html, expected",
    [
        ('<a href="/Client">Client</a>', "[Client](/Client)"),
        ('<a href="/Client"><code>Client</code></a>', "[`Client`](/Client)"),
        (
            'before<a href="/Client"> Client </a>after',
            "before [Client](/Client) after",
        ),
    ],
)
def test_links_outside_code_remain_links(html: str, expected: str) -> None:
    result = HtmlConverter().convert_string(html)

    assert result.markdown == expected
