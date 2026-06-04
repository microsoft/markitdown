from pathlib import Path
from types import SimpleNamespace
import tomllib

import pytest

from markitdown.gui import (
    APPEARANCE_MODE,
    ModernFilePicker,
    convert_file_to_markdown,
    list_directory_entries,
)


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


def test_markitdown_gui_script_points_to_gui_main():
    pyproject = tomllib.loads(
        Path("pyproject.toml").read_text(encoding="utf-8")
    )

    assert pyproject["project"]["scripts"]["markitdown-gui"] == "markitdown.gui:main"


def test_markitdown_gui_uses_dark_appearance_mode():
    assert APPEARANCE_MODE == "dark"


def test_markitdown_gui_depends_on_customtkinter():
    pyproject = tomllib.loads(
        Path("pyproject.toml").read_text(encoding="utf-8")
    )

    assert "customtkinter>=5.2.2" in pyproject["project"]["dependencies"]


def test_list_directory_entries_sorts_directories_before_files(tmp_path):
    (tmp_path / "z-file.md").write_text("z", encoding="utf-8")
    (tmp_path / "a-dir").mkdir()
    (tmp_path / ".hidden").write_text("hidden", encoding="utf-8")

    entries = list_directory_entries(tmp_path)

    assert [entry.name for entry in entries] == ["a-dir", ".hidden", "z-file.md"]
    assert [entry.is_dir for entry in entries] == [True, False, False]


def test_gui_uses_custom_picker_instead_of_native_filedialog():
    source = Path("src/markitdown/gui.py").read_text(encoding="utf-8")

    assert "filedialog" not in source
    assert ModernFilePicker.__name__ == "ModernFilePicker"
