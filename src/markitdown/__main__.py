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
        usage="""
SYNTAX: 
    
    markitdown <OPTIONAL: FILENAME>
    If FILENAME is empty, markitdown reads from stdin.

EXAMPLE:
    
    markitdown example.pdf
    
    OR

    cat example.pdf | markitdown

    OR 

    markitdown < example.pdf
""".strip(),
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
