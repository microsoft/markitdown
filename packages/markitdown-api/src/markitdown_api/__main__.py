"""uvicorn 启动入口。

用法：
    python -m markitdown_api
    markitdown-api
    uvicorn markitdown_api.app:app --reload --port 8000
"""

import os

import uvicorn


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"

    uvicorn.run(
        "markitdown_api.app:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    main()
