import os
import tempfile
from typing import Union
from ._base import DocumentConverter, DocumentConverterResult
from ._wav_converter import WavConverter, IS_WHISPER_CAPABLE
from warnings import resetwarnings, catch_warnings

# Optional Transcription support
IS_AUDIO_TRANSCRIPTION_CAPABLE = False
try:
    # Using warnings' catch_warnings to catch
    # pydub's warning of ffmpeg or avconv missing
    with catch_warnings(record=True) as w:
        import pydub

        if w:
            raise ModuleNotFoundError
    import speech_recognition as sr

    IS_AUDIO_TRANSCRIPTION_CAPABLE = True
except ModuleNotFoundError:
    pass
finally:
    resetwarnings()


class Mp3Converter(WavConverter):
    """
    Converts MP3 files to markdown via extraction of metadata (if `exiftool` is installed), 
    and speech transcription (if `speech_recognition` AND `pydub` are installed, or OpenAI Whisper is configured).
    """

    def __init__(
        self, priority: float = DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT
    ):
        super().__init__(priority=priority)

    def convert(self, local_path, **kwargs) -> Union[None, DocumentConverterResult]:
        # Bail if not a MP3
        extension = kwargs.get("file_extension", "")
        if extension.lower() != ".mp3":
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
        if IS_WHISPER_CAPABLE and llm_client is not None:
            try:
                transcript = self._transcribe_with_whisper(local_path, llm_client)
                if transcript:
                    md_content += "\n\n### Audio Transcript (Whisper):\n" + transcript
            except Exception as e:
                md_content += f"\n\n### Audio Transcript:\nError transcribing with Whisper: {str(e)}"
        # Fall back to speech_recognition if Whisper failed or isn't available
        elif IS_AUDIO_TRANSCRIPTION_CAPABLE:
            handle, temp_path = tempfile.mkstemp(suffix=".wav")
            os.close(handle)
            try:
                sound = pydub.AudioSegment.from_mp3(local_path)
                sound.export(temp_path, format="wav")
                
                _args = dict()
                _args.update(kwargs)
                _args["file_extension"] = ".wav"
                
                try:
                    transcript = super()._transcribe_audio(temp_path).strip()
                    md_content += "\n\n### Audio Transcript:\n" + (
                        "[No speech detected]" if transcript == "" else transcript
                    )
                except Exception:
                    md_content += "\n\n### Audio Transcript:\nError. Could not transcribe this audio."
            finally:
                os.unlink(temp_path)

        return DocumentConverterResult(
            title=None,
            text_content=md_content.strip(),
        )

