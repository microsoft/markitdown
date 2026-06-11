from __future__ import annotations

import argparse
import sys
from typing import Iterator

import grpc

from .v1 import markitdown_pb2, markitdown_pb2_grpc

# Matches the server default so large documents and results round-trip.
DEFAULT_MAX_MESSAGE_BYTES = 100 * 1024 * 1024


class MarkItDownClient:
    """A simple gRPC client for the MarkItDown service."""

    def __init__(
        self,
        address: str = "127.0.0.1:50051",
        channel: grpc.Channel | None = None,
        max_message_bytes: int = DEFAULT_MAX_MESSAGE_BYTES,
    ) -> None:
        """Create a client.

        Args:
            address: host:port of the server. Ignored when `channel` is given.
            channel: An externally managed channel to use instead of creating
                one. Message size limits are then the caller's responsibility.
            max_message_bytes: Send/receive message size limit for the
                internally created channel. Defaults to 100 MiB to match the
                server.
        """
        if channel is not None:
            self._channel = channel
            self._owns_channel = False
        else:
            self._channel = grpc.insecure_channel(
                address,
                options=[
                    ("grpc.max_receive_message_length", max_message_bytes),
                    ("grpc.max_send_message_length", max_message_bytes),
                ],
            )
            self._owns_channel = True
        self._stub = markitdown_pb2_grpc.MarkItDownServiceStub(self._channel)

    def close(self) -> None:
        if self._owns_channel:
            self._channel.close()

    def __enter__(self) -> MarkItDownClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def convert(
        self,
        *,
        local_path: str | None = None,
        uri: str | None = None,
        content: bytes | None = None,
        mimetype: str | None = None,
        extension: str | None = None,
        charset: str | None = None,
        keep_data_uris: bool | None = None,
    ) -> markitdown_pb2.ConversionResult:
        """Convert a document and return the full result."""
        request = _build_convert_request(
            local_path=local_path,
            uri=uri,
            content=content,
            mimetype=mimetype,
            extension=extension,
            charset=charset,
            keep_data_uris=keep_data_uris,
        )
        response: markitdown_pb2.ConvertResponse = self._stub.Convert(request)
        return response.result

    def convert_stream(
        self,
        *,
        local_path: str | None = None,
        uri: str | None = None,
        content: bytes | None = None,
        mimetype: str | None = None,
        extension: str | None = None,
        charset: str | None = None,
        keep_data_uris: bool | None = None,
        chunk_size_bytes: int | None = None,
        incremental: bool | None = None,
    ) -> Iterator[markitdown_pb2.ConvertStreamResponse]:
        """Convert a document and yield streaming response events.

        Set `incremental=True` to opt into EXPERIMENTAL incremental
        conversion: supported formats (PDF, PPTX) stream chunks as each
        page or slide converts, instead of after the whole document.
        """
        source = _build_source(
            local_path=local_path,
            uri=uri,
            content=content,
            mimetype=mimetype,
            extension=extension,
            charset=charset,
        )
        conversion_options = markitdown_pb2.ConversionOptions()
        if keep_data_uris is not None:
            conversion_options.keep_data_uris = keep_data_uris

        streaming_options = markitdown_pb2.StreamingOptions()
        if chunk_size_bytes is not None:
            streaming_options.markdown_chunk_size_bytes = chunk_size_bytes
        if incremental is not None:
            streaming_options.experimental_incremental = incremental

        request = markitdown_pb2.ConvertStreamRequest(
            source=source,
            conversion_options=conversion_options,
            streaming_options=streaming_options,
        )
        yield from self._stub.ConvertStream(request)

    def convert_document_stream(
        self,
        *,
        local_path: str | None = None,
        uri: str | None = None,
        content: bytes | None = None,
        mimetype: str | None = None,
        extension: str | None = None,
        charset: str | None = None,
        keep_data_uris: bool | None = None,
        incremental: bool | None = None,
    ) -> Iterator[markitdown_pb2.ConvertDocumentStreamResponse]:
        """Convert a document and yield structured document elements.

        Events arrive in order: one `started`, zero or more `element`
        (headings, paragraphs, tables, lists, code blocks, images, ...),
        then one `completed`.

        Set `incremental=True` to opt into EXPERIMENTAL incremental
        conversion: supported formats (PDF, PPTX) stream elements as each
        page or slide converts, instead of after the whole document.
        """
        source = _build_source(
            local_path=local_path,
            uri=uri,
            content=content,
            mimetype=mimetype,
            extension=extension,
            charset=charset,
        )
        conversion_options = markitdown_pb2.ConversionOptions()
        if keep_data_uris is not None:
            conversion_options.keep_data_uris = keep_data_uris

        streaming_options = markitdown_pb2.StreamingOptions()
        if incremental is not None:
            streaming_options.experimental_incremental = incremental

        request = markitdown_pb2.ConvertDocumentStreamRequest(
            source=source,
            conversion_options=conversion_options,
            streaming_options=streaming_options,
        )
        yield from self._stub.ConvertDocumentStream(request)


def _build_source(
    *,
    local_path: str | None,
    uri: str | None,
    content: bytes | None,
    mimetype: str | None,
    extension: str | None,
    charset: str | None,
) -> markitdown_pb2.Source:
    stream_info_kwargs: dict[str, str] = {}
    if mimetype is not None:
        stream_info_kwargs["mimetype"] = mimetype
    if extension is not None:
        stream_info_kwargs["extension"] = extension
    if charset is not None:
        stream_info_kwargs["charset"] = charset
    stream_info = markitdown_pb2.StreamInfo(**stream_info_kwargs)

    if local_path is not None:
        return markitdown_pb2.Source(local_path=local_path, stream_info=stream_info)
    if uri is not None:
        return markitdown_pb2.Source(uri=uri, stream_info=stream_info)
    if content is not None:
        return markitdown_pb2.Source(content=content, stream_info=stream_info)
    raise ValueError("One of local_path, uri, or content must be provided.")


def _build_convert_request(
    *,
    local_path: str | None,
    uri: str | None,
    content: bytes | None,
    mimetype: str | None,
    extension: str | None,
    charset: str | None,
    keep_data_uris: bool | None,
) -> markitdown_pb2.ConvertRequest:
    source = _build_source(
        local_path=local_path,
        uri=uri,
        content=content,
        mimetype=mimetype,
        extension=extension,
        charset=charset,
    )
    conversion_options = markitdown_pb2.ConversionOptions()
    if keep_data_uris is not None:
        conversion_options.keep_data_uris = keep_data_uris

    return markitdown_pb2.ConvertRequest(
        source=source,
        conversion_options=conversion_options,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send a convert request to a running MarkItDown gRPC server.",
        prog="markitdown-grpc-client",
    )
    parser.add_argument(
        "--address",
        default="127.0.0.1:50051",
        help="Address of the gRPC server (default: 127.0.0.1:50051).",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file. If not provided, output is written to stdout.",
    )
    parser.add_argument(
        "-x",
        "--extension",
        help="Hint about the file extension (e.g. .pdf).",
    )
    parser.add_argument(
        "-m",
        "--mime-type",
        help="Hint about the file MIME type.",
    )
    parser.add_argument(
        "-c",
        "--charset",
        help="Hint about the file charset (e.g. UTF-8).",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Use the streaming ConvertStream RPC instead of the unary Convert RPC.",
    )

    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        "--uri",
        help="Remote URI to convert.",
    )
    source_group.add_argument(
        "filename",
        nargs="?",
        help="Local file path to convert. Reads from stdin if omitted.",
    )

    args = parser.parse_args()

    extension = args.extension
    if extension and not extension.startswith("."):
        extension = "." + extension

    with MarkItDownClient(address=args.address) as client:
        if args.uri:
            kwargs = dict(
                uri=args.uri,
                mimetype=args.mime_type,
                extension=extension,
                charset=args.charset,
            )
        elif args.filename:
            kwargs = dict(
                local_path=args.filename,
                mimetype=args.mime_type,
                extension=extension,
                charset=args.charset,
            )
        else:
            data = sys.stdin.buffer.read()
            kwargs = dict(
                content=data,
                mimetype=args.mime_type,
                extension=extension,
                charset=args.charset,
            )

        if args.stream:
            markdown_parts: list[str] = []
            for event in client.convert_stream(**kwargs):  # type: ignore[arg-type]
                if event.HasField("markdown_chunk"):
                    markdown_parts.append(event.markdown_chunk.markdown)
            markdown = "".join(markdown_parts)
        else:
            result = client.convert(**kwargs)  # type: ignore[arg-type]
            markdown = result.markdown

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
    else:
        try:
            sys.stdout.reconfigure(errors="replace")
        except AttributeError:
            pass  # stdout replaced by a non-reconfigurable stream
        print(markdown)


if __name__ == "__main__":
    main()
