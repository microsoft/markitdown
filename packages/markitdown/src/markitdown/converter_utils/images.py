import os
import re

from .._stream_info import StreamInfo


def resolve_images_dir(
    save_images: bool | str,
    stream_info: StreamInfo,
    fallback_name: str,
) -> tuple[str, str]:
    """Resolve the image output directory and Markdown path prefix."""
    if isinstance(save_images, str):
        actual_images_dir = save_images
        md_images_prefix = save_images
    else:
        file_stem = re.sub(
            r"[^\w\-]",
            "_",
            os.path.splitext(stream_info.filename or fallback_name)[0],
        )
        actual_images_dir = f"images_{file_stem}"
        md_images_prefix = f"./images_{file_stem}"

    os.makedirs(actual_images_dir, exist_ok=True)
    return actual_images_dir, md_images_prefix
