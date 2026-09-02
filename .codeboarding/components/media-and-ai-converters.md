---
component_id: 4
component_name: Media & AI Converters
---

# Media & AI Converters

## Component Description

An AI-native component that handles non-textual media. It uses LLMs and transcription services to convert audio and images into descriptive Markdown text.

---

## Key References:

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converters/_audio_converter.py (lines 23-101)
```
class AudioConverter(DocumentConverter):
    """
    Converts audio files to markdown via extraction of metadata (if `exiftool` is installed), and speech transcription (if `speech_recognition` is installed).
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        md_content = ""

        # Add metadata
        metadata = exiftool_metadata(
            file_stream, exiftool_path=kwargs.get("exiftool_path")
        )
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
                # "Duration", -- Wrong values when read from memory
                "NumChannels",
                "SampleRate",
                "AvgBytesPerSec",
                "BitsPerSample",
            ]:
                if f in metadata:
                    md_content += f"{f}: {metadata[f]}\n"

        # Figure out the audio format for transcription
        if stream_info.extension == ".wav" or stream_info.mimetype == "audio/x-wav":
            audio_format = "wav"
        elif stream_info.extension == ".mp3" or stream_info.mimetype == "audio/mpeg":
            audio_format = "mp3"
        elif (
            stream_info.extension in [".mp4", ".m4a"]
            or stream_info.mimetype == "video/mp4"
        ):
            audio_format = "mp4"
        else:
            audio_format = None

        # Transcribe
        if audio_format:
            try:
                transcript = transcribe_audio(file_stream, audio_format=audio_format)
                if transcript:
                    md_content += "\n\n### Audio Transcript:\n" + transcript
            except MissingDependencyException:
                pass

        # Return the result
        return DocumentConverterResult(markdown=md_content.strip())
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converters/_image_converter.py (lines 16-138)
```
class ImageConverter(DocumentConverter):
    """
    Converts images to markdown via extraction of metadata (if `exiftool` is installed), and description via a multimodal LLM (if an llm_client is configured).
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        md_content = ""

        # Add metadata
        metadata = exiftool_metadata(
            file_stream, exiftool_path=kwargs.get("exiftool_path")
        )

        if metadata:
            for f in [
                "ImageSize",
                "Title",
                "Caption",
                "Description",
                "Keywords",
                "Artist",
                "Author",
                "DateTimeOriginal",
                "CreateDate",
                "GPSPosition",
            ]:
                if f in metadata:
                    md_content += f"{f}: {metadata[f]}\n"

        # Try describing the image with GPT
        llm_client = kwargs.get("llm_client")
        llm_model = kwargs.get("llm_model")
        if llm_client is not None and llm_model is not None:
            llm_description = self._get_llm_description(
                file_stream,
                stream_info,
                client=llm_client,
                model=llm_model,
                prompt=kwargs.get("llm_prompt"),
            )

            if llm_description is not None:
                md_content += "\n# Description:\n" + llm_description.strip() + "\n"

        return DocumentConverterResult(
            markdown=md_content,
        )

    def _get_llm_description(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        *,
        client,
        model,
        prompt=None,
    ) -> Union[None, str]:
        if prompt is None or prompt.strip() == "":
            prompt = "Write a detailed caption for this image."

        # Get the content type
        content_type = stream_info.mimetype
        if not content_type:
            content_type, _ = mimetypes.guess_type(
                "_dummy" + (stream_info.extension or "")
            )
        if not content_type:
            content_type = "application/octet-stream"

        # Convert to base64
        cur_pos = file_stream.tell()
        try:
            base64_image = base64.b64encode(file_stream.read()).decode("utf-8")
        except Exception as e:
            return None
        finally:
            file_stream.seek(cur_pos)

        # Prepare the data-uri
        data_uri = f"data:{content_type};base64,{base64_image}"

        # Prepare the OpenAI API request
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_uri,
                        },
                    },
                ],
            }
        ]

        # Call the OpenAI API
        response = client.chat.completions.create(model=model, messages=messages)
        return response.choices[0].message.content
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/converters/_transcribe_audio.py (lines 23-49)
```
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
```


## Source Files:

- `packages/markitdown/src/markitdown/converters/_audio_converter.py`
- `packages/markitdown/src/markitdown/converters/_exiftool.py`
- `packages/markitdown/src/markitdown/converters/_image_converter.py`
- `packages/markitdown/src/markitdown/converters/_transcribe_audio.py`

