"""Tests for ZipConverter safety limits: file count, per-file size, total size, and zip slip."""

import io
import zipfile
from unittest.mock import MagicMock

from markitdown import StreamInfo
from markitdown.converters import ZipConverter


def _make_zip(files: list[tuple[str, bytes]]) -> bytes:
    """Build an in-memory ZIP from a list of (name, data) tuples."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_STORED) as zf:
        for name, data in files:
            zf.writestr(name, data)
    return buf.getvalue()


def _mock_markitdown(content: str = "converted") -> MagicMock:
    md = MagicMock()
    result = MagicMock()
    result.markdown = content
    md.convert_stream.return_value = result
    return md


class TestZipConverterFileLimits:
    def test_file_count_limit_stops_processing(self):
        files = [(f"file{i}.txt", f"content {i}".encode()) for i in range(5)]
        zip_bytes = _make_zip(files)
        md = _mock_markitdown("ok")

        converter = ZipConverter(markitdown=md, max_file_count=3)
        result = converter.convert(io.BytesIO(zip_bytes), StreamInfo(extension=".zip"))

        assert md.convert_stream.call_count == 3
        assert "file count limit" in result.markdown

    def test_file_count_limit_not_hit_when_under(self):
        files = [(f"file{i}.txt", b"hi") for i in range(3)]
        zip_bytes = _make_zip(files)
        md = _mock_markitdown("ok")

        converter = ZipConverter(markitdown=md, max_file_count=10)
        result = converter.convert(io.BytesIO(zip_bytes), StreamInfo(extension=".zip"))

        assert md.convert_stream.call_count == 3
        assert "file count limit" not in result.markdown

    def test_per_file_size_limit_skips_oversized_file(self):
        large_data = b"x" * 1000
        files = [("big.txt", large_data), ("small.txt", b"tiny")]
        zip_bytes = _make_zip(files)
        md = _mock_markitdown("ok")

        converter = ZipConverter(markitdown=md, max_file_size=500)
        result = converter.convert(io.BytesIO(zip_bytes), StreamInfo(extension=".zip"))

        assert "big.txt" in result.markdown
        assert "exceeds per-file limit" in result.markdown
        # small.txt should still be processed
        assert md.convert_stream.call_count == 1

    def test_total_size_limit_stops_processing(self):
        # Two files each 600 bytes; total limit is 700 bytes - only first fits
        files = [("a.txt", b"a" * 600), ("b.txt", b"b" * 600)]
        zip_bytes = _make_zip(files)
        md = _mock_markitdown("ok")

        converter = ZipConverter(markitdown=md, max_total_size=700)
        result = converter.convert(io.BytesIO(zip_bytes), StreamInfo(extension=".zip"))

        assert md.convert_stream.call_count == 1
        assert "total size limit" in result.markdown

    def test_directory_entries_are_skipped(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.mkdir("subdir")  # directory entry
            zf.writestr("subdir/file.txt", "hello")
        zip_bytes = buf.getvalue()
        md = _mock_markitdown("ok")

        converter = ZipConverter(markitdown=md)
        converter.convert(io.BytesIO(zip_bytes), StreamInfo(extension=".zip"))

        # Only the file should be converted, not the directory entry
        assert md.convert_stream.call_count == 1


class TestZipConverterZipSlip:
    def test_absolute_path_entry_is_skipped(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            info = zipfile.ZipInfo("/etc/passwd")
            zf.writestr(info, "root:x:0:0")
            zf.writestr("safe.txt", "hello")
        zip_bytes = buf.getvalue()
        md = _mock_markitdown("ok")

        converter = ZipConverter(markitdown=md)
        converter.convert(io.BytesIO(zip_bytes), StreamInfo(extension=".zip"))

        # /etc/passwd should be skipped, only safe.txt converted
        assert md.convert_stream.call_count == 1

    def test_path_traversal_entry_is_skipped(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            info = zipfile.ZipInfo("../../evil.txt")
            zf.writestr(info, "malicious")
            zf.writestr("safe.txt", "hello")
        zip_bytes = buf.getvalue()
        md = _mock_markitdown("ok")

        converter = ZipConverter(markitdown=md)
        converter.convert(io.BytesIO(zip_bytes), StreamInfo(extension=".zip"))

        assert md.convert_stream.call_count == 1


class TestZipConverterAccepts:
    def test_accepts_zip_extension(self):
        converter = ZipConverter(markitdown=MagicMock())
        assert converter.accepts(io.BytesIO(b""), StreamInfo(extension=".zip"))

    def test_accepts_zip_mimetype(self):
        converter = ZipConverter(markitdown=MagicMock())
        assert converter.accepts(
            io.BytesIO(b""), StreamInfo(mimetype="application/zip")
        )

    def test_rejects_other_extension(self):
        converter = ZipConverter(markitdown=MagicMock())
        assert not converter.accepts(io.BytesIO(b""), StreamInfo(extension=".pdf"))
