import os
import re

from .._stream_info import StreamInfo


def resolve_images_dir(
    save_images: bool | str,
    stream_info: StreamInfo,
    fallback_name: str,
) -> tuple[str, str]:
    """Resolve the images directory and markdown prefix from a ``save_images`` kwarg.

    Parameters
    ----------
    save_images:
        - ``str``  — use this path directly as both the directory and the
                     markdown image prefix.
        - ``True`` — auto-derive ``images_{stem}`` from *stream_info.filename*,
                     falling back to *fallback_name* when no filename is available.
    stream_info:
        Stream metadata; ``stream_info.filename`` is used for auto-naming.
    fallback_name:
        Format-specific fallback stem (e.g. ``"epub"``, ``"pdf"``) used when
        no filename is available and *save_images* is ``True``.

    Returns
    -------
    (actual_images_dir, md_images_prefix)
        The directory to write images into, and the prefix to use in markdown
        ``![alt](prefix/filename)`` references.  The directory is created
        (including any parents) before returning.
    """
    if isinstance(save_images, str):
        actual_images_dir = save_images
        md_images_prefix = save_images
    else:
        file_stem = re.sub(
            r"[^\w\-]", "_", os.path.splitext(stream_info.filename or fallback_name)[0]
        )
        actual_images_dir = f"images_{file_stem}"
        md_images_prefix = f"./images_{file_stem}"

    os.makedirs(actual_images_dir, exist_ok=True)
    return actual_images_dir, md_images_prefix
