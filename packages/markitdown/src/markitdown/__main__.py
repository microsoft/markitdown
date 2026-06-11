# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import sys
import os
import codecs
import zipfile
from typing import Any, Dict
from textwrap import dedent
from importlib.metadata import entry_points
from .__about__ import __version__
from ._markitdown import MarkItDown, StreamInfo, DocumentConverterResult


def count_docx_images(filename: str) -> int:
    """快速预检：统计 DOCX 中嵌入的图片数量"""
    try:
        with zipfile.ZipFile(filename) as z:
            return len([f for f in z.namelist() if f.startswith("word/media/")])
    except (zipfile.BadZipFile, FileNotFoundError):
        return 0


def ask_extract_images(image_count: int) -> bool:
    """交互式询问是否提取图片"""
    if not sys.stdin.isatty():
        return False  # 非交互终端，不询问
    print(f"\n📄 检测到文档中包含 {image_count} 张图片")
    try:
        answer = input("   是否提取图片到本地文件？(y/n): ").strip().lower()
        return answer in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


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

    cloud_group = parser.add_mutually_exclusive_group()
    cloud_group.add_argument(
        "-d",
        "--use-docintel",
        action="store_true",
        help="Use Document Intelligence to extract text instead of offline conversion. Requires a valid Document Intelligence Endpoint.",
    )

    cloud_group.add_argument(
        "--use-cu",
        "--use-content-understanding",
        action="store_true",
        dest="use_cu",
        help="Use Azure Content Understanding to extract text. Requires --cu-endpoint.",
    )

    parser.add_argument(
        "-e",
        "--endpoint",
        type=str,
        help="Document Intelligence Endpoint. Required if using Document Intelligence.",
    )

    parser.add_argument(
        "--cu-endpoint",
        type=str,
        help="Content Understanding Endpoint. Required if using --use-cu.",
    )

    parser.add_argument(
        "--cu-analyzer",
        type=str,
        help="Content Understanding analyzer ID. If not specified, auto-selects by file type.",
    )

    parser.add_argument(
        "--cu-file-types",
        type=str,
        help="Comma-separated list of file types to route to Content Understanding (e.g., pdf,jpeg,mp4). If omitted, all supported types are routed.",
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
        "--extract-images",
        action="store_true",
        help="Extract embedded images from DOCX to a local directory.",
    )

    parser.add_argument(
        "--no-extract-images",
        action="store_true",
        help="Do not extract images (skip interactive prompt).",
    )

    parser.add_argument(
        "--images-dir",
        default="images",
        help="Directory name for extracted images (default: images).",
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
    elif args.use_cu:
        if args.cu_endpoint is None:
            _exit_with_error(
                "Content Understanding Endpoint (--cu-endpoint) is required when using --use-cu."
            )
        elif args.filename is None:
            _exit_with_error("Filename is required when using Content Understanding.")

        cu_kwargs: Dict[str, Any] = {
            "cu_endpoint": args.cu_endpoint,
        }
        if args.cu_analyzer is not None:
            cu_kwargs["cu_analyzer_id"] = args.cu_analyzer
        if args.cu_file_types is not None:
            # Parse comma-separated file types into ContentUnderstandingFileType list
            from .converters import ContentUnderstandingFileType

            type_names = [
                t.strip().lower() for t in args.cu_file_types.split(",") if t.strip()
            ]
            cu_types = []
            for name in type_names:
                # Try matching by value (e.g., "pdf", "jpeg", "mp4")
                try:
                    cu_types.append(ContentUnderstandingFileType(name))
                except ValueError:
                    _exit_with_error(f"Unknown file type: {name}")
            cu_kwargs["cu_file_types"] = cu_types

        markitdown = MarkItDown(enable_plugins=args.use_plugins, **cu_kwargs)
    else:
        markitdown = MarkItDown(enable_plugins=args.use_plugins)

    # --- 图片提取逻辑 ---
    extract_images = False
    if args.extract_images:
        extract_images = True
    elif args.no_extract_images:
        extract_images = False
    elif args.filename and args.output and args.filename.lower().endswith(".docx"):
        count = count_docx_images(args.filename)
        if count > 0:
            extract_images = ask_extract_images(count)

    # 构建 kwargs
    convert_kwargs: Dict[str, Any] = {
        "keep_data_uris": args.keep_data_uris,
    }

    if extract_images and args.output:
        images_dir_name = args.images_dir or "images"
        abs_images_dir = os.path.join(
            os.path.dirname(os.path.abspath(args.output)),
            images_dir_name,
        )
        os.makedirs(abs_images_dir, exist_ok=True)
        convert_kwargs["extract_images"] = True
        convert_kwargs["images_dir"] = abs_images_dir
        convert_kwargs["images_rel_dir"] = images_dir_name
        # extract_images 优先于 keep_data_uris
        convert_kwargs["keep_data_uris"] = False

    # --- 转换 ---
    if args.filename is None:
        result = markitdown.convert_stream(
            sys.stdin.buffer,
            stream_info=stream_info,
            **convert_kwargs,
        )
    else:
        result = markitdown.convert(
            args.filename,
            stream_info=stream_info,
            **convert_kwargs,
        )

    _handle_output(args, result, extract_images=extract_images)


def _handle_output(args, result: DocumentConverterResult, extract_images: bool = False):
    """Handle output to stdout or file"""
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        if extract_images:
            images_dir = args.images_dir or "images"
            print(f"[OK] Generated {args.output}")
            print(f"[OK] Images extracted to ./{images_dir}/")
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
