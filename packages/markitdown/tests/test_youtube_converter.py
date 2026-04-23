import io

from markitdown import StreamInfo
from markitdown.converters._youtube_converter import YouTubeConverter


def _stream_info(url: str) -> StreamInfo:
    return StreamInfo(url=url, mimetype="text/html", extension=".html")


def test_accepts_youtube_short_urls() -> None:
    converter = YouTubeConverter()

    assert converter.accepts(io.BytesIO(b""), _stream_info("https://youtu.be/dQw4w9WgXcQ"))
    assert converter.accepts(
        io.BytesIO(b""), _stream_info("https://www.youtube.com/shorts/dQw4w9WgXcQ")
    )
    assert converter.accepts(
        io.BytesIO(b""), _stream_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    )


def test_extract_video_id_from_supported_youtube_urls() -> None:
    converter = YouTubeConverter()

    assert (
        converter._extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        == "dQw4w9WgXcQ"
    )
    assert converter._extract_video_id("https://youtu.be/dQw4w9WgXcQ?t=42") == "dQw4w9WgXcQ"
    assert (
        converter._extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ")
        == "dQw4w9WgXcQ"
    )
    assert converter._extract_video_id("https://example.com/watch?v=dQw4w9WgXcQ") is None
