import logging
import signal
import sys
import threading

from .config import ConfigError, load_config
from .server import create_server


def main() -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    try:
        config = load_config()
    except ConfigError as exc:
        print(f"[config] {exc}", file=sys.stderr)
        return 1
    server = create_server(config)
    logging.getLogger("markitdown_service").info(
        "listening on %s:%d (max %d MB, %ds, %d at a time)",
        config.host,
        config.port,
        config.max_upload_bytes // (1024 * 1024),
        config.timeout_seconds,
        config.max_concurrent,
    )
    # Docker stops the container with SIGTERM; as PID 1 Python would otherwise ignore it and wait to be killed.
    signal.signal(
        signal.SIGTERM,
        lambda *_: threading.Thread(target=server.shutdown, daemon=True).start(),
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
