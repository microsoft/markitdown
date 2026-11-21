import base64
import ipaddress
import ntpath
import os
import socket
from typing import Tuple, Dict
from urllib.request import url2pathname
from urllib.parse import urlparse, unquote_to_bytes


def _is_unc_or_device_path(path: str) -> bool:
    """Recognize Windows UNC and device namespace prefixes on any platform."""
    drive, _ = ntpath.splitdrive(path)
    return drive.replace("\\", "/").startswith("//")


def file_uri_to_path(file_uri: str) -> Tuple[str | None, str]:
    """Convert a file URI to a path, rejecting UNC and Windows device paths."""
    parsed = urlparse(file_uri)
    if parsed.scheme != "file":
        raise ValueError(f"Not a file URL: {file_uri}")

    decoded_path = unquote_to_bytes(parsed.path).replace(b"\\", b"/")
    if decoded_path.startswith(b"//"):
        raise ValueError(
            f"Unsupported file URI: {file_uri}. "
            "UNC and Windows device paths are not supported."
        )

    netloc = parsed.netloc if parsed.netloc else None
    path = url2pathname(parsed.path)
    if os.name == "nt" and path[:1] in "/\\" and path[2:3] == ":":
        path = path[1:]
    path = os.path.abspath(path)

    if _is_unc_or_device_path(path):
        raise ValueError(
            f"Unsupported file URI: {file_uri}. "
            "UNC and Windows device paths are not supported."
        )
    return netloc, path


def parse_data_uri(uri: str) -> Tuple[str | None, Dict[str, str], bytes]:
    if uri[:5].lower() != "data:":
        raise ValueError("Not a data URI")

    header, _, data = uri.partition(",")
    if not _:
        raise ValueError("Malformed data URI, missing ',' separator")

    meta = header[5:]  # Strip 'data:'
    parts = meta.split(";")

    is_base64 = False
    # Ends with base64?
    if parts[-1].lower() == "base64":
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
            attributes[key.lower()] = value
        elif len(part) > 0:
            attributes[part.lower()] = ""

    content = base64.b64decode(data) if is_base64 else unquote_to_bytes(data)

    return mime_type, attributes, content


def is_ssrf_safe_host(hostname: str | None) -> bool:
    """Return False if hostname resolves to a private or local address.

    Blocking these addresses stops markitdown from being used as an SSRF proxy
    to reach internal services (e.g. instance metadata) when converting a
    user-supplied http/https URL.
    """
    if not hostname:
        return True
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return True  # Unresolvable hosts cannot be fetched anyway
    for info in infos:
        sockaddr = info[4]
        try:
            ip = ipaddress.ip_address(sockaddr[0])
        except ValueError:
            continue
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            return False
    return True
