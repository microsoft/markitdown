"""Conversion worker: runs in its own process so a hostile or broken file can be killed (timeout) or
confined (memory cap) without taking the HTTP server down.

Protocol: the file bytes arrive on stdin, the extension (".pdf", ...) is argv[1]. On success the Markdown
is written to stdout (UTF-8) and the exit code is 0. Failures exit non-zero with a short reason code on
stderr's last line.
"""

import io
import os
import sys

EXIT_FAILED = 2  # the converter could not read the file
EXIT_UNSUPPORTED = 3  # no converter accepted the format


def _limit_memory() -> None:
    mb = int(os.environ.get("MARKITDOWN_WORKER_MEMORY_MB", "0") or 0)
    if mb <= 0:
        return
    try:
        import resource

        limit = mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except (
        ImportError,
        ValueError,
        OSError,
    ):  # not available (e.g. Windows): the timeout still applies
        pass


def main(argv=None) -> int:
    argv = sys.argv if argv is None else argv
    extension = argv[1] if len(argv) > 1 else ""
    _limit_memory()
    data = sys.stdin.buffer.read()
    try:
        from markitdown import (
            FileConversionException,
            MarkItDown,
            StreamInfo,
            UnsupportedFormatException,
        )

        md = MarkItDown(enable_plugins=False)
        result = md.convert_stream(
            io.BytesIO(data), stream_info=StreamInfo(extension=extension)
        )
    except UnsupportedFormatException:
        sys.stderr.write("unsupported\n")
        return EXIT_UNSUPPORTED
    except FileConversionException:
        sys.stderr.write("conversion_failed\n")
        return EXIT_FAILED
    except MemoryError:
        sys.stderr.write("out_of_memory\n")
        return EXIT_FAILED
    except Exception:  # any other converter crash is "could not read this file"
        sys.stderr.write("conversion_failed\n")
        return EXIT_FAILED
    sys.stdout.buffer.write(result.markdown.encode("utf-8"))
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
