# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

import argparse
import os
from typing import Any

from .__about__ import __version__

_USAGE = """SYNTAX:

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

        markitdown example.pdf > example.md"""

_ARGUMENTS: list[tuple[tuple[str, ...], dict[str, Any], bool]] = [
    (
        ("-v", "--version"),
        {
            "action": "version",
            "version": f"%(prog)s {__version__}",
            "help": "show the version number and exit",
        },
        False,
    ),
    (
        ("-o", "--output"),
        {"help": "Output file name. If not provided, output is written to stdout."},
        False,
    ),
    (
        ("-x", "--extension"),
        {
            "help": "Provide a hint about the file extension (e.g., when reading from stdin)."
        },
        False,
    ),
    (
        ("-m", "--mime-type"),
        {"help": "Provide a hint about the file's MIME type."},
        False,
    ),
    (
        ("-c", "--charset"),
        {"help": "Provide a hint about the file's charset (e.g., UTF-8)."},
        False,
    ),
    (
        ("-d", "--use-docintel"),
        {
            "action": "store_true",
            "help": "Use Document Intelligence to extract text instead of offline conversion. Requires a valid Document Intelligence Endpoint.",
        },
        True,
    ),
    (
        ("--use-cu", "--use-content-understanding"),
        {
            "action": "store_true",
            "dest": "use_cu",
            "help": "Use Azure Content Understanding to extract text. Requires --cu-endpoint.",
        },
        True,
    ),
    (
        ("-e", "--endpoint"),
        {
            "type": str,
            "help": "Document Intelligence Endpoint. Required if using Document Intelligence. Defaults to the MARKITDOWN_DOCINTEL_ENDPOINT environment variable.",
        },
        False,
    ),
    (
        ("--cu-endpoint",),
        {
            "type": str,
            "help": "Content Understanding Endpoint. Required if using --use-cu. Defaults to the MARKITDOWN_CU_ENDPOINT environment variable.",
        },
        False,
    ),
    (
        ("--cu-analyzer",),
        {
            "type": str,
            "help": "Content Understanding analyzer ID. If not specified, auto-selects by file type.",
        },
        False,
    ),
    (
        ("--cu-file-types",),
        {
            "type": str,
            "help": "Comma-separated list of file types to route to Content Understanding (e.g., pdf,jpeg,mp4). If omitted, all supported types are routed.",
        },
        False,
    ),
    (
        ("--docintel-model-id",),
        {
            "type": str,
            "default": None,
            "help": "Document Intelligence model ID (e.g., 'prebuilt-layout', 'prebuilt-invoice', or a custom model ID). Defaults to 'prebuilt-layout'.",
        },
        False,
    ),
    (
        ("--docintel-query-fields",),
        {
            "type": str,
            "default": None,
            "help": "Comma-separated list of field names to extract via the billable Document Intelligence queryFields add-on (OCR file types only).",
        },
        False,
    ),
    (
        ("--docintel-features",),
        {
            "type": str,
            "default": None,
            "help": "Comma-separated Document Intelligence analysis add-ons for OCR file types. Available values: barcodes, formulas, keyValuePairs, languages, ocrHighResolution, and styleFont. The formulas, ocrHighResolution, and styleFont incur additional charges. No add-ons are enabled by default; use 'none' to explicitly request none.",
        },
        False,
    ),
    (
        ("-p", "--use-plugins"),
        {
            "action": "store_true",
            "help": "Use 3rd-party plugins to convert files. Use --list-plugins to see installed plugins.",
        },
        False,
    ),
    (
        ("--list-plugins",),
        {
            "action": "store_true",
            "help": "List installed 3rd-party plugins. Plugins are loaded when using the -p or --use-plugins option.",
        },
        False,
    ),
    (
        ("--keep-data-uris",),
        {
            "action": "store_true",
            "help": "Keep data URIs (like base64-encoded images) in the output. By default, data URIs are truncated.",
        },
        False,
    ),
    (("filename",), {"nargs": "?"}, False),
]


def parse_args() -> argparse.Namespace:
    """Build the existing CLI argument contract and read its runtime defaults."""
    parser = argparse.ArgumentParser(
        description="Convert various file formats to markdown.",
        prog="markitdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=_USAGE,
    )
    cloud_group = parser.add_mutually_exclusive_group()
    for names, options, exclusive in _ARGUMENTS:
        target = cloud_group if exclusive else parser
        target.add_argument(*names, **options)
    parser.set_defaults(
        endpoint=os.environ.get("MARKITDOWN_DOCINTEL_ENDPOINT") or None,
        cu_endpoint=os.environ.get("MARKITDOWN_CU_ENDPOINT") or None,
    )
    return parser.parse_args()
