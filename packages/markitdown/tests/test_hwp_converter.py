import io
from pathlib import Path

import pytest

from markitdown import MarkItDown, MissingDependencyException, StreamInfo
from markitdown.converters import HwpConverter
from markitdown.converters import _hwp_converter


@pytest.mark.parametrize(
    ("extension", "mimetype"),
    [
        (".hwp", None),
        (".hwpx", None),
        (None, "application/x-hwp"),
        (None, "application/vnd.hancom.hwpx"),
    ],
)
def test_hwp_converter_accepts_hwp_and_hwpx(
    extension: str | None, mimetype: str | None
) -> None:
    assert HwpConverter().accepts(
        io.BytesIO(), StreamInfo(extension=extension, mimetype=mimetype)
    )


def test_hwp_converter_uses_rhwp_python(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeDocument:
        def to_ir(self):
            return self

        def to_markdown(self) -> str:
            return "# HWPX input\n\n| Header |\n| --- |"

    class FakeRhwp:
        @staticmethod
        def parse(path: str) -> FakeDocument:
            input_path = Path(path)

            assert input_path.suffix == ".hwpx"
            assert input_path.read_bytes() == b"HWPX input"
            return FakeDocument()

    monkeypatch.setattr(_hwp_converter, "rhwp", FakeRhwp())
    monkeypatch.setattr(_hwp_converter, "_dependency_exc_info", None)

    result = MarkItDown().convert_stream(
        io.BytesIO(b"HWPX input"),
        stream_info=StreamInfo(extension=".hwpx"),
    )

    assert result.markdown == "# HWPX input\n\n| Header |\n| --- |"


def test_hwp_converter_requires_rhwp_python(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        _hwp_converter, "_dependency_exc_info", (ImportError, ImportError(), None)
    )

    with pytest.raises(MissingDependencyException, match=r"markitdown\[hwp\]"):
        HwpConverter().convert(io.BytesIO(b"HWP input"), StreamInfo(extension=".hwp"))
