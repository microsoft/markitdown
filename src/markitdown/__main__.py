# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import sys
import argparse
from ._markitdown import MarkItDown


def main():
    parser = argparse.ArgumentParser(
        description="Convert various file formats to markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  markitdown example.pdf
  cat example.pdf | markitdown
  markitdown < example.pdf""",
    )

    parser.add_argument(
        "filename", nargs="?", help="if unspecified, defaults to stdin"
    )
    args = parser.parse_args()
    markitdown = MarkItDown()
    result = markitdown.convert(args.filename or sys.stdin.buffer)
    print(result.text_content)


if __name__ == "__main__":
    main()
