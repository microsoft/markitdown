"""File URI validation must reject network paths before opening a file."""

import os
from pathlib import Path

import pytest

import markitdown._uri_utils as uri_utils
from markitdown import MarkItDown
from markitdown._uri_utils import _is_unc_or_device_path, file_uri_to_path


UNC_URI_PATHS = [
    "//server.example/share/x.txt",
    "///server.example/share/x.txt",
    "////server.example/share/x.txt",
    r"/\server.example/share/x.txt",
    r"\/server.example/share/x.txt",
    r"\\server.example\share\x.txt",
    "/%2Fserver.example/share/x.txt",
    "/%2fserver.example/share/x.txt",
    "/%5Cserver.example/share/x.txt",
    "/%5cserver.example/share/x.txt",
    "%2F%2Fserver.example/share/x.txt",
    "%5C%5Cserver.example%5Cshare%5Cx.txt",
    "/%5C%3F%5CUNC%5Cserver.example%5Cshare%5Cx.txt",
    "/%5C.%5CUNC%5Cserver.example%5Cshare%5Cx.txt",
    "/%5C%3F%5CC:%5CTemp%5Cx.txt",
    "/%5C.%5CPhysicalDrive0",
]

BLOCKED_URIS = (
    [
        f"file://{authority}{path}"
        for authority in ("", "localhost")
        for path in UNC_URI_PATHS
        # An authority must be followed by a slash to introduce its path.
        if path.startswith("/")
    ]
    + [f"file:{path}" for path in UNC_URI_PATHS if not path.startswith("/")]
    + [
        "FILE:////server.example/share/x.txt",
        "file:////C:/Temp/x.txt",
    ]
)


@pytest.mark.parametrize("uri", BLOCKED_URIS)
def test_file_uri_rejects_unc_or_device_path(uri: str) -> None:
    with pytest.raises(ValueError, match="UNC"):
        file_uri_to_path(uri)


class _NoFileAccessMarkItDown(MarkItDown):
    def convert_local(self, *args, **kwargs):
        pytest.fail("Rejected file URIs must not reach convert_local()")


@pytest.fixture(scope="module")
def no_file_access_markitdown() -> MarkItDown:
    return _NoFileAccessMarkItDown(enable_builtins=False)


@pytest.mark.parametrize("method", ["convert", "convert_uri"])
@pytest.mark.parametrize("uri", BLOCKED_URIS + ["file://server.example/share/x.txt"])
def test_convert_rejects_remote_file_uri_before_file_access(
    no_file_access_markitdown: MarkItDown, method: str, uri: str
) -> None:
    with pytest.raises(ValueError, match="Unsupported file URI"):
        getattr(no_file_access_markitdown, method)(uri)


@pytest.mark.parametrize(
    "path, blocked",
    [
        (r"\\server\share\x.txt", True),
        ("//server/share/x.txt", True),
        (r"/\server/share/x.txt", True),
        (r"\/server/share/x.txt", True),
        (r"\\?\UNC\server\share\x.txt", True),
        (r"\\?\C:\Temp\x.txt", True),
        (r"\\.\PhysicalDrive0", True),
        (r"C:\Temp\x.txt", False),
        ("C:/Temp/x.txt", False),
        ("/home/user/x.txt", False),
        ("relative.txt", False),
    ],
)
def test_resolved_path_validation(path: str, blocked: bool) -> None:
    assert _is_unc_or_device_path(path) is blocked


def test_file_uri_rejects_unc_after_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    # Check the final guard independently of the URI prefix check. Replace only
    # the helper's converter binding, leaving the stdlib functions unchanged.
    monkeypatch.setattr(
        uri_utils, "url2pathname", lambda _: "//server.example/share/x.txt"
    )

    with pytest.raises(ValueError, match="UNC"):
        file_uri_to_path("file:///local.txt")


@pytest.mark.parametrize("filename", ["notes.txt", "notes café.txt", "%5C%5Cx.txt"])
@pytest.mark.parametrize("authority", ["", "localhost"])
def test_local_file_uri_conversion(
    tmp_path: Path, filename: str, authority: str
) -> None:
    local_file = tmp_path / filename
    local_file.write_text("Local file contents", encoding="utf-8")
    uri = local_file.as_uri().replace("file://", f"file://{authority}", 1)

    netloc, path = file_uri_to_path(uri)

    assert netloc == (authority or None)
    assert path == str(local_file)
    markitdown = MarkItDown()
    assert markitdown.convert(uri).markdown == "Local file contents"
    assert markitdown.convert(str(local_file)).markdown == "Local file contents"


@pytest.mark.skipif(os.name != "nt", reason="Requires native Windows path conversion")
@pytest.mark.parametrize("authority", ["", "localhost"])
@pytest.mark.parametrize(
    "uri_path, expected",
    [
        ("/C:/Temp/notes.txt", r"C:\Temp\notes.txt"),
        ("/C%3A/Temp/notes.txt", r"C:\Temp\notes.txt"),
        ("/C%3a/Temp/notes.txt", r"C:\Temp\notes.txt"),
        ("/C:/Temp/notes%20caf%C3%A9.txt", "C:\\Temp\\notes café.txt"),
        ("/C:/Temp/%255C%255Cx.txt", r"C:\Temp\%5C%5Cx.txt"),
    ],
)
def test_windows_local_drive_uri(authority: str, uri_path: str, expected: str) -> None:
    netloc, path = file_uri_to_path(f"file://{authority}{uri_path}")

    assert netloc == (authority or None)
    assert path == expected
