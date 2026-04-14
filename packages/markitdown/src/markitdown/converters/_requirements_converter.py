import re
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo

ACCEPTED_FILE_EXTENSIONS = [".txt"]
PIPFILE_FILENAME = "Pipfile"


def _parse_requirements_line(line: str):
    """Parse a single requirements.txt line.
    Returns (package, version_constraint, note) or None to skip.
    """
    # Strip inline comment
    note = ""
    if " #" in line or "\t#" in line:
        parts = re.split(r"\s+#", line, maxsplit=1)
        line = parts[0].strip()
        note = parts[1].strip() if len(parts) > 1 else ""
    elif line.startswith("#"):
        return None

    line = line.strip()
    if not line:
        return None

    # Skip options like -r, -c, --index-url, etc.
    if line.startswith("-"):
        return None

    # Split package from version specifier
    # Handles: pkg==1.0, pkg>=1.0,<2.0, pkg[extra]>=1.0, pkg @ url
    match = re.match(
        r"^([A-Za-z0-9_\-\.]+(?:\[[^\]]*\])?)\s*(@.+|[><=!~^][^#]*)?$",
        line,
    )
    if match:
        package = match.group(1).strip()
        version = (match.group(2) or "").strip()
        return package, version, note

    return None


def _parse_pipfile(content: str):
    """Very simple Pipfile parser — extract [packages] and [dev-packages] sections."""
    rows = []
    in_packages = False
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith("[packages]") or line.startswith("[dev-packages]"):
            in_packages = True
            continue
        if line.startswith("[") and in_packages:
            in_packages = False
            continue
        if not in_packages:
            continue
        if not line or line.startswith("#"):
            continue
        # Lines like: requests = "*" or requests = ">=2.0"
        match = re.match(r'^([A-Za-z0-9_\-\.]+)\s*=\s*["\']?([^"\']*)["\']?', line)
        if match:
            package = match.group(1).strip()
            version = match.group(2).strip()
            if version == "*":
                version = ""
            rows.append((package, version, ""))
    return rows


def _rows_to_markdown_table(rows) -> str:
    """Render a list of (package, version, note) tuples as a Markdown table."""
    lines = [
        "| Package | Version Constraint | Notes |",
        "| --- | --- | --- |",
    ]
    for package, version, note in rows:
        lines.append(f"| {package} | {version} | {note} |")
    return "\n".join(lines)


class RequirementsConverter(DocumentConverter):
    """
    Converts requirements.txt / requirements*.txt / Pipfile to a Markdown table.
    Columns: Package | Version Constraint | Notes
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        filename = (stream_info.filename or "").strip()
        extension = (stream_info.extension or "").lower()

        # Accept Pipfile exactly
        if filename == PIPFILE_FILENAME:
            return True

        # Accept .txt files whose filename matches requirements*.txt
        if extension in ACCEPTED_FILE_EXTENSIONS:
            if re.match(r"requirements.*\.txt$", filename, re.IGNORECASE):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        encoding = stream_info.charset or "utf-8"
        content = file_stream.read().decode(encoding)
        filename = (stream_info.filename or "").strip()

        if filename == PIPFILE_FILENAME:
            rows = _parse_pipfile(content)
            title = "Pipfile Dependencies"
        else:
            rows = []
            for line in content.splitlines():
                parsed = _parse_requirements_line(line)
                if parsed:
                    rows.append(parsed)
            title = f"{filename} Dependencies"

        if not rows:
            markdown = f"# {title}\n\n_No dependencies found._"
        else:
            markdown = f"# {title}\n\n{_rows_to_markdown_table(rows)}"

        return DocumentConverterResult(markdown=markdown, title=title)
