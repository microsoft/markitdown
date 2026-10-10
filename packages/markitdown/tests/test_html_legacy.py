from __future__ import annotations

import sys
from io import BytesIO
from typing import Final

import pytest

from markitdown import StreamInfo
from markitdown.converters import HtmlConverter, RssConverter


@pytest.mark.skipif(
    sys.version_info >= (3, 11),
    reason="Python 3.10 retains markdownify's recursion fallback",
)
@pytest.mark.parametrize(
    "extension",
    [
        pytest.param(".html", id="html"),
        pytest.param(".rss", id="rss"),
        pytest.param(".atom", id="atom"),
    ],
)
@pytest.mark.parametrize(
    "strict", [pytest.param(False, id="plain-text"), pytest.param(True, id="raise")]
)
def test_python310_deep_content_fallback(extension: str, *, strict: bool) -> None:
    content: Final = "<div>" * 500 + "<p>Deep <b>garden</b>.</p>" + "</div>" * 500
    source: Final = (
        content
        if extension == ".html"
        else "<rss><channel><item><description><![CDATA["
        + content
        + "]]></description></item></channel></rss>"
        if extension == ".rss"
        else '<feed xmlns="http://www.w3.org/2005/Atom"><entry><content type="html"><![CDATA['
        + content
        + "]]></content></entry></feed>"
    )
    converter: Final = HtmlConverter() if extension == ".html" else RssConverter()
    recursion_limit: Final = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(200)
        if strict:
            with pytest.raises(RecursionError):
                converter.convert(
                    BytesIO(source.encode()),
                    StreamInfo(extension=extension),
                    strict=True,
                )
        else:
            with pytest.warns(UserWarning, match="too deeply nested"):
                result: Final = converter.convert(
                    BytesIO(source.encode()), StreamInfo(extension=extension)
                )
            assert result.markdown == "Deep\ngarden\n."
    finally:
        sys.setrecursionlimit(recursion_limit)
