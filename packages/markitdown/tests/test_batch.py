#!/usr/bin/env python3 -m pytest
"""Tests for batch directory conversion (convert_batch API and CLI --output-dir)."""
import os
import shutil
import subprocess
import tempfile

import pytest

from markitdown import (
    MarkItDown,
    BatchResult,
    BatchItemResult,
)

TEST_FILES_DIR = os.path.join(
    os.path.dirname(__file__), "test_files"
)


@pytest.fixture
def markitdown():
    return MarkItDown()


@pytest.fixture
def batch_dir(tmp_path):
    """Create a temporary directory structure with test files for batch conversion."""
    # Copy a few known-good test files into a temp structure
    source_files = {
        "test.xlsx": "test.xlsx",
        "test.pdf": "test.pdf",
        "test.json": "test.json",
    }
    for dest_name, src_name in source_files.items():
        src = os.path.join(TEST_FILES_DIR, src_name)
        if os.path.exists(src):
            shutil.copy2(src, tmp_path / dest_name)

    # Create a subdirectory with another file
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    csv_src = os.path.join(TEST_FILES_DIR, "test_mskanji.csv")
    if os.path.exists(csv_src):
        shutil.copy2(csv_src, subdir / "nested.csv")

    return tmp_path


@pytest.fixture
def batch_dir_with_unsupported(batch_dir):
    """Add an unsupported binary file to the batch directory."""
    bin_src = os.path.join(TEST_FILES_DIR, "random.bin")
    if os.path.exists(bin_src):
        shutil.copy2(bin_src, batch_dir / "random.bin")
    return batch_dir


# ============================================================
# Unit tests for convert_batch() API
# ============================================================


class TestConvertBatchAPI:

    def test_batch_converts_directory(self, markitdown, batch_dir):
        """Basic batch conversion of a directory should return results for each file."""
        result = markitdown.convert_batch(batch_dir)
        assert isinstance(result, BatchResult)
        assert len(result) > 0
        assert len(result.succeeded) > 0

    def test_batch_result_contains_markdown(self, markitdown, batch_dir):
        """Successful items should have non-empty markdown content."""
        result = markitdown.convert_batch(batch_dir)
        for item in result.succeeded:
            assert item.result is not None
            assert len(item.result.markdown) > 0

    def test_batch_recursive_default(self, markitdown, batch_dir):
        """By default, recursive=True should find files in subdirectories."""
        result = markitdown.convert_batch(batch_dir, recursive=True)
        paths = [item.source_path for item in result.items]
        nested_found = any("subdir" in p for p in paths)
        assert nested_found, f"Expected nested files, got paths: {paths}"

    def test_batch_non_recursive(self, markitdown, batch_dir):
        """With recursive=False, subdirectory files should not be included."""
        result = markitdown.convert_batch(batch_dir, recursive=False)
        paths = [item.source_path for item in result.items]
        nested_found = any("subdir" in p for p in paths)
        assert not nested_found, f"Unexpected nested files in paths: {paths}"

    def test_batch_extension_filter(self, markitdown, batch_dir):
        """Extension filter should only include matching files."""
        result = markitdown.convert_batch(batch_dir, extensions=[".pdf"])
        for item in result.items:
            assert item.source_path.endswith(".pdf"), (
                f"Non-PDF file found: {item.source_path}"
            )

    def test_batch_extension_filter_without_dot(self, markitdown, batch_dir):
        """Extension filter without leading dot should still work."""
        result = markitdown.convert_batch(batch_dir, extensions=["pdf"])
        for item in result.items:
            assert item.source_path.endswith(".pdf"), (
                f"Non-PDF file found: {item.source_path}"
            )

    def test_batch_extension_filter_multiple(self, markitdown, batch_dir):
        """Multiple extension filters should include all matching types."""
        result = markitdown.convert_batch(
            batch_dir, extensions=[".pdf", ".json"]
        )
        for item in result.items:
            assert item.source_path.endswith(".pdf") or item.source_path.endswith(
                ".json"
            ), f"Unexpected file: {item.source_path}"

    def test_batch_continue_on_error(self, markitdown, batch_dir_with_unsupported):
        """With on_error='continue', unsupported files should not stop processing."""
        result = markitdown.convert_batch(
            batch_dir_with_unsupported, on_error="continue"
        )
        # Should have both successes and possibly failures
        assert len(result) > 0
        # Successful items should still exist
        assert len(result.succeeded) > 0

    def test_batch_raise_on_error(self, markitdown, batch_dir_with_unsupported):
        """With on_error='raise', first unsupported file should raise an exception."""
        # Only test if we know there's an unsupported file
        bin_path = batch_dir_with_unsupported / "random.bin"
        if bin_path.exists():
            with pytest.raises(Exception):
                markitdown.convert_batch(
                    batch_dir_with_unsupported,
                    on_error="raise",
                    extensions=[".bin"],
                )

    def test_batch_not_a_directory(self, markitdown):
        """Passing a file path instead of a directory should raise NotADirectoryError."""
        with pytest.raises(NotADirectoryError):
            markitdown.convert_batch("/tmp/nonexistent_dir_12345")

    def test_batch_invalid_on_error(self, markitdown, batch_dir):
        """Invalid on_error value should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid on_error mode"):
            markitdown.convert_batch(batch_dir, on_error="invalid")

    def test_batch_empty_directory(self, markitdown, tmp_path):
        """Empty directory should return empty BatchResult."""
        result = markitdown.convert_batch(tmp_path)
        assert len(result) == 0
        assert len(result.succeeded) == 0
        assert len(result.failed) == 0

    def test_batch_progress_callback(self, markitdown, batch_dir):
        """Progress callback should be called for each file."""
        progress_calls = []

        def on_progress(file_path, current, total):
            progress_calls.append((file_path, current, total))

        result = markitdown.convert_batch(
            batch_dir, progress_callback=on_progress
        )
        assert len(progress_calls) == len(result)
        # Verify indices are sequential
        for i, (_, current, total) in enumerate(progress_calls):
            assert current == i
            assert total == len(result)

    def test_batch_result_iteration(self, markitdown, batch_dir):
        """BatchResult should be iterable."""
        result = markitdown.convert_batch(batch_dir)
        items_from_iter = list(result)
        assert len(items_from_iter) == len(result)

    def test_batch_item_result_fields(self, markitdown, batch_dir):
        """Each BatchItemResult should have the expected fields."""
        result = markitdown.convert_batch(batch_dir, extensions=[".pdf"])
        if len(result) > 0:
            item = result.items[0]
            assert isinstance(item, BatchItemResult)
            assert isinstance(item.source_path, str)
            assert isinstance(item.success, bool)
            if item.success:
                assert item.result is not None
                assert item.error is None
            else:
                assert item.error is not None

    def test_batch_accepts_path_object(self, markitdown, batch_dir):
        """convert_batch should accept pathlib.Path objects."""
        from pathlib import Path
        result = markitdown.convert_batch(Path(batch_dir))
        assert len(result) > 0

    def test_batch_accepts_string_path(self, markitdown, batch_dir):
        """convert_batch should accept string paths."""
        result = markitdown.convert_batch(str(batch_dir))
        assert len(result) > 0

    def test_batch_deterministic_order(self, markitdown, batch_dir):
        """Files should be processed in sorted order for deterministic output."""
        result1 = markitdown.convert_batch(batch_dir)
        result2 = markitdown.convert_batch(batch_dir)
        paths1 = [item.source_path for item in result1.items]
        paths2 = [item.source_path for item in result2.items]
        assert paths1 == paths2


# ============================================================
# CLI integration tests for batch mode
# ============================================================


class TestBatchCLI:

    def test_cli_batch_directory(self, batch_dir, tmp_path):
        """CLI should convert a directory when --output-dir is provided."""
        output_dir = tmp_path / "output"
        result = subprocess.run(
            [
                "python",
                "-m",
                "markitdown",
                str(batch_dir),
                "--output-dir",
                str(output_dir),
                "--extensions",
                "json",
            ],
            capture_output=True,
            text=True,
        )
        # Should produce output files
        assert output_dir.exists(), f"Output dir not created. stderr: {result.stderr}"
        md_files = list(output_dir.rglob("*.md"))
        assert len(md_files) > 0, f"No .md files found. stderr: {result.stderr}"

    def test_cli_batch_preserves_structure(self, batch_dir, tmp_path):
        """CLI batch mode should preserve directory structure in output."""
        output_dir = tmp_path / "output"
        subprocess.run(
            [
                "python",
                "-m",
                "markitdown",
                str(batch_dir),
                "--output-dir",
                str(output_dir),
            ],
            capture_output=True,
            text=True,
        )
        # Check that subdir structure is preserved
        nested_files = list((output_dir / "subdir").rglob("*.md"))
        if (batch_dir / "subdir").exists() and list((batch_dir / "subdir").iterdir()):
            assert len(nested_files) > 0, "Nested directory structure not preserved"

    def test_cli_batch_no_recursive(self, batch_dir, tmp_path):
        """CLI --no-recursive should skip subdirectories."""
        output_dir = tmp_path / "output"
        subprocess.run(
            [
                "python",
                "-m",
                "markitdown",
                str(batch_dir),
                "--output-dir",
                str(output_dir),
                "--no-recursive",
            ],
            capture_output=True,
            text=True,
        )
        if output_dir.exists():
            nested_dir = output_dir / "subdir"
            if nested_dir.exists():
                nested_files = list(nested_dir.rglob("*.md"))
                assert len(nested_files) == 0, "Nested files found despite --no-recursive"

    def test_cli_batch_requires_output_dir(self, batch_dir):
        """CLI should error if directory is given without --output-dir."""
        result = subprocess.run(
            [
                "python",
                "-m",
                "markitdown",
                str(batch_dir),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "output-dir" in result.stdout.lower() or "output-dir" in result.stderr.lower(), (
            f"Expected error about --output-dir. stdout: {result.stdout}, stderr: {result.stderr}"
        )

    def test_cli_batch_extension_filter(self, batch_dir, tmp_path):
        """CLI --extensions should filter by file type."""
        output_dir = tmp_path / "output"
        subprocess.run(
            [
                "python",
                "-m",
                "markitdown",
                str(batch_dir),
                "--output-dir",
                str(output_dir),
                "--extensions",
                "pdf",
            ],
            capture_output=True,
            text=True,
        )
        if output_dir.exists():
            md_files = list(output_dir.rglob("*.md"))
            for f in md_files:
                # The output file should be original.pdf.md
                assert ".pdf.md" in f.name, f"Unexpected output file: {f.name}"

    def test_cli_batch_progress_output(self, batch_dir, tmp_path):
        """CLI batch mode should print progress to stderr."""
        output_dir = tmp_path / "output"
        result = subprocess.run(
            [
                "python",
                "-m",
                "markitdown",
                str(batch_dir),
                "--output-dir",
                str(output_dir),
                "--extensions",
                "json",
            ],
            capture_output=True,
            text=True,
        )
        assert "Converting:" in result.stderr, (
            f"Expected progress output. stderr: {result.stderr}"
        )
        assert "Batch complete:" in result.stderr, (
            f"Expected summary. stderr: {result.stderr}"
        )

    def test_cli_single_file_still_works(self):
        """Single file conversion should still work as before."""
        test_file = os.path.join(TEST_FILES_DIR, "test.json")
        if os.path.exists(test_file):
            result = subprocess.run(
                ["python", "-m", "markitdown", test_file],
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0
            assert len(result.stdout) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
