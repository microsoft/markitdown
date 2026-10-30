import json
import subprocess
from typing import Any, BinaryIO, Union


def _parse_version(version: str) -> tuple:
    return tuple(map(int, (version.split("."))))


# Upper bound for each exiftool invocation. ExifTool normally answers in
# well under a second; the timeout exists so a hung or pathological process
# cannot block a conversion indefinitely.
DEFAULT_TIMEOUT_SECONDS = 120.0


def exiftool_metadata(
    file_stream: BinaryIO,
    *,
    exiftool_path: Union[str, None],
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> Any:  # Need a better type for json data
    # Nothing to do
    if not exiftool_path:
        return {}

    # Verify exiftool version
    try:
        version_output = subprocess.run(
            [exiftool_path, "-ver"],
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        ).stdout.strip()
        version = _parse_version(version_output)
        min_version = (12, 24)
        if version < min_version:
            raise RuntimeError(
                f"ExifTool version {version_output} is vulnerable to CVE-2021-22204. "
                "Please upgrade to version 12.24 or later."
            )
    except OSError as e:
        raise RuntimeError(f"Failed to invoke exiftool at {exiftool_path}: {e}") from e
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(
            f"ExifTool version check timed out after {timeout} seconds."
        ) from e
    except (subprocess.CalledProcessError, ValueError) as e:
        raise RuntimeError("Failed to verify ExifTool version.") from e

    # Run exiftool
    cur_pos = file_stream.tell()
    try:
        output = subprocess.run(
            [exiftool_path, "-json", "-"],
            input=file_stream.read(),
            capture_output=True,
            text=False,
            timeout=timeout,
        ).stdout

        return json.loads(
            output.decode(
                "utf-8"
            ),  # ExifTool always outputs UTF-8 encoded JSON, even if the input file is not UTF-8 encoded
        )[0]
    except OSError as e:
        raise RuntimeError(f"Failed to invoke exiftool at {exiftool_path}: {e}") from e
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(
            f"ExifTool metadata extraction timed out after {timeout} seconds."
        ) from e
    finally:
        file_stream.seek(cur_pos)
