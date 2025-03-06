import json
import subprocess
import locale
import sys
import shutil
import os
import warnings
from typing import BinaryIO, Optional, Any


def exiftool_metadata(
    file_stream: BinaryIO, *, exiftool_path: Optional[str] = None
) -> Any:  # Need a better type for json data
    # Check if we have a valid pointer to exiftool
    if not exiftool_path:
        which_exiftool = shutil.which("exiftool")
        if which_exiftool:
            warnings.warn(
                f"""Implicit discovery of 'exiftool' is disabled. If you would like to continue to use exiftool in MarkItDown, please set the exiftool_path parameter in the MarkItDown consructor. E.g., 

    md = MarkItDown(exiftool_path="{which_exiftool}")

This warning will be removed in future releases.
""",
                DeprecationWarning,
            )
        # Nothing to do
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
