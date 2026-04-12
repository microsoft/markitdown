"""后台 ThreadPoolExecutor，用于异步文件转换任务。"""

import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from markitdown import MarkItDown

from .task_store import Status, update_task

_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="markitdown-worker")


def _run_file_conversion(task_id: str, md: MarkItDown, data: bytes, suffix: str) -> None:
    """在后台线程中执行文件转换，结果写入 task_store。"""
    update_task(task_id, status=Status.running)
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        result = md.convert(tmp_path)
        Path(tmp_path).unlink(missing_ok=True)
        update_task(task_id, status=Status.done, result=result.text_content)
    except Exception as exc:
        update_task(task_id, status=Status.failed, error=str(exc))


def _run_url_conversion(task_id: str, md: MarkItDown, url: str) -> None:
    """在后台线程中执行 URL 转换，结果写入 task_store。"""
    update_task(task_id, status=Status.running)
    try:
        result = md.convert(url)
        update_task(task_id, status=Status.done, result=result.text_content)
    except Exception as exc:
        update_task(task_id, status=Status.failed, error=str(exc))


def submit_file(task_id: str, md: MarkItDown, data: bytes, suffix: str) -> None:
    """提交文件转换任务到线程池。"""
    _executor.submit(_run_file_conversion, task_id, md, data, suffix)


def submit_url(task_id: str, md: MarkItDown, url: str) -> None:
    """提交 URL 转换任务到线程池。"""
    _executor.submit(_run_url_conversion, task_id, md, url)
