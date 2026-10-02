"""Shared helpers for converters that write Markdown directly."""

import re


# Matches a pipe together with the (possibly empty) run of backslashes in front
# of it, so that run can be doubled before the pipe is escaped.
# The lookbehind avoids retrying from each position inside a backslash run.
_PIPE_ESCAPE_RE = re.compile(r"(?<!\\)(\\*)\|")


def _escape_table_cell(value: str) -> str:
    r"""Escape a value so it is safe inside a Markdown table cell.

    A pipe is a column separator, so it must be escaped.
    Line breaks would end the row early, so they collapse to a single space.
    """
    value = _PIPE_ESCAPE_RE.sub(lambda m: m.group(1) * 2 + r"\|", value)
    return value.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
