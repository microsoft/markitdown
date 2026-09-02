import os
import sys
import base64
from typing import Any, BinaryIO, List, Optional, Union

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException

# Try loading the optional (but in this case, required) dependency.
# Save reporting of any exceptions for later.
_dependency_exc_info = None
try:
    from twelvelabs import TwelveLabs
    from twelvelabs.types.video_context import VideoContext_Base64String
except ImportError:
    # Preserve the error and stack trace for later
    _dependency_exc_info = sys.exc_info()

    # Define these names for type hinting when the package is not available
    class TwelveLabs:  # type: ignore[no-redef]
        pass

    class VideoContext_Base64String:  # type: ignore[no-redef]
        pass


# Video container formats understood by the Pegasus video-understanding model.
ACCEPTED_MIME_TYPE_PREFIXES = [
    "video/mp4",
    "video/quicktime",
    "video/webm",
    "video/x-matroska",
    "video/x-msvideo",
    "video/x-m4v",
]

ACCEPTED_FILE_EXTENSIONS = [
    ".mp4",
    ".mov",
    ".webm",
    ".mkv",
    ".avi",
    ".m4v",
]

DEFAULT_PROMPT = (
    "Describe this video in detail as Markdown. Summarize what happens, "
    "transcribe any spoken words, and note key visual scenes in order."
)


class TwelveLabsConverter(DocumentConverter):
    """Converts video files to Markdown using the TwelveLabs Pegasus video-understanding model.

    This converter is opt-in: it is only registered when a TwelveLabs API key is
    supplied (via the ``twelvelabs_api_key`` argument to ``MarkItDown`` or the
    ``TWELVELABS_API_KEY`` environment variable). Pegasus reads the actual video
    frames and audio, so the resulting Markdown can capture visual scenes in
    addition to speech, unlike the speech-only built-in ``AudioConverter``.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model_name: str = "pegasus1.5",
        prompt: Optional[str] = None,
        max_tokens: int = 2048,
        file_extensions: Optional[List[str]] = None,
        mime_type_prefixes: Optional[List[str]] = None,
    ):
        """
        Initialize the TwelveLabsConverter.

        Args:
            api_key: TwelveLabs API key. Falls back to the ``TWELVELABS_API_KEY``
                environment variable when not provided.
            model_name: Pegasus model to use (e.g. ``"pegasus1.5"``).
            prompt: Instruction sent to Pegasus describing how to summarize the
                video. Defaults to a general "describe this video as Markdown" prompt.
            max_tokens: Maximum number of tokens Pegasus may generate.
            file_extensions: Override the list of accepted file extensions.
            mime_type_prefixes: Override the list of accepted MIME-type prefixes.
        """
        super().__init__()

        # Raise an error if the dependency is not available. This converter is
        # only instantiated when explicitly requested, so failing here is correct.
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                "TwelveLabsConverter requires the optional dependency [twelvelabs] (or [all]) to be installed. E.g., `pip install markitdown[twelvelabs]`"
            ) from _dependency_exc_info[
                1
            ].with_traceback(  # type: ignore[union-attr]
                _dependency_exc_info[2]
            )

        resolved_key = api_key or os.environ.get("TWELVELABS_API_KEY")
        if not resolved_key:
            raise ValueError(
                "TwelveLabsConverter requires an API key. Pass twelvelabs_api_key=... "
                "or set the TWELVELABS_API_KEY environment variable. "
                "Grab a free key at https://twelvelabs.io."
            )

        self._model_name = model_name
        self._prompt = prompt
        self._max_tokens = max_tokens
        self._file_extensions = (
            file_extensions if file_extensions is not None else ACCEPTED_FILE_EXTENSIONS
        )
        self._mime_type_prefixes = (
            mime_type_prefixes
            if mime_type_prefixes is not None
            else ACCEPTED_MIME_TYPE_PREFIXES
        )
        self._client = TwelveLabs(api_key=resolved_key)

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in self._file_extensions:
            return True

        for prefix in self._mime_type_prefixes:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        prompt = kwargs.get("twelvelabs_prompt") or self._prompt or DEFAULT_PROMPT

        # Read the video bytes and base64-encode them for the analyze request.
        cur_pos = file_stream.tell()
        try:
            base64_video = base64.b64encode(file_stream.read()).decode("ascii")
        finally:
            file_stream.seek(cur_pos)

        response = self._client.analyze(
            model_name=self._model_name,
            video=VideoContext_Base64String(base_64_string=base64_video),
            prompt=prompt,
            max_tokens=self._max_tokens,
        )

        markdown = response.data or ""

        title: Union[str, None] = stream_info.filename
        return DocumentConverterResult(markdown=markdown.strip(), title=title)
