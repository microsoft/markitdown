"""线程安全的异步任务状态管理。"""

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum


class Status(str, Enum):
    pending = "pending"
    running = "running"
    done = "done"
    failed = "failed"


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: Status = Status.pending
    result: str | None = None
    error: str | None = None


_store: dict[str, Task] = {}
_lock = threading.Lock()


def create_task() -> Task:
    """创建一个新任务并存入 store，返回任务对象。"""
    task = Task()
    with _lock:
        _store[task.id] = task
    return task


def get_task(task_id: str) -> Task | None:
    """按 ID 查询任务，不存在返回 None。"""
    with _lock:
        return _store.get(task_id)


def update_task(
    task_id: str,
    *,
    status: Status | None = None,
    result: str | None = None,
    error: str | None = None,
) -> None:
    """更新任务状态/结果/错误信息。"""
    with _lock:
        task = _store.get(task_id)
        if task is None:
            return
        if status is not None:
            task.status = status
        if result is not None:
            task.result = result
        if error is not None:
            task.error = error
