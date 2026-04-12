"""FastAPI 应用实例——路由注册与全局异常处理。"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .__about__ import __version__
from .routes import convert

app = FastAPI(
    title="MarkItDown API",
    description="将任意文件或 URL 转换为 Markdown 的 HTTP 服务",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(convert.router, tags=["convert"])


@app.get("/health", tags=["health"])
async def health() -> dict:
    """健康检查端点。"""
    return {"status": "ok", "version": __version__}


@app.exception_handler(Exception)
async def _global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """捕获未处理异常，统一返回 HTTP 500。"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"服务内部错误: {exc}"},
    )
