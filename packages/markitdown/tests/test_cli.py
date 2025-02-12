#!/usr/bin/env python3 -m pytest
import os
import subprocess
import pytest
from markitdown import __version__

try:
    from .test_markitdown import TEST_FILES_DIR, DOCX_TEST_STRINGS
except ImportError:
    from test_markitdown import TEST_FILES_DIR, DOCX_TEST_STRINGS


@pytest.fixture(scope="session")
def shared_tmp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("pytest_tmp")


def test_version(shared_tmp_dir) -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--version"], capture_output=True, text=True
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert __version__ in result.stdout, f"Version not found in output: {result.stdout}"


def test_invalid_flag(shared_tmp_dir) -> None:
    result = subprocess.run(
        ["python", "-m", "markitdown", "--foobar"], capture_output=True, text=True
    )

    assert result.returncode != 0, f"CLI exited with error: {result.stderr}"
    assert (
        "unrecognized arguments" in result.stderr
    ), f"Expected 'unrecognized arguments' to appear in STDERR"
    assert "SYNTAX" in result.stderr, f"Expected 'SYNTAX' to appear in STDERR"


def test_output_to_stdout(shared_tmp_dir) -> None:
    # DOC X
    result = subprocess.run(
        ["python", "-m", "markitdown", os.path.join(TEST_FILES_DIR, "test.docx")],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    for test_string in DOCX_TEST_STRINGS:
        assert (
            test_string in result.stdout
        ), f"Expected string not found in output: {test_string}"


def test_output_to_file(shared_tmp_dir) -> None:
    # DOC X, flag -o at the end
    docx_output_file_1 = os.path.join(shared_tmp_dir, "test_docx_1.md")
    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            os.path.join(TEST_FILES_DIR, "test.docx"),
            "-o",
            docx_output_file_1,
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert os.path.exists(
        docx_output_file_1
    ), f"Output file not created: {docx_output_file_1}"

    with open(docx_output_file_1, "r") as f:
        output = f.read()
        for test_string in DOCX_TEST_STRINGS:
            assert (
                test_string in output
            ), f"Expected string not found in output: {test_string}"

    # DOC X, flag -o at the beginning
    docx_output_file_2 = os.path.join(shared_tmp_dir, "test_docx_2.md")
    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            "-o",
            docx_output_file_2,
            os.path.join(TEST_FILES_DIR, "test.docx"),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert os.path.exists(
        docx_output_file_2
    ), f"Output file not created: {docx_output_file_2}"

    with open(docx_output_file_2, "r") as f:
        output = f.read()
        for test_string in DOCX_TEST_STRINGS:
            assert (
                test_string in output
            ), f"Expected string not found in output: {test_string}"


if __name__ == "__main__":
    """Runs this file's tests from the command line."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_version(tmp_dir)
        test_invalid_flag(tmp_dir)
        test_output_to_stdout(tmp_dir)
        test_output_to_file(tmp_dir)
    print("All tests passed!")
