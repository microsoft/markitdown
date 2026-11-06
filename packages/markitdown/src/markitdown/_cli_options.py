# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

import argparse
import codecs
from typing import Any, Optional

from ._stream_info import StreamInfo


def stream_info_from_args(args: argparse.Namespace) -> Optional[StreamInfo]:
    """Validate the input hints and preserve an absent hint as None."""
    extension = _extension_hint(args.extension)
    mimetype = _mime_type_hint(args.mime_type)
    charset = _charset_hint(args.charset)
    if extension is None and mimetype is None and charset is None:
        return None
    return StreamInfo(extension=extension, mimetype=mimetype, charset=charset)


def _extension_hint(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    extension = value.strip().lower()
    if extension and not extension.startswith("."):
        extension = "." + extension
    return extension or None


def _mime_type_hint(value: Optional[str]) -> Optional[str]:
    mimetype = value.strip() if value is not None else ""
    if not mimetype:
        return None
    if mimetype.count("/") != 1:
        raise ValueError(f"Invalid MIME type: {mimetype}")
    return mimetype


def _charset_hint(value: Optional[str]) -> Optional[str]:
    charset = value.strip() if value is not None else ""
    if not charset:
        return None
    try:
        return codecs.lookup(charset).name
    except LookupError as exc:
        raise ValueError(f"Invalid charset: {charset}") from exc


def converter_options(args: argparse.Namespace) -> dict[str, Any]:
    """Build only the options selected by the existing CLI arguments."""
    options = {"enable_plugins": args.use_plugins}
    if args.use_docintel:
        options.update(_docintel_options(args))
    elif args.use_cu:
        options.update(_content_understanding_options(args))
    return options


def _comma_separated(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def _docintel_options(args: argparse.Namespace) -> dict[str, Any]:
    if args.endpoint is None:
        raise ValueError(
            "Document Intelligence Endpoint is required when using Document Intelligence. "
            "Pass -e/--endpoint or set MARKITDOWN_DOCINTEL_ENDPOINT."
        )
    if args.filename is None:
        raise ValueError("Filename is required when using Document Intelligence.")
    options: dict[str, Any] = {"docintel_endpoint": args.endpoint}
    if args.docintel_model_id:
        options["docintel_model_id"] = args.docintel_model_id
    if args.docintel_features is not None:
        options["docintel_features"] = (
            []
            if args.docintel_features.strip().lower() == "none"
            else _comma_separated(args.docintel_features)
        )
    if args.docintel_query_fields:
        fields = _comma_separated(args.docintel_query_fields)
        if fields:
            options["docintel_query_fields"] = fields
    return options


def _content_understanding_options(args: argparse.Namespace) -> dict[str, Any]:
    if args.cu_endpoint is None:
        raise ValueError(
            "Content Understanding Endpoint (--cu-endpoint) is required when using --use-cu. "
            "Pass --cu-endpoint or set MARKITDOWN_CU_ENDPOINT."
        )
    options: dict[str, Any] = {"cu_endpoint": args.cu_endpoint}
    if args.cu_analyzer is not None:
        options["cu_analyzer_id"] = args.cu_analyzer
    if args.cu_file_types is not None:
        options["cu_file_types"] = _content_understanding_types(args.cu_file_types)
    return options


def _content_understanding_types(value: str) -> list[Any]:
    from .converters import ContentUnderstandingFileType

    types = []
    for raw_name in _comma_separated(value):
        name = raw_name.lower()
        try:
            types.append(ContentUnderstandingFileType(name))
        except ValueError as exc:
            raise ValueError(f"Unknown file type: {name}") from exc
    return types
