"""
Reproducer for microsoft/markitdown issue #1408.



When a .docx/.pptx/.xlsx file is corrupt or is not a valid OOXML archive,
MarkItDown should raise FileConversionException. Instead it silently
returns a DocumentConverterResult containing the raw text content of the
invalid file — making it impossible for callers to distinguish a successful
conversion from a failed one using normal exception handling.

Root cause
----------
The conversion loop in _markitdown._convert() tries converters in priority
order. When a specific converter (e.g. PptxConverter, priority=0) accepts a
file by extension and then fails, markitdown records the failure and continues
to the next stream_info guess. Magika has by then identified the file content
as plain text (with a charset), so PlainTextConverter.accepts() returns True
on the next guess, and the conversion "succeeds" with the raw bytes as output.

Run:
    python reproduce_issue_1408.py
"""

import os
import tempfile

from markitdown import MarkItDown, FileConversionException

# A plain-text file masquerading as OOXML — not a valid ZIP/OOXML archive.
FAKE_CONTENT = b"This is definitely not a real Office document."


def _try_convert(md: MarkItDown, path: str, label: str) -> None:
    print(f"\n--- {label} ---")
    try:
        result = md.convert(path)
        # Bug: we reach here instead of the except block.
        print(f"  BUG: No exception raised.")
        print(f"  text_content = {result.text_content!r}")
    except FileConversionException as exc:
        print(f"  FIXED: FileConversionException raised as expected.")
        print(f"  {exc}")
    except Exception as exc:
        print(f"  Unexpected {type(exc).__name__}: {exc}")


def main():
    print("=== Reproducer for issue #1408 ===")
    print(
        "Each test creates a plain-text file with an OOXML extension.\n"
        "Expected: FileConversionException.  Actual (bug): silent success.\n"
    )

    md = MarkItDown()

    for ext in (".docx", ".pptx", ".xlsx"):
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
            f.write(FAKE_CONTENT)
            path = f.name
        try:
            _try_convert(md, path, f"fake {ext}")
        finally:
            os.unlink(path)

    print()


if __name__ == "__main__":
    main()
