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
    
    print(f"Starting MarkItDown Web UI on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server")
    print()
    
    uvicorn.run(
        "markitdown.web_server.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
