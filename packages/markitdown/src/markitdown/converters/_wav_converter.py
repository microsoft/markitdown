import logging
from typing import Union
from ._base import DocumentConverter, DocumentConverterResult
from ._media_converter import MediaConverter

logger = logging.getLogger(__name__)

# Optional Transcription support
IS_AUDIO_TRANSCRIPTION_CAPABLE = False
IS_WHISPER_CAPABLE = False
try:
    import speech_recognition as sr
    IS_AUDIO_TRANSCRIPTION_CAPABLE = True
except ModuleNotFoundError:
    pass

try:
    from openai import OpenAI
    IS_WHISPER_CAPABLE = True
except ModuleNotFoundError:
    pass


class WavConverter(MediaConverter):
    """
    Converts WAV files to markdown via extraction of metadata (if `exiftool` is installed), 
    and speech transcription (if `speech_recognition` is installed or OpenAI Whisper is configured).
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(self, local_path, **kwargs) -> Union[None, DocumentConverterResult]:
        # Bail if not a WAV
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".wav":
            return None

        md_content = ""

        # Add metadata
        metadata = self._get_metadata(local_path, kwargs.get("exiftool_path"))
        if metadata:
            for f in [
                "Title",
                "Artist",
                "Author",
                "Band",
                "Album",
                "Genre",
                "Track",
                "DateTimeOriginal",
                "CreateDate",
                "Duration",
            ]:
                if f in metadata:
                    md_content += f"{f}: {metadata[f]}\n"

        # Try transcribing with Whisper first if OpenAI client is available
        llm_client = kwargs.get("llm_client")
        if IS_WHISPER_CAPABLE and llm_client is not None :
            try:
                transcript = self._transcribe_with_whisper(local_path, llm_client)
                if transcript:
                    md_content += "\n\n### Audio Transcript (Whisper):\n" + transcript
            except Exception as e:
                md_content += f"\n\n### Audio Transcript:\nError transcribing with Whisper: {str(e)}"
        # Fall back to speech_recognition if Whisper failed or isn't available
        elif IS_AUDIO_TRANSCRIPTION_CAPABLE:
            try:
                transcript = self._transcribe_audio(local_path)
                md_content += "\n\n### Audio Transcript:\n" + (
                    "[No speech detected]" if transcript == "" else transcript
                )
            except Exception:
                md_content += (
                    "\n\n### Audio Transcript:\nError. Could not transcribe this audio."
                )

        return DocumentConverterResult(
            title=None,
            text_content=md_content.strip(),
        )

    def _transcribe_with_whisper(self, local_path: str, client) -> str:
        """Transcribe audio using OpenAI's Whisper model, falling back to speech_recognition if it fails."""
        try:
            with open(local_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                return transcription.text.strip()
        except Exception as e:
            logger.warning(f"Whisper transcription attempt failed: {str(e)}")
            logger.info("Falling back to speech_recognition...")
            return self._transcribe_audio(local_path)

    def _transcribe_audio(self, local_path) -> str:
        recognizer = sr.Recognizer()
        with sr.AudioFile(local_path) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio).strip()
