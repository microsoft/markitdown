#!/usr/bin/env python3 -m pytest
"""Regression tests for the SSRF destination policy on convert_uri HTTP(S) fetches.

These tests exercise the network-egress hardening added for the unauthenticated
MCP ``convert_to_markdown`` SSRF finding: caller-supplied HTTP(S) destinations
are validated before any socket is opened, redirects are re-validated on every
hop, and non-public targets require an explicit opt-in.
"""

import socket
from unittest.mock import MagicMock, patch

import pytest
import requests

from markitdown import MarkItDown
from markitdown._markitdown import _validate_fetch_destination


class _FakeResponse:
    """Minimal stand-in for requests.Response used to observe fetch behavior."""

    def __init__(self, status_code=200, headers=None, body=b"hello world", url="https://example.com/"):
        self.status_code = status_code
        self.headers = headers or {}
        self._body = body
        self.url = url

    @property
    def is_redirect(self):
        return self.status_code in (301, 302, 303, 307, 308)

    is_permanent_redirect = False

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")

    def close(self):
        pass

    def iter_content(self, chunk_size=65536):
        for i in range(0, len(self._body), chunk_size):
            yield self._body[i : i + chunk_size]


def _session_that_records(monkeypatch):
    """Return a fake requests.Session recording each (url, kwargs) it is asked to GET."""
    recorded = []
    session = MagicMock()

    def fake_get(url, **kwargs):
        recorded.append((url, kwargs))
        return _FakeResponse(headers={"content-type": "text/plain"}, body=b"ok", url=url)

    session.get.side_effect = fake_get
    return session, recorded


@pytest.mark.parametrize(
    "uri",
    [
        "http://127.0.0.1/",
        "http://localhost/",
        "http://169.254.169.254/latest/meta-data/",
        "http://10.1.2.3/",
        "http://192.168.0.10/",
        "http://172.16.5.5/",
        "http://[::1]/",
        "http://[fd00::1]/",
    ],
)
def test_non_public_destinations_are_rejected(uri):
    with pytest.raises(ValueError):
        _validate_fetch_destination(uri)


@pytest.mark.parametrize("uri", ["ftp://example.com/x", "gopher://example.com/x", "file:///etc/passwd"])
def test_non_http_schemes_are_rejected(uri):
    with pytest.raises(ValueError):
        _validate_fetch_destination(uri)


def test_allow_private_networks_opt_in():
    # Loopback is rejected by default but permitted with the explicit opt-in.
    with pytest.raises(ValueError):
        _validate_fetch_destination("http://127.0.0.1/")
    _validate_fetch_destination("http://127.0.0.1/", allow_private_networks=True)


def test_convert_uri_does_not_open_socket_for_internal_target(monkeypatch):
    """The internal destination must be refused before any request is issued."""
    session, recorded = _session_that_records(monkeypatch)
    md = MarkItDown(requests_session=session)

    with pytest.raises(ValueError):
        md.convert_uri("http://169.254.169.254/latest/meta-data/iam/security-credentials/")

    assert recorded == [], "no HTTP request should be made to a non-public host"


def test_convert_uri_sends_explicit_timeout(monkeypatch):
    """Every outbound request must carry a finite connect/read timeout."""
    session, recorded = _session_that_records(monkeypatch)
    md = MarkItDown(requests_session=session)

    with patch("markitdown._markitdown._validate_fetch_destination", return_value=None):
        md.convert_uri("https://example.com/")

    assert recorded, "expected a request to be issued"
    _, kwargs = recorded[0]
    assert kwargs.get("timeout"), "timeout must be set on the outbound request"
    assert kwargs.get("allow_redirects") is False, "requests must not follow redirects itself"


def test_redirect_to_internal_host_is_rejected(monkeypatch):
    """A redirect that lands on an internal address must be refused on the hop."""
    session = MagicMock()
    calls = []

    def fake_get(url, **kwargs):
        calls.append(url)
        if url == "https://example.com/":
            return _FakeResponse(status_code=302, headers={"Location": "http://169.254.169.254/"})
        return _FakeResponse(body=b"internal")

    session.get.side_effect = fake_get
    md = MarkItDown(requests_session=session)

    with pytest.raises(ValueError):
        md.convert_uri("https://example.com/")

    # The first (public) hop was allowed, the redirect target was refused.
    assert "http://169.254.169.254/" not in calls
