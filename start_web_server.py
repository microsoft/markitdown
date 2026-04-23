import sys
import os
from pathlib import Path

project_root = Path(__file__).parent
markitdown_src = project_root / "packages" / "markitdown" / "src"

if str(markitdown_src) not in sys.path:
    sys.path.insert(0, str(markitdown_src))

import warnings
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv")

import argparse
import uvicorn


def main():
    parser = argparse.ArgumentParser(
        description="Start the MarkItDown Web UI server",
        prog="markitdown-web"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (development mode)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  MarkItDown Web UI")
    print("=" * 60)
    print(f"Starting server on: http://{args.host}:{args.port}")
    print(f"API Documentation: http://{args.host}:{args.port}/docs")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    original_cwd = os.getcwd()
    server_dir = project_root / "packages" / "markitdown" / "src" / "markitdown" / "web_server"
    
    if args.reload:
        os.chdir(server_dir)
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=True,
            log_level="info"
        )
    else:
        uvicorn.run(
            "markitdown.web_server.main:app",
            host=args.host,
            port=args.port,
            log_level="info"
        )


if __name__ == "__main__":
    main()
