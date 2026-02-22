# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import sys
import codecs
from textwrap import dedent
from importlib.metadata import entry_points
from .__about__ import __version__
from ._markitdown import MarkItDown, StreamInfo, DocumentConverterResult
from ._base_converter import PageInfo
import json


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

                OR to extract pages separately from PDF

                markitdown example.pdf --extract-pages

                OR to get page information as JSON

                markitdown example.pdf --extract-pages --pages-json
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
        "--extract-pages",
        action="store_true",
        help="Extract pages separately for PDF files. Returns page-by-page information.",
    )

    parser.add_argument(
        "--pages-json",
        action="store_true",
        help="Output page information as JSON when using --extract-pages.",
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
            extract_pages=args.extract_pages,
        )
    else:
        result = markitdown.convert(
            args.filename,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
            extract_pages=args.extract_pages,
        )

    _handle_output(args, result)


def _handle_output(args, result: DocumentConverterResult):
    """Handle output to stdout or file"""
    output_content = ""

    if args.extract_pages and result.pages and args.pages_json:
        # Output as JSON with page information
        pages_data = [
            {"page_number": page.page_number, "content": page.content}
            for page in result.pages
        ]
        output_data = {
            "markdown": result.markdown,
            "title": result.title,
            "pages": pages_data,
        }
        output_content = json.dumps(output_data, ensure_ascii=False, indent=2)
    elif args.extract_pages and result.pages:
        # Output with page separators
        output_content = result.markdown
        output_content += "\n\n" + "=" * 50 + "\n"
        output_content += f"EXTRACTED {len(result.pages)} PAGES:\n"
        output_content += "=" * 50 + "\n\n"

        for page in result.pages:
            output_content += f"--- PAGE {page.page_number} ---\n"
            output_content += page.content
            output_content += "\n\n"
    else:
        # Standard output
        output_content = result.markdown

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_content)
    else:
        # Handle stdout encoding errors more gracefully
        print(
            output_content.encode(sys.stdout.encoding, errors="replace").decode(
                sys.stdout.encoding
            )
        )


def _exit_with_error(message: str):
    print(message)
    sys.exit(1)


if __name__ == "__main__":
    main()
