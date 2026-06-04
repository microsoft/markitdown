from pathlib import Path
from types import SimpleNamespace

import pytest

from markitdown.gui import convert_file_to_markdown


class FakeConverter:
    def __init__(self, markdown: str = "# Converted", error: Exception | None = None):
        self.markdown = markdown
        self.error = error
        self.converted_paths: list[Path] = []

    def convert(self, path: Path):
        self.converted_paths.append(path)
        if self.error is not None:
            raise self.error
        return SimpleNamespace(markdown=self.markdown)


def test_convert_file_to_markdown_writes_utf8_output(tmp_path):
    input_path = tmp_path / "source.txt"
    output_path = tmp_path / "source.md"
    input_path.write_text("hello", encoding="utf-8")
    converter = FakeConverter(markdown="# Halo")

    convert_file_to_markdown(input_path, output_path, converter=converter)

    assert output_path.read_text(encoding="utf-8") == "# Halo"
    assert converter.converted_paths == [input_path]


def test_convert_file_to_markdown_requires_existing_input_file(tmp_path):
    output_path = tmp_path / "out.md"

    with pytest.raises(ValueError, match="Input file does not exist"):
        convert_file_to_markdown(
            tmp_path / "missing.pdf", output_path, converter=FakeConverter()
        )


def test_convert_file_to_markdown_rejects_directory_input(tmp_path):
    output_path = tmp_path / "out.md"

    with pytest.raises(ValueError, match="Input path is not a file"):
        convert_file_to_markdown(tmp_path, output_path, converter=FakeConverter())


def test_convert_file_to_markdown_requires_output_path(tmp_path):
    input_path = tmp_path / "source.txt"
    input_path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="Output path is required"):
        convert_file_to_markdown(input_path, "", converter=FakeConverter())


def test_convert_file_to_markdown_requires_existing_output_parent(tmp_path):
    input_path = tmp_path / "source.txt"
    input_path.write_text("hello", encoding="utf-8")

    with pytest.raises(ValueError, match="Output directory does not exist"):
        convert_file_to_markdown(
            input_path,
            tmp_path / "missing" / "out.md",
            converter=FakeConverter(),
        )


def test_convert_file_to_markdown_preserves_conversion_error(tmp_path):
    input_path = tmp_path / "source.txt"
    output_path = tmp_path / "source.md"
    input_path.write_text("hello", encoding="utf-8")

    with pytest.raises(RuntimeError, match="boom"):
        convert_file_to_markdown(
            input_path,
            output_path,
            converter=FakeConverter(error=RuntimeError("boom")),
        )
