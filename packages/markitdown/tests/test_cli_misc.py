#!/usr/bin/env python3 -m pytest
import os
import subprocess
import tempfile
from pathlib import Path
from markitdown import __version__

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.


def test_version() -> None:
    result = subprocess.run(
        ["python3", "-m", "markitdown", "--version"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_invalid_flag() -> None:
    result = subprocess.run(
        ["python3", "-m", "markitdown", "--foobar"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), "Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, "Expected 'SYNTAX' to appear in STDERR"


def test_batch_conversion_basic():
    """Test basic batch conversion CLI functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create test files
        (source_dir / "test1.txt").write_text("# Document 1\nContent 1")
        (source_dir / "test2.txt").write_text("# Document 2\nContent 2")
        
        # Test batch conversion
        result = subprocess.run(
            ["python3", "-m", "markitdown", "--batch", str(source_dir), "--output-dir", str(output_dir)],
            capture_output=True, text=True
        )
        
        assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
        assert "Successfully converted 2 files" in result.stdout
        assert output_dir.exists()
        assert (output_dir / "test1.md").exists()
        assert (output_dir / "test2.md").exists()


def test_batch_conversion_with_extensions():
    """Test batch conversion with file extension filtering."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create test files with different extensions
        (source_dir / "test.txt").write_text("# Text Document")
        (source_dir / "test.docx").write_text("# DOCX Document")
        
        # Test batch conversion with only .txt files
        result = subprocess.run(
            ["python3", "-m", "markitdown", "--batch", str(source_dir), "--output-dir", str(output_dir), "--extensions", "txt"],
            capture_output=True, text=True
        )
        
        assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
        assert "Successfully converted 1 files" in result.stdout
        assert (output_dir / "test.md").exists()


def test_batch_conversion_missing_output_dir():
    """Test batch conversion without output directory (should fail)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        source_dir.mkdir()
        
        # Create test file
        (source_dir / "test.txt").write_text("# Test Document")
        
        # Test batch conversion without output directory
        result = subprocess.run(
            ["python3", "-m", "markitdown", "--batch", str(source_dir)],
            capture_output=True, text=True
        )
        
        assert result.returncode != 0, "CLI should have failed"
        assert "--output-dir is required when using --batch" in result.stderr


def test_batch_conversion_with_filename():
    """Test batch conversion with filename (should fail)."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create test file
        test_file = source_dir / "test.txt"
        test_file.write_text("# Test Document")
        
        # Test batch conversion with filename
        result = subprocess.run(
            ["python3", "-m", "markitdown", "--batch", str(source_dir), "--output-dir", str(output_dir), str(test_file)],
            capture_output=True, text=True
        )
        
        assert result.returncode != 0, "CLI should have failed"
        assert "Cannot specify both --batch and a filename" in result.stderr


def test_batch_conversion_recursive():
    """Test batch conversion with recursive search."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create files in subdirectories
        (source_dir / "test.txt").write_text("# Root Document")
        (source_dir / "subdir").mkdir()
        (source_dir / "subdir" / "sub_test.txt").write_text("# Sub Document")
        
        # Test recursive batch conversion
        result = subprocess.run(
            ["python3", "-m", "markitdown", "--batch", str(source_dir), "--output-dir", str(output_dir), "--recursive"],
            capture_output=True, text=True
        )
        
        assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
        assert "Successfully converted 2 files" in result.stdout
        assert (output_dir / "test.md").exists()
        assert (output_dir / "subdir" / "sub_test.md").exists()


def test_batch_conversion_empty_directory():
    """Test batch conversion with empty directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Test batch conversion with empty directory
        result = subprocess.run(
            ["python3", "-m", "markitdown", "--batch", str(source_dir), "--output-dir", str(output_dir)],
            capture_output=True, text=True
        )
        
        assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
        assert "No files were converted" in result.stdout


def test_batch_conversion_nonexistent_directory():
    """Test batch conversion with nonexistent directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "nonexistent"
        output_dir = Path(temp_dir) / "output"
        
        # Test batch conversion with nonexistent directory
        result = subprocess.run(
            ["python3", "-m", "markitdown", "--batch", str(source_dir), "--output-dir", str(output_dir)],
            capture_output=True, text=True
        )
        
        assert result.returncode != 0, "CLI should have failed"
        assert "Batch conversion failed" in result.stderr


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    test_batch_conversion_basic()
    test_batch_conversion_with_extensions()
    test_batch_conversion_missing_output_dir()
    test_batch_conversion_with_filename()
    test_batch_conversion_recursive()
    test_batch_conversion_empty_directory()
    test_batch_conversion_nonexistent_directory()
    print("All tests passed!")
