#!/usr/bin/env python3 -m pytest
import os
import time
import pytest
import subprocess
import locale
from typing import List

if __name__ == "__main__":
    from _test_vectors import (
        GENERAL_TEST_VECTORS,
        DATA_URI_TEST_VECTORS,
        FileTestVector,
    )
else:
    from ._test_vectors import (
        GENERAL_TEST_VECTORS,
        DATA_URI_TEST_VECTORS,
        FileTestVector,
    )

skip_remote = (
    True if os.environ.get("GITHUB_ACTIONS") else False
)  # Don't run these tests in CI

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
TEST_FILES_URL = "https://raw.githubusercontent.com/microsoft/markitdown/refs/heads/main/packages/markitdown/tests/test_files"


# Prepare CLI test vectors (remove vectors that require mockig the url)
CLI_TEST_VECTORS: List[FileTestVector] = []
for test_vector in GENERAL_TEST_VECTORS:
    if test_vector.url is not None:
        continue
    CLI_TEST_VECTORS.append(test_vector)


@pytest.fixture(scope="session")
def shared_tmp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("pytest_tmp")


@pytest.mark.parametrize("test_vector", CLI_TEST_VECTORS)
def test_output_to_stdout(shared_tmp_dir, test_vector) -> None:
    """Test that the CLI outputs to stdout correctly."""

    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            os.path.join(TEST_FILES_DIR, test_vector.filename),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    for test_string in test_vector.must_include:
        assert test_string in result.stdout
    for test_string in test_vector.must_not_include:
        assert test_string not in result.stdout


@pytest.mark.parametrize("test_vector", CLI_TEST_VECTORS)
def test_output_to_file(shared_tmp_dir, test_vector) -> None:
    """Test that the CLI outputs to a file correctly."""

    output_file = os.path.join(shared_tmp_dir, test_vector.filename + ".output")
    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            "-o",
            output_file,
            os.path.join(TEST_FILES_DIR, test_vector.filename),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert os.path.exists(output_file), f"Output file not created: {output_file}"

    with open(output_file, "r") as f:
        output_data = f.read()
        for test_string in test_vector.must_include:
            assert test_string in output_data
        for test_string in test_vector.must_not_include:
            assert test_string not in output_data

    os.remove(output_file)
    assert not os.path.exists(output_file), f"Output file not deleted: {output_file}"


@pytest.mark.parametrize("test_vector", CLI_TEST_VECTORS)
def test_input_from_stdin_without_hints(shared_tmp_dir, test_vector) -> None:
    """Test that the CLI readds from stdin correctly."""

    test_input = b""
    with open(os.path.join(TEST_FILES_DIR, test_vector.filename), "rb") as stream:
        test_input = stream.read()

    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            os.path.join(TEST_FILES_DIR, test_vector.filename),
        ],
        input=test_input,
        capture_output=True,
        text=False,
    )

    stdout = result.stdout.decode(locale.getpreferredencoding())
    assert (
        result.returncode == 0
    ), f"CLI exited with error: {result.stderr.decode('utf-8')}"
    for test_string in test_vector.must_include:
        assert test_string in stdout
    for test_string in test_vector.must_not_include:
        assert test_string not in stdout


@pytest.mark.skipif(
    skip_remote,
    reason="do not run tests that query external urls",
)
@pytest.mark.parametrize("test_vector", CLI_TEST_VECTORS)
def test_convert_url(shared_tmp_dir, test_vector):
    """Test the conversion of a stream with no stream info."""
    # Note: tmp_dir is not used here, but is needed to match the signature

    time.sleep(1)  # Ensure we don't hit rate limits
    result = subprocess.run(
        ["python", "-m", "markitdown", TEST_FILES_URL + "/" + test_vector.filename],
        capture_output=True,
        text=False,
    )

    stdout = result.stdout.decode(locale.getpreferredencoding())
    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    for test_string in test_vector.must_include:
        assert test_string in stdout
    for test_string in test_vector.must_not_include:
        assert test_string not in stdout


@pytest.mark.parametrize("test_vector", DATA_URI_TEST_VECTORS)
def test_output_to_file_with_data_uris(shared_tmp_dir, test_vector) -> None:
    """Test CLI functionality when keep_data_uris is enabled"""

    output_file = os.path.join(shared_tmp_dir, test_vector.filename + ".output")
    result = subprocess.run(
        [
            "python",
            "-m",
            "markitdown",
            "--keep-data-uris",
            "-o",
            output_file,
            os.path.join(TEST_FILES_DIR, test_vector.filename),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"CLI exited with error: {result.stderr}"
    assert os.path.exists(output_file), f"Output file not created: {output_file}"

    with open(output_file, "r") as f:
        output_data = f.read()
        for test_string in test_vector.must_include:
            assert test_string in output_data
        for test_string in test_vector.must_not_include:
            assert test_string not in output_data

    os.remove(output_file)
    assert not os.path.exists(output_file), f"Output file not deleted: {output_file}"


if __name__ == "__main__":
    import tempfile

    """Runs this file's tests from the command line."""

    with tempfile.TemporaryDirectory() as tmp_dir:
        # General tests
        for test_function in [
            test_output_to_stdout,
            test_output_to_file,
            test_input_from_stdin_without_hints,
            test_convert_url,
        ]:
            for test_vector in CLI_TEST_VECTORS:
                print(
                    f"Running {test_function.__name__} on {test_vector.filename}...",
                    end="",
                )
                test_function(tmp_dir, test_vector)
                print("OK")

        # Data URI tests
        for test_function in [
            test_output_to_file_with_data_uris,
        ]:
            for test_vector in DATA_URI_TEST_VECTORS:
                print(
                    f"Running {test_function.__name__} on {test_vector.filename}...",
                    end="",
                )
                test_function(tmp_dir, test_vector)
                print("OK")

    print("All tests passed!")
