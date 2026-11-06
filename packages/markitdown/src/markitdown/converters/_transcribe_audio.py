import io
import shutil
import subprocess
import sys
from typing import BinaryIO
from .._exceptions import FileConversionException, MissingDependencyException

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    # Suppress some warnings on library import
    import warnings

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=SyntaxWarning)
        warnings.filterwarnings(
            "ignore",
            category=RuntimeWarning,
            message=".*ffmpeg.*",
            append=True,
        )
        import speech_recognition as sr
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

# Bounds for decoding untrusted audio with ffmpeg. The decode must not
# block indefinitely on a hostile or broken input, and ffmpeg must not
# open network protocols on the strength of crafted container contents,
# so the input is restricted to local protocols. The stream is fed
# through ffmpeg's cache protocol (as pydub's invocation did): a plain
# pipe is not seekable, so containers whose index sits at the end of
# the file (e.g. mp4/m4a with a trailing moov atom) would decode to
# nothing. cache only spools the pipe to a local temporary file; it
# opens no network protocol.
_FFMPEG_TIMEOUT_SECONDS = 300
_FFMPEG_PROTOCOL_WHITELIST = "file,pipe,cache"


def _decode_audio_to_wav(file_stream: BinaryIO, audio_format: str) -> io.BytesIO:
    """Decode an mp3/mp4 stream to WAV bytes with a bounded ffmpeg call.

    Replaces pydub's decode, whose subprocess calls carry neither a
    timeout nor a protocol whitelist. Raises FileConversionException on
    timeout or decode failure, so a bad input fails the conversion
    instead of hanging it.
    """
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise MissingDependencyException(
            "Speech transcription of mp3/mp4 audio requires the `ffmpeg` "
            "executable, which was not found on PATH."
        )

    command = [
        ffmpeg,
        "-y",  # always overwrite existing files
        "-protocol_whitelist",
        _FFMPEG_PROTOCOL_WHITELIST,
        "-f",
        audio_format,
        "-i",
        "cache:pipe:0",
        "-vn",  # Drop any video streams if there are any
        "-f",
        "wav",
        "pipe:1",
    ]
    try:
        completed = subprocess.run(
            command,
            input=file_stream.read(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=_FFMPEG_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise FileConversionException(
            f"ffmpeg timed out after {_FFMPEG_TIMEOUT_SECONDS} seconds "
            f"while decoding {audio_format} audio; the conversion was "
            "aborted instead of blocking indefinitely."
        ) from exc

    if completed.returncode != 0 or len(completed.stdout) == 0:
        stderr_tail = completed.stderr.decode(errors="ignore").strip()[-500:]
        raise FileConversionException(
            f"ffmpeg failed to decode {audio_format} audio "
            f"(exit code {completed.returncode}):\n{stderr_tail}"
        )

    return io.BytesIO(completed.stdout)


def transcribe_audio(
    file_stream: BinaryIO, *, audio_format: str = "wav", language: str = "en-US"
) -> str:
    # Check for installed dependencies
    if _dependency_exc_info is not None:
        raise MissingDependencyException(
            "Speech transcription requires installing MarkItDown with the "
            "[audio-transcription] optional dependencies. E.g., "
            "`pip install 'markitdown[audio-transcription]'` or "
            "`pip install 'markitdown[all]'`"
        ) from _dependency_exc_info[
            1
        ].with_traceback(  # type: ignore[union-attr]
            _dependency_exc_info[2]
        )

    if audio_format in ["wav", "aiff", "flac"]:
        audio_source = file_stream
    elif audio_format in ["mp3", "mp4"]:
        audio_source = _decode_audio_to_wav(file_stream, audio_format)
    else:
        raise ValueError(f"Unsupported audio format: {audio_format}")

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_source) as source:
        audio = recognizer.record(source)
        transcript = recognizer.recognize_google(audio, language=language).strip()
        return "[No speech detected]" if transcript == "" else transcript
