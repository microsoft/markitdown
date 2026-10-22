"""Fences may open on the same line as a Markdown list marker."""

import io

import pytest

from markitdown import MarkItDown, StreamInfo


@pytest.mark.parametrize(
    "marker,indent", [("- ", "  "), ("1. ", "   "), ("> - ", ">   ")]
)
@pytest.mark.parametrize("fence", ["```", "~~~"])
def test_fence_after_list_marker_preserves_whitespace(marker, indent, fence):
    content = f"{marker}{fence}text\n{indent}first  \n{indent}\n{indent}\n{indent}second\n{indent}{fence}\noutside  \n"
    result = (
        MarkItDown()
        .convert(
            io.BytesIO(content.encode()),
            stream_info=StreamInfo(
                mimetype="text/markdown", extension=".md", charset="utf-8"
            ),
        )
        .markdown
    )
    assert result == content.replace("outside  \n", "outside\n")


def test_list_marker_inside_fence_does_not_close_fence():
    content = "```text\n- ```\nkept  \n\n\nlast\n```\n"
    result = (
        MarkItDown()
        .convert(
            io.BytesIO(content.encode()),
            stream_info=StreamInfo(
                mimetype="text/markdown", extension=".md", charset="utf-8"
            ),
        )
        .markdown
    )
    assert result == content
