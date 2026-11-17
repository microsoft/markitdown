import json
import threading
import urllib.error
import urllib.request
from dataclasses import replace
from pathlib import Path

import pytest

from markitdown_service.config import Config, ConfigError, load_config
from markitdown_service.server import create_server

FILES = Path(__file__).resolve().parents[2] / "markitdown" / "tests" / "test_files"
TOKEN = "t" * 40

BASE = Config(
    token=TOKEN,
    host="127.0.0.1",
    port=0,
    max_upload_bytes=2 * 1024 * 1024,
    timeout_seconds=60,
)


class Running:
    def __init__(self, config: Config):
        self.server = create_server(config)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

    def post(self, name, body, token=TOKEN, headers=None):
        h = {"Content-Type": "application/octet-stream"}
        if token:
            h["Authorization"] = f"Bearer {token}"
        h.update(headers or {})
        req = urllib.request.Request(
            f"{self.url}/converter?nome={name}", data=body, headers=h, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())


@pytest.fixture(scope="module")
def svc():
    s = Running(BASE)
    yield s
    s.stop()


def test_healthz_needs_no_token(svc):
    with urllib.request.urlopen(f"{svc.url}/healthz") as r:
        assert json.loads(r.read()) == {"ok": True}


@pytest.mark.parametrize("token", [None, "errado", TOKEN[:-1], TOKEN + "x"])
def test_refuses_missing_or_wrong_token(svc, token):
    status, body = svc.post("a.pdf", b"%PDF-1.4", token=token)
    assert (status, body["erro"]) == (401, "nao_autorizado")


def test_refuses_unknown_extension(svc):
    for name in ["a.exe", "a.html", "a.txt", "semextensao", "a.pdf.exe", ""]:
        status, body = svc.post(name, b"x")
        assert (status, body["erro"]) == (415, "formato_nao_suportado"), name


def test_refuses_empty_and_oversized(svc):
    assert svc.post("a.pdf", b"")[1]["erro"] == "arquivo_vazio"
    # The answer comes before the body is read, so test it with a client that only sends the headers.
    import socket

    c = socket.create_connection(("127.0.0.1", svc.server.server_address[1]))
    c.sendall(
        (
            f"POST /converter?nome=a.pdf HTTP/1.0\r\nAuthorization: Bearer {TOKEN}\r\n"
            f"Content-Length: {BASE.max_upload_bytes + 1}\r\n\r\n"
        ).encode()
    )
    answer = c.recv(4096).decode()
    c.close()
    assert answer.startswith("HTTP/1.0 413") and "arquivo_grande_demais" in answer


def test_unknown_routes_and_methods(svc):
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(f"{svc.url}/outra")
    assert e.value.code == 404
    req = urllib.request.Request(f"{svc.url}/converter?nome=a.pdf", method="DELETE")
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(req)
    assert e.value.code == 405


def test_converts_a_pdf(svc):
    status, body = svc.post("relatorio.pdf", (FILES / "test.pdf").read_bytes())
    assert status == 200 and body["ok"] is True
    assert body["extensao"] == ".pdf"
    assert body["caracteres"] == len(body["markdown"]) > 100


def test_converts_docx_pptx_xls(svc):
    for name in ["test.docx", "test.pptx", "test.xls"]:
        status, body = svc.post(name, (FILES / name).read_bytes())
        assert status == 200, (name, body)
        assert body["markdown"].strip()


def test_extension_in_upper_case_is_accepted(svc):
    status, _ = svc.post("RELATORIO.PDF", (FILES / "test.pdf").read_bytes())
    assert status == 200


def test_content_must_match_the_extension(svc):
    cases = {
        "falso.pdf": b"isto e so um texto renomeado" * 20,
        "falso.docx": (FILES / "test.pdf").read_bytes(),
        "falso.xls": (FILES / "test.docx").read_bytes(),
    }
    for name, data in cases.items():
        status, body = svc.post(name, data)
        assert (status, body["erro"]) == (415, "conteudo_nao_confere"), name


def test_corrupt_file_is_a_clean_error(svc):
    status, body = svc.post("quebrado.docx", b"PK\x03\x04" + b"lixo" * 200)
    assert status == 422
    assert body["erro"] == "conversao_falhou"
    assert "Traceback" not in json.dumps(body)


def test_error_never_echoes_the_file_name(svc):
    _, body = svc.post("segredo-do-cliente.exe", b"x")
    assert "segredo" not in json.dumps(body)


def test_busy_when_all_slots_are_taken():
    s = Running(replace(BASE, max_concurrent=1))
    try:
        assert (
            s.server.RequestHandlerClass
        )  # the gate is private: take it through a slow client instead
        import socket

        c = socket.create_connection(("127.0.0.1", s.server.server_address[1]))
        head = (
            f"POST /converter?nome=a.pdf HTTP/1.0\r\nAuthorization: Bearer {TOKEN}\r\n"
            "Content-Length: 1000\r\n\r\n"
        ).encode()
        c.sendall(
            head + b"x" * 10
        )  # holds the only slot waiting for the other 990 bytes
        import time

        time.sleep(0.5)
        status, body = s.post("b.pdf", b"x")
        assert (status, body["erro"]) == (429, "ocupado")
        c.close()
    finally:
        s.stop()


def test_timeout_is_a_504(svc, monkeypatch):
    import subprocess

    def slow(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="worker", timeout=1)

    monkeypatch.setattr("markitdown_service.server.subprocess.run", slow)
    status, body = svc.post("a.pdf", (FILES / "test.pdf").read_bytes())
    assert (status, body["erro"]) == (504, "tempo_esgotado")


def test_worker_has_a_real_timeout(monkeypatch):
    """The conversion process is really killed when it runs too long (not just reported)."""
    import sys
    import time

    from markitdown_service import server

    real_run = server.subprocess.run

    def sleeper(cmd, **kw):
        return real_run([sys.executable, "-c", "import time; time.sleep(30)"], **kw)

    monkeypatch.setattr(server.subprocess, "run", sleeper)
    started = time.monotonic()
    markdown, error = server.run_worker(b"x", ".pdf", replace(BASE, timeout_seconds=1))
    assert (markdown, error) == (None, "tempo_esgotado")
    assert time.monotonic() - started < 10


def test_config_requires_a_strong_token():
    with pytest.raises(ConfigError):
        load_config({})
    with pytest.raises(ConfigError):
        load_config({"MARKITDOWN_ADMIN_TOKEN": "curto"})
    with pytest.raises(ConfigError):
        load_config({"MARKITDOWN_ADMIN_TOKEN": TOKEN, "PORT": "abc"})
    cfg = load_config(
        {"MARKITDOWN_ADMIN_TOKEN": TOKEN, "MARKITDOWN_MAX_UPLOAD_MB": "5"}
    )
    assert cfg.max_upload_bytes == 5 * 1024 * 1024 and cfg.port == 8000
