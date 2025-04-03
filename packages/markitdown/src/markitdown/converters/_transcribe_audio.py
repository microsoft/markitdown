import io
import sys
from typing import BinaryIO
from .._exceptions import MissingDependencyException

# Try loading optional (but in this case, required) dependencies
# Save reporting of any exceptions for later
_dependency_exc_info = None
try:
    # Suppress some warnings on library import
    import warnings

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=SyntaxWarning)
        import speech_recognition as sr
        import pydub
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


def transcribe_audio(file_stream: BinaryIO, *, audio_format: str = "wav") -> str:
    # Check for installed dependencies
    if _dependency_exc_info is not None:
        raise MissingDependencyException(
            "Speech transcription requires installing MarkItdown with the [audio-transcription] optional dependencies. E.g., `pip install markitdown[audio-transcription]` or `pip install markitdown[all]`"
        ) from _dependency_exc_info[
            1
        ].with_traceback(  # type: ignore[union-attr]
            _dependency_exc_info[2]
        )

    if audio_format in ["wav", "aiff", "flac"]:
        audio_source = file_stream
    elif audio_format in ["mp3", "mp4"]:
        audio_segment = pydub.AudioSegment.from_file(file_stream, format=audio_format)

        audio_source = io.BytesIO()
        audio_segment.export(audio_source, format="wav")
        audio_source.seek(0)
    else:
        raise ValueError(f"Unsupported audio format: {audio_format}")

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_source) as source:
        audio = recognizer.record(source)
        transcript = recognizer.recognize_google(audio).strip()
        return "[No speech detected]" if transcript == "" else transcript
