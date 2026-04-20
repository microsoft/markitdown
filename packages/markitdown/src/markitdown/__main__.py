# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import os
import sys
import codecs
from pathlib import Path
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

            BATCH CONVERSION:

                markitdown path/to/docs/ --output-dir ./converted/

                OR with extension filter and non-recursive

                markitdown path/to/docs/ --output-dir ./converted/ --extensions pdf,docx --no-recursive
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
        help="Output file name. If not provided, output is written to stdout.",
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
        "--output-dir",
        help="Output directory for batch conversion. When the input is a directory, "
        "converted files are written here preserving the directory structure.",
    )

    parser.add_argument(
        "--extensions",
        help="Comma-separated list of file extensions to include in batch conversion "
        "(e.g., pdf,docx,pptx). If not provided, all files are attempted.",
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Do not process subdirectories when converting a directory.",
    )

    parser.add_argument("filename", nargs="?")
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
        # List installed plugins, then exit
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
        elif args.filename is None:
            _exit_with_error("Filename is required when using Document Intelligence.")

        markitdown = MarkItDown(
            enable_plugins=args.use_plugins, docintel_endpoint=args.endpoint
        )
    else:
        markitdown = MarkItDown(enable_plugins=args.use_plugins)

    if args.filename is None:
        result = markitdown.convert_stream(
            sys.stdin.buffer,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )
    elif os.path.isdir(args.filename):
        # Batch directory mode
        _handle_batch(args, markitdown)
        return
    else:
        result = markitdown.convert(
            args.filename, stream_info=stream_info, keep_data_uris=args.keep_data_uris
        )

    _handle_output(args, result)


def _handle_batch(args, markitdown: MarkItDown):
    """Handle batch directory conversion."""
    source_dir = args.filename

    if args.output_dir is None:
        _exit_with_error(
            "An --output-dir is required when converting a directory."
        )

    output_dir = Path(args.output_dir)
    source_path = Path(source_dir).resolve()

    # Parse extensions filter
    extensions = None
    if args.extensions:
        extensions = [
            ext.strip() for ext in args.extensions.split(",") if ext.strip()
        ]

    recursive = not args.no_recursive

    def progress(file_path: str, current: int, total: int):
        print(
            f"[{current + 1}/{total}] Converting: {file_path}",
            file=sys.stderr,
        )

    batch_result = markitdown.convert_batch(
        source_dir,
        extensions=extensions,
        recursive=recursive,
        on_error="continue",
        progress_callback=progress,
        keep_data_uris=args.keep_data_uris,
    )

    # Write output files
    for item in batch_result:
        if not item.success:
            print(
                f"  ERROR: {item.source_path}: {item.error}",
                file=sys.stderr,
            )
            continue

        # Compute relative path from source dir to preserve structure
        rel_path = Path(item.source_path).resolve().relative_to(source_path)
        out_path = output_dir / (str(rel_path) + ".md")

        # Ensure the output subdirectory exists
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(item.result.markdown)

    # Print summary
    total = len(batch_result)
    succeeded = len(batch_result.succeeded)
    failed = len(batch_result.failed)
    print(
        f"\nBatch complete: {succeeded}/{total} succeeded, {failed} failed.",
        file=sys.stderr,
    )

    if failed > 0:
        sys.exit(1)


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
