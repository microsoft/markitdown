---
component_id: 1.2
component_name: Format Detection & Metadata
---

# Format Detection & Metadata

## Component Description

Provides the intelligence layer for identifying the content type and encoding of the input stream. It combines fast heuristics (file extensions, MIME types) with deep inspection (via Magika) to produce a prioritized list of format "guesses" used to select the appropriate converter.

---

## Key References:

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/_markitdown.py (lines 654-753)
```
        being tried first (i.e., higher priority).

        Just prior to conversion, the converters are sorted by priority, using
        a stable sort. This means that converters with the same priority will
        remain in the same order, with the most recently registered converters
        appearing first.

        We have tight control over the order of built-in converters, but
        plugins can register converters in any order. The registration's priority
        field reasserts some control over the order of converters.

        Plugins can register converters with any priority, to appear before or
        after the built-ins. For example, a plugin with priority 9 will run
        before the PlainTextConverter, but after the built-in converters.
        """
        self._converters.insert(
            0, ConverterRegistration(converter=converter, priority=priority)
        )

    def _get_stream_info_guesses(
        self, file_stream: BinaryIO, base_guess: StreamInfo
    ) -> List[StreamInfo]:
        """
        Given a base guess, attempt to guess or expand on the stream info using the stream content (via magika).
        """
        guesses: List[StreamInfo] = []

        # Enhance the base guess with information based on the extension or mimetype
        enhanced_guess = base_guess.copy_and_update()

        # If there's an extension and no mimetype, try to guess the mimetype
        if base_guess.mimetype is None and base_guess.extension is not None:
            _m, _ = mimetypes.guess_type(
                "placeholder" + base_guess.extension, strict=False
            )
            if _m is not None:
                enhanced_guess = enhanced_guess.copy_and_update(mimetype=_m)

        # If there's a mimetype and no extension, try to guess the extension
        if base_guess.mimetype is not None and base_guess.extension is None:
            _e = mimetypes.guess_all_extensions(base_guess.mimetype, strict=False)
            if len(_e) > 0:
                enhanced_guess = enhanced_guess.copy_and_update(extension=_e[0])

        # Call magika to guess from the stream
        cur_pos = file_stream.tell()
        try:
            result = self._magika.identify_stream(file_stream)
            if result.status == "ok" and result.prediction.output.label != "unknown":
                # If it's text, also guess the charset
                charset = None
                if result.prediction.output.is_text:
                    # Read the first 4k to guess the charset
                    file_stream.seek(cur_pos)
                    stream_page = file_stream.read(4096)
                    charset_result = charset_normalizer.from_bytes(stream_page).best()

                    if charset_result is not None:
                        charset = self._normalize_charset(charset_result.encoding)

                # Normalize the first extension listed
                guessed_extension = None
                if len(result.prediction.output.extensions) > 0:
                    guessed_extension = "." + result.prediction.output.extensions[0]

                # Determine if the guess is compatible with the base guess
                compatible = True
                if (
                    base_guess.mimetype is not None
                    and base_guess.mimetype != result.prediction.output.mime_type
                ):
                    compatible = False

                if (
                    base_guess.extension is not None
                    and base_guess.extension.lstrip(".")
                    not in result.prediction.output.extensions
                ):
                    compatible = False

                if (
                    base_guess.charset is not None
                    and self._normalize_charset(base_guess.charset) != charset
                ):
                    compatible = False

                if compatible:
                    # Add the compatible base guess
                    guesses.append(
                        StreamInfo(
                            mimetype=base_guess.mimetype
                            or result.prediction.output.mime_type,
                            extension=base_guess.extension or guessed_extension,
                            charset=base_guess.charset or charset,
                            filename=base_guess.filename,
                            local_path=base_guess.local_path,
                            url=base_guess.url,
                        )
                    )
                else:
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/_stream_info.py (lines 6-32)
```
class StreamInfo:
    """The StreamInfo class is used to store information about a file stream.
    All fields can be None, and will depend on how the stream was opened.
    """

    mimetype: Optional[str] = None
    extension: Optional[str] = None
    charset: Optional[str] = None
    filename: Optional[
        str
    ] = None  # From local path, url, or Content-Disposition header
    local_path: Optional[str] = None  # If read from disk
    url: Optional[str] = None  # If read from url

    def copy_and_update(self, *args, **kwargs):
        """Copy the StreamInfo object and update it with the given StreamInfo
        instance and/or other keyword arguments."""
        new_info = asdict(self)

        for si in args:
            assert isinstance(si, StreamInfo)
            new_info.update({k: v for k, v in asdict(si).items() if v is not None})

        if len(kwargs) > 0:
            new_info.update(kwargs)

        return StreamInfo(**new_info)
```


## Source Files:

- `packages/markitdown/src/markitdown/converters/_docx_converter.py`
- `packages/markitdown/src/markitdown/converters/_epub_converter.py`
- `packages/markitdown/src/markitdown/converters/_html_converter.py`
- `packages/markitdown/src/markitdown/converters/_image_converter.py`
- `packages/markitdown/src/markitdown/converters/_ipynb_converter.py`
- `packages/markitdown/src/markitdown/converters/_outlook_msg_converter.py`
- `packages/markitdown/src/markitdown/converters/_pdf_converter.py`
- `packages/markitdown/src/markitdown/converters/_plain_text_converter.py`

