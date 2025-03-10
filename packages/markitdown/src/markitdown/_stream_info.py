import mimetypes
import os
from dataclasses import dataclass, asdict
from typing import Optional, BinaryIO, List, TypeVar, Type
from magika import Magika

magika = Magika()


@dataclass(kw_only=True, frozen=True)
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


# Behavior subject to change.
# Do not rely on this outside of this module.
def _guess_stream_info_from_stream(
    file_stream: BinaryIO,
    *,
    filename_hint: Optional[str] = None,
) -> List[StreamInfo]:
    """
    Guess StreamInfo properties (mostly mimetype and extension) from a stream.

    Args:
    - stream: The stream to guess the StreamInfo from.
    - filename_hint [Optional]: A filename hint to help with the guessing (may be a placeholder, and not actually be the file name)

    Returns a list of StreamInfo objects in order of confidence.
    """
    guesses: List[StreamInfo] = []

    # Call magika to guess from the stream
    cur_pos = file_stream.tell()
    try:
        result = magika.identify_bytes(file_stream.read())
        if result.status == "ok" and result.prediction.output.label != "unknown":
            extension = None
            if len(result.prediction.output.extensions) > 0:
                extension = result.prediction.output.extensions[0]
            if extension and not extension.startswith("."):
                extension = "." + extension
            guesses.append(
                StreamInfo(
                    mimetype=result.prediction.output.mime_type,
                    extension=extension,
                )
            )
    finally:
        file_stream.seek(cur_pos)

    # Add a guess purely based on the filename hint
    if filename_hint:
        try:
            # Requires Python 3.13+
            mimetype, _ = mimetypes.guess_file_type(filename_hint)  # type: ignore
        except AttributeError:
            mimetype, _ = mimetypes.guess_type(filename_hint)

        if mimetype:
            guesses.append(
                StreamInfo(
                    mimetype=mimetype, extension=os.path.splitext(filename_hint)[1]
                )
            )

    return guesses
