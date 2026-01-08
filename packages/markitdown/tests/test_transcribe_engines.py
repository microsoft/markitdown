#!/usr/bin/env python3 -m pytest
import os
import pytest
from markitdown.converters._transcribe_audio import transcribe_audio

# This file contains tests for multi-engine speech recognition functionality.
# Tests are skipped in CI and require audio test files and optional API keys.

skip_transcription = (
    True if os.environ.get("GITHUB_ACTIONS") else False
)  # Don't run these tests in CI

TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), "test_files")

# Test audio files with expected content
AUDIO_TEST_FILES = [
    ("test.wav", "wav"),
    ("test.mp3", "mp3"),
    ("test.m4a", "mp4"),  # M4A uses MP4 container format
]


def get_audio_file(filename: str) -> str:
    """Get full path to test audio file."""
    return os.path.join(TEST_FILES_DIR, filename)


@pytest.mark.skipif(skip_transcription, reason="do not run speech transcription tests in CI")
class TestEngineGoogle:
    """Tests for Google Speech Recognition (free, no API key)."""
    
    @pytest.mark.parametrize("filename,format", AUDIO_TEST_FILES)
    def test_google_basic(self, filename: str, format: str) -> None:
        """Test basic Google engine transcription."""
        audio_path = get_audio_file(filename)
        
        if not os.path.exists(audio_path):
            pytest.skip(f"Test file not found: {filename}")
        
        with open(audio_path, "rb") as f:
            result = transcribe_audio(
                f,
                audio_format=format,
                engine="google"
            )
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Note: Result may be "[No speech detected]" for test files without speech


@pytest.mark.skipif(skip_transcription, reason="do not run speech transcription tests in CI")
@pytest.mark.skipif(
    not os.environ.get("GOOGLE_CLOUD_SPEECH_CREDENTIALS"),
    reason="do not run without GOOGLE_CLOUD_SPEECH_CREDENTIALS"
)
class TestEngineGoogleCloud:
    """Tests for Google Cloud Speech-to-Text."""
    
    def test_google_cloud_basic(self) -> None:
        """Test Google Cloud Speech-to-Text."""
        credentials_json = os.environ.get("GOOGLE_CLOUD_SPEECH_CREDENTIALS")
        audio_path = get_audio_file("test.wav")
        
        if not os.path.exists(audio_path):
            pytest.skip("test.wav not found")
        
        with open(audio_path, "rb") as f:
            result = transcribe_audio(
                f,
                audio_format="wav",
                engine="google_cloud",
                credentials_json=credentials_json
            )
        
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.skipif(skip_transcription, reason="do not run speech transcription tests in CI")
@pytest.mark.skipif(
    not os.environ.get("WIT_AI_KEY"),
    reason="do not run without WIT_AI_KEY"
)
class TestEngineWit:
    """Tests for Wit.ai Speech Recognition."""
    
    def test_wit_basic(self) -> None:
        """Test Wit.ai transcription."""
        wit_key = os.environ.get("WIT_AI_KEY")
        audio_path = get_audio_file("test.wav")
        
        if not os.path.exists(audio_path):
            pytest.skip("test.wav not found")
        
        with open(audio_path, "rb") as f:
            result = transcribe_audio(
                f,
                audio_format="wav",
                engine="wit",
                key=wit_key
            )
        
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.skipif(skip_transcription, reason="do not run speech transcription tests in CI")
@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="do not run without OPENAI_API_KEY"
)
class TestEngineWhisperAPI:
    """Tests for OpenAI Whisper API."""
    
    def test_whisper_api_basic(self) -> None:
        """Test Whisper API transcription."""
        openai_key = os.environ.get("OPENAI_API_KEY")
        audio_path = get_audio_file("test.wav")
        
        if not os.path.exists(audio_path):
            pytest.skip("test.wav not found")
        
        with open(audio_path, "rb") as f:
            result = transcribe_audio(
                f,
                audio_format="wav",
                engine="whisper_api",
                api_key=openai_key
            )
        
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.skipif(skip_transcription, reason="do not run speech transcription tests in CI")
class TestEngineSphinx:
    """Tests for CMU Sphinx (offline)."""
    
    def test_sphinx_basic(self) -> None:
        """Test Sphinx offline transcription."""
        audio_path = get_audio_file("test.wav")
        
        if not os.path.exists(audio_path):
            pytest.skip("test.wav not found")
        
        try:
            with open(audio_path, "rb") as f:
                result = transcribe_audio(
                    f,
                    audio_format="wav",
                    engine="sphinx"
                )
            
            assert isinstance(result, str)
        except Exception as e:
            # Sphinx requires additional installation
            if "pocketsphinx" in str(e).lower():
                pytest.skip("PocketSphinx not installed")
            raise


@pytest.mark.skipif(skip_transcription, reason="do not run speech transcription tests in CI")
class TestEngineErrors:
    """Tests for error handling."""
    
    def test_invalid_engine(self) -> None:
        """Test that invalid engine raises ValueError."""
        audio_path = get_audio_file("test.wav")
        
        if not os.path.exists(audio_path):
            pytest.skip("test.wav not found")
        
        with pytest.raises(ValueError, match="Unsupported engine"):
            with open(audio_path, "rb") as f:
                transcribe_audio(
                    f,
                    audio_format="wav",
                    engine="invalid_engine"
                )
    
    def test_invalid_audio_format(self) -> None:
        """Test that invalid audio format raises ValueError."""
        audio_path = get_audio_file("test.wav")
        
        if not os.path.exists(audio_path):
            pytest.skip("test.wav not found")
        
        with pytest.raises(ValueError, match="Unsupported audio format"):
            with open(audio_path, "rb") as f:
                transcribe_audio(
                    f,
                    audio_format="invalid_format",
                    engine="google"
                )


@pytest.mark.skipif(skip_transcription, reason="do not run speech transcription tests in CI")
class TestAudioFormats:
    """Tests for different audio formats."""
    
    @pytest.mark.parametrize("filename,format", AUDIO_TEST_FILES)
    def test_supported_formats(self, filename: str, format: str) -> None:
        """Test that different audio formats work."""
        audio_path = get_audio_file(filename)
        
        if not os.path.exists(audio_path):
            pytest.skip(f"Test file not found: {filename}")
        
        # Just test that the format is accepted without errors
        with open(audio_path, "rb") as f:
            result = transcribe_audio(
                f,
                audio_format=format,
                engine="google"
            )
        
        assert isinstance(result, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
