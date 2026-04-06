import json
import locale
import os
import shutil
import subprocess
from typing import Any, BinaryIO, Union


def _parse_version(version: str) -> tuple:
    return tuple(map(int, (version.split("."))))


def exiftool_metadata(
    file_stream: BinaryIO,
    *,
    exiftool_path: Union[str, None],
) -> Any:  # Need a better type for json data
    # Nothing to do
    if not exiftool_path:
        return {}

    # Validate the exiftool path to prevent path traversal and ensure it resolves
    # to an actual executable before passing it to subprocess
    resolved_path = shutil.which(exiftool_path)
    if not resolved_path:
        raise RuntimeError(
            f"ExifTool executable not found or not executable: {exiftool_path}"
        )
    # Use the fully-resolved absolute path to prevent any path manipulation
    exiftool_path = os.path.realpath(resolved_path)

    # Verify exiftool version
    try:
        version_output = subprocess.run(
            [exiftool_path, "-ver"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        ).stdout.strip()
        version = _parse_version(version_output)
        min_version = (12, 24)
        if version < min_version:
            raise RuntimeError(
                f"ExifTool version {version_output} is vulnerable to CVE-2021-22204. "
                "Please upgrade to version 12.24 or later."
            )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError) as e:
        raise RuntimeError("Failed to verify ExifTool version.") from e

    # Run exiftool — pass file content via stdin using "-" so that no user-controlled
    # file path is ever passed as a command-line argument to ExifTool.
    # The "--" separator is added to prevent any argument injection.
    cur_pos = file_stream.tell()
    try:
        output = subprocess.run(
            [exiftool_path, "-json", "--", "-"],
            input=file_stream.read(),
            capture_output=True,
            text=False,
            timeout=120,
        ).stdout

        return json.loads(
            output.decode(locale.getpreferredencoding(False)),
        )[0]
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("ExifTool timed out while processing file.") from e
    finally:
        file_stream.seek(cur_pos)
