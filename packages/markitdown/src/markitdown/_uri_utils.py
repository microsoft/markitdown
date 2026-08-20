import base64
import os
from typing import Tuple, Dict
from urllib.request import url2pathname
from urllib.parse import urlparse, unquote_to_bytes


def file_uri_to_path(file_uri: str) -> Tuple[str | None, str]:
    """Convert a file URI to a local file path"""
    parsed = urlparse(file_uri)
    if parsed.scheme != "file":
        raise ValueError(f"Not a file URL: {file_uri}")

    netloc = parsed.netloc if parsed.netloc else None
    path = url2pathname(parsed.path)

    # On Windows, we need to guard against UNC path bypass attempts
    # (where UNC paths are encoded in the URI path component to bypass netloc checks)
    if os.name == 'nt':
        # Check for UNC path in the path component (bypasses netloc check)
        if netloc is None and (path.startswith('\\\\') or path.startswith('//')):
            # Extract the server name part from potential UNC path
            # Both \\server\share and //server/share start the server name after the 2nd char
            unc_part = path[2:]

            # Get the server name by splitting on the first separator
            potential_server = unc_part.replace('/', '\\').split('\\', 1)[0]

            # If it looks like a server name (doesn't contain : for drive letters like C:)
            # and is not empty, it's likely a UNC path attempt
            if potential_server and ':' not in potential_server:
                raise ValueError(f"File URI contains UNC path in path component: {file_uri}")

    path = os.path.abspath(path)
    return netloc, path


def parse_data_uri(uri: str) -> Tuple[str | None, Dict[str, str], bytes]:
    if not uri.startswith("data:"):
        raise ValueError("Not a data URI")

    header, _, data = uri.partition(",")
    if not _:
        raise ValueError("Malformed data URI, missing ',' separator")

    meta = header[5:]  # Strip 'data:'
    parts = meta.split(";")

    is_base64 = False
    # Ends with base64?
    if parts[-1] == "base64":
        parts.pop()
        is_base64 = True

    mime_type = None  # Normally this would default to text/plain but we won't assume
    if len(parts) and len(parts[0]) > 0:
        # First part is the mime type
        mime_type = parts.pop(0)

    attributes: Dict[str, str] = {}
    for part in parts:
        # Handle key=value pairs in the middle
        if "=" in part:
            key, value = part.split("=", 1)
            attributes[key] = value
        elif len(part) > 0:
            attributes[part] = ""

    content = base64.b64decode(data) if is_base64 else unquote_to_bytes(data)

    return mime_type, attributes, content
