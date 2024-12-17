# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import sys
from textwrap import dedent
from importlib.metadata import entry_points
from .__about__ import __version__
from ._markitdown import MarkItDown, DocumentConverterResult

parser = argparse.ArgumentParser(
    description="Convert various file formats to markdown.",
    prog="markitdown",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=dedent(
        """\
        examples:
          markitdown example.pdf
          markitdown -o example.md example.pdf
          cat example.pdf | markitdown > example.md"""
    ),
)
parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {__version__}",
    help="show the version number and exit",
)
parser.add_argument(
    "-o",
    "--output",
    metavar="OUTFILENAME",
    help="if unspecified, defaults to stdout",
)
parser.add_argument(
    "-d",
    "--use-docintel",
    action="store_true",
    help="use online Document Intelligence to extract text (requires a valid `--endpoint`)",
)
parser.add_argument(
    "-e",
    "--endpoint",
    type=str,
    help="required for `--use-docintel`",
)
parser.add_argument(
    "-p",
    "--use-plugins",
    action="store_true",
    help="use 3rd-party plugins to convert files (see `--list-plugins`)",
)
parser.add_argument(
    "--list-plugins",
    action="store_true",
    help="list installed 3rd-party plugins (loaded with `--use-plugin`)",
)
parser.add_argument("--llm-client", choices={"OpenAI"}, help="default None")
parser.add_argument("--llm-client-url", help="base URL for --llm-client")
parser.add_argument("--llm-model", help="required for --llm-client")
parser.add_argument(
    "filename", metavar="FILENAME", nargs="?", help="if unspecified, defaults to stdin"
)


def main(args=None):
    args = parser.parse_args(args)

    if args.list_plugins:
        # List installed plugins, then exit
        print("Installed MarkItDown 3rd-party Plugins:\n")
        plugin_entry_points = list(entry_points(group="markitdown.plugin"))
        if plugin_entry_points:
            for entry_point in plugin_entry_points:
                print(f"  * {entry_point.name:<16}\t(package: {entry_point.value})")
            print(
                "\nUse the -p (or --use-plugins) option to enable 3rd-party plugins.\n"
            )
        else:
            print("No 3rd-party plugins installed.")
            print(
                "\nFind plugins by searching for the hashtag #markitdown-plugin on GitHub.\n"
            )
        sys.exit(0)

    if args.use_docintel:
        if args.endpoint is None:
            raise ValueError(
                "Document Intelligence Endpoint is required when using Document Intelligence."
            )
        elif args.filename is None:
            raise ValueError("Filename is required when using Document Intelligence.")

    if args.llm_client == "OpenAI":
        from openai import OpenAI
        llm_client = OpenAI(base_url=args.llm_client_url)
    else:
        llm_client = None

    markitdown = MarkItDown(
        enable_plugins=args.use_plugins,
        docintel_endpoint=args.endpoint if args.use_docintel else None,
        llm_client=llm_client,
        llm_model=args.llm_model,
    )

    if args.filename:
        result = markitdown.convert(args.filename)
    else:
        result = markitdown.convert_stream(sys.stdin.buffer)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            print(result.text_content, file=f)
    else:
        print(result.text_content)


if __name__ == "__main__":
    main()
