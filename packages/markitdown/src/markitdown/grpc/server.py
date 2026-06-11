from __future__ import annotations

import argparse
import io
import sys
from concurrent import futures
from typing import Iterable, Iterator, NoReturn

import grpc

from markitdown import (
    DocumentConverterResult,
    FileConversionException,
    MarkItDown,
    MarkItDownException,
    MissingDependencyException,
    StreamInfo,
    UnsupportedFormatException,
)
from markitdown.converters import ContentUnderstandingFileType
from markitdown.streaming import StreamingConverterController

from . import _segmenter
from .v1 import markitdown_pb2, markitdown_pb2_grpc

_DEFAULT_MARKDOWN_CHUNK_SIZE_BYTES = 4096

# Generous default so large documents (big PDFs, Office files with embedded
# media) can be sent inline via Source.content. Operators can lower this with
# --max-receive-message-bytes when exposing the server more broadly.
DEFAULT_MAX_MESSAGE_BYTES = 100 * 1024 * 1024

_CU_FILE_TYPE_MAP: dict[int, ContentUnderstandingFileType] = {
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_PDF: ContentUnderstandingFileType.PDF,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_DOCX: ContentUnderstandingFileType.DOCX,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_PPTX: ContentUnderstandingFileType.PPTX,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_XLSX: ContentUnderstandingFileType.XLSX,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_HTML: ContentUnderstandingFileType.HTML,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_TXT: ContentUnderstandingFileType.TXT,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_MD: ContentUnderstandingFileType.MD,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_RTF: ContentUnderstandingFileType.RTF,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_XML: ContentUnderstandingFileType.XML,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_EML: ContentUnderstandingFileType.EML,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_MSG: ContentUnderstandingFileType.MSG,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_JPEG: ContentUnderstandingFileType.JPEG,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_PNG: ContentUnderstandingFileType.PNG,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_BMP: ContentUnderstandingFileType.BMP,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_TIFF: ContentUnderstandingFileType.TIFF,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_HEIF: ContentUnderstandingFileType.HEIF,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_MP4: ContentUnderstandingFileType.MP4,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_M4V: ContentUnderstandingFileType.M4V,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_MOV: ContentUnderstandingFileType.MOV,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_AVI: ContentUnderstandingFileType.AVI,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_MKV: ContentUnderstandingFileType.MKV,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_WEBM: ContentUnderstandingFileType.WEBM,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_FLV: ContentUnderstandingFileType.FLV,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_WMV: ContentUnderstandingFileType.WMV,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_WAV: ContentUnderstandingFileType.WAV,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_MP3: ContentUnderstandingFileType.MP3,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_M4A: ContentUnderstandingFileType.M4A,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_FLAC: ContentUnderstandingFileType.FLAC,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_OGG: ContentUnderstandingFileType.OGG,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_AAC: ContentUnderstandingFileType.AAC,
    markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_WMA: ContentUnderstandingFileType.WMA,
}


def _abort_from_exception(
    context: grpc.ServicerContext, exc: BaseException
) -> NoReturn:
    if isinstance(exc, FileNotFoundError):
        context.abort(grpc.StatusCode.NOT_FOUND, str(exc))
    if isinstance(exc, UnsupportedFormatException):
        context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(exc))
    if isinstance(exc, MissingDependencyException):
        context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(exc))
    if isinstance(exc, FileConversionException):
        context.abort(grpc.StatusCode.INTERNAL, str(exc))
    if isinstance(exc, MarkItDownException):
        context.abort(grpc.StatusCode.INTERNAL, str(exc))
    if isinstance(exc, ValueError):
        context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
    if isinstance(exc, OSError) and exc.errno == 2:
        context.abort(grpc.StatusCode.NOT_FOUND, str(exc))
    raise exc


class MarkItDownServiceServicer(markitdown_pb2_grpc.MarkItDownServiceServicer):
    def __init__(self) -> None:
        self._streaming_controller = StreamingConverterController()

    def Convert(
        self, request: markitdown_pb2.ConvertRequest, context: grpc.ServicerContext
    ) -> markitdown_pb2.ConvertResponse:
        try:
            conversion_result = self._convert_request(request, context)
        except Exception as exc:
            _abort_from_exception(context, exc)
        return markitdown_pb2.ConvertResponse(
            result=self._to_proto_result(conversion_result)
        )

    def ConvertStream(
        self,
        request: markitdown_pb2.ConvertStreamRequest,
        context: grpc.ServicerContext,
    ) -> Iterator[markitdown_pb2.ConvertStreamResponse]:
        source_kind = request.source.WhichOneof("input")
        if source_kind is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "source.input is required and must set one of local_path, uri, or content.",
            )

        chunk_size = _resolve_chunk_size(request, context)

        yield markitdown_pb2.ConvertStreamResponse(
            started=markitdown_pb2.ConversionStarted(source_kind=source_kind)
        )

        title: str | None = None
        try:
            fragments = self._try_incremental_fragments(request)
            if fragments is not None:
                chunk_count = 0
                for markdown_chunk, is_last in _iter_incremental_chunks(
                    fragments, chunk_size
                ):
                    yield markitdown_pb2.ConvertStreamResponse(
                        markdown_chunk=markitdown_pb2.MarkdownChunk(
                            chunk_index=chunk_count,
                            markdown=markdown_chunk,
                            is_last=is_last,
                        )
                    )
                    chunk_count += 1
                total_chunks = chunk_count
            else:
                conversion_result = self._convert_request(request, context)
                title = conversion_result.title
                chunks = list(_chunk_markdown(conversion_result.markdown, chunk_size))
                if not chunks:
                    chunks = [""]
                for chunk_index, markdown_chunk in enumerate(chunks):
                    yield markitdown_pb2.ConvertStreamResponse(
                        markdown_chunk=markitdown_pb2.MarkdownChunk(
                            chunk_index=chunk_index,
                            markdown=markdown_chunk,
                            is_last=chunk_index == len(chunks) - 1,
                        )
                    )
                total_chunks = len(chunks)
        except Exception as exc:
            _abort_from_exception(context, exc)

        completed = markitdown_pb2.ConversionCompleted(total_chunks=total_chunks)
        if title:
            completed.title = title
        yield markitdown_pb2.ConvertStreamResponse(completed=completed)

    def ConvertDocumentStream(
        self,
        request: markitdown_pb2.ConvertDocumentStreamRequest,
        context: grpc.ServicerContext,
    ) -> Iterator[markitdown_pb2.ConvertDocumentStreamResponse]:
        source_kind = request.source.WhichOneof("input")
        if source_kind is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "source.input is required and must set one of local_path, uri, or content.",
            )

        yield markitdown_pb2.ConvertDocumentStreamResponse(
            started=markitdown_pb2.ConversionStarted(source_kind=source_kind)
        )

        title: str | None = None
        element_index = 0
        try:
            fragments = self._try_incremental_fragments(request)
            if fragments is not None:
                # Fragments are separated by blank lines, so blocks never
                # span fragments and per-fragment segmentation matches
                # whole-document segmentation.
                for fragment in fragments:
                    for block in _segmenter.segment_markdown(fragment):
                        yield markitdown_pb2.ConvertDocumentStreamResponse(
                            element=_to_proto_element(block, element_index)
                        )
                        element_index += 1
            else:
                conversion_result = self._convert_request(request, context)
                title = conversion_result.title
                for block in _segmenter.segment_markdown(conversion_result.markdown):
                    yield markitdown_pb2.ConvertDocumentStreamResponse(
                        element=_to_proto_element(block, element_index)
                    )
                    element_index += 1
        except Exception as exc:
            _abort_from_exception(context, exc)

        completed = markitdown_pb2.DocumentStreamCompleted(total_elements=element_index)
        if title:
            completed.title = title
        yield markitdown_pb2.ConvertDocumentStreamResponse(completed=completed)

    def _try_incremental_fragments(
        self,
        request: (
            markitdown_pb2.ConvertStreamRequest
            | markitdown_pb2.ConvertDocumentStreamRequest
        ),
    ) -> Iterator[str] | None:
        """Return an incremental fragment iterator, or None to use the
        whole-document conversion path.

        Incremental conversion is experimental and opt-in via
        streaming_options.experimental_incremental. It only applies to
        inline content and local paths with a format a streaming converter
        accepts, and is skipped when service options route conversion
        elsewhere (Azure backends, plugins).
        """
        if not (
            request.HasField("streaming_options")
            and request.streaming_options.experimental_incremental
        ):
            return None

        service_options = request.service_options
        if (
            service_options.HasField("document_intelligence")
            or service_options.HasField("content_understanding")
            or (
                service_options.HasField("enable_plugins")
                and service_options.enable_plugins
            )
            or (
                service_options.HasField("enable_builtins")
                and not service_options.enable_builtins
            )
        ):
            return None

        source_kind = request.source.WhichOneof("input")
        if source_kind == "content":
            file_stream: io.BufferedIOBase = io.BytesIO(request.source.content)
        elif source_kind == "local_path":
            file_stream = open(request.source.local_path, "rb")
        else:
            return None  # URIs use the standard path, which handles fetching.

        stream_info = _to_stream_info(request.source.stream_info) or StreamInfo()
        kwargs: dict[str, object] = {}
        if request.conversion_options.HasField("keep_data_uris"):
            kwargs["keep_data_uris"] = request.conversion_options.keep_data_uris

        fragments = self._streaming_controller.iter_markdown(
            file_stream, stream_info, **kwargs
        )
        if fragments is None:
            file_stream.close()
            return None

        def _closing() -> Iterator[str]:
            try:
                yield from fragments
            finally:
                file_stream.close()

        return _closing()

    def _convert_request(
        self,
        request: (
            markitdown_pb2.ConvertRequest
            | markitdown_pb2.ConvertStreamRequest
            | markitdown_pb2.ConvertDocumentStreamRequest
        ),
        context: grpc.ServicerContext,
    ) -> DocumentConverterResult:
        source_kind = request.source.WhichOneof("input")
        if source_kind is None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "source.input is required and must set one of local_path, uri, or content.",
            )

        markitdown_client = _create_markitdown(request.service_options)
        convert_kwargs = _build_convert_kwargs(
            request.conversion_options, request.source
        )

        if source_kind == "local_path":
            return markitdown_client.convert_local(
                request.source.local_path, **convert_kwargs
            )
        if source_kind == "uri":
            return markitdown_client.convert_uri(request.source.uri, **convert_kwargs)

        assert source_kind == "content"
        return markitdown_client.convert_stream(
            io.BytesIO(request.source.content), **convert_kwargs
        )

    @staticmethod
    def _to_proto_result(
        conversion_result: DocumentConverterResult,
    ) -> markitdown_pb2.ConversionResult:
        proto_result = markitdown_pb2.ConversionResult(
            markdown=conversion_result.markdown
        )
        if conversion_result.title:
            proto_result.title = conversion_result.title
        return proto_result


def _build_convert_kwargs(
    conversion_options: markitdown_pb2.ConversionOptions,
    source: markitdown_pb2.Source,
) -> dict[str, object]:
    kwargs: dict[str, object] = {}
    if conversion_options.HasField("keep_data_uris"):
        kwargs["keep_data_uris"] = conversion_options.keep_data_uris

    stream_info = _to_stream_info(source.stream_info)
    if stream_info is not None:
        kwargs["stream_info"] = stream_info
    return kwargs


def _to_stream_info(stream_info: markitdown_pb2.StreamInfo) -> StreamInfo | None:
    values: dict[str, str] = {}

    if stream_info.HasField("mimetype"):
        values["mimetype"] = stream_info.mimetype
    if stream_info.HasField("extension"):
        values["extension"] = stream_info.extension
    if stream_info.HasField("charset"):
        values["charset"] = stream_info.charset
    if stream_info.HasField("filename"):
        values["filename"] = stream_info.filename
    if stream_info.HasField("local_path"):
        values["local_path"] = stream_info.local_path
    if stream_info.HasField("url"):
        values["url"] = stream_info.url

    if not values:
        return None
    return StreamInfo(**values)


def _create_markitdown(service_options: markitdown_pb2.ServiceOptions) -> MarkItDown:
    kwargs: dict[str, object] = {}

    if service_options.HasField("enable_builtins"):
        kwargs["enable_builtins"] = service_options.enable_builtins
    if service_options.HasField("enable_plugins"):
        kwargs["enable_plugins"] = service_options.enable_plugins

    if service_options.HasField("document_intelligence"):
        kwargs["docintel_endpoint"] = service_options.document_intelligence.endpoint

    if service_options.HasField("content_understanding"):
        cu_options = service_options.content_understanding
        kwargs["cu_endpoint"] = cu_options.endpoint
        if cu_options.HasField("analyzer_id"):
            kwargs["cu_analyzer_id"] = cu_options.analyzer_id
        if cu_options.file_types:
            kwargs["cu_file_types"] = _to_cu_file_types(cu_options.file_types)

    return MarkItDown(**kwargs)


def _to_cu_file_types(
    file_types: Iterable[int],
) -> list[ContentUnderstandingFileType]:
    converted: list[ContentUnderstandingFileType] = []
    for file_type in file_types:
        if file_type == markitdown_pb2.CONTENT_UNDERSTANDING_FILE_TYPE_UNSPECIFIED:
            continue
        mapped = _CU_FILE_TYPE_MAP.get(file_type)
        if mapped is None:
            raise ValueError(
                f"Unknown content_understanding.file_types value: {file_type}"
            )
        converted.append(mapped)
    return converted


def _resolve_chunk_size(
    request: markitdown_pb2.ConvertStreamRequest,
    context: grpc.ServicerContext,
) -> int:
    chunk_size = _DEFAULT_MARKDOWN_CHUNK_SIZE_BYTES
    if request.HasField("streaming_options") and request.streaming_options.HasField(
        "markdown_chunk_size_bytes"
    ):
        chunk_size = request.streaming_options.markdown_chunk_size_bytes
    if chunk_size == 0:
        context.abort(
            grpc.StatusCode.INVALID_ARGUMENT,
            "streaming_options.markdown_chunk_size_bytes must be greater than zero.",
        )
    return int(chunk_size)


def _warn_if_non_local_bind(bind_address: str) -> None:
    host = bind_address.rsplit(":", maxsplit=1)[0]
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    if host not in ("127.0.0.1", "localhost", "::1"):
        print(
            "\n"
            "WARNING: The gRPC server is being bound to a non-localhost interface "
            f"({host}).\n"
            "This exposes the server to other machines on the network or Internet.\n"
            "The server has NO authentication and runs with your user's privileges.\n"
            "Any process or user that can reach this interface can read files and\n"
            "fetch network resources accessible to this user.\n"
            "Only proceed if you understand the security implications.\n",
            file=sys.stderr,
        )


def _chunk_markdown(markdown: str, chunk_size: int) -> Iterator[str]:
    if not markdown:
        return

    start = 0
    while start < len(markdown):
        end = min(start + chunk_size, len(markdown))
        yield markdown[start:end]
        start = end


def _iter_incremental_chunks(
    fragments: Iterator[str], chunk_size: int
) -> Iterator[tuple[str, bool]]:
    """Re-chunk incremental markdown fragments into (chunk, is_last) pairs.

    Joins fragments with a blank line (matching whole-document conversion
    output) and emits fixed-size chunks as soon as they fill, holding back
    a partial tail so the final chunk can be flagged is_last without
    waiting for the whole document.
    """
    buffer = ""
    first = True
    for fragment in fragments:
        if not first:
            buffer += "\n\n"
        first = False
        buffer += fragment
        while len(buffer) > chunk_size:
            yield buffer[:chunk_size], False
            buffer = buffer[chunk_size:]
    yield buffer, True


def _to_proto_element(
    block: _segmenter.DocumentBlock, element_index: int
) -> markitdown_pb2.DocumentElement:
    element = markitdown_pb2.DocumentElement(element_index=element_index)

    if isinstance(block, _segmenter.HeadingBlock):
        element.heading.level = block.level
        element.heading.text = block.text
    elif isinstance(block, _segmenter.TableBlock):
        element.table.markdown = block.markdown
        for row in block.rows:
            element.table.rows.add(cells=row)
    elif isinstance(block, _segmenter.ListBlock):
        element.list.markdown = block.markdown
        element.list.ordered = block.ordered
        element.list.items.extend(block.items)
    elif isinstance(block, _segmenter.CodeBlock):
        element.code_block.language = block.language
        element.code_block.code = block.code
    elif isinstance(block, _segmenter.ImageBlock):
        element.image.alt_text = block.alt_text
        element.image.url = block.url
        if block.title is not None:
            element.image.title = block.title
    elif isinstance(block, _segmenter.BlockQuoteBlock):
        element.block_quote.text = block.text
    elif isinstance(block, _segmenter.HorizontalRuleBlock):
        element.horizontal_rule.SetInParent()
    else:
        assert isinstance(block, _segmenter.ParagraphBlock)
        element.paragraph.text = block.text

    return element


def _enable_health_and_reflection(grpc_server: grpc.Server) -> None:
    """Register standard health and reflection services when available.

    Both packages ship with the markitdown[grpc] extra; the guards keep the
    server usable in minimal environments where only grpcio is installed.
    """
    service_names = [
        markitdown_pb2.DESCRIPTOR.services_by_name["MarkItDownService"].full_name,
    ]

    try:
        from grpc_health.v1 import health, health_pb2, health_pb2_grpc

        health_servicer = health.HealthServicer()
        health_pb2_grpc.add_HealthServicer_to_server(health_servicer, grpc_server)
        for service_name in [*service_names, ""]:
            health_servicer.set(service_name, health_pb2.HealthCheckResponse.SERVING)
        service_names.append(health.SERVICE_NAME)
    except ImportError:
        pass

    try:
        from grpc_reflection.v1alpha import reflection

        reflection.enable_server_reflection(
            [*service_names, reflection.SERVICE_NAME], grpc_server
        )
    except ImportError:
        pass


def serve(
    bind_address: str = "127.0.0.1:50051",
    max_workers: int = 10,
    max_receive_message_bytes: int = DEFAULT_MAX_MESSAGE_BYTES,
) -> grpc.Server:
    """Start a MarkItDown gRPC server and return it.

    Args:
        bind_address: host:port to listen on. The server is insecure
            (no TLS, no authentication); bind to localhost unless the
            network path is otherwise secured.
        max_workers: Maximum worker threads for handling requests.
        max_receive_message_bytes: Upper bound for incoming request size,
            which limits inline `Source.content` payloads. Defaults to
            100 MiB.
    """
    options = [
        ("grpc.max_receive_message_length", max_receive_message_bytes),
        ("grpc.max_send_message_length", max_receive_message_bytes),
    ]

    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers), options=options
    )
    markitdown_pb2_grpc.add_MarkItDownServiceServicer_to_server(
        MarkItDownServiceServicer(), grpc_server
    )
    _enable_health_and_reflection(grpc_server)
    grpc_server.add_insecure_port(bind_address)
    grpc_server.start()
    return grpc_server


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the MarkItDown gRPC server.")
    parser.add_argument(
        "--bind-address",
        default="127.0.0.1:50051",
        help="Address the gRPC server listens on.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=10,
        help="Maximum worker threads for handling requests.",
    )
    parser.add_argument(
        "--max-receive-message-bytes",
        type=int,
        default=DEFAULT_MAX_MESSAGE_BYTES,
        help=(
            "Maximum size of incoming request messages in bytes, which bounds "
            "inline Source.content payloads (default: 100 MiB)."
        ),
    )
    args = parser.parse_args()

    _warn_if_non_local_bind(args.bind_address)
    grpc_server = serve(
        bind_address=args.bind_address,
        max_workers=args.max_workers,
        max_receive_message_bytes=args.max_receive_message_bytes,
    )
    grpc_server.wait_for_termination()


if __name__ == "__main__":
    main()
