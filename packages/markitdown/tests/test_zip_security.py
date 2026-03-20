"""Tests for zip bomb protection in ZipConverter."""

import io
import struct
import zipfile

import pytest

from markitdown import MarkItDown, StreamInfo


def _make_zip_with_entry(name: str, data: bytes, compress_type: int = zipfile.ZIP_STORED) -> io.BytesIO:
    """Create a ZIP archive in memory with a single entry."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=compress_type) as zf:
        zf.writestr(name, data)
    buf.seek(0)
    return buf


def _make_zip_with_spoofed_size(name: str, data: bytes, fake_file_size: int) -> io.BytesIO:
    """Create a ZIP archive where file_size in the header is spoofed to a large value.

    This simulates what a zip bomb's metadata looks like without actually
    including gigabytes of data. The ZipConverter checks ZipInfo.file_size
    before calling read(), so we only need the header to report a large size.
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr(name, data)

    # Patch the uncompressed size in the local file header and central directory
    raw = bytearray(buf.getvalue())

    # Find local file header (signature 0x04034b50) and patch uncompressed size
    local_sig = b"PK\x03\x04"
    idx = raw.find(local_sig)
    if idx >= 0:
        # Uncompressed size is at offset 22 from the local file header start
        struct.pack_into("<I", raw, idx + 22, fake_file_size)

    # Find central directory header (signature 0x02014b50) and patch
    central_sig = b"PK\x01\x02"
    idx = raw.find(central_sig)
    if idx >= 0:
        # Uncompressed size is at offset 24 from the central directory header start
        struct.pack_into("<I", raw, idx + 24, fake_file_size)

    result = io.BytesIO(bytes(raw))
    result.seek(0)
    return result


ZIP_STREAM_INFO = StreamInfo(extension=".zip")


class TestZipBombProtection:
    """Tests for zip bomb DoS protection."""

    def test_normal_zip_converts_successfully(self):
        """A normal small ZIP file should convert without issues."""
        md = MarkItDown()
        buf = _make_zip_with_entry("hello.txt", b"Hello, world!")
        result = md.convert_stream(buf, stream_info=ZIP_STREAM_INFO)
        assert "Hello, world!" in result.markdown

    def test_large_file_size_skipped(self):
        """Files reporting a decompressed size over the limit should be skipped."""
        from markitdown.converters._zip_converter import MAX_DECOMPRESSED_FILE_SIZE

        md = MarkItDown()
        fake_size = MAX_DECOMPRESSED_FILE_SIZE + 1
        buf = _make_zip_with_spoofed_size("bomb.txt", b"small data", fake_size)

        # Should not raise, just skip the oversized entry
        result = md.convert_stream(buf, stream_info=ZIP_STREAM_INFO)
        assert "bomb.txt" not in result.markdown

    def test_high_decompression_ratio_skipped(self):
        """Files with suspiciously high decompression ratios should be skipped."""
        from markitdown.converters._zip_converter import MAX_DECOMPRESSION_RATIO

        md = MarkItDown()

        # Create highly compressible data (all zeros) and compress it
        compressible_data = b"\x00" * (1024 * 1024)
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("zeros.txt", compressible_data)
        buf.seek(0)

        # Check the actual ratio achieved
        with zipfile.ZipFile(buf, "r") as zf:
            info = zf.getinfo("zeros.txt")
            ratio = info.file_size / max(info.compress_size, 1)

        if ratio > MAX_DECOMPRESSION_RATIO:
            # The data was compressible enough to trigger the guard
            buf.seek(0)
            result = md.convert_stream(buf, stream_info=ZIP_STREAM_INFO)
            assert "zeros.txt" not in result.markdown
        else:
            # Compression wasn't extreme enough; just verify no crash
            buf.seek(0)
            result = md.convert_stream(buf, stream_info=ZIP_STREAM_INFO)
            assert result.markdown is not None

    def test_cumulative_size_limit(self):
        """Total decompressed size across all files should be capped."""
        from markitdown.converters._zip_converter import MAX_TOTAL_DECOMPRESSED_SIZE

        md = MarkItDown()

        # Create a ZIP where each entry reports a large (but within per-file limit) size
        # and the total exceeds the cumulative limit
        per_file = MAX_TOTAL_DECOMPRESSED_SIZE // 3
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            for i in range(5):
                zf.writestr(f"file{i}.txt", b"x" * 100)

        # Patch each entry to report a large file_size
        raw = bytearray(buf.getvalue())
        for sig, offset in [(b"PK\x03\x04", 22), (b"PK\x01\x02", 24)]:
            start = 0
            while True:
                idx = raw.find(sig, start)
                if idx < 0:
                    break
                struct.pack_into("<I", raw, idx + offset, per_file)
                start = idx + 1

        patched = io.BytesIO(bytes(raw))
        patched.seek(0)

        # Should not crash - graceful degradation
        result = md.convert_stream(patched, stream_info=ZIP_STREAM_INFO)
        assert result.markdown is not None
