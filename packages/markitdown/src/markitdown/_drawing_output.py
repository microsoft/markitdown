"""Publish drawing output without overwriting source or existing destinations."""
import os
import tempfile
from pathlib import Path
from urllib.parse import quote

from ._base_converter import DocumentConverterResult


def write_drawing_output(
    output: str | None, report: str, result: DocumentConverterResult
) -> str:
    """Write a new report/output/assets set; return Markdown for stdout use."""
    if result.conversion_report is None:
        raise ValueError(
            "Drawing mode did not convert a PDF; no drawing report is available."
        )
    markdown = result.markdown
    destinations = {Path(report): result.conversion_report.encode("utf-8")}
    asset_dir = None
    if result.assets:
        if output is None:
            raise ValueError("External page views require an output file.")
        asset_dir = Path(output).with_suffix(".assets")
        for name, data in result.assets.items():
            relative = Path(name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("Invalid drawing asset name.")
            destination = asset_dir / relative
            destinations[destination] = data
            url = quote(asset_dir.name + "/" + relative.as_posix(), safe="/")
            markdown = markdown.replace(f"]({relative.as_posix()})", f"]({url})")
    if output is not None:
        output_path = Path(output)
        if output_path in destinations:
            raise ValueError("Output and report paths must differ.")
        destinations[output_path] = markdown.encode("utf-8")
    resolved = [p.resolve() for p in destinations]
    if len(set(resolved)) != len(resolved):
        raise ValueError("Drawing output paths must differ.")
    for path in destinations:
        if path.exists() or path.is_symlink():
            raise FileExistsError(f"Drawing output already exists: {path}")
    if asset_dir is not None and (asset_dir.exists() or asset_dir.is_symlink()):
        raise FileExistsError(f"Drawing asset directory already exists: {asset_dir}")

    # Stage everything before publishing. Hard links create destinations
    # atomically without replacing files created after the preflight checks.
    staged = []
    published = []
    created_dirs = []
    try:
        if asset_dir is not None:
            asset_dir.mkdir()
            created_dirs.append(asset_dir)
            for path in destinations:
                if asset_dir in path.parents:
                    for parent in reversed(path.parent.parents):
                        if (
                            parent != asset_dir
                            and asset_dir in parent.parents
                            and not parent.exists()
                        ):
                            parent.mkdir()
                            created_dirs.append(parent)
                    if path.parent != asset_dir and not path.parent.exists():
                        path.parent.mkdir()
                        created_dirs.append(path.parent)
        for path, data in destinations.items():
            with tempfile.NamedTemporaryFile(
                dir=path.parent, delete=False
            ) as temporary:
                staged.append((Path(temporary.name), path))
                temporary.write(data)
        for temporary, path in staged:
            os.link(temporary, path)
            published.append((temporary, path))
    except BaseException:
        for temporary, path in reversed(published):
            # Roll back only our own inode, not a concurrently replaced file.
            if path.exists() and os.path.samefile(temporary, path):
                path.unlink()
        raise
    finally:
        for temporary, _ in staged:
            temporary.unlink(missing_ok=True)
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass  # Successful assets, or another writer's files, remain.
    return markdown
