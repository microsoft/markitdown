import json
import subprocess
import locale
from typing import BinaryIO, Any, Union


def exiftool_metadata(
    file_stream: BinaryIO,
    *,
    exiftool_path: Union[str, None],
) -> Any:  # Need a better type for json data
    # Nothing to do
    if not exiftool_path:
        return {}

    # Run exiftool
    cur_pos = file_stream.tell()
    try:
        output = subprocess.run(
            [exiftool_path, "-json", "-"],
            input=file_stream.read(),
            capture_output=True,
            text=False,
        ).stdout

        return json.loads(
            output.decode(locale.getpreferredencoding(False)),
        )[0]
    finally:
        file_stream.seek(cur_pos)
