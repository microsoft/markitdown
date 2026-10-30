"""Regression tests for the MarkItDown safeguard fixes.

Every safeguard test FAILS against stock markitdown 0.1.9 and PASSES against
the patched tree. The control test (a small, legitimate archive / response)
passes on both, proving the limits do not block ordinary conversions.

Run against stock:   pytest test_markitdown_safeguards.py
Run against patched: PYTHONPATH=<patched tree root> pytest test_markitdown_safeguards.py
"""

import io
import os
import stat
import time
import zipfile

import pytest

from markitdown import MarkItDown
from markitdown._stream_info import StreamInfo
from markitdown._exceptions import FileConversionException
from markitdown.converters._zip_converter import ZipConverter


def make_zip(members):
    """members: list of (name, bytes). Returns BytesIO positioned at 0."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in members:
            z.writestr(name, data)
    buf.seek(0)
    return buf


def nested_zip(depth, leaf=b"hello leaf"):
    """A zip inside a zip, `depth` wrappings around a leaf .txt."""
    inner = io.BytesIO()
    with zipfile.ZipFile(inner, "w") as z:
        z.writestr("leaf.txt", leaf)
    data = inner.getvalue()
    for i in range(depth):
        b = io.BytesIO()
        with zipfile.ZipFile(b, "w") as z:
            z.writestr(f"level{i}.zip", data)
        data = b.getvalue()
    return io.BytesIO(data)


ZIP_INFO = StreamInfo(extension=".zip", filename="test.zip")


# --------------------------------------------------------------------------
# ZipConverter limits
# --------------------------------------------------------------------------


def test_zip_member_size_limit():
    md = MarkItDown()
    conv = ZipConverter(markitdown=md)
    stream = make_zip([("big.txt", b"A" * 4096)])
    with pytest.raises(FileConversionException):
        conv.convert(stream, ZIP_INFO, zip_max_member_size=1024)


def test_zip_total_size_limit():
    md = MarkItDown()
    conv = ZipConverter(markitdown=md)
    stream = make_zip([(f"f{i}.txt", b"B" * 1000) for i in range(3)])
    with pytest.raises(FileConversionException):
        conv.convert(stream, ZIP_INFO, zip_max_total_size=2500)


def test_zip_member_count_limit():
    md = MarkItDown()
    conv = ZipConverter(markitdown=md)
    stream = make_zip([(f"f{i}.txt", b"x") for i in range(5)])
    with pytest.raises(FileConversionException):
        conv.convert(stream, ZIP_INFO, zip_max_members=3)


def test_zip_depth_limit_default_blocks_six_deep_nesting():
    # Same shape as safeguard-verification/repro.py (6 wrappings).
    md = MarkItDown()
    with pytest.raises(FileConversionException):
        md.convert_stream(stream=nested_zip(6), stream_info=ZIP_INFO)


def test_zip_nested_breach_aborts_instead_of_silent_skip():
    # The offending member lives in a NESTED archive. Stock code swallows the
    # inner FileConversionException per member and returns partial output;
    # a limit breach must instead reject the whole archive.
    inner = make_zip([("big.txt", b"A" * 4096)])
    outer = make_zip([("inner.zip", inner.getvalue())])
    md = MarkItDown()
    conv = ZipConverter(markitdown=md)
    with pytest.raises(FileConversionException):
        conv.convert(outer, ZIP_INFO, zip_max_member_size=1024)


def test_zip_bomb_integration_via_convert_stream():
    payload = b"A" * (2 * 1024 * 1024)
    md = MarkItDown()
    with pytest.raises(FileConversionException):
        md.convert_stream(
            stream=make_zip([("big.txt", payload)]),
            stream_info=ZIP_INFO,
            zip_max_member_size=1024 * 1024,
        )


def test_zip_small_archive_still_converts_control():
    md = MarkItDown()
    res = md.convert_stream(
        stream=make_zip([("note.txt", b"ordinary content")]),
        stream_info=ZIP_INFO,
    )
    assert "ordinary content" in res.markdown


def test_zip_limit_defaults_are_finite():
    from markitdown.converters import _zip_converter as zc

    for name in (
        "DEFAULT_MAX_MEMBER_SIZE",
        "DEFAULT_MAX_TOTAL_SIZE",
        "DEFAULT_MAX_MEMBERS",
        "DEFAULT_MAX_DEPTH",
    ):
        value = getattr(zc, name)  # AttributeError on stock -> test fails
        assert isinstance(value, int) and value > 0


# --------------------------------------------------------------------------
# _exiftool subprocess timeouts (stub binary on disk that sleeps)
# --------------------------------------------------------------------------


def _write_stub(tmp_path, body):
    stub = tmp_path / "exiftool"
    stub.write_text(body)
    stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    return str(stub)


def test_exiftool_version_probe_timeout(tmp_path):
    from markitdown.converters._exiftool import exiftool_metadata

    stub = _write_stub(tmp_path, "#!/bin/sh\nsleep 30\n")
    start = time.monotonic()
    with pytest.raises(RuntimeError):
        exiftool_metadata(io.BytesIO(b"x"), exiftool_path=stub, timeout=0.5)
    assert time.monotonic() - start < 20


def test_exiftool_metadata_call_timeout(tmp_path):
    from markitdown.converters._exiftool import exiftool_metadata

    # Answers -ver promptly, hangs on the -json run.
    stub = _write_stub(
        tmp_path,
        '#!/bin/sh\nif [ "$1" = "-ver" ]; then echo 13.00; else sleep 30; fi\n',
    )
    start = time.monotonic()
    with pytest.raises(RuntimeError):
        exiftool_metadata(io.BytesIO(b"x"), exiftool_path=stub, timeout=0.5)
    assert time.monotonic() - start < 20


# --------------------------------------------------------------------------
# convert_uri timeout / convert_response byte cap
# --------------------------------------------------------------------------


class FakeResponse:
    def __init__(self, total_bytes, url="http://example.com/big.txt"):
        self.url = url
        self.headers = {"content-type": "text/plain"}
        self._total = total_bytes

    def raise_for_status(self):
        return None

    def iter_content(self, chunk_size=65536):
        sent = 0
        chunk = b"B" * chunk_size
        while sent < self._total:
            yield chunk
            sent += chunk_size


def test_convert_response_byte_cap():
    md = MarkItDown()
    with pytest.raises(FileConversionException):
        md.convert_response(
            FakeResponse(2 * 1024 * 1024), max_response_bytes=1024 * 1024
        )


def test_convert_response_small_body_control():
    md = MarkItDown()
    res = md.convert_response(FakeResponse(2048))
    assert len(res.markdown) >= 2048


class FakeSession:
    def __init__(self, response):
        self._response = response
        self.get_calls = []

    def get(self, uri, **kwargs):
        self.get_calls.append((uri, kwargs))
        return self._response


def test_convert_uri_passes_timeout_to_session():
    session = FakeSession(FakeResponse(128, url="http://example.com/a.txt"))
    md = MarkItDown(requests_session=session)
    md.convert_uri("http://example.com/a.txt")
    assert session.get_calls, "session.get was never called"
    _, kwargs = session.get_calls[0]
    assert "timeout" in kwargs and kwargs["timeout"]


def test_convert_uri_byte_cap_is_enforced_end_to_end():
    session = FakeSession(
        FakeResponse(2 * 1024 * 1024, url="http://example.com/big.txt")
    )
    md = MarkItDown(requests_session=session)
    with pytest.raises(FileConversionException):
        md.convert_uri("http://example.com/big.txt", max_response_bytes=1024)
