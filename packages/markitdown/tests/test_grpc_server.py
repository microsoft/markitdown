from __future__ import annotations

from concurrent import futures
from pathlib import Path

import grpc
import pytest

from markitdown.grpc.server import (
    MarkItDownServiceServicer,
    _enable_health_and_reflection,
)
from markitdown.grpc.v1 import markitdown_pb2, markitdown_pb2_grpc


@pytest.fixture
def grpc_channel():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    markitdown_pb2_grpc.add_MarkItDownServiceServicer_to_server(
        MarkItDownServiceServicer(), server
    )
    _enable_health_and_reflection(server)
    port = server.add_insecure_port("127.0.0.1:0")
    server.start()
    channel = grpc.insecure_channel(f"127.0.0.1:{port}")
    try:
        yield channel
    finally:
        channel.close()
        server.stop(grace=None)


@pytest.fixture
def grpc_client(grpc_channel):
    return markitdown_pb2_grpc.MarkItDownServiceStub(grpc_channel)


def test_convert_local_file(grpc_client, tmp_path: Path):
    sample_path = tmp_path / "sample.txt"
    sample_path.write_text("hello\ngrpc\n", encoding="utf-8")

    response = grpc_client.Convert(
        markitdown_pb2.ConvertRequest(
            source=markitdown_pb2.Source(
                local_path=str(sample_path),
                stream_info=markitdown_pb2.StreamInfo(
                    extension=".txt",
                    mimetype="text/plain",
                    charset="utf-8",
                ),
            ),
            conversion_options=markitdown_pb2.ConversionOptions(keep_data_uris=False),
            service_options=markitdown_pb2.ServiceOptions(
                enable_builtins=True, enable_plugins=False
            ),
        )
    )

    assert "hello" in response.result.markdown
    assert "grpc" in response.result.markdown


def test_convert_stream_returns_chunk_sequence(grpc_client):
    request = markitdown_pb2.ConvertStreamRequest(
        source=markitdown_pb2.Source(
            content=b"one\ntwo\nthree\n",
            stream_info=markitdown_pb2.StreamInfo(
                extension=".txt", mimetype="text/plain", charset="utf-8"
            ),
        ),
        conversion_options=markitdown_pb2.ConversionOptions(keep_data_uris=False),
        service_options=markitdown_pb2.ServiceOptions(enable_builtins=True),
        streaming_options=markitdown_pb2.StreamingOptions(markdown_chunk_size_bytes=4),
    )

    stream = list(grpc_client.ConvertStream(request))

    assert stream[0].HasField("started")
    markdown_events = [
        event.markdown_chunk for event in stream if event.HasField("markdown_chunk")
    ]
    assert len(markdown_events) > 0
    assert stream[-1].HasField("completed")
    assert stream[-1].completed.total_chunks == len(markdown_events)
    assert "".join(event.markdown for event in markdown_events).startswith("one")
    assert markdown_events[-1].is_last


def test_convert_requires_source_oneof(grpc_client):
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_client.Convert(markitdown_pb2.ConvertRequest())

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_convert_missing_local_file_returns_not_found(grpc_client):
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_client.Convert(
            markitdown_pb2.ConvertRequest(
                source=markitdown_pb2.Source(local_path="/nonexistent/file.txt")
            )
        )

    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND


def test_convert_invalid_cu_file_type_returns_invalid_argument(grpc_client):
    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_client.Convert(
            markitdown_pb2.ConvertRequest(
                source=markitdown_pb2.Source(
                    content=b"hello",
                    stream_info=markitdown_pb2.StreamInfo(extension=".txt"),
                ),
                service_options=markitdown_pb2.ServiceOptions(
                    content_understanding=markitdown_pb2.ContentUnderstandingOptions(
                        endpoint="https://example.invalid",
                        file_types=[999],
                    )
                ),
            )
        )

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT
    assert "999" in exc_info.value.details()


def test_convert_stream_yields_started_before_chunks(grpc_client):
    request = markitdown_pb2.ConvertStreamRequest(
        source=markitdown_pb2.Source(
            content=b"hello\n",
            stream_info=markitdown_pb2.StreamInfo(
                extension=".txt", mimetype="text/plain", charset="utf-8"
            ),
        ),
        conversion_options=markitdown_pb2.ConversionOptions(keep_data_uris=False),
        service_options=markitdown_pb2.ServiceOptions(enable_builtins=True),
    )

    stream = list(grpc_client.ConvertStream(request))

    assert stream[0].HasField("started")
    assert stream[0].started.source_kind == "content"
    assert any(event.HasField("markdown_chunk") for event in stream)


def test_convert_stream_zero_chunk_size_returns_invalid_argument(grpc_client):
    request = markitdown_pb2.ConvertStreamRequest(
        source=markitdown_pb2.Source(
            content=b"hello\n",
            stream_info=markitdown_pb2.StreamInfo(extension=".txt"),
        ),
        streaming_options=markitdown_pb2.StreamingOptions(markdown_chunk_size_bytes=0),
    )

    with pytest.raises(grpc.RpcError) as exc_info:
        list(grpc_client.ConvertStream(request))

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_convert_document_stream_returns_structured_elements(grpc_client):
    markdown_source = (
        b"# Title\n"
        b"\n"
        b"Intro paragraph.\n"
        b"\n"
        b"| A | B |\n"
        b"| - | - |\n"
        b"| 1 | 2 |\n"
        b"\n"
        b"- alpha\n"
        b"- beta\n"
    )
    request = markitdown_pb2.ConvertDocumentStreamRequest(
        source=markitdown_pb2.Source(
            content=markdown_source,
            stream_info=markitdown_pb2.StreamInfo(
                extension=".md", mimetype="text/markdown", charset="utf-8"
            ),
        ),
    )

    stream = list(grpc_client.ConvertDocumentStream(request))

    assert stream[0].HasField("started")
    assert stream[-1].HasField("completed")

    elements = [event.element for event in stream if event.HasField("element")]
    assert stream[-1].completed.total_elements == len(elements)
    assert [element.element_index for element in elements] == list(range(len(elements)))

    kinds = [element.WhichOneof("kind") for element in elements]
    assert "heading" in kinds
    assert "paragraph" in kinds
    assert "table" in kinds
    assert "list" in kinds

    heading = next(e.heading for e in elements if e.WhichOneof("kind") == "heading")
    assert heading.level == 1
    assert heading.text == "Title"

    table = next(e.table for e in elements if e.WhichOneof("kind") == "table")
    assert [list(row.cells) for row in table.rows] == [["A", "B"], ["1", "2"]]

    list_block = next(e.list for e in elements if e.WhichOneof("kind") == "list")
    assert not list_block.ordered
    assert list(list_block.items) == ["alpha", "beta"]


def test_convert_document_stream_requires_source(grpc_client):
    with pytest.raises(grpc.RpcError) as exc_info:
        list(
            grpc_client.ConvertDocumentStream(
                markitdown_pb2.ConvertDocumentStreamRequest()
            )
        )

    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_health_service_reports_serving(grpc_channel):
    health_pb2 = pytest.importorskip("grpc_health.v1.health_pb2")
    health_pb2_grpc = pytest.importorskip("grpc_health.v1.health_pb2_grpc")

    health_stub = health_pb2_grpc.HealthStub(grpc_channel)
    response = health_stub.Check(
        health_pb2.HealthCheckRequest(service="markitdown.v1.MarkItDownService")
    )
    assert response.status == health_pb2.HealthCheckResponse.SERVING


def test_convert_stream_incremental_pdf_streams_pages(grpc_client):
    pdf_path = (
        Path(__file__).parent / "test_files" / "REPAIR-2022-INV-001_multipage.pdf"
    )
    request = markitdown_pb2.ConvertStreamRequest(
        source=markitdown_pb2.Source(
            content=pdf_path.read_bytes(),
            stream_info=markitdown_pb2.StreamInfo(extension=".pdf"),
        ),
        streaming_options=markitdown_pb2.StreamingOptions(
            markdown_chunk_size_bytes=256, experimental_incremental=True
        ),
    )

    stream = list(grpc_client.ConvertStream(request))

    assert stream[0].HasField("started")
    chunks = [
        event.markdown_chunk for event in stream if event.HasField("markdown_chunk")
    ]
    assert len(chunks) > 1
    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))
    assert chunks[-1].is_last
    assert all(not chunk.is_last for chunk in chunks[:-1])
    assert stream[-1].HasField("completed")
    assert stream[-1].completed.total_chunks == len(chunks)

    # Incremental reassembly must match whole-document conversion exactly
    # for documents with table/form pages.
    unary = grpc_client.Convert(
        markitdown_pb2.ConvertRequest(
            source=markitdown_pb2.Source(
                content=pdf_path.read_bytes(),
                stream_info=markitdown_pb2.StreamInfo(extension=".pdf"),
            )
        )
    )
    assert "".join(chunk.markdown for chunk in chunks) == unary.result.markdown


def test_convert_document_stream_incremental_pptx(grpc_client):
    pptx_path = Path(__file__).parent / "test_files" / "test.pptx"
    request = markitdown_pb2.ConvertDocumentStreamRequest(
        source=markitdown_pb2.Source(
            content=pptx_path.read_bytes(),
            stream_info=markitdown_pb2.StreamInfo(extension=".pptx"),
        ),
        streaming_options=markitdown_pb2.StreamingOptions(
            experimental_incremental=True
        ),
    )

    stream = list(grpc_client.ConvertDocumentStream(request))

    assert stream[0].HasField("started")
    assert stream[-1].HasField("completed")
    elements = [event.element for event in stream if event.HasField("element")]
    assert stream[-1].completed.total_elements == len(elements)
    assert [element.element_index for element in elements] == list(range(len(elements)))

    kinds = {element.WhichOneof("kind") for element in elements}
    assert "heading" in kinds


def test_convert_stream_incremental_falls_back_for_unsupported_format(grpc_client):
    request = markitdown_pb2.ConvertStreamRequest(
        source=markitdown_pb2.Source(
            content=b"plain text\n",
            stream_info=markitdown_pb2.StreamInfo(extension=".txt"),
        ),
        streaming_options=markitdown_pb2.StreamingOptions(
            experimental_incremental=True
        ),
    )

    stream = list(grpc_client.ConvertStream(request))

    chunks = [
        event.markdown_chunk.markdown
        for event in stream
        if event.HasField("markdown_chunk")
    ]
    assert "".join(chunks).startswith("plain text")
    assert stream[-1].HasField("completed")


def test_large_document_round_trip(tmp_path: Path):
    """Documents larger than gRPC's stock 4 MiB limit round-trip by default."""
    from markitdown.grpc import MarkItDownClient
    from markitdown.grpc.server import serve

    import socket

    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    server = serve(bind_address=f"127.0.0.1:{port}", max_workers=1)
    try:
        # ~8 MiB of text: above the 4 MiB stock limit in both directions.
        large_text = ("lorem ipsum dolor sit amet " * 38 + "\n") * 8192
        content = large_text.encode("utf-8")
        assert len(content) > 4 * 1024 * 1024

        with MarkItDownClient(f"127.0.0.1:{port}") as client:
            result = client.convert(content=content, extension=".txt")

        assert len(result.markdown) > 4 * 1024 * 1024
        assert result.markdown.startswith("lorem ipsum")
    finally:
        server.stop(grace=None)


def test_reflection_lists_markitdown_service(grpc_channel):
    reflection_pb2 = pytest.importorskip("grpc_reflection.v1alpha.reflection_pb2")
    reflection_pb2_grpc = pytest.importorskip(
        "grpc_reflection.v1alpha.reflection_pb2_grpc"
    )

    reflection_stub = reflection_pb2_grpc.ServerReflectionStub(grpc_channel)
    responses = reflection_stub.ServerReflectionInfo(
        iter([reflection_pb2.ServerReflectionRequest(list_services="")])
    )
    services = {
        service.name
        for response in responses
        for service in response.list_services_response.service
    }
    assert "markitdown.v1.MarkItDownService" in services
