"""Unit tests for the YouTube URL-shape helper.

Covers the URL forms that used to fall through to the generic HTML
converter: ``youtu.be/<id>`` short links, ``youtube.com/shorts/<id>``,
``/embed/<id>``, ``/live/<id>``, and the mobile host ``m.youtube.com``.
"""

from markitdown.converters._youtube_converter import _extract_video_id


def test_canonical_watch_url():
    assert _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_watch_url_with_extra_params():
    assert (
        _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s&feature=share")
        == "dQw4w9WgXcQ"
    )


def test_mobile_watch_url():
    assert _extract_video_id("https://m.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_music_youtube_watch_url():
    assert (
        _extract_video_id("https://music.youtube.com/watch?v=dQw4w9WgXcQ")
        == "dQw4w9WgXcQ"
    )


def test_short_url():
    assert _extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_short_url_with_timestamp():
    assert _extract_video_id("https://youtu.be/dQw4w9WgXcQ?t=30") == "dQw4w9WgXcQ"


def test_shorts_url():
    assert (
        _extract_video_id("https://www.youtube.com/shorts/dQw4w9WgXcQ")
        == "dQw4w9WgXcQ"
    )


def test_embed_url():
    assert (
        _extract_video_id("https://www.youtube.com/embed/dQw4w9WgXcQ")
        == "dQw4w9WgXcQ"
    )


def test_live_url():
    assert (
        _extract_video_id("https://www.youtube.com/live/dQw4w9WgXcQ")
        == "dQw4w9WgXcQ"
    )


def test_non_youtube_url_returns_none():
    assert _extract_video_id("https://vimeo.com/12345") is None


def test_watch_without_v_param_returns_none():
    assert _extract_video_id("https://www.youtube.com/watch") is None


def test_channel_url_returns_none():
    assert _extract_video_id("https://www.youtube.com/channel/UC123") is None


def test_empty_string_returns_none():
    assert _extract_video_id("") is None


def test_unknown_host_returns_none():
    assert _extract_video_id("https://example.com/watch?v=dQw4w9WgXcQ") is None
