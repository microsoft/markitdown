"""A deliberately small HTTP API in front of MarkItDown.

    GET  /healthz                       -> 200 {"ok": true}            (no auth)
    POST /converter?nome=<file name>    -> 200 {"ok": true, "markdown": "..."}
         Authorization: Bearer <MARKITDOWN_ADMIN_TOKEN>
         body: the raw bytes of the file (no multipart)

Only uploaded bytes are converted: there is no way to make the service fetch a URL or read a path, so it cannot
be used to reach other machines or files. Each conversion runs in a separate, time- and memory-limited process.
Error bodies are {"ok": false, "erro": "<code>", "mensagem": "<text>"}; the codes are what the portal maps.
"""

import hmac
import json
import logging
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional, Tuple
from urllib.parse import parse_qs, urlsplit

from .config import EXTENSIONS, Config
from .worker import EXIT_FAILED, EXIT_UNSUPPORTED

log = logging.getLogger("markitdown_service")

MESSAGES = {
    "nao_autorizado": "Token ausente ou inválido.",
    "nao_encontrado": "Rota não encontrada.",
    "metodo_nao_permitido": "Método não permitido.",
    "tamanho_obrigatorio": "Envie o cabeçalho Content-Length.",
    "arquivo_vazio": "O arquivo está vazio.",
    "arquivo_grande_demais": "O arquivo passa do tamanho máximo.",
    "formato_nao_suportado": "Formato não suportado. Aceitos: "
    + ", ".join(EXTENSIONS)
    + ".",
    "ocupado": "O conversor está ocupado. Tente de novo em instantes.",
    "tempo_esgotado": "A conversão demorou demais e foi cancelada.",
    "conteudo_nao_confere": "O conteúdo do arquivo não corresponde à extensão (ele não é um arquivo desse tipo de verdade).",
    "conversao_falhou": "Não consegui ler este arquivo. Ele pode estar corrompido ou protegido por senha.",
    "memoria_insuficiente": "O arquivo é complexo demais para converter.",
    "sem_texto": "Não encontrei texto no arquivo. Se for um PDF escaneado (imagens de páginas), ele precisa de OCR.",
    "interno": "Erro interno do conversor.",
}


def extension_of(name: str) -> str:
    return os.path.splitext(name or "")[1].lower()


ZIP = b"PK\x03\x04"  # .docx, .pptx and .xlsx are ZIP containers
OLE2 = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"  # legacy .xls


def content_matches(extension: str, data: bytes) -> bool:
    """Is this really that kind of file? Without it MarkItDown would happily return a text file renamed to .pdf as if
    it had been converted."""
    if extension == ".pdf":
        return b"%PDF-" in data[:1024]
    if extension in (".docx", ".pptx", ".xlsx"):
        return data.startswith(ZIP)
    if extension == ".xls":
        return data.startswith(OLE2)
    return False


def run_worker(
    data: bytes, extension: str, config: Config
) -> Tuple[Optional[str], Optional[str]]:
    """Convert in a child process. Returns (markdown, None) or (None, error_code)."""
    env = dict(os.environ)
    env["MARKITDOWN_WORKER_MEMORY_MB"] = str(config.worker_memory_mb)
    env.setdefault("ORT_DISABLE_TELEMETRY", "1")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "markitdown_service.worker", extension],
            input=data,
            capture_output=True,
            timeout=config.timeout_seconds,
            env=env,
        )
    except subprocess.TimeoutExpired:
        return None, "tempo_esgotado"
    if proc.returncode == 0:
        return proc.stdout.decode("utf-8", errors="replace"), None
    if proc.returncode == EXIT_UNSUPPORTED:
        return None, "formato_nao_suportado"
    reason = proc.stderr.decode("utf-8", errors="replace").strip().splitlines()[
        -1:
    ] or [""]
    if proc.returncode == EXIT_FAILED and reason[0] == "out_of_memory":
        return None, "memoria_insuficiente"
    # EXIT_FAILED, or killed by a signal (e.g. the kernel's OOM killer): either way, this file could not be read.
    return None, "conversao_falhou"


STATUS = {
    "nao_autorizado": 401,
    "nao_encontrado": 404,
    "metodo_nao_permitido": 405,
    "tamanho_obrigatorio": 411,
    "arquivo_vazio": 400,
    "arquivo_grande_demais": 413,
    "formato_nao_suportado": 415,
    "ocupado": 429,
    "tempo_esgotado": 504,
    "conteudo_nao_confere": 415,
    "conversao_falhou": 422,
    "memoria_insuficiente": 422,
    "sem_texto": 422,
    "interno": 500,
}


def make_handler(config: Config, gate: threading.BoundedSemaphore):
    token = config.token.encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        server_version = "markitdown-service"
        sys_version = ""
        timeout = 30  # seconds without a byte from the client (slow or stalled uploads)

        def log_message(
            self, fmt, *args
        ):  # never log the request line: it carries file names
            pass

        def _send(self, status: int, body: dict):
            payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(payload)
            self.close_connection = True

        def _fail(self, code: str):
            self._send(
                STATUS[code], {"ok": False, "erro": code, "mensagem": MESSAGES[code]}
            )

        def _authorized(self) -> bool:
            header = self.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return False
            return hmac.compare_digest(header[len("Bearer ") :].encode("utf-8"), token)

        def do_GET(self):
            if urlsplit(self.path).path == "/healthz":
                return self._send(200, {"ok": True})
            self._fail("nao_encontrado")

        def do_POST(self):
            parts = urlsplit(self.path)
            if parts.path != "/converter":
                return self._fail("nao_encontrado")
            # Everything is checked before the body is read, so a refused request costs nothing.
            if not self._authorized():
                return self._fail("nao_autorizado")
            name = (parse_qs(parts.query).get("nome") or [""])[0]
            extension = extension_of(name)
            if extension not in EXTENSIONS:
                return self._fail("formato_nao_suportado")
            raw_length = self.headers.get("Content-Length")
            if raw_length is None or not raw_length.isdigit():
                return self._fail("tamanho_obrigatorio")
            length = int(raw_length)
            if length == 0:
                return self._fail("arquivo_vazio")
            if length > config.max_upload_bytes:
                return self._fail("arquivo_grande_demais")
            if not gate.acquire(blocking=False):
                return self._fail("ocupado")
            try:
                started = time.monotonic()
                try:
                    data = self.rfile.read(length)
                except (TimeoutError, OSError):
                    return  # the client stalled or left: nobody to answer
                if len(data) != length:
                    return
                if not content_matches(extension, data):
                    markdown, error = None, "conteudo_nao_confere"
                else:
                    markdown, error = run_worker(data, extension, config)
                if error is None and not (markdown or "").strip():
                    error = "sem_texto"
                elapsed = time.monotonic() - started
                log.info(
                    "%s %s %d bytes %.1fs",
                    "ok" if error is None else error,
                    extension,
                    length,
                    elapsed,
                )
                if error:
                    return self._fail(error)
                self._send(
                    200,
                    {
                        "ok": True,
                        "markdown": markdown,
                        "caracteres": len(markdown),
                        "extensao": extension,
                    },
                )
            except Exception:  # never leak internals to the caller
                log.exception("unexpected error")
                if not self.wfile.closed:
                    try:
                        self._fail("interno")
                    except OSError:
                        pass
            finally:
                gate.release()

        def do_PUT(self):
            self._fail("metodo_nao_permitido")

        do_DELETE = do_PATCH = do_PUT

    return Handler


def create_server(config: Config) -> ThreadingHTTPServer:
    gate = threading.BoundedSemaphore(config.max_concurrent)
    server = ThreadingHTTPServer((config.host, config.port), make_handler(config, gate))
    server.daemon_threads = True
    return server
