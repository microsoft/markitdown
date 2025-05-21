import mimetypes
import os
import re
import sys
import shutil
import traceback
import io
from dataclasses import dataclass
from importlib.metadata import entry_points
from typing import Any, List, Dict, Optional, Union, BinaryIO
from pathlib import Path
from urllib.parse import urlparse
from warnings import warn
import requests
import magika
import charset_normalizer
import codecs

from ._stream_info import StreamInfo
from ._uri_utils import parse_data_uri, file_uri_to_path

from .converters import (
    PlainTextConverter,
    HtmlConverter,
    RssConverter,
    WikipediaConverter,
    YouTubeConverter,
    IpynbConverter,
    BingSerpConverter,
    PdfConverter,
    DocxConverter,
    XlsxConverter,
    XlsConverter,
    PptxConverter,
    ImageConverter,
    AudioConverter,
    OutlookMsgConverter,
    ZipConverter,
    EpubConverter,
    DocumentIntelligenceConverter,
    CsvConverter,
)

from ._base_converter import DocumentConverter, DocumentConverterResult

from ._exceptions import (
    FileConversionException,
    UnsupportedFormatException,
    FailedConversionAttempt,
)


# Lower priority values are tried first.
PRIORITY_SPECIFIC_FILE_FORMAT = (
    0.0  # e.g., .docx, .pdf, .xlsx, Or specific pages, e.g., wikipedia
)
PRIORITY_GENERIC_FILE_FORMAT = (
    10.0  # Near catch-all converters for mimetypes like text/*, etc.
)


_plugins: Union[None, List[Any]] = None  # If None, plugins have not been loaded yet.


def _load_plugins() -> Union[None, List[Any]]:
    """Lazy load plugins, exiting early if already loaded."""
    global _plugins

    # Skip if we've already loaded plugins
    if _plugins is not None:
        return _plugins

    # Load plugins
    _plugins = []
    for entry_point in entry_points(group="markitdown.plugin"):
        try:
            _plugins.append(entry_point.load())
        except Exception:
            tb = traceback.format_exc()
            warn(f"Plugin '{entry_point.name}' failed to load ... skipping:\n{tb}")

    return _plugins


@dataclass(kw_only=True, frozen=True)
class ConverterRegistration:
    """A registration of a converter with its priority and other metadata."""

    converter: DocumentConverter
    priority: float


class MarkItDown:
    """(In preview) An extremely simple text-based document reader, suitable for LLM use.
    This reader will convert common file-types or webpages to Markdown."""

    def __init__(
        self,
        *,
        enable_builtins: Union[None, bool] = None,
        enable_plugins: Union[None, bool] = None,
        **kwargs,
    ):
        self._builtins_enabled = False
        self._plugins_enabled = False

        requests_session = kwargs.get("requests_session")
        if requests_session is None:
            self._requests_session = requests.Session()
        else:
            self._requests_session = requests_session

        self._magika = magika.Magika()

        # TODO - remove these (see enable_builtins)
        self._llm_client: Any = None
        self._llm_model: Union[str | None] = None
        self._exiftool_path: Union[str | None] = None
        self._style_map: Union[str | None] = None

        # Register the converters
        self._converters: List[ConverterRegistration] = []

        if (
            enable_builtins is None or enable_builtins
        ):  # Default to True when not specified
            self.enable_builtins(**kwargs)

        if enable_plugins:
            self.enable_plugins(**kwargs)

    def enable_builtins(self, **kwargs) -> None:
        """
        Enable and register built-in converters.
        Built-in converters are enabled by default.
        This method should only be called once, if built-ins were initially disabled.
        """
        if not self._builtins_enabled:
            # TODO: Move these into converter constructors
            self._llm_client = kwargs.get("llm_client")
            self._llm_model = kwargs.get("llm_model")
            self._exiftool_path = kwargs.get("exiftool_path")
            self._style_map = kwargs.get("style_map")

            if self._exiftool_path is None:
                self._exiftool_path = os.getenv("EXIFTOOL_PATH")

            # Still none? Check well-known paths
            if self._exiftool_path is None:
                candidate = shutil.which("exiftool")
                if candidate:
                    candidate = os.path.abspath(candidate)
                    if any(
                        d == os.path.dirname(candidate)
                        for d in [
                            "/usr/bin",
                            "/usr/local/bin",
                            "/opt",
                            "/opt/bin",
                            "/opt/local/bin",
                            "/opt/homebrew/bin",
                            "C:\\Windows\\System32",
                            "C:\\Program Files",
                            "C:\\Program Files (x86)",
                        ]
                    ):
                        self._exiftool_path = candidate

            # Register converters for successful browsing operations
            # Later registrations are tried first / take higher priority than earlier registrations
            # To this end, the most specific converters should appear below the most generic converters
            self.register_converter(
                PlainTextConverter(), priority=PRIORITY_GENERIC_FILE_FORMAT
            )
            self.register_converter(
                ZipConverter(markitdown=self), priority=PRIORITY_GENERIC_FILE_FORMAT
            )
            self.register_converter(
                HtmlConverter(), priority=PRIORITY_GENERIC_FILE_FORMAT
            )
            self.register_converter(RssConverter())
            self.register_converter(WikipediaConverter())
            self.register_converter(YouTubeConverter())
            self.register_converter(BingSerpConverter())
            self.register_converter(DocxConverter())
            self.register_converter(XlsxConverter())
            self.register_converter(XlsConverter())
            self.register_converter(PptxConverter())
            self.register_converter(AudioConverter())
            self.register_converter(ImageConverter())
            self.register_converter(IpynbConverter())
            self.register_converter(PdfConverter())
            self.register_converter(OutlookMsgConverter())
            self.register_converter(EpubConverter())
            self.register_converter(CsvConverter())

            # Register Document Intelligence converter at the top of the stack if endpoint is provided
            docintel_endpoint = kwargs.get("docintel_endpoint")
            if docintel_endpoint is not None:
                docintel_args: Dict[str, Any] = {}
                docintel_args["endpoint"] = docintel_endpoint

                docintel_credential = kwargs.get("docintel_credential")
                if docintel_credential is not None:
                    docintel_args["credential"] = docintel_credential

                docintel_types = kwargs.get("docintel_file_types")
                if docintel_types is not None:
                    docintel_args["file_types"] = docintel_types

                docintel_version = kwargs.get("docintel_api_version")
                if docintel_version is not None:
                    docintel_args["api_version"] = docintel_version

                self.register_converter(
                    DocumentIntelligenceConverter(**docintel_args),
                )

            self._builtins_enabled = True
        else:
            warn("Built-in converters are already enabled.", RuntimeWarning)

    def enable_plugins(self, **kwargs) -> None:
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
            else:
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
        )

        # Extend the base_guess with any additional info from the arguments
        if stream_info is not None:
            base_guess = base_guess.copy_and_update(stream_info)

        if file_extension is not None:
            # Deprecated -- use stream_info
            base_guess = base_guess.copy_and_update(extension=file_extension)

        if url is not None:
            # Deprecated -- use stream_info
            base_guess = base_guess.copy_and_update(url=url)

        with open(path, "rb") as fh:
            guesses = self._get_stream_info_guesses(
                file_stream=fh, base_guess=base_guess
            )
            return self._convert(file_stream=fh, stream_info_guesses=guesses, **kwargs)

    def convert_stream(
        self,
        stream: BinaryIO,
        *,
        stream_info: Optional[StreamInfo] = None,
        file_extension: Optional[str] = None,  # Deprecated -- use stream_info
        url: Optional[str] = None,  # Deprecated -- use stream_info
        **kwargs: Any,
    ) -> DocumentConverterResult:
        guesses: List[StreamInfo] = []

        # Do we have anything on which to base a guess?
        base_guess = None
        if stream_info is not None or file_extension is not None or url is not None:
            # Start with a non-Null base guess
            if stream_info is None:
                base_guess = StreamInfo()
            else:
                base_guess = stream_info

            if file_extension is not None:
                # Deprecated -- use stream_info
                assert base_guess is not None  # for mypy
                base_guess = base_guess.copy_and_update(extension=file_extension)

            if url is not None:
                # Deprecated -- use stream_info
                assert base_guess is not None  # for mypy
                base_guess = base_guess.copy_and_update(url=url)

        # Check if we have a seekable stream. If not, load the entire stream into memory.
        if not stream.seekable():
            buffer = io.BytesIO()
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    break
                buffer.write(chunk)
            buffer.seek(0)
            stream = buffer

        # Add guesses based on stream content
        guesses = self._get_stream_info_guesses(
            file_stream=stream, base_guess=base_guess or StreamInfo()
        )
        return self._convert(file_stream=stream, stream_info_guesses=guesses, **kwargs)

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
                file_extension=file_extension,
                url=mock_url,
                **kwargs,
            )
        # HTTP/HTTPS URIs
        elif uri.startswith("http:") or uri.startswith("https:"):
            response = self._requests_session.get(uri, stream=True)
            response.raise_for_status()
            return self.convert_response(
                response,
                stream_info=stream_info,
                file_extension=file_extension,
                url=mock_url,
                **kwargs,
            )
        else:
            raise ValueError(
                f"Unsupported URI scheme: {uri.split(':')[0]}. Supported schemes are: file:, data:, http:, https:"
            )

    def convert_response(
        self,
        response: requests.Response,
        *,
        stream_info: Optional[StreamInfo] = None,
        file_extension: Optional[str] = None,  # Deprecated -- use stream_info
        url: Optional[str] = None,  # Deprecated -- use stream_info
        **kwargs: Any,
    ) -> DocumentConverterResult:
        # If there is a content-type header, get the mimetype and charset (if present)
        mimetype: Optional[str] = None
        charset: Optional[str] = None

        if "content-type" in response.headers:
            parts = response.headers["content-type"].split(";")
            mimetype = parts.pop(0).strip()
            for part in parts:
                if part.strip().startswith("charset="):
                    _charset = part.split("=")[1].strip()
                    if len(_charset) > 0:
                        charset = _charset

        # If there is a content-disposition header, get the filename and possibly the extension
        filename: Optional[str] = None
        extension: Optional[str] = None
        if "content-disposition" in response.headers:
            m = re.search(r"filename=([^;]+)", response.headers["content-disposition"])
            if m:
                filename = m.group(1).strip("\"'")
                _, _extension = os.path.splitext(filename)
                if len(_extension) > 0:
                    extension = _extension

        # If there is still no filename, try to read it from the url
        if filename is None:
            parsed_url = urlparse(response.url)
            _, _extension = os.path.splitext(parsed_url.path)
            if len(_extension) > 0:  # Looks like this might be a file!
                filename = os.path.basename(parsed_url.path)
                extension = _extension

        # Create an initial guess from all this information
        base_guess = StreamInfo(
            mimetype=mimetype,
            charset=charset,
            filename=filename,
            extension=extension,
            url=response.url,
        )

        # Update with any additional info from the arguments
        if stream_info is not None:
            base_guess = base_guess.copy_and_update(stream_info)
        if file_extension is not None:
            # Deprecated -- use stream_info
            base_guess = base_guess.copy_and_update(extension=file_extension)
        if url is not None:
            # Deprecated -- use stream_info
            base_guess = base_guess.copy_and_update(url=url)

        # Read into BytesIO
        buffer = io.BytesIO()
        for chunk in response.iter_content(chunk_size=512):
            buffer.write(chunk)
        buffer.seek(0)

        # Convert
        guesses = self._get_stream_info_guesses(
            file_stream=buffer, base_guess=base_guess
        )
        return self._convert(file_stream=buffer, stream_info_guesses=guesses, **kwargs)

    def _convert(
        self, *, file_stream: BinaryIO, stream_info_guesses: List[StreamInfo], **kwargs
    ) -> DocumentConverterResult:
        res: Union[None, DocumentConverterResult] = None

        # Keep track of which converters throw exceptions
        failed_attempts: List[FailedConversionAttempt] = []

        # Create a copy of the page_converters list, sorted by priority.
        # We do this with each call to _convert because the priority of converters may change between calls.
        # The sort is guaranteed to be stable, so converters with the same priority will remain in the same order.
        sorted_registrations = sorted(self._converters, key=lambda x: x.priority)

        # Remember the initial stream position so that we can return to it
        cur_pos = file_stream.tell()

        for stream_info in stream_info_guesses + [StreamInfo()]:
            for converter_registration in sorted_registrations:
                converter = converter_registration.converter
                # Sanity check -- make sure the cur_pos is still the same
                assert (
                    cur_pos == file_stream.tell()
                ), "File stream position should NOT change between guess iterations"

                _kwargs = {k: v for k, v in kwargs.items()}

                # Copy any additional global options
                if "llm_client" not in _kwargs and self._llm_client is not None:
                    _kwargs["llm_client"] = self._llm_client

                if "llm_model" not in _kwargs and self._llm_model is not None:
                    _kwargs["llm_model"] = self._llm_model

                if "style_map" not in _kwargs and self._style_map is not None:
                    _kwargs["style_map"] = self._style_map

                if "exiftool_path" not in _kwargs and self._exiftool_path is not None:
                    _kwargs["exiftool_path"] = self._exiftool_path

                # Add the list of converters for nested processing
                _kwargs["_parent_converters"] = self._converters

                # Add legaxy kwargs
                if stream_info is not None:
                    if stream_info.extension is not None:
                        _kwargs["file_extension"] = stream_info.extension

                    if stream_info.url is not None:
                        _kwargs["url"] = stream_info.url

                # Check if the converter will accept the file, and if so, try to convert it
                _accepts = False
                try:
                    _accepts = converter.accepts(file_stream, stream_info, **_kwargs)
                except NotImplementedError:
                    pass

                # accept() should not have changed the file stream position
                assert (
                    cur_pos == file_stream.tell()
                ), f"{type(converter).__name__}.accept() should NOT change the file_stream position"

                # Attempt the conversion
                if _accepts:
                    try:
                        res = converter.convert(file_stream, stream_info, **_kwargs)
                    except Exception:
                        failed_attempts.append(
                            FailedConversionAttempt(
                                converter=converter, exc_info=sys.exc_info()
                            )
                        )
                    finally:
                        file_stream.seek(cur_pos)

                if res is not None:
                    # Normalize the content
                    res.text_content = "\n".join(
                        [line.rstrip() for line in re.split(r"\r?\n", res.text_content)]
                    )
                    res.text_content = re.sub(r"\n{3,}", "\n\n", res.text_content)
                    return res

        # If we got this far without success, report any exceptions
        if len(failed_attempts) > 0:
            raise FileConversionException(attempts=failed_attempts)

        # Nothing can handle it!
        raise UnsupportedFormatException(
            "Could not convert stream to Markdown. No converter attempted a conversion, suggesting that the filetype is simply not supported."
        )

    def register_page_converter(self, converter: DocumentConverter) -> None:
        """DEPRECATED: User register_converter instead."""
        warn(
            "register_page_converter is deprecated. Use register_converter instead.",
            DeprecationWarning,
        )
        self.register_converter(converter)

    def register_converter(
        self,
        converter: DocumentConverter,
        *,
        priority: float = PRIORITY_SPECIFIC_FILE_FORMAT,
    ) -> None:
        """
        Register a DocumentConverter with a given priority.

        Priorities work as follows: By default, most converters get priority
        DocumentConverter.PRIORITY_SPECIFIC_FILE_FORMAT (== 0). The exception
        is the PlainTextConverter, HtmlConverter, and ZipConverter, which get
        priority PRIORITY_SPECIFIC_FILE_FORMAT (== 10), with lower values
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
                    # The magika guess was incompatible with the base guess, so add both guesses
                    guesses.append(enhanced_guess)
                    guesses.append(
                        StreamInfo(
                            mimetype=result.prediction.output.mime_type,
                            extension=guessed_extension,
                            charset=charset,
                            filename=base_guess.filename,
                            local_path=base_guess.local_path,
                            url=base_guess.url,
                        )
                    )
            else:
                # There were no other guesses, so just add the base guess
                guesses.append(enhanced_guess)
        finally:
            file_stream.seek(cur_pos)

        return guesses

    def _normalize_charset(self, charset: str | None) -> str | None:
        """
        Normalize a charset string to a canonical form.
        """
        if charset is None:
            return None
        try:
            return codecs.lookup(charset).name
        except LookupError:
            return charset
