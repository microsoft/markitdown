# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import sys
from textwrap import dedent

from .__about__ import __version__
from ._markitdown import MarkItDown


def main():
    parser = argparse.ArgumentParser(
        description="Convert various file formats to markdown.",
        prog="markitdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=dedent(
            """
            SYNTAX:

                markitdown <OPTIONAL: FILENAME>
                If FILENAME is empty, markitdown reads from stdin.

            EXAMPLE:

                markitdown example.pdf

                OR

                cat example.pdf | markitdown

                OR

                markitdown < example.pdf
            """
        ).strip(),
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show the version number and exit",
    )

    parser.add_argument("filename", nargs="?")
    args = parser.parse_args()

    if args.filename is None:
        markitdown = MarkItDown()
        result = markitdown.convert_stream(sys.stdin.buffer)
        print(result.text_content)
    else:
        markitdown = MarkItDown()
        result = markitdown.convert(args.filename)
        print(result.text_content)


if __name__ == "__main__":
    main()
