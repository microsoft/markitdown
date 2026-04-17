#!/usr/bin/env python3 -m pytest
import os
import shutil
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch

from markitdown import MarkItDown, DocumentConverterResult

# This file contains tests for the bulk conversion feature

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")


def test_convert_directory_basic():
    """Test basic directory conversion functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create test files
        test_file1 = source_dir / "test.txt"
        test_file2 = source_dir / "test2.txt"
        
        test_file1.write_text("# Test Document 1\nThis is a test document.")
        test_file2.write_text("# Test Document 2\nThis is another test document.")
        
        # Test conversion
        md = MarkItDown()
        results = md.convert_directory(source_dir, output_dir)
        
        # Verify results
        assert len(results) == 2
        assert output_dir.exists()
        assert (output_dir / "test.md").exists()
        assert (output_dir / "test2.md").exists()
        
        # Verify content
        content1 = (output_dir / "test.md").read_text()
        content2 = (output_dir / "test2.md").read_text()
        
        assert "Test Document 1" in content1
        assert "Test Document 2" in content2


def test_convert_directory_with_extensions():
    """Test directory conversion with file extension filtering."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create test files with different extensions
        (source_dir / "test.txt").write_text("# Text Document")
        (source_dir / "test.docx").write_text("# DOCX Document")
        (source_dir / "test.pdf").write_text("# PDF Document")
        
        # Test conversion with only .txt files
        md = MarkItDown()
        results = md.convert_directory(source_dir, output_dir, extensions=["txt"])
        
        # Verify only .txt files were converted
        assert len(results) == 1
        assert (output_dir / "test.md").exists()
        assert not (output_dir / "test.docx.md").exists()
        assert not (output_dir / "test.pdf.md").exists()


def test_convert_directory_recursive():
    """Test directory conversion with recursive search."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create files in subdirectories
        (source_dir / "test.txt").write_text("# Root Document")
        (source_dir / "subdir").mkdir()
        (source_dir / "subdir" / "sub_test.txt").write_text("# Sub Document")
        
        # Test recursive conversion
        md = MarkItDown()
        results = md.convert_directory(source_dir, output_dir, recursive=True)
        
        # Verify both files were converted
        assert len(results) == 2
        assert (output_dir / "test.md").exists()
        assert (output_dir / "sub_test.md").exists()


def test_convert_directory_non_recursive():
    """Test directory conversion without recursive search."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create files in subdirectories
        (source_dir / "test.txt").write_text("# Root Document")
        (source_dir / "subdir").mkdir()
        (source_dir / "subdir" / "sub_test.txt").write_text("# Sub Document")
        
        # Test non-recursive conversion (default)
        md = MarkItDown()
        results = md.convert_directory(source_dir, output_dir, recursive=False)
        
        # Verify only root file was converted
        assert len(results) == 1
        assert (output_dir / "test.md").exists()
        assert not (output_dir / "sub_test.md").exists()


def test_convert_batch():
    """Test batch conversion with specific file list."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create test files
        file1 = source_dir / "test1.txt"
        file2 = source_dir / "test2.txt"
        file3 = source_dir / "test3.txt"
        
        file1.write_text("# Document 1")
        file2.write_text("# Document 2")
        file3.write_text("# Document 3")
        
        # Test batch conversion with specific files
        md = MarkItDown()
        results = md.convert_batch([file1, file3], output_dir)
        
        # Verify only specified files were converted
        assert len(results) == 2
        assert (output_dir / "test1.md").exists()
        assert (output_dir / "test3.md").exists()
        assert not (output_dir / "test2.md").exists()


def test_convert_batch_nonexistent_file():
    """Test batch conversion with nonexistent file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Create one test file
        existing_file = source_dir / "test.txt"
        existing_file.write_text("# Test Document")
        
        # Test batch conversion with nonexistent file
        md = MarkItDown()
        results = md.convert_batch([existing_file, "nonexistent.txt"], output_dir)
        
        # Verify only existing file was converted
        assert len(results) == 1
        assert (output_dir / "test.md").exists()


def test_convert_directory_empty():
    """Test conversion of empty directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        
        # Test conversion of empty directory
        md = MarkItDown()
        results = md.convert_directory(source_dir, output_dir)
        
        # Verify no files were converted
        assert len(results) == 0
        assert output_dir.exists()


def test_convert_directory_nonexistent():
    """Test conversion of nonexistent directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "nonexistent"
        output_dir = Path(temp_dir) / "output"
        
        # Test conversion of nonexistent directory
        md = MarkItDown()
        
        # Should raise ValueError
        with pytest.raises(ValueError, match="Source directory does not exist"):
            md.convert_directory(source_dir, output_dir)


def test_convert_directory_not_directory():
    """Test conversion when source is not a directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_file = Path(temp_dir) / "not_a_dir.txt"
        source_file.write_text("# Not a directory")
        output_dir = Path(temp_dir) / "output"
        
        # Test conversion when source is not a directory
        md = MarkItDown()
        
        # Should raise ValueError
        with pytest.raises(ValueError, match="Source path is not a directory"):
            md.convert_directory(source_file, output_dir)


def test_find_files_basic():
    """Test the _find_files helper method."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir)
        
        # Create test files
        (source_dir / "test.txt").write_text("test")
        (source_dir / "test.docx").write_text("test")
        (source_dir / "subdir").mkdir()
        (source_dir / "subdir" / "sub.txt").write_text("test")
        
        # Test finding files
        md = MarkItDown()
        files = md._find_files(source_dir)
        
        # Should find files in root directory only
        assert len(files) == 2
        assert any(f.name == "test.txt" for f in files)
        assert any(f.name == "test.docx" for f in files)


def test_find_files_with_extensions():
    """Test the _find_files helper method with extension filtering."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir)
        
        # Create test files
        (source_dir / "test.txt").write_text("test")
        (source_dir / "test.docx").write_text("test")
        (source_dir / "test.pdf").write_text("test")
        
        # Test finding files with extension filter
        md = MarkItDown()
        files = md._find_files(source_dir, extensions=["txt", "pdf"])
        
        # Should find only .txt and .pdf files
        assert len(files) == 2
        assert any(f.name == "test.txt" for f in files)
        assert any(f.name == "test.pdf" for f in files)
        assert not any(f.name == "test.docx" for f in files)


def test_find_files_recursive():
    """Test the _find_files helper method with recursive search."""
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir)
        
        # Create test files
        (source_dir / "test.txt").write_text("test")
        (source_dir / "subdir").mkdir()
        (source_dir / "subdir" / "sub.txt").write_text("test")
        
        # Test finding files recursively
        md = MarkItDown()
        files = md._find_files(source_dir, recursive=True)
        
        # Should find files in both root and subdirectory
        assert len(files) == 2
        assert any(f.name == "test.txt" for f in files)
        assert any(f.name == "sub.txt" for f in files)


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    import pytest
    pytest.main([__file__])
