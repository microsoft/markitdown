import copy
import mimetypes
import os
import re
import sys
import tempfile
import warnings
import traceback
import io
from importlib.metadata import entry_points
from typing import Any, List, Optional, Union, BinaryIO
from pathlib import Path
from urllib.parse import urlparse
from warnings import warn

# File-format detection
import puremagic
import requests

from ._stream_info import StreamInfo

from .converters import (
    DocumentConverter,
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
    WavConverter,
    Mp3Converter,
    OutlookMsgConverter,
    ZipConverter,
    DocumentIntelligenceConverter,
)

from ._base_converter import DocumentConverterResult

from ._exceptions import (
    FileConversionException,
    UnsupportedFormatException,
    FailedConversionAttempt,
)

# Override mimetype for csv to fix issue on windows
mimetypes.add_type("text/csv", ".csv")

_plugins: Union[None | List[Any]] = None


def _load_plugins() -> Union[None | List[Any]]:
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

        # TODO - remove these (see enable_builtins)
        self._llm_client = None
        self._llm_model = None
        self._exiftool_path = None
        self._style_map = None

        # Register the converters
        self._page_converters: List[DocumentConverter] = []

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

            # Register converters for successful browsing operations
            # Later registrations are tried first / take higher priority than earlier registrations
            # To this end, the most specific converters should appear below the most generic converters
            self.register_converter(PlainTextConverter())
            self.register_converter(ZipConverter())
            self.register_converter(HtmlConverter())
            self.register_converter(RssConverter())
            self.register_converter(WikipediaConverter())
            self.register_converter(YouTubeConverter())
            self.register_converter(BingSerpConverter())
            self.register_converter(DocxConverter())
            self.register_converter(XlsxConverter())
            self.register_converter(XlsConverter())
            self.register_converter(PptxConverter())
            self.register_converter(WavConverter())
            self.register_converter(Mp3Converter())
            self.register_converter(ImageConverter())
            self.register_converter(IpynbConverter())
            self.register_converter(PdfConverter())
            self.register_converter(OutlookMsgConverter())

            # Register Document Intelligence converter at the top of the stack if endpoint is provided
            docintel_endpoint = kwargs.get("docintel_endpoint")
            if docintel_endpoint is not None:
                self.register_converter(
                    DocumentIntelligenceConverter(endpoint=docintel_endpoint)
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
            for plugin in _load_plugins():
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
                source.startswith("http://")
                or source.startswith("https://")
                or source.startswith("file://")
            ):
                return self.convert_url(source, **kwargs)
            else:
                return self.convert_local(source, stream_info=stream_info, **kwargs)
        # Path object
        elif isinstance(source, Path):
            return self.convert_local(source, stream_info=stream_info, **kwargs)
        # Request response
        elif isinstance(source, requests.Response):
            return self.convert_response(source, **kwargs)
        # Binary stream
        elif (
            hasattr(source, "read")
            and callable(source.read)
            and not isinstance(source, io.TextIOBase)
        ):
            return self.convert_stream(source, **kwargs)
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
        base_stream_info = StreamInfo(
            local_path=path,
            extension=os.path.splitext(path)[1],
            filename=os.path.basename(path),
        )

        # Extend the base_stream_info with any additional info from the arguments
        if stream_info is not None:
            base_stream_info = base_stream_info.copy_and_update(stream_info)

        if file_extension is not None:
            # Deprecated -- use stream_info
            base_stream_info = base_stream_info.copy_and_update(
                extension=file_extension
            )

        if url is not None:
            # Deprecated -- use stream_info
            base_stream_info = base_stream_info.copy_and_update(url=url)

        with open(path, "rb") as fh:
            # Prepare a list of configurations to try, starting with the base_stream_info
            guesses: List[StreamInfo] = [base_stream_info]
            for guess in StreamInfo.guess_from_stream(
                file_stream=fh, filename_hint=path
            ):
                guesses.append(base_stream_info.copy_and_update(guess))
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
            base_guess = stream_info if stream_info is not None else StreamInfo()
            if file_extension is not None:
                # Deprecated -- use stream_info
                base_guess = base_guess.copy_and_update(extension=file_extension)
            if url is not None:
                # Deprecated -- use stream_info
                base_guess = base_guess.copy_and_update(url=url)

        # Append the base guess, if it's non-trivial
        if base_guess is not None:
            if base_guess.mimetype is not None or base_guess.extension is not None:
                guesses.append(base_guess)
        else:
            # Create a base guess with no information
            base_guess = StreamInfo()

        # Create a placeholder filename to help with guessing
        placeholder_filename = None
        if base_guess.filename is not None:
            placeholder_filename = base_guess.filename
        elif base_guess.extension is not None:
            placeholder_filename = "placeholder" + base_guess.extension

        # Add guesses based on stream content
        for guess in StreamInfo.guess_from_stream(
            file_stream=stream, filename_hint=placeholder_filename
        ):
            guesses.append(base_guess.copy_and_update(guess))

        # Perform the conversion
        return self._convert(file_stream=stream, stream_info_guesses=guesses, **kwargs)

    def convert_url(
        self, url: str, **kwargs: Any
    ) -> DocumentConverterResult:  # TODO: fix kwargs type
        # Send a HTTP request to the URL
        response = self._requests_session.get(url, stream=True)
        response.raise_for_status()
        return self.convert_response(response, **kwargs)

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

        # Add the guess if its non-trivial
        guesses: List[StreamInfo] = []
        if base_guess.mimetype is not None or base_guess.extension is not None:
            guesses.append(base_guess)

        # Read into BytesIO
        buffer = io.BytesIO()
        for chunk in response.iter_content(chunk_size=512):
            buffer.write(chunk)
        buffer.seek(0)

        # Create a placeholder filename to help with guessing
        placeholder_filename = None
        if base_guess.filename is not None:
            placeholder_filename = base_guess.filename
        elif base_guess.extension is not None:
            placeholder_filename = "placeholder" + base_guess.extension

        # Add guesses based on stream content
        for guess in StreamInfo.guess_from_stream(
            file_stream=buffer, filename_hint=placeholder_filename
        ):
            guesses.append(base_guess.copy_and_update(guess))

        # Convert
        return self._convert(file_stream=buffer, stream_info_guesses=guesses, **kwargs)

    def _convert(
        self, *, file_stream: BinaryIO, stream_info_guesses: List[StreamInfo], **kwargs
    ) -> DocumentConverterResult:
        # Lazily create a temporary file, if needed, for backward compatibility
        # This is to support a deprecated feature, and will be removed in the future
        temp_file = None

        def get_temp_file():
            nonlocal temp_file

            if temp_file is not None:
                return temp_file
            else:
                cur_pos = file_stream.tell()
                handle, temp_file = tempfile.mkstemp()
                fh = os.fdopen(handle, "wb")
                file_stream.seek(0)
                fh.write(file_stream.read())
                file_stream.seek(cur_pos)
                fh.close()
            return temp_file

        try:
            res: Union[None, DocumentConverterResult] = None

            # Keep track of which converters throw exceptions
            failed_attempts: List[FailedConversionAttempt] = []

            # Create a copy of the page_converters list, sorted by priority.
            # We do this with each call to _convert because the priority of converters may change between calls.
            # The sort is guaranteed to be stable, so converters with the same priority will remain in the same order.
            sorted_converters = sorted(self._page_converters, key=lambda x: x.priority)

            for file_info in stream_info_guesses + [None]:
                for converter in sorted_converters:
                    _kwargs = copy.deepcopy(kwargs)

                    # Copy any additional global options
                    if "llm_client" not in _kwargs and self._llm_client is not None:
                        _kwargs["llm_client"] = self._llm_client

                    if "llm_model" not in _kwargs and self._llm_model is not None:
                        _kwargs["llm_model"] = self._llm_model

                    if "style_map" not in _kwargs and self._style_map is not None:
                        _kwargs["style_map"] = self._style_map

                    if (
                        "exiftool_path" not in _kwargs
                        and self._exiftool_path is not None
                    ):
                        _kwargs["exiftool_path"] = self._exiftool_path

                    # Add the list of converters for nested processing
                    _kwargs["_parent_converters"] = self._page_converters

                    # Add backwards compatibility
                    if isinstance(converter, DocumentConverter):
                        if file_info is not None:
                            # Legacy converters need a file_extension
                            if file_info.extension is not None:
                                _kwargs["file_extension"] = file_info.extension

                            # And benefit from urls, when available
                            if file_info.url is not None:
                                _kwargs["url"] = file_info.url

                        try:
                            res = converter.convert(get_temp_file(), **_kwargs)
                        except Exception:
                            failed_attempts.append(
                                FailedConversionAttempt(
                                    converter=converter, exc_info=sys.exc_info()
                                )
                            )
                    else:
                        raise NotImplementedError("TODO")

                    if res is not None:
                        # Normalize the content
                        res.text_content = "\n".join(
                            [
                                line.rstrip()
                                for line in re.split(r"\r?\n", res.text_content)
                            ]
                        )
                        res.text_content = re.sub(r"\n{3,}", "\n\n", res.text_content)
                        return res

            # If we got this far without success, report any exceptions
            if len(failed_attempts) > 0:
                raise FileConversionException(attempts=failed_attempts)

            # Nothing can handle it!
            raise UnsupportedFormatException(
                f"Could not convert stream to Markdown. No converter attempted a conversion, suggesting that the filetype is simply not supported."
            )

        finally:
            # Clean up the temporary file
            if temp_file is not None:
                try:
                    os.unlink(temp_file)
                except Exception:
                    pass

    def register_page_converter(self, converter: DocumentConverter) -> None:
        """DEPRECATED: User register_converter instead."""
        warn(
            "register_page_converter is deprecated. Use register_converter instead.",
            DeprecationWarning,
        )
        self.register_converter(converter)

    def register_converter(self, converter: DocumentConverter) -> None:
        """Register a page text converter."""
        self._page_converters.insert(0, converter)
