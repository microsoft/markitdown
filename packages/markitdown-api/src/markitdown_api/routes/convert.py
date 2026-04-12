"""文件/URL 转 Markdown 路由——同步与异步两种接口。"""

import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from markitdown import MarkItDown

from ..converter import get_converter
from ..task_store import Status, create_task, get_task
from ..worker import submit_file, submit_url

router = APIRouter()

# 文件大小阈值：超过此值走异步接口（同步 /convert 会自动升级为异步）
SYNC_SIZE_LIMIT = 10 * 1024 * 1024  # 10 MB


# ---------------------------------------------------------------------------
# 同步接口
# ---------------------------------------------------------------------------


@router.post("/convert")
async def convert(
    md: Annotated[MarkItDown, Depends(get_converter)],
    file: UploadFile | None = File(default=None),
    url: str | None = Form(default=None),
):
    """将上传文件或 URL 转换为 Markdown。

    - 文件 < 5 MB：同步返回 `{ "markdown": "..." }`
    - 文件 ≥ 5 MB：自动转异步，返回 `{ "job_id": "...", "poll_url": "/tasks/{job_id}" }`
    - 仅传 url：同步执行（网络请求较快，超时由调用方控制）
    """
    if file is None and url is None:
        raise HTTPException(status_code=422, detail="请提供 file 或 url 参数之一")

    if url and file is None:
        try:
            result = md.convert(url)
            return {"markdown": result.text_content}
        except Exception as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    # 文件上传路径
    data = await file.read()
    suffix = Path(file.filename or "upload").suffix or ".bin"

    if len(data) >= SYNC_SIZE_LIMIT:
        task = create_task()
        submit_file(task.id, md, data, suffix)
        return JSONResponse(
            status_code=202,
            content={
                "job_id": task.id,
                "poll_url": f"/tasks/{task.id}",
                "detail": "文件较大，已提交后台转换，请轮询 poll_url 查询结果",
            },
        )

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        result = md.convert(tmp_path)
        Path(tmp_path).unlink(missing_ok=True)
        return {"markdown": result.text_content}
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


# ---------------------------------------------------------------------------
# 异步接口
# ---------------------------------------------------------------------------


@router.post("/convert/async", status_code=202)
async def convert_async(
    md: Annotated[MarkItDown, Depends(get_converter)],
    file: UploadFile | None = File(default=None),
    url: str | None = Form(default=None),
):
    """强制异步：立即返回 job_id，结果通过 GET /tasks/{job_id} 轮询。"""
    if file is None and url is None:
        raise HTTPException(status_code=422, detail="请提供 file 或 url 参数之一")

    task = create_task()

    if url and file is None:
        submit_url(task.id, md, url)
    else:
        data = await file.read()
        suffix = Path(file.filename or "upload").suffix or ".bin"
        submit_file(task.id, md, data, suffix)

    return {"job_id": task.id, "poll_url": f"/tasks/{task.id}"}


# ---------------------------------------------------------------------------
# 任务查询
# ---------------------------------------------------------------------------


@router.get("/tasks/{job_id}")
async def get_task_status(job_id: str):
    """查询异步任务状态。

    返回示例：
    - `{ "status": "pending" }`
    - `{ "status": "running" }`
    - `{ "status": "done", "markdown": "..." }`
    - `{ "status": "failed", "error": "..." }`
    """
    task = get_task(job_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"任务 {job_id} 不存在")

    response: dict = {"status": task.status}
    if task.status == Status.done:
        response["markdown"] = task.result
    elif task.status == Status.failed:
        response["error"] = task.error
    return response
