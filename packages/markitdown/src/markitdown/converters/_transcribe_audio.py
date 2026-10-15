import io
import sys
from typing import Any, BinaryIO
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
        warnings.filterwarnings(
            "ignore",
            category=RuntimeWarning,
            message=".*ffmpeg.*",
            append=True,
        )
        import speech_recognition as sr
        import pydub
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


def transcribe_audio(
    file_stream: BinaryIO,
    *,
    audio_format: str = "wav",
    language: str = "en-US",
    client: Any = None,
) -> str:
    if client is not None:
        # An explicit provider stays selected, including on authentication/network
        # errors. Upload the original encoding with its filename and media type;
        # this path does not need the legacy Google or local decoder dependencies.
        media_type = {"mp3": "audio/mpeg"}.get(audio_format, f"audio/{audio_format}")
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=(f"audio.{audio_format}", file_stream, media_type),
        )
        transcript = transcription.text.strip()
        return "[No speech detected]" if not transcript else transcript

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
        audio_segment = pydub.AudioSegment.from_file(file_stream, format=audio_format)

        audio_source = io.BytesIO()
        audio_segment.export(audio_source, format="wav")
        audio_source.seek(0)
    else:
        raise ValueError(f"Unsupported audio format: {audio_format}")

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_source) as source:
        audio = recognizer.record(source)
        transcript = recognizer.recognize_google(audio, language=language).strip()
        return "[No speech detected]" if transcript == "" else transcript
