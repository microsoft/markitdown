---
component_id: 1.1
component_name: Input Normalization & Dispatching
---

# Input Normalization & Dispatching

## Component Description

Acts as the primary entry point for the library, responsible for resolving various input types (local paths, URLs, binary streams) into a standardized, seekable binary stream and initial metadata. It handles URI parsing and extracts hints from sources like HTTP headers.

---

## Key References:

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/_markitdown.py (lines 233-281)
```
        """
        Enable and register converters provided by plugins.
        Plugins are disabled by default.
        This method should only be called once, if plugins were initially disabled.
        """
        if not self._plugins_enabled:
            # Load plugins
            plugins = _load_plugins()
            assert plugins is not None
            for plugin in plugins:
                try:
                    plugin.register_converters(self, **kwargs)
                except Exception:
                    tb = traceback.format_exc()
                    warn(f"Plugin '{plugin}' failed to register converters:\n{tb}")
            self._plugins_enabled = True
        else:
            warn("Plugins converters are already enabled.", RuntimeWarning)

    def convert(
        self,
        source: Union[str, requests.Response, Path, BinaryIO],
        *,
        stream_info: Optional[StreamInfo] = None,
        **kwargs: Any,
    ) -> DocumentConverterResult:  # TODO: deal with kwargs
        """
        Args:
            - source: can be a path (str or Path), url, or a requests.response object
            - stream_info: optional stream info to use for the conversion. If None, infer from source
            - kwargs: additional arguments to pass to the converter
        """

        # Local path or url
        if isinstance(source, str):
            if (
                source.startswith("http:")
                or source.startswith("https:")
                or source.startswith("file:")
                or source.startswith("data:")
            ):
                # Rename the url argument to mock_url
                # (Deprecated -- use stream_info)
                _kwargs = {k: v for k, v in kwargs.items()}
                if "url" in _kwargs:
                    _kwargs["mock_url"] = _kwargs["url"]
                    del _kwargs["url"]

                return self.convert_uri(source, stream_info=stream_info, **_kwargs)
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/_markitdown.py (lines 386-445)
```
    def convert_url(
        self,
        url: str,
        *,
        stream_info: Optional[StreamInfo] = None,
        file_extension: Optional[str] = None,
        mock_url: Optional[str] = None,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        """Alias for convert_uri()"""
        # convert_url will likely be deprecated in the future in favor of convert_uri
        return self.convert_uri(
            url,
            stream_info=stream_info,
            file_extension=file_extension,
            mock_url=mock_url,
            **kwargs,
        )

    def convert_uri(
        self,
        uri: str,
        *,
        stream_info: Optional[StreamInfo] = None,
        file_extension: Optional[str] = None,  # Deprecated -- use stream_info
        mock_url: Optional[
            str
        ] = None,  # Mock the request as if it came from a different URL
        **kwargs: Any,
    ) -> DocumentConverterResult:
        uri = uri.strip()

        # File URIs
        if uri.startswith("file:"):
            netloc, path = file_uri_to_path(uri)
            if netloc and netloc != "localhost":
                raise ValueError(
                    f"Unsupported file URI: {uri}. Netloc must be empty or localhost."
                )
            return self.convert_local(
                path,
                stream_info=stream_info,
                file_extension=file_extension,
                url=mock_url,
                **kwargs,
            )
        # Data URIs
        elif uri.startswith("data:"):
            mimetype, attributes, data = parse_data_uri(uri)

            base_guess = StreamInfo(
                mimetype=mimetype,
                charset=attributes.get("charset"),
            )
            if stream_info is not None:
                base_guess = base_guess.copy_and_update(stream_info)

            return self.convert_stream(
                io.BytesIO(data),
                stream_info=base_guess,
```

### /Users/imilev/StartUp/repos/markitdown/packages/markitdown/src/markitdown/_markitdown.py (lines 283-318)
```
                return self.convert_local(source, stream_info=stream_info, **kwargs)
        # Path object
        elif isinstance(source, Path):
            return self.convert_local(source, stream_info=stream_info, **kwargs)
        # Request response
        elif isinstance(source, requests.Response):
            return self.convert_response(source, stream_info=stream_info, **kwargs)
        # Binary stream
        elif (
            hasattr(source, "read")
            and callable(source.read)
            and not isinstance(source, io.TextIOBase)
        ):
            return self.convert_stream(source, stream_info=stream_info, **kwargs)
        else:
            raise TypeError(
                f"Invalid source type: {type(source)}. Expected str, requests.Response, BinaryIO."
            )

    def convert_local(
        self,
        path: Union[str, Path],
        *,
        stream_info: Optional[StreamInfo] = None,
        file_extension: Optional[str] = None,  # Deprecated -- use stream_info
        url: Optional[str] = None,  # Deprecated -- use stream_info
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if isinstance(path, Path):
            path = str(path)

        # Build a base StreamInfo object from which to start guesses
        base_guess = StreamInfo(
            local_path=path,
            extension=os.path.splitext(path)[1],
            filename=os.path.basename(path),
```


## Source Files:

- `packages/markitdown/src/markitdown/_base_converter.py`
- `packages/markitdown/src/markitdown/_exceptions.py`
- `packages/markitdown/src/markitdown/_markitdown.py`

