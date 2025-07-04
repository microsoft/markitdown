import re
from urllib.parse import urlparse, urljoin


def convert_relative_to_absolute_path(resource_url: str, path: str) -> str:
    """
    Convert a relative path to an absolute path based on the current URL.
    """
    if not isinstance(resource_url, str) or not isinstance(path, str):
        return path

    try:
        parsed_url = urlparse(path)
        if parsed_url.netloc:
            return path

        parsed_base = urlparse(resource_url)
        normalized_path = urljoin(parsed_base.path, path)

        # Security: Check for path traversal attempts
        if re.search(r'(\.\./|~)', normalized_path):
            return path  # Fail-safe: return original path if traversal detected

        return parsed_base._replace(path=normalized_path).geturl()
    except Exception as e:
        # Improved logging (ensure logging is imported and configured elsewhere)
        import logging
        logging.warning(f"Path conversion error: {type(e).__name__}: {str(e)}")
        return path
