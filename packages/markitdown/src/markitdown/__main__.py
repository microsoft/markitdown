# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import os
import sys
import codecs
from textwrap import dedent
from importlib.metadata import entry_points
from .__about__ import __version__
from ._markitdown import MarkItDown, StreamInfo, DocumentConverterResult


def main():
    parser = argparse.ArgumentParser(
        description="Convert various file formats to markdown.",
        prog="markitdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=dedent(
            """
            SYNTAX:

                markitdown <OPTIONAL: FILENAME [FILENAME ...]>
                If FILENAME is empty, markitdown reads from stdin.

            EXAMPLES:

                markitdown example.pdf

                markitdown file1.pdf file2.docx file3.html

                cat example.pdf | markitdown

                markitdown example.pdf -o example.md

                markitdown file1.pdf file2.docx --output-dir ./output/
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

    parser.add_argument(
        "-o",
        "--output",
        help="Output file name. Only valid for single-file conversion.",
    )

    parser.add_argument(
        "--output-dir",
        help="Output directory for batch conversion. Each file is written to <dir>/<filename>.md.",
    )

    parser.add_argument(
        "-x",
        "--extension",
        help="Provide a hint about the file extension (e.g., when reading from stdin).",
    )

    parser.add_argument(
        "-m",
        "--mime-type",
        help="Provide a hint about the file's MIME type.",
    )

    parser.add_argument(
        "-c",
        "--charset",
        help="Provide a hint about the file's charset (e.g, UTF-8).",
    )

    parser.add_argument(
        "-d",
        "--use-docintel",
        action="store_true",
        help="Use Document Intelligence to extract text instead of offline conversion. Requires a valid Document Intelligence Endpoint.",
    )

    parser.add_argument(
        "-e",
        "--endpoint",
        type=str,
        help="Document Intelligence Endpoint. Required if using Document Intelligence.",
    )

    parser.add_argument(
        "-p",
        "--use-plugins",
        action="store_true",
        help="Use 3rd-party plugins to convert files. Use --list-plugins to see installed plugins.",
    )

    parser.add_argument(
        "--list-plugins",
        action="store_true",
        help="List installed 3rd-party plugins. Plugins are loaded when using the -p or --use-plugin option.",
    )

    parser.add_argument(
        "--keep-data-uris",
        action="store_true",
        help="Keep data URIs (like base64-encoded images) in the output. By default, data URIs are truncated.",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Number of parallel threads for batch conversion.",
    )

    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Abort batch conversion on the first error (default: collect errors and continue).",
    )

    parser.add_argument("filename", nargs="*")
    args = parser.parse_args()

    # Parse the extension hint
    extension_hint = args.extension
    if extension_hint is not None:
        extension_hint = extension_hint.strip().lower()
        if len(extension_hint) > 0:
            if not extension_hint.startswith("."):
                extension_hint = "." + extension_hint
        else:
            extension_hint = None

    # Parse the mime type
    mime_type_hint = args.mime_type
    if mime_type_hint is not None:
        mime_type_hint = mime_type_hint.strip()
        if len(mime_type_hint) > 0:
            if mime_type_hint.count("/") != 1:
                _exit_with_error(f"Invalid MIME type: {mime_type_hint}")
        else:
            mime_type_hint = None

    # Parse the charset
    charset_hint = args.charset
    if charset_hint is not None:
        charset_hint = charset_hint.strip()
        if len(charset_hint) > 0:
            try:
                charset_hint = codecs.lookup(charset_hint).name
            except LookupError:
                _exit_with_error(f"Invalid charset: {charset_hint}")
        else:
            charset_hint = None

    stream_info = None
    if (
        extension_hint is not None
        or mime_type_hint is not None
        or charset_hint is not None
    ):
        stream_info = StreamInfo(
            extension=extension_hint, mimetype=mime_type_hint, charset=charset_hint
        )

    if args.list_plugins:
        print("Installed MarkItDown 3rd-party Plugins:\n")
        plugin_entry_points = list(entry_points(group="markitdown.plugin"))
        if len(plugin_entry_points) == 0:
            print("  * No 3rd-party plugins installed.")
            print(
                "\nFind plugins by searching for the hashtag #markitdown-plugin on GitHub.\n"
            )
        else:
            for entry_point in plugin_entry_points:
                print(f"  * {entry_point.name:<16}\t(package: {entry_point.value})")
            print(
                "\nUse the -p (or --use-plugins) option to enable 3rd-party plugins.\n"
            )
        sys.exit(0)

    if args.use_docintel:
        if args.endpoint is None:
            _exit_with_error(
                "Document Intelligence Endpoint is required when using Document Intelligence."
            )
        elif not args.filename:
            _exit_with_error("Filename is required when using Document Intelligence.")

        markitdown = MarkItDown(
            enable_plugins=args.use_plugins, docintel_endpoint=args.endpoint
        )
    else:
        markitdown = MarkItDown(enable_plugins=args.use_plugins)

    # Stdin mode
    if not args.filename:
        result = markitdown.convert_stream(
            sys.stdin.buffer,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )
        _handle_output(args, result)
        return

    # Single-file mode (preserves original behaviour exactly)
    if len(args.filename) == 1 and args.output_dir is None:
        result = markitdown.convert(
            args.filename[0],
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )
        _handle_output(args, result)
        return

    # Batch mode
    on_error = "raise" if args.fail_fast else "collect"
    exit_code = 0
    try:
        for batch_result in markitdown.convert_batch(
            args.filename,
            on_error=on_error,
            workers=args.workers,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        ):
            if not batch_result.success:
                print(
                    f"Error converting {batch_result.source}: {batch_result.error}",
                    file=sys.stderr,
                )
                exit_code = 1
            elif args.output_dir:
                os.makedirs(args.output_dir, exist_ok=True)
                source_name = os.path.basename(str(batch_result.source))
                out_path = os.path.join(args.output_dir, source_name + ".md")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(batch_result.result.markdown)
                print(f"Converted: {batch_result.source} -> {out_path}", file=sys.stderr)
            else:
                print(f"\n--- {batch_result.source} ---\n")
                print(
                    batch_result.result.markdown.encode(
                        sys.stdout.encoding, errors="replace"
                    ).decode(sys.stdout.encoding)
                )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit_code = 1

    sys.exit(exit_code)


def _handle_output(args, result: DocumentConverterResult):
    """Handle output to stdout or file"""
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result.markdown)
    else:
        # Handle stdout encoding errors more gracefully
        print(
            result.markdown.encode(sys.stdout.encoding, errors="replace").decode(
                sys.stdout.encoding
            )
        )


def _exit_with_error(message: str):
    print(message)
    sys.exit(1)


if __name__ == "__main__":
    main()
