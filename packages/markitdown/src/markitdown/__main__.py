# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

import argparse
import sys
import os
import codecs
import logging
from textwrap import dedent
from importlib.metadata import entry_points
from .__about__ import __version__
from ._markitdown import MarkItDown, StreamInfo, DocumentConverterResult

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDFs and other supported formats to clean Markdown output. Supports local or Azure Document Intelligence extraction.",
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
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file name. If not provided, output is written to stdout."
    )

    parser.add_argument(
        "-x", "--extension",
        help="Provide a hint about the file extension (e.g., when reading from stdin)."
    )

    parser.add_argument(
        "-m", "--mime-type",
        help="Provide a hint about the file's MIME type."
    )

    parser.add_argument(
        "-c", "--charset",
        help="Provide a hint about the file's charset (e.g, UTF-8)."
    )

    parser.add_argument(
        "-d", "--use-docintel",
        action="store_true",
        help="Use Document Intelligence to extract text instead of offline conversion. Requires a valid Document Intelligence Endpoint."
    )

    parser.add_argument(
        "-e", "--endpoint",
        type=str,
        help="Document Intelligence Endpoint. Required if using Document Intelligence."
    )

    parser.add_argument(
        "-p", "--use-plugins",
        action="store_true",
        help="Use 3rd-party plugins to convert files. Use --list-plugins to see installed plugins."
    )

    parser.add_argument(
        "--list-plugins",
        action="store_true",
        help="List installed 3rd-party plugins. Plugins are loaded when using the -p or --use-plugin option."
    )

    parser.add_argument(
        "--keep-data-uris",
        action="store_true",
        help="Keep data URIs (like base64-encoded images) in the output. By default, data URIs are truncated."
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress non-error messages."
    )

    parser.add_argument("filename", nargs="?")
    args = parser.parse_args()

    # Parse the extension hint
    extension_hint = _normalize_extension(args.extension)

    # Parse the MIME type
    mime_type_hint = _validate_mime(args.mime_type)

    # Parse the charset
    charset_hint = _validate_charset(args.charset)

    stream_info = None
    if extension_hint or mime_type_hint or charset_hint:
        stream_info = StreamInfo(
            extension=extension_hint,
            mimetype=mime_type_hint,
            charset=charset_hint
        )

    if args.list_plugins:
        _list_plugins(args.quiet)
        sys.exit(0)

    if args.use_docintel:
        if args.endpoint is None:
            _exit_with_error("Document Intelligence Endpoint is required when using Document Intelligence.")
        elif args.filename is None:
            _exit_with_error("Filename is required when using Document Intelligence.")
        elif not os.path.isfile(args.filename):
            _exit_with_error(f"Input file not found: {args.filename}")
        markitdown = MarkItDown(enable_plugins=args.use_plugins, docintel_endpoint=args.endpoint)
    else:
        markitdown = MarkItDown(enable_plugins=args.use_plugins)

    # Check if file exists before processing
    if args.filename and not os.path.isfile(args.filename):
        _exit_with_error(f"Input file not found: {args.filename}")

    try:
        if args.filename is None:
            result = markitdown.convert_stream(
                sys.stdin.buffer,
                stream_info=stream_info,
                keep_data_uris=args.keep_data_uris
            )
        else:
            result = markitdown.convert(
                args.filename,
                stream_info=stream_info,
                keep_data_uris=args.keep_data_uris
            )

        _handle_output(args, result)
        sys.exit(0 if result and result.markdown else 2)
    except Exception as e:
        logging.error(f"Conversion failed: {e}")
        sys.exit(1)


def _handle_output(args, result: DocumentConverterResult):
    """Handle output to stdout or file"""
    try:
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result.markdown)
        else:
            print(
                result.markdown.encode(sys.stdout.encoding, errors="replace").decode(sys.stdout.encoding)
            )
    except IOError as e:
        _exit_with_error(f"Error writing to output: {e}")


def _normalize_extension(ext):
    if ext:
        ext = ext.strip().lower()
        if len(ext) > 0:
            return "." + ext if not ext.startswith(".") else ext
    return None


def _validate_mime(mime):
    if mime:
        mime = mime.strip()
        if mime.count("/") != 1:
            _exit_with_error(f"Invalid MIME type: {mime}")
        return mime
    return None


def _validate_charset(charset):
    if charset:
        charset = charset.strip()
        try:
            return codecs.lookup(charset).name
        except LookupError:
            _exit_with_error(f"Invalid charset: {charset}")
    return None


def _list_plugins(quiet=False):
    if not quiet:
        print("Installed MarkItDown 3rd-party Plugins:\n")
    plugin_entry_points = list(entry_points(group="markitdown.plugin"))
    if len(plugin_entry_points) == 0:
        print("  * No 3rd-party plugins installed.")
        print("\nFind plugins by searching for the hashtag #markitdown-plugin on GitHub.\n")
    else:
        for entry_point in plugin_entry_points:
            print(f"  * {entry_point.name:<16}\t(package: {entry_point.value})")
        print("\nUse the -p (or --use-plugins) option to enable 3rd-party plugins.\n")


def _exit_with_error(message: str):
    logging.error(message)
    sys.exit(1)


if __name__ == "__main__":
    main()
