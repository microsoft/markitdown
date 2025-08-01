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
from ._exceptions import UnsupportedFormatException, FileConversionException


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
        "-b",
        "--batch",
        action="store_true",
        help="Process all supported files in a directory. If specified, filename should be a directory path.",
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Process subdirectories recursively when using batch mode.",
    )

    parser.add_argument(
        "--types",
        help="Comma-separated list of file extensions to process in batch mode (e.g., pdf,docx,pptx). If not specified, all supported types are processed.",
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

    if args.batch:
        if args.filename is None:
            _exit_with_error("Directory path is required when using batch mode.")
        
        _handle_batch_processing(args, markitdown, stream_info)
    elif args.filename is None:
        result = markitdown.convert_stream(
            sys.stdin.buffer,
            stream_info=stream_info,
            keep_data_uris=args.keep_data_uris,
        )
        _handle_output(args, result)
    else:
        result = markitdown.convert(
            args.filename, stream_info=stream_info, keep_data_uris=args.keep_data_uris
        )
        _handle_output(args, result)


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


def _handle_batch_processing(args, markitdown: MarkItDown, stream_info):
    """Handle batch processing of files in a directory"""
    from pathlib import Path
    from ._exceptions import UnsupportedFormatException, FileConversionException
    
    input_dir = Path(args.filename)
    if not input_dir.exists():
        _exit_with_error(f"Directory does not exist: {input_dir}")
    if not input_dir.is_dir():
        _exit_with_error(f"Path is not a directory: {input_dir}")
    
    # Determine output directory
    output_dir = Path(args.output) if args.output else input_dir / "converted"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all files to process
    pattern = "**/*" if args.recursive else "*"
    all_files = []
    
    for file_path in input_dir.glob(pattern):
        if file_path.is_file():
            all_files.append(file_path)
    
    if not all_files:
        print(f"No files found in {input_dir}")
        return
    
    print(f"Found {len(all_files)} files to process")
    
    # Process files
    processed = 0
    failed = 0
    unsupported = 0
    
    for i, file_path in enumerate(all_files, 1):
        try:
            # Calculate relative path and output path
            rel_path = file_path.relative_to(input_dir)
            output_file = output_dir / Path(str(rel_path) + '.md')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"[{i}/{len(all_files)}] Processing: {rel_path}")
            
            # Convert file
            result = markitdown.convert(
                str(file_path), 
                stream_info=stream_info, 
                keep_data_uris=args.keep_data_uris
            )
            
            # Write output
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.markdown)
            
            print(f"✓ Success: {rel_path}")
            processed += 1
            
        except UnsupportedFormatException:
            print(f"⚠ Skipped (unsupported): {rel_path}")
            unsupported += 1
        except FileConversionException as e:
            print(f"✗ Failed (conversion error): {rel_path} - {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Failed (unexpected error): {rel_path} - {e}")
            failed += 1
    
    print(f"\nBatch processing complete!")
    print(f"Success: {processed} files")
    print(f"Failed: {failed} files")
    print(f"Unsupported: {unsupported} files")
    print(f"Output directory: {output_dir}")


if __name__ == "__main__":
    main()
