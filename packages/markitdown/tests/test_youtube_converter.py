import io
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from markitdown import MarkItDown, StreamInfo
from markitdown.converters import HtmlConverter, YouTubeConverter
import markitdown.converters._youtube_converter as youtube_module


@pytest.fixture
def transcript_api(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    api = MagicMock()
    api.return_value.list.return_value = []
    api.return_value.fetch.return_value = []
    monkeypatch.setattr(youtube_module, "YouTubeTranscriptApi", api, raising=False)
    monkeypatch.setattr(youtube_module, "IS_YOUTUBE_TRANSCRIPT_CAPABLE", False)
    return api


@pytest.mark.parametrize("head", ["", "<title></title>"])
@pytest.mark.parametrize("use_dispatcher", [False, True])
@pytest.mark.parametrize("transcript_capable", [False, True])
def test_youtube_empty_extraction_preserves_html(
    head: str,
    use_dispatcher: bool,
    transcript_capable: bool,
    transcript_api: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        youtube_module, "IS_YOUTUBE_TRANSCRIPT_CAPABLE", transcript_capable
    )
    html = (
        f"<html><head>{head}"
        "<script>do_not_render_script()</script>"
        "<style>.do_not_render_style { color: red; }</style></head><body>"
        "<h1>Saved transcript</h1>"
        "<table><tr><th>Time</th><th>Text</th></tr>"
        "<tr><td>00:01</td><td>caf\u00e9</td></tr></table></body></html>"
    ).encode("windows-1252")
    prefix = b"<p>Ignored stream prefix</p>"
    stream = io.BytesIO(prefix + html)
    stream.seek(len(prefix))
    stream_info = StreamInfo(
        mimetype="text/html",
        extension=".html",
        charset="windows-1252",
        url="https://www.youtube.com/watch?v=12345",
    )

    if use_dispatcher:
        result = MarkItDown().convert_stream(
            stream, stream_info=stream_info, heading_style="ATX_CLOSED"
        )
    else:
        result = YouTubeConverter().convert(
            stream, stream_info, heading_style="ATX_CLOSED"
        )

    expected = HtmlConverter().convert(
        io.BytesIO(html), stream_info, heading_style="ATX_CLOSED"
    )
    assert result.markdown == expected.markdown
    assert result.title == expected.title
    assert "# Saved transcript #" in result.markdown
    assert "| 00:01 | caf\u00e9 |" in result.markdown
    assert "Ignored stream prefix" not in result.markdown
    assert "do_not_render" not in result.markdown
    if transcript_capable:
        transcript_api.return_value.fetch.assert_called_once()
    else:
        transcript_api.assert_not_called()


@pytest.mark.parametrize(
    ("head", "title", "content"),
    [
        ("<title>Video title</title>", "Video title", "\n## Video title\n"),
        (
            '<meta property="og:title" content="Video title">',
            "Video title",
            "\n## Video title\n",
        ),
        (
            '<meta itemprop="name" content="Video title">',
            "Video title",
            "\n## Video title\n",
        ),
        (
            '<meta name="description" content="Video description">',
            "",
            "\n### Description\nVideo description\n",
        ),
        (
            '<meta property="og:description" content="Video description">',
            "",
            "\n### Description\nVideo description\n",
        ),
        (
            '<script>var ytInitialData = {"attributedDescriptionBodyText": '
            '{"content": "Video description"}};</script>',
            "",
            "\n### Description\nVideo description\n",
        ),
        (
            '<meta itemprop="interactionCount" content="42">'
            '<meta name="keywords" content="example">'
            '<meta itemprop="duration" content="PT1M">',
            "",
            "\n### Video Metadata\n"
            "- **Views:** 42\n- **Keywords:** example\n- **Runtime:** PT1M\n\n",
        ),
    ],
)
def test_youtube_preserves_metadata_output(
    head: str, title: str, content: str, transcript_api: MagicMock
) -> None:
    html = f"<html><head>{head}</head><body>Unused HTML body</body></html>"
    result = YouTubeConverter().convert(
        io.BytesIO(html.encode("utf-8")),
        StreamInfo(
            mimetype="text/html",
            charset="utf-8",
            url="https://www.youtube.com/watch?v=12345",
        ),
    )

    assert result.title == title
    assert result.markdown == "# YouTube\n" + content
    transcript_api.assert_not_called()


@pytest.mark.parametrize("title", ["", "Video title"])
def test_youtube_preserves_library_transcript(
    title: str,
    transcript_api: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(youtube_module, "IS_YOUTUBE_TRANSCRIPT_CAPABLE", True)
    transcript_api.return_value.list.return_value = [
        SimpleNamespace(language_code="fr")
    ]
    transcript_api.return_value.fetch.return_value = [
        SimpleNamespace(text="Bonjour"),
        SimpleNamespace(text="tout le monde"),
    ]
    head = f"<title>{title}</title>" if title else ""
    html = f"<html><head>{head}</head><body>Unused HTML body</body></html>"

    result = YouTubeConverter().convert(
        io.BytesIO(html.encode("utf-8")),
        StreamInfo(
            mimetype="text/html",
            charset="utf-8",
            url="https://www.youtube.com/watch?v=12345",
        ),
        youtube_transcript_languages=["fr"],
    )

    title_section = f"\n## {title}\n" if title else ""
    assert result.title == title
    assert result.markdown == (
        f"# YouTube\n{title_section}\n### Transcript\nBonjour tout le monde\n"
    )
    transcript_api.return_value.list.assert_called_once_with("12345")
    transcript_api.return_value.fetch.assert_called_once_with("12345", languages=["fr"])
