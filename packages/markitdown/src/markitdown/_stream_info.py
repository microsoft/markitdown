from dataclasses import asdict, dataclass


@dataclass(kw_only=True, frozen=True)
class StreamInfo:
    """The StreamInfo class is used to store information about a file stream.
    All fields can be None, and will depend on how the stream was opened.
    """

    mimetype: str | None = None
    extension: str | None = None
    charset: str | None = None
    filename: str | None = None  # From local path, url, or Content-Disposition header
    local_path: str | None = None  # If read from disk
    url: str | None = None  # If read from url

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
