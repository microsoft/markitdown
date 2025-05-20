import io
import sys
from typing import BinaryIO, Optional
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

# Check for OpenAI Whisper support
IS_WHISPER_CAPABLE = False
try:
    from openai import OpenAI
    IS_WHISPER_CAPABLE = True
except ImportError:
    pass


def transcribe_audio(file_stream: BinaryIO, *, audio_format: str = "wav", client: Optional[object] = None) -> str:
    """
    Transcribe audio using OpenAI Whisper if available and client is provided,
    falling back to Google Speech Recognition otherwise.
    
    Args:
        file_stream: Binary stream containing audio data
        audio_format: Format of the audio (wav, mp3, mp4, etc.)
        client: Optional OpenAI client for Whisper transcription
        
    Returns:
        Transcribed text from the audio
    """
    # Check for installed dependencies
    if _dependency_exc_info is not None:
        raise MissingDependencyException(
            "Speech transcription requires installing MarkItdown with the [audio-transcription] optional dependencies. E.g., `pip install markitdown[audio-transcription]` or `pip install markitdown[all]`"
        ) from _dependency_exc_info[
            1
        ].with_traceback(  # type: ignore[union-attr]
            _dependency_exc_info[2]
        )

    # Convert to WAV if needed
    if audio_format in ["wav", "aiff", "flac"]:
        audio_source = file_stream
    elif audio_format in ["mp3", "mp4"]:
        audio_segment = pydub.AudioSegment.from_file(file_stream, format=audio_format)

        audio_source = io.BytesIO()
        audio_segment.export(audio_source, format="wav")
        audio_source.seek(0)
    else:
        raise ValueError(f"Unsupported audio format: {audio_format}")
    
    # Try Whisper if client is provided and whisper is available
    if IS_WHISPER_CAPABLE and client is not None:
        try:
            # Make a copy since we might need to use it for fallback
            whisper_source = io.BytesIO()
            audio_source.seek(0)
            whisper_source.write(audio_source.read())
            whisper_source.seek(0)
            audio_source.seek(0)
            
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=whisper_source
            )
            transcript = transcription.text.strip()
            return "[No speech detected]" if transcript == "" else transcript
        except Exception as e:
            # Log the error and fall back to Google Speech Recognition
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Whisper transcription attempt failed: {str(e)}")
            logger.info("Falling back to speech_recognition...")
            # Continue to Google Speech Recognition fallback
    
    # Fall back to Google Speech Recognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_source) as source:
        audio = recognizer.record(source)
        transcript = recognizer.recognize_google(audio).strip()
        return "[No speech detected]" if transcript == "" else transcript
