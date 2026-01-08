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
        import speech_recognition as sr
        import pydub
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()


def transcribe_audio(file_stream: BinaryIO, *, audio_format: str = "wav", engine: str = "google", **engine_kwargs: Any) -> str:
    """
    Transcribe audio to text using various speech recognition engines.
    This function is a wrapper around the SpeechRecognition library: https://github.com/Uberi/speech_recognition
    
    Args:
        file_stream: Binary stream of the audio file
        audio_format: Format of the audio file. Supported:
            - Direct: 'wav', 'aiff', 'flac'
            - Converted: 'mp3', 'mp4'
        engine: Speech recognition engine to use. Supported:
            - 'google': Google Speech Recognition (free, no API key, 1 minute per request, 50 requests per day) (https://pypi.org/project/SpeechRecognition/)
            - 'google_cloud': Google Cloud Speech-to-Text (requires credentials_json) (https://cloud.google.com/speech-to-text/docs)
            - 'wit': Wit.ai (requires key) (https://wit.ai/docs/http/)
            - 'azure': Microsoft Azure (requires key, location) (https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text)
            - 'bing': Microsoft Bing (requires key) (https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text)
            - 'houndify': Houndify (requires client_id, client_key) [(https://www.houndify.com/docs)
            - 'assemblyai': AssemblyAI (requires api_token) https://www.assemblyai.com/docs/)
            - 'ibm': IBM Watson (requires key) (https://cloud.ibm.com/docs/speech-to-text)
            - 'whisper_api': OpenAI Whisper API (requires api_key) (https://platform.openai.com/docs/api-reference/audio)
            - 'sphinx': CMU Sphinx (offline, no API key) (https://cmusphinx.github.io/wiki/)
        **engine_kwargs: Engine-specific parameters:
            - google_cloud: credentials_json (path to JSON file)
            - wit: key (API key)
            - azure: key (API key), location (region), profanity (masked/removed/raw)
            - bing: key (API key), language
            - houndify: client_id, client_key
            - assemblyai: api_token (API token)
            - ibm: key (API key)
            - whisper_api: api_key, model, language, prompt, temperature
    
    Returns:
        Transcribed text or "[No speech detected]" if no speech found
    
    Raises:
        ValueError: Invalid engine or audio format
        MissingDependencyException: Required packages not installed
        sr.RequestError: API request failed
        sr.UnknownValueError: Speech could not be understood
    
    Examples:
        >>> # Google (free)
        >>> with open("audio.mp3", "rb") as f:
        ...     text = transcribe_audio(f, audio_format="mp3", engine="google")
        
        >>> # Whisper API
        >>> with open("audio.wav", "rb") as f:
        ...     text = transcribe_audio(f, audio_format="wav", 
        ...                           engine="whisper_api", 
        ...                           api_key="sk-...")
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
        
        # Validate engine exists
        try:
            recognize_method = getattr(recognizer, f"recognize_{engine}")
        except AttributeError:
            raise ValueError(
                f"Unsupported engine: '{engine}'. "
                f"Supported engines: google, google_cloud, wit, azure, houndify, ibm, whisper_api, sphinx"
            )

        # Perform transcription with engine-specific error handling
        try:
            transcript = recognize_method(audio, **engine_kwargs).strip()
            return "[No speech detected]" if transcript == "" else transcript
        except sr.RequestError as e:
            # API request failed (network, auth, quota, etc.)
            raise ValueError(
                f"Speech recognition request failed for engine '{engine}': {e}. "
                f"Check your API credentials and network connection."
            ) from e
        except sr.UnknownValueError:
            # Speech was unintelligible
            return "[No speech detected]"
