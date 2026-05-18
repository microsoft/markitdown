"""Unit tests for YouTubeConverter utility methods.

Covers:
- _findKey() recursive key search in nested dicts/lists
- _get() metadata lookup by priority keys
- _retry_operation() retry logic
"""

import pytest
from unittest.mock import MagicMock, patch

from markitdown.converters._youtube_converter import YouTubeConverter


def _make_converter():
    return YouTubeConverter()


# ============================================================
# _findKey
# ============================================================


def test_find_key_direct_match():
    conv = _make_converter()
    assert conv._findKey({"title": "Hello"}, "title") == "Hello"


def test_find_key_nested_dict():
    conv = _make_converter()
    data = {"outer": {"inner": {"target": "found"}}}
    assert conv._findKey(data, "target") == "found"


def test_find_key_in_list():
    conv = _make_converter()
    data = {"items": [{"name": "A"}, {"name": "B", "id": "target"}]}
    assert conv._findKey(data, "id") == "target"


def test_find_key_deeply_nested():
    conv = _make_converter()
    data = {
        "level1": [
            {"level2": {"level3": [{"level4": {"key": "deep_value"}}]}}
        ]
    }
    assert conv._findKey(data, "key") == "deep_value"


def test_find_key_not_found_returns_none():
    conv = _make_converter()
    assert conv._findKey({"a": 1, "b": 2}, "z") is None


def test_find_key_empty_data():
    conv = _make_converter()
    assert conv._findKey({}, "any") is None
    assert conv._findKey([], "any") is None


def test_find_key_finds_first_match():
    conv = _make_converter()
    data = {
        "first": {"key": "first_value"},
        "second": {"key": "second_value"},
    }
    # Dict iteration order is insertion order in Python 3.7+
    assert conv._findKey(data, "key") == "first_value"


def test_find_key_value_is_none_preserved():
    conv = _make_converter()
    data = {"key": None}
    # _findKey should return None (the value) — same as not-found
    result = conv._findKey(data, "key")
    assert result is None  # because None is falsy in `if result :=`


# ============================================================
# _get
# ============================================================


def test_get_first_matching_key():
    conv = _make_converter()
    metadata = {"title": "Hello", "og:title": "OG Hello"}
    assert conv._get(metadata, ["title", "og:title"]) == "Hello"


def test_get_second_key_when_first_missing():
    conv = _make_converter()
    metadata = {"og:title": "OG Title"}
    assert conv._get(metadata, ["title", "og:title"]) == "OG Title"


def test_get_default_when_no_match():
    conv = _make_converter()
    metadata = {"other": "value"}
    assert conv._get(metadata, ["title", "name"]) is None


def test_get_custom_default():
    conv = _make_converter()
    metadata = {}
    assert conv._get(metadata, ["title"], default="Untitled") == "Untitled"


def test_get_empty_metadata():
    conv = _make_converter()
    assert conv._get({}, ["any"]) is None


# ============================================================
# _retry_operation
# ============================================================


def test_retry_operation_success_first_try():
    conv = _make_converter()
    counter = [0]

    def op():
        counter[0] += 1
        return "ok"

    result = conv._retry_operation(op, retries=3, delay=0.01)
    assert result == "ok"
    assert counter[0] == 1


def test_retry_operation_success_after_retry():
    conv = _make_converter()
    counter = [0]

    def op():
        counter[0] += 1
        if counter[0] < 3:
            raise RuntimeError(f"fail {counter[0]}")
        return "finally"

    result = conv._retry_operation(op, retries=5, delay=0.01)
    assert result == "finally"
    assert counter[0] == 3


def test_retry_operation_all_failures():
    conv = _make_converter()
    call_count = [0]

    def op():
        call_count[0] += 1
        raise RuntimeError("always fails")

    with pytest.raises(RuntimeError, match="Operation failed after"):
        conv._retry_operation(op, retries=3, delay=0.01)
    assert call_count[0] == 3


def test_retry_operation_single_retry():
    conv = _make_converter()
    counter = [0]

    def op():
        counter[0] += 1
        if counter[0] == 1:
            raise RuntimeError("first fail")
        return "ok"

    result = conv._retry_operation(op, retries=2, delay=0.01)
    assert result == "ok"
    assert counter[0] == 2
