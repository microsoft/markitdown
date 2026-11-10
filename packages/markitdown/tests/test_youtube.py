"""YouTube URL handling, metadata, transcripts, and HTML fallback."""

import io
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
import requests

import markitdown.converters._youtube_converter as youtube_module
from markitdown import MarkItDown, StreamInfo
from markitdown.converters import HtmlConverter, YouTubeConverter

# Extraction and fallback


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


# Conversion regressions


@pytest.mark.parametrize("list_raises", [False, True])
@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=12345",
        "https://youtu.be/12345",
        "https://www.youtube.com/shorts/12345",
        "https://www.youtube.com/embed/12345",
    ],
)
def test_youtube_transcript_list_failure_preserves_metadata(
    url: str,
    list_raises: bool,
    transcript_api: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Transcript listing failures must not send video metadata to HTML fallback."""
    monkeypatch.setattr(youtube_module, "IS_YOUTUBE_TRANSCRIPT_CAPABLE", True)
    api = transcript_api.return_value
    if list_raises:
        api.list.side_effect = RuntimeError("Transcript listing unavailable")

    response = requests.Response()
    response.status_code = 200
    response.url = url
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.raw = io.BytesIO(
        b"<html><head><title>Regression video</title>"
        b'<meta itemprop="interactionCount" content="42">'
        b'<meta name="keywords" content="regression, metadata">'
        b'<meta itemprop="duration" content="PT1M">'
        b'<script>var ytInitialData = {"attributedDescriptionBodyText": '
        b'{"content": "Description only available in video data"}};</script>'
        b"</head><body><p>Generic HTML fallback content</p></body></html>"
    )

    result = MarkItDown().convert(response)

    assert result.title == "Regression video"
    assert "# YouTube\n" in result.markdown
    assert "## Regression video" in result.markdown
    assert (
        "### Description\nDescription only available in video data" in result.markdown
    )
    assert "- **Views:** 42" in result.markdown
    assert "- **Keywords:** regression, metadata" in result.markdown
    assert "- **Runtime:** PT1M" in result.markdown
    assert "Generic HTML fallback content" not in result.markdown
    api.list.assert_called_once_with("12345")
    if list_raises:
        assert "### Transcript\n*(Transcript unavailable)*" in result.markdown
        api.fetch.assert_not_called()
    else:
        assert "### Transcript" not in result.markdown
        api.fetch.assert_called_once_with("12345", languages=["en"])


@pytest.mark.parametrize(
    ("url", "video_id"),
    [
        ("https://www.youtube.com/watch?v=V2qZ_lgxTzg", "V2qZ_lgxTzg"),
        ("https://youtu.be/V2qZ_lgxTzg", "V2qZ_lgxTzg"),
        ("https://www.youtube.com/shorts/V2qZ_lgxTzg", "V2qZ_lgxTzg"),
        ("https://www.youtube.com/embed/V2qZ_lgxTzg", "V2qZ_lgxTzg"),
    ],
)
def test_youtube_converter_extracts_supported_video_ids(
    url: str, video_id: str
) -> None:
    converter = YouTubeConverter()
    assert converter._get_video_id(url) == video_id


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=V2qZ_lgxTzg",
        "https://youtu.be/V2qZ_lgxTzg",
        "https://www.youtube.com/shorts/V2qZ_lgxTzg",
    ],
)
def test_youtube_converter_accepts_supported_url_formats(url: str) -> None:
    converter = YouTubeConverter()
    assert converter.accepts(
        io.BytesIO(b"<html></html>"),
        StreamInfo(url=url, extension=".html"),
    )


def test_youtube_converter_missing_title_metadata() -> None:
    """Missing titles fall back to HTML when no video content is extracted."""
    from unittest.mock import patch
    from markitdown.converters._youtube_converter import YouTubeConverter

    converter = YouTubeConverter()
    stream_info = StreamInfo(
        mimetype="text/html",
        extension=".html",
        url="https://www.youtube.com/watch?v=12345",
    )

    with patch(
        "markitdown.converters._youtube_converter.IS_YOUTUBE_TRANSCRIPT_CAPABLE",
        False,
    ):
        # Case 1: Stream with no title metadata or title tag
        html_content_no_title = b"<html><head></head><body>Video Content</body></html>"
        stream_no_title = io.BytesIO(html_content_no_title)
        result_no_title = converter.convert(stream_no_title, stream_info)
        assert result_no_title.title is None
        assert result_no_title.markdown == "Video Content"

        # Case 2: Stream with an empty <title> tag
        html_content_empty_title = (
            b"<html><head><title></title></head><body>Video Content</body></html>"
        )
        stream_empty_title = io.BytesIO(html_content_empty_title)
        result_empty_title = converter.convert(stream_empty_title, stream_info)
        assert result_empty_title.title is None
        assert result_empty_title.markdown == "Video Content"

        # Case 3: Stream whose title is only available from the <title> tag
        html_content_title_tag = b"<html><head><title>Fallback Title</title></head><body>Video Content</body></html>"
        stream_title_tag = io.BytesIO(html_content_title_tag)
        result_title_tag = converter.convert(stream_title_tag, stream_info)
        assert result_title_tag.title == "Fallback Title"
        assert result_title_tag.markdown == "# YouTube\n\n## Fallback Title\n"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
