"""Command line interface for the API server."""

import argparse
import uvicorn
from markitdown_api import app, Settings, __version__


def main():
    """Run the API server."""
    settings = Settings()

    parser = argparse.ArgumentParser(
        description="Run the MarkItDown API server."
    )
    parser.add_argument(
        "--host",
        default=settings.host,
        help=f"Host to bind to (default: {settings.host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.port,
        help=f"Port to listen on (default: {settings.port})",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=settings.workers,
        help=f"Number of worker processes (default: {settings.workers})",
    )
    parser.add_argument(
        "--enable-plugins",
        action="store_true",
        default=settings.enable_plugins,
        help="Enable MarkItDown plugins",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version number and exit",
    )

    args = parser.parse_args()

    # Override settings from command line
    settings.host = args.host
    settings.port = args.port
    settings.workers = args.workers
    settings.enable_plugins = args.enable_plugins

    # Run server
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
    )


if __name__ == "__main__":
    main()