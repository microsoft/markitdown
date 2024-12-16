# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import sys
from markitdown._markitdown import MarkItDown


def main():
    if len(sys.argv) == 1:
        markitdown = MarkItDown()
        result = markitdown.convert_stream(sys.stdin.buffer)
        print(result.text_content)
    elif len(sys.argv) == 2:
        markitdown = MarkItDown()
        result = markitdown.convert(sys.argv[1])
        print(result.text_content)
    else:
        sys.stderr.write(
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
""".strip()
            + "\n"
        )


if __name__ == "__main__":
    main()

