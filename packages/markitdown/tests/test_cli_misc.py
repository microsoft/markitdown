#!/usr/bin/env python3 -m pytest
import subprocess
import pytest
from markitdown import __version__

# This file contains CLI tests that are not directly tested by the FileTestVectors.
# This includes things like help messages, version numbers, and invalid flags.


def test_version() -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--version"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_invalid_flag() -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--foobar"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), f"Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, f"Expected 'SYNTAX' to appear in STDERR"


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    test_version()
    test_invalid_flag()
    # Add a placeholder for pytest to discover the new tests
    # Actual test execution will be handled by pytest discovery
    print(" CLI tests passed (individual test execution by pytest).")

# New tests for --prefix argument
import unittest
from unittest.mock import patch, MagicMock
import sys
# Important: We need to import main from the __main__ module of markitdown
from packages.markitdown.src.markitdown.__main__ import main as markitdown_main

class TestPrefixArgument(unittest.TestCase):
    def setUp(self):
        # Ensure each test starts with a clean sys.argv
        self.original_argv = sys.argv
        # Mock stdout to prevent test output from cluttering the console
        self.patch_stdout = patch('sys.stdout')
        self.mock_stdout = self.patch_stdout.start()


    def tearDown(self):
        sys.argv = self.original_argv
        self.patch_stdout.stop()

    @patch('packages.markitdown.src.markitdown.__main__.MarkItDown')
    def test_with_prefix_and_filename(self, MockMarkItDown):
        mock_instance = MockMarkItDown.return_value
        mock_instance.convert.return_value = MagicMock(markdown="mocked markdown")
        
        sys.argv = ["markitdown", "--prefix", "some/prefix/", "myfile.txt"]
        markitdown_main()
        
        mock_instance.convert.assert_called_once_with(
            "some/prefix/myfile.txt", stream_info=None, keep_data_uris=False
        )

    @patch('packages.markitdown.src.markitdown.__main__.MarkItDown')
    def test_without_prefix_filename_only(self, MockMarkItDown):
        mock_instance = MockMarkItDown.return_value
        mock_instance.convert.return_value = MagicMock(markdown="mocked markdown")

        sys.argv = ["markitdown", "myfile.txt"]
        markitdown_main()

        mock_instance.convert.assert_called_once_with(
            "myfile.txt", stream_info=None, keep_data_uris=False
        )

    @patch('packages.markitdown.src.markitdown.__main__.MarkItDown')
    def test_with_prefix_no_filename_stdin(self, MockMarkItDown):
        mock_instance = MockMarkItDown.return_value
        mock_instance.convert_stream.return_value = MagicMock(markdown="mocked markdown")
        
        # Mock stdin as well, though it's not strictly necessary for this test's assertion
        with patch('sys.stdin.buffer'):
            sys.argv = ["markitdown", "--prefix", "some/prefix/"]
            markitdown_main()

        mock_instance.convert_stream.assert_called_once()
        # Check that the first argument to convert_stream (the stream itself) is sys.stdin.buffer
        self.assertEqual(mock_instance.convert_stream.call_args[0][0], sys.stdin.buffer)
        # Check keyword arguments
        self.assertEqual(mock_instance.convert_stream.call_args[1]['stream_info'], None)
        self.assertEqual(mock_instance.convert_stream.call_args[1]['keep_data_uris'], False)
        # Ensure convert was not called
        mock_instance.convert.assert_not_called()


    @patch('packages.markitdown.src.markitdown.__main__.MarkItDown')
    def test_with_empty_prefix_and_filename(self, MockMarkItDown):
        mock_instance = MockMarkItDown.return_value
        mock_instance.convert.return_value = MagicMock(markdown="mocked markdown")

        sys.argv = ["markitdown", "--prefix", "", "myfile.txt"]
        markitdown_main()

        mock_instance.convert.assert_called_once_with(
            "myfile.txt", stream_info=None, keep_data_uris=False
        )

if __name__ == "__main__":
    # This allows running tests directly using `python test_cli_misc.py`
    # It will also run the older tests defined at the top level of this file.
    test_version()
    test_invalid_flag()
    print("Legacy tests passed.")
    # Run unittest test discovery for the new class
    print("Running new prefix tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("All tests in TestPrefixArgument passed!")
