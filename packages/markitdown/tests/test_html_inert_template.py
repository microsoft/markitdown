"""HTML template rendering regressions."""

import io

import pytest

from markitdown import MarkItDown


def _convert(html: str) -> str:
    return MarkItDown().convert_stream(
        io.BytesIO(html.encode("utf-8")), file_extension=".html"
    ).markdown


@pytest.mark.parametrize(
    "html, omitted",
    [
        (
            "<p>Before</p><template><p>Inactive draft</p></template><p>After</p>",
            "Inactive draft",
        ),
        (
            '<template id="row"><b>Client-side row blueprint</b></template>'
            '<p>Visible</p>',
            "Client-side row blueprint",
        ),
        (
            '<template shadowrootmode="invalid"><p>Inert</p></template><p>Visible</p>',
            "Inert",
        ),
        (
            '<template><template shadowrootmode="open"><p>Nested inert</p>'
            '</template></template><p>Visible</p>',
            "Nested inert",
        ),
    ],
)
def test_inert_html_templates_are_not_in_markdown(html: str, omitted: str) -> None:
    markdown = _convert(html)
    assert omitted not in markdown
    assert "Visible" in markdown or "Before" in markdown


@pytest.mark.parametrize("mode", ["open", "closed", "OPEN", "ClOsEd"])
def test_declarative_shadow_dom_content_is_retained(mode: str) -> None:
    markdown = _convert(
        f'<div><template shadowrootmode="{mode}"><p>Shadow content</p>'
        "</template></div>"
    )
    assert "Shadow content" in markdown


def test_scripts_and_styles_are_still_filtered() -> None:
    markdown = _convert(
        "<p>Visible</p><script>secret()</script><style>.a{color:red}</style>"
    )
    assert "Visible" in markdown
    assert "secret" not in markdown
    assert "color" not in markdown


def test_non_template_hidden_content_is_unchanged() -> None:
    # The change does not attempt general CSS or hidden-attribute evaluation.
    markdown = _convert('<p>Visible</p><div hidden>Hidden attribute</div>')
    assert "Hidden attribute" in markdown
