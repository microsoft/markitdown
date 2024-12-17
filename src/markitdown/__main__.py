# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import sys
import argparse
from textwrap import dedent
import shtab
from ._markitdown import MarkItDown


def main():
    parser = argparse.ArgumentParser(
        description="Convert various file formats to markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """\
            examples:
              markitdown example.pdf
              cat example.pdf | markitdown
              markitdown < example.pdf"""
        ),
    )

    parser.add_argument(
        "filename", nargs="?", help="if unspecified, defaults to stdin"
    ).complete = shtab.FILE
    parser.add_argument("--llm-client", choices={"OpenAI"}, help="default None")
    parser.add_argument("--llm-client-url", help="base URL for --llm-client")
    parser.add_argument("--llm-model", help="required for --llm-client")
    shtab.add_argument_to(parser)
    args = parser.parse_args()
    if args.llm_client == "OpenAI":
        from openai import OpenAI
        llm_client = OpenAI(base_url=args.llm_client_url)
    else:
        llm_client = None
    markitdown = MarkItDown(llm_client=llm_client, llm_model=args.llm_model)
    result = markitdown.convert(args.filename or sys.stdin.buffer)
    print(result.text_content)


if __name__ == "__main__":
    main()
