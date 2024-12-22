# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import sys
from textwrap import dedent
from .__about__ import __version__
from ._markitdown import MarkItDown, DocumentConverterResult
import uvicorn


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
                
                OR to save to a file use
    
                markitdown example.pdf -o example.md
                
                OR
                
                markitdown example.pdf > example.md
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
    parser.add_argument(
        "-o",
        "--output",
        help="Output file name. If not provided, output is written to stdout.",
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start the FastAPI server",
    )
    args = parser.parse_args()

    if args.api:
        uvicorn.run("src.markitdown.api:app", host="0.0.0.0", port=8000)
    elif args.filename is None:
        markitdown = MarkItDown()
        result = markitdown.convert_stream(sys.stdin.buffer)
        _handle_output(args, result)
    else:
        markitdown = MarkItDown()
        result = markitdown.convert(args.filename)
        _handle_output(args, result)


def _handle_output(args, result: DocumentConverterResult):
    """Handle output to stdout or file"""
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result.text_content)
    else:
        print(result.text_content)


if __name__ == "__main__":
    main()
