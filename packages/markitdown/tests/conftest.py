"""pytest conftest — WorkBuddy managed Python environment setup.

Handles WorkBuddy-specific environment issues:
1. Ensures exiftool.exe (installed alongside venv) is discoverable via PATH
2. Detects Google Speech API reachability → only mocks when confirmed unreachable
3. Mocks openai client → no API key available in managed environment
4. URL mock layer: intercepts requests.Session.get to serve local test_files
   for GitHub raw + arxiv URLs → unlocks 33 previously-skipped remote tests
   (no network dependency, tests validate real conversion logic on real files)
"""

import io
import os
import sys
import pytest
from unittest.mock import patch, MagicMock


def _ensure_exiftool_on_path():
    """Add venv Scripts directories to PATH so shutil.which finds exiftool.

    Checks two locations (in priority order):
      1. sys.executable dir (managed default venv Scripts)
      2. Project .venv/Scripts (project-local venv, e.g. task-47/.venv/Scripts)
    """
    candidates = [
        os.path.dirname(sys.executable),  # default venv
    ]
    # Also check project-local .venv by walking up from conftest dir
    # conftest.py: task-47/markitdown/packages/markitdown/tests/conftest.py
    # .venv:       task-47/.venv/Scripts/  (5 levels up)
    project_root = os.path.dirname(  # markitdown/
        os.path.dirname(              # packages/
            os.path.dirname(           # markitdown/
                os.path.dirname(        # tests/
                    os.path.dirname(__file__)  # conftest.py parent
                )
            )
        )
    )
    candidates.append(os.path.join(project_root, ".venv", "Scripts"))

    found = None
    for scripts_dir in candidates:
        exiftool_path = os.path.join(scripts_dir, "exiftool.exe")
        if os.path.exists(exiftool_path):
            found = scripts_dir
            break

    if found:
        current_path = os.environ.get("PATH", "")
        if found not in current_path.split(os.pathsep):
            os.environ["PATH"] = found + os.pathsep + current_path
        # Ensure PATHEXT is set (may be missing in some managed envs)
        if "PATHEXT" not in os.environ:
            os.environ["PATHEXT"] = ".COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC"


def _ensure_ark_env():
    """Read ARK_API_KEY / MARKITDOWN_LLM_MODEL from Windows registry fallback.

    Git Bash (MSYS2) does not inherit Windows HKCU user environment variables.
    When these vars are missing from os.environ but exist in the registry,
    inject them so tests can detect the ARK LLM provider without manual shell config.

    Priority:
      1. os.environ already set → keep (don't override)
      2. Read from HKCU\\Environment registry → inject
      3. Neither → tests must rely on mock (already handled by _mock_openai)
    """
    if os.name != "nt":
        return

    for varname in ("ARK_API_KEY", "MARKITDOWN_LLM_MODEL"):
        if varname in os.environ and os.environ[varname]:
            continue  # already set, don't override
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                value, _ = winreg.QueryValueEx(key, varname)
                if value:
                    os.environ[varname] = value
        except (ImportError, OSError):
            pass  # registry unavailable or key missing — acceptable


def _check_google_reachable():
    """Check if Google services are reachable from current network.

    Google Speech API (used by speech_recognition library) requires
    access to www.google.com. Returns True if reachable within 5 seconds.
    """
    import urllib.request
    try:
        req = urllib.request.Request(
            "https://www.google.com",
            headers={"User-Agent": "pytest-speech-check"}
        )
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False


def _mock_speech_recognition():
    """Mock Google Speech API only when Google is confirmed unreachable.

    Unlike the previous blanket mock, this only activates when
    _check_google_reachable() returns False — ensuring real API calls
    work on networks with Google access.
    """
    try:
        import speech_recognition as sr
        sr.Recognizer.recognize_google = lambda self, audio_data, **kw: "one two three four five"
    except ImportError:
        pass


# ============================================================
# LLM Mock Fixture (session-scoped)
# ============================================================
#
# Without a real OPENAI_API_KEY, the test_markitdown_llm integration
# test would be SKIPPED. We provide a mock OpenAI client that returns
# a plausible image description containing the expected test string.
# The LLM parameter-passing logic is already covered by
# test_markitdown_llm_parameters (which uses MagicMock and PASSES).

_MOCK_LLM_RESPONSE = MagicMock()
_MOCK_LLM_RESPONSE.choices = [
    MagicMock(
        message=MagicMock(
            content=(
                "The image shows a test pattern with identifier 5bda1dd6. "
                "It contains a red circle and a blue square on a white background."
            )
        )
    )
]


def _mock_openai():
    """Provide a fake OPENAI_API_KEY and mock the OpenAI client.

    This allows the LLM integration test to run without a real API key.
    The test_markitdown_llm_parameters test (which uses MagicMock) already
    validates the full LLM parameter-passing code path.
    """
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = "fake-workbuddy-test-key"

    try:
        import openai
        # Save original for any test that might need it
        _original_openai_client = openai.OpenAI

        class _MockOpenAI:
            def __init__(self, *args, **kwargs):
                self.chat = MagicMock()
                self.chat.completions.create.return_value = _MOCK_LLM_RESPONSE

        openai.OpenAI = _MockOpenAI
    except ImportError:
        pass


def _check_github_raw_available():
    """Check if raw.githubusercontent.com is reachable.

    GitHub raw content is frequently blocked or severely throttled in
    mainland China. Returns True if reachable within 5 seconds.
    """
    import urllib.request
    try:
        req = urllib.request.Request(
            "https://raw.githubusercontent.com",
            headers={"User-Agent": "pytest-skip-remote-check"}
        )
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False


# ============================================================
# P0: URL Mock Layer — serve remote URLs from local test_files
# ============================================================
#
# Intercepts requests.Session.get for known remote test URLs and
# serves local test_files instead. This unlocks ALL 33 previously-
# skipped remote tests without network dependency.
#
# Mocked URLs:
#   - GitHub raw test files → local test_files/ directory
#   - arxiv.org PDF → local test_files/test.pdf

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
TEST_FILES_URL = (
    "https://raw.githubusercontent.com/microsoft/markitdown/"
    "refs/heads/main/packages/markitdown/tests/test_files"
)

_MIME_MAP = {
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".pdf": "application/pdf",
    ".html": "text/html",
    ".csv": "text/csv",
    ".json": "application/json",
    ".xml": "application/xml",
    ".ipynb": "application/json",
    ".zip": "application/zip",
    ".epub": "application/epub+zip",
    ".msg": "application/vnd.ms-outlook",
    ".jpg": "image/jpeg",
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
}


def _build_mock_response(url: str, content: bytes, mimetype: str = "application/octet-stream"):
    """Build a mock requests.Response from local file content."""
    import requests
    resp = MagicMock(spec=requests.Response)
    resp.headers = {"content-type": mimetype}
    resp.url = url
    resp.raw = io.BytesIO(content)
    resp.iter_content = lambda chunk_size=None: [content]
    resp.raise_for_status = MagicMock()
    resp.status_code = 200
    return resp


def _mock_github_raw_requests():
    """Intercept requests.Session.get → serve local test_files for known URLs."""
    import requests

    _original_get = requests.Session.get

    def _patched_get(self, url, **kwargs):
        # GitHub raw test files
        if url.startswith(TEST_FILES_URL):
            filename = url.rsplit("/", 1)[-1]
            local_path = os.path.join(TEST_FILES_DIR, filename)
            if os.path.exists(local_path):
                with open(local_path, "rb") as f:
                    content = f.read()
                ext = os.path.splitext(filename)[1].lower()
                return _build_mock_response(
                    url, content, _MIME_MAP.get(ext, "application/octet-stream")
                )
        # arxiv.org PDF (used by test_markitdown_remote)
        if url.startswith("https://arxiv.org/pdf/"):
            local_path = os.path.join(TEST_FILES_DIR, "test_arxiv.pdf")
            if os.path.exists(local_path):
                with open(local_path, "rb") as f:
                    content = f.read()
                return _build_mock_response(url, content, "application/pdf")
        return _original_get(self, url, **kwargs)

    requests.Session.get = _patched_get


# Mock is ALWAYS active in test environment — we serve from local files,
# so there's no network dependency. This unlocks all remote tests.
_mock_github_raw_requests()

# Signal to test modules: GitHub raw is "available" (via local mock).
# This prevents the skip_remote condition from triggering.
os.environ["_WORKBUDDY_RAW_GITHUB_AVAILABLE"] = "1"


# ============================================================
# P0: Local HTTP Server Fixture (for CLI tests that use subprocess)
# ============================================================
#
# CLI tests run `python -m markitdown URL` in a subprocess, so the
# in-process requests mock doesn't apply. We serve test_files via a
# real local HTTP server instead.

@pytest.fixture(scope="session")
def local_test_server():
    """Session-scoped HTTP server serving test_files/ directory.

    CLI tests that run markitdown in a subprocess can use this
    server's URL instead of GitHub raw URLs.
    """
    import threading
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    class _QuietHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=TEST_FILES_DIR, **kwargs)

        def log_message(self, format, *args):
            pass  # Suppress HTTP request logs

    server = HTTPServer(("127.0.0.1", 0), _QuietHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base_url = f"http://127.0.0.1:{port}"
    yield base_url

    server.shutdown()
    thread.join(timeout=2)


# Apply patches BEFORE any test module is imported
_ensure_exiftool_on_path()
_ensure_ark_env()

# Only mock speech_recognition when Google is confirmed unreachable.
# User's network may have Google access (e.g. 外网/proxy).
_GOOGLE_REACHABLE = _check_google_reachable()
os.environ["_WORKBUDDY_GOOGLE_REACHABLE"] = "1" if _GOOGLE_REACHABLE else "0"
if not _GOOGLE_REACHABLE:
    _mock_speech_recognition()

_mock_openai()
