# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import io
import sys
from importlib.metadata import entry_points
from typing import NoReturn

from ._cli_args import parse_args
from ._cli_options import converter_options, stream_info_from_args
from ._markitdown import DocumentConverterResult, MarkItDown


def main() -> None:
    args = parse_args()
    try:
        stream_info = stream_info_from_args(args)
    except ValueError as exc:
        _exit_with_error(str(exc))

    if args.list_plugins:
        _list_plugins()
        sys.exit(0)

    try:
        options = converter_options(args)
    except ValueError as exc:
        _exit_with_error(str(exc))
    markitdown = MarkItDown(**options)
    if args.filename is None:
        result = markitdown.convert_stream(
            io.BytesIO(sys.stdin.buffer.read()),
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )
    else:
        result = markitdown.convert(
            args.filename, stream_info=stream_info, keep_data_uris=args.keep_data_uris
        )
    _handle_output(args, result)


def _list_plugins() -> None:
    print("Installed MarkItDown 3rd-party Plugins:\n")
    plugin_entry_points = list(entry_points(group="markitdown.plugin"))
    if not plugin_entry_points:
        print("  * No 3rd-party plugins installed.")
        print(
            "\nFind plugins by searching for the hashtag #markitdown-plugin on GitHub.\n"
        )
    else:
        for entry_point in plugin_entry_points:
            print(f"  * {entry_point.name:<16}\t(package: {entry_point.value})")
        print("\nUse the -p (or --use-plugins) option to enable 3rd-party plugins.\n")


def _handle_output(args: argparse.Namespace, result: DocumentConverterResult) -> None:
    """Handle output to stdout or file."""
    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(result.markdown)
    elif (
        buffer := getattr(sys.stdout, "buffer", None)
    ) is not None and not sys.stdout.isatty():
        buffer.write((result.markdown + "\n").encode("utf-8"))
    else:
        encoding = sys.stdout.encoding or "utf-8"
        print(result.markdown.encode(encoding, errors="replace").decode(encoding))


def _exit_with_error(message: str) -> NoReturn:
    print(message)
    sys.exit(1)


if __name__ == "__main__":
    main()
