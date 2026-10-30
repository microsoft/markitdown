"""Regression tests: the mp3/mp4 transcription decode must be bounded.

transcribe_audio() used to decode mp3/mp4 through pydub, whose
ffprobe/ffmpeg subprocess calls carry no timeout and no protocol
whitelist: a hanging ffmpeg blocks the conversion indefinitely (and
outlives its caller), and crafted container contents can steer ffmpeg
to network protocols. The decode is now one explicit ffmpeg call:
``-protocol_whitelist file,pipe,cache`` before ``-i cache:pipe:0``
(the cache protocol keeps the pipe seekable for containers with a
trailing index), bounded by a 300 s timeout, failing with
FileConversionException.

The tests drive transcribe_audio() on the test.mp3 / test.wav fixtures
with stub ``ffmpeg`` binaries on PATH (see stub_ffmpeg/ next to this
file). The recognizer's network call is stubbed throughout, following
the precedent in test_image.py. The hang test runs the conversion in
a child process (audio_hardening_driver.py) so that a build without
the timeout can be bounded by the test's own outer timeout instead of
hanging the suite.
"""

import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from markitdown._exceptions import FileConversionException
from markitdown.converters._transcribe_audio import transcribe_audio

pytestmark = pytest.mark.skipif(
    os.name != "posix", reason="stub ffmpeg scripts require a POSIX shell"
)

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")
STUB_DIR = os.path.join(os.path.dirname(__file__), "stub_ffmpeg")
DRIVER = os.path.join(os.path.dirname(__file__), "audio_hardening_driver.py")


@pytest.fixture(autouse=True)
def stub_recognizer(monkeypatch: pytest.MonkeyPatch) -> None:
    sr = pytest.importorskip("speech_recognition")
    monkeypatch.setattr(
        sr.Recognizer,
        "recognize_google",
        lambda self, audio, language=None: "stub transcript",
    )


def load_fixture(name: str) -> bytes:
    path = os.path.join(TEST_FILES_DIR, name)
    if not os.path.exists(path):
        pytest.skip(f"Test file not found: {path}")
    with open(path, "rb") as f:
        return f.read()


def test_hanging_ffmpeg_fails_within_the_bound() -> None:
    """A ffmpeg that never returns must fail the conversion, fast."""
    env = dict(os.environ)
    env["PATH"] = os.path.join(STUB_DIR, "hang") + os.pathsep + env["PATH"]
    env["TRANSCRIBE_TIMEOUT_PATCH"] = "3"
    env["FFMPEG_STUB_LOG"] = os.devnull
    try:
        completed = subprocess.run(
            [sys.executable, DRIVER],
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired:
        # Unpatched path: the conversion never returns. Clean up the
        # leaked stub (it would self-terminate at 45 s), then fail.
        subprocess.run(["pkill", "-f", "sleep 45"], capture_output=True, check=False)
        pytest.fail(
            "conversion was still blocked 30 s after a hanging ffmpeg "
            "started: the decode carries no timeout"
        )

    outcome = json.loads(completed.stdout.strip().splitlines()[-1])
    assert outcome["status"] == "raised", outcome
    assert outcome["exception"] == "FileConversionException", outcome
    assert "timed out" in outcome["message"], outcome
    assert outcome["elapsed_s"] < 15, outcome

    # The killed decode must not leave the stub running behind it.
    # -fx (exact full-command match): the stub execs `sleep 45`, so its
    # command line is exactly that; a substring match could false-positive
    # on an ancestor process whose command line merely mentions the pattern.
    survivors = subprocess.run(
        ["pgrep", "-fx", "sleep 45"], capture_output=True, text=True, check=False
    )
    assert survivors.stdout.strip() == "", "hang stub survived the timeout kill"


def test_ffmpeg_invocation_is_whitelisted_and_pipe_fed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The decode passes -protocol_whitelist before -i, input on a pipe."""
    real_ffmpeg = shutil.which("ffmpeg")
    if real_ffmpeg is None:
        pytest.skip("ffmpeg is not installed")
    log = tmp_path / "argv.log"
    monkeypatch.setenv("FFMPEG_STUB_LOG", str(log))
    monkeypatch.setenv("FFMPEG_REAL", real_ffmpeg)
    monkeypatch.setenv(
        "PATH", os.path.join(STUB_DIR, "log") + os.pathsep + os.environ["PATH"]
    )

    result = transcribe_audio(io.BytesIO(load_fixture("test.mp3")), audio_format="mp3")
    assert result == "stub transcript"

    lines = log.read_text().splitlines()
    ffmpeg_lines = [line for line in lines if line.startswith("ffmpeg ")]
    assert len(ffmpeg_lines) == 1, lines
    argv = ffmpeg_lines[0]
    assert "-protocol_whitelist file,pipe,cache" in argv, argv
    assert argv.index("-protocol_whitelist") < argv.index("-i cache:pipe:0"), argv


def test_failing_ffmpeg_fails_loudly(monkeypatch: pytest.MonkeyPatch) -> None:
    """A decode error raises FileConversionException carrying stderr."""
    monkeypatch.setenv(
        "PATH", os.path.join(STUB_DIR, "fail") + os.pathsep + os.environ["PATH"]
    )
    with pytest.raises(FileConversionException) as excinfo:
        transcribe_audio(io.BytesIO(load_fixture("test.mp3")), audio_format="mp3")
    assert "failed to decode" in str(excinfo.value)
    assert "stub ffmpeg" in str(excinfo.value)


def test_wav_path_needs_no_ffmpeg(monkeypatch: pytest.MonkeyPatch) -> None:
    """Control: wav input still transcribes without touching ffmpeg."""
    monkeypatch.setenv(
        "PATH", os.path.join(STUB_DIR, "fail") + os.pathsep + os.environ["PATH"]
    )
    result = transcribe_audio(io.BytesIO(load_fixture("test.wav")), audio_format="wav")
    assert result == "stub transcript"
