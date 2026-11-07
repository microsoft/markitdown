import io
import zipfile

from markitdown import MarkItDown


def _zip(files):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    return buf.getvalue()


def _convert(data, **kw):
    return (
        MarkItDown()
        .convert_stream(io.BytesIO(data), file_extension=".zip", **kw)
        .markdown
    )


def test_normal_zip_still_works():
    md = _convert(_zip({"hello.txt": b"hello world"}))
    assert "hello world" in md
    assert "Skipped" not in md


def test_oversized_member_is_skipped():
    md = _convert(
        _zip({"big.txt": b"0" * 5000, "ok.txt": b"small"}), zip_max_entry_bytes=1000
    )
    assert "`big.txt` (too large once decompressed)" in md
    assert "small" in md


def test_total_limit():
    md = _convert(
        _zip({"a.txt": b"a" * 800, "b.txt": b"b" * 800}), zip_max_total_bytes=1000
    )
    assert "`b.txt`" in md and "Skipped" in md


def test_entry_count_limit():
    md = _convert(_zip({f"f{i}.txt": b"x" for i in range(5)}), zip_max_entries=2)
    assert "3 files beyond the limit of 2" in md


def test_nesting_limit():
    inner = _zip({"deep.txt": b"deep content"})
    for _ in range(4):
        inner = _zip({"n.zip": inner})
    md = _convert(inner)
    assert "nested deeper than 3 levels" in md
    assert "deep content" not in md


def test_shallow_nesting_ok():
    md = _convert(_zip({"n.zip": _zip({"deep.txt": b"visible"})}))
    assert "visible" in md


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("OK", name)
