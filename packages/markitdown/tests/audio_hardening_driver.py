"""Child-process driver for the audio-hardening hang regression test.

Runs markitdown's transcribe_audio() on test_files/test.mp3 with the
recognizer stubbed, and prints one JSON line describing the outcome.
Run as a subprocess so that a build without the timeout can be
bounded by the test's own outer timeout instead of hanging the suite.

Env:
  TRANSCRIBE_TIMEOUT_PATCH -- if set, monkeypatch the module's
  _FFMPEG_TIMEOUT_SECONDS constant to this value. On a build without
  the constant, the driver notes it on stderr and runs unpatched, so
  the test's outer bound is what fires.
"""

import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "test_files", "test.mp3")


def main() -> int:
    import speech_recognition as sr

    sr.Recognizer.recognize_google = (
        lambda self, audio, language=None: "stub transcript"
    )

    from markitdown.converters import _transcribe_audio as ta

    timeout_patch = os.environ.get("TRANSCRIBE_TIMEOUT_PATCH")
    if timeout_patch:
        if hasattr(ta, "_FFMPEG_TIMEOUT_SECONDS"):
            ta._FFMPEG_TIMEOUT_SECONDS = float(timeout_patch)
        else:
            print(
                "note: no _FFMPEG_TIMEOUT_SECONDS; running unpatched",
                file=sys.stderr,
            )

    with open(FIXTURE, "rb") as f:
        data = f.read()

    start = time.monotonic()
    try:
        result = ta.transcribe_audio(io.BytesIO(data), audio_format="mp3")
        outcome = {"status": "returned", "result": result}
    except Exception as exc:  # noqa: BLE001 - report whatever the path raises
        outcome = {
            "status": "raised",
            "exception": type(exc).__name__,
            "message": str(exc),
        }
    outcome["elapsed_s"] = round(time.monotonic() - start, 2)
    print(json.dumps(outcome))
    return 0


if __name__ == "__main__":
    sys.exit(main())
