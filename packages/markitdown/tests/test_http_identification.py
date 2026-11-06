"""Exercise HTTP identification through real downloads and built-in conversion."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

import pytest
import requests

from markitdown import MarkItDown, __version__


@pytest.fixture
def identified_http_server():
    received = []
    default_agent = (
        f"MarkItDown/{__version__} (https://github.com/microsoft/markitdown)"
    )
    caller_agent = "KnowledgeIndexer/2.0 (https://example.com/contact)"

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            received.append(
                {
                    "path": self.path,
                    "user_agent": self.headers.get("User-Agent"),
                    "accept": self.headers.get("Accept"),
                    "caller": self.headers.get("X-Indexer"),
                }
            )
            if self.headers.get("User-Agent") not in (default_agent, caller_agent):
                self.send_error(403, "An identifiable client is required")
            elif self.path == "/redirect":
                self.send_response(302)
                self.send_header("Location", "/article.html")
                self.end_headers()
            else:
                body = (
                    "<html><head><title>Knowledge source</title></head>"
                    "<body><h1>Knowledge source</h1>"
                    "<p>HTTP transport preserves café and 中文.</p></body></html>"
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", received, caller_agent
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)
        assert not worker.is_alive()


@pytest.mark.parametrize("path", ["/article.html", "/redirect"])
def test_default_identification_reaches_download_and_conversion(
    identified_http_server, path
):
    base_url, received, _ = identified_http_server

    result = MarkItDown().convert(base_url + path)

    assert "# Knowledge source" in result.markdown
    assert "café and 中文" in result.markdown
    expected_paths = [path, "/article.html"] if path == "/redirect" else [path]
    assert [request["path"] for request in received] == expected_paths
    assert all(
        request["user_agent"]
        == f"MarkItDown/{__version__} (https://github.com/microsoft/markitdown)"
        for request in received
    )
    assert all(request["accept"].startswith("text/markdown") for request in received)


@pytest.mark.parametrize("path", ["/article.html", "/redirect"])
def test_caller_session_headers_survive_download_redirect_and_conversion(
    identified_http_server, path
):
    base_url, received, caller_agent = identified_http_server
    with requests.Session() as session:
        session.headers.update(
            {
                "User-Agent": caller_agent,
                "Accept": "text/html",
                "X-Indexer": "preserved",
            }
        )
        original_headers = dict(session.headers)

        result = MarkItDown(requests_session=session).convert(base_url + path)

        assert dict(session.headers) == original_headers
    assert "# Knowledge source" in result.markdown
    assert "café and 中文" in result.markdown
    expected_paths = [path, "/article.html"] if path == "/redirect" else [path]
    assert [request["path"] for request in received] == expected_paths
    assert all(request["user_agent"] == caller_agent for request in received)
    assert all(request["accept"] == "text/html" for request in received)
    assert all(request["caller"] == "preserved" for request in received)
