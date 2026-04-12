"""基础集成测试——覆盖 URL 转换、文件上传、异步接口和任务查询。"""

import time
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from markitdown_api.app import app
from markitdown_api.converter import get_converter

client = TestClient(app)

# MarkItDown.convert 的 mock 返回值
_FAKE_RESULT = MagicMock()
_FAKE_RESULT.text_content = "# Example\n\nThis is example.com"


def _make_mock_md():
    mock_md = MagicMock()
    mock_md.convert.return_value = _FAKE_RESULT
    return mock_md


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_convert_url():
    mock_md = _make_mock_md()
    app.dependency_overrides[get_converter] = lambda: mock_md
    try:
        r = client.post("/convert", data={"url": "https://example.com"})
    finally:
        app.dependency_overrides.pop(get_converter, None)

    assert r.status_code == 200
    body = r.json()
    assert "markdown" in body
    assert "Example" in body["markdown"]


def test_convert_txt_file():
    r = client.post(
        "/convert",
        files={"file": ("hello.txt", b"hello world", "text/plain")},
    )
    assert r.status_code == 200
    body = r.json()
    assert "markdown" in body
    assert "hello" in body["markdown"]


def test_convert_missing_params():
    r = client.post("/convert")
    assert r.status_code == 422


def test_convert_async_url():
    from markitdown_api import task_store

    def fake_submit_url(task_id, md, url):
        task_store.update_task(
            task_id,
            status=task_store.Status.done,
            result="# Mocked\n\nAsync URL result",
        )

    with patch("markitdown_api.routes.convert.submit_url", side_effect=fake_submit_url):
        r = client.post("/convert/async", data={"url": "https://example.com"})

    assert r.status_code == 202
    body = r.json()
    assert "job_id" in body
    job_id = body["job_id"]

    poll = client.get(f"/tasks/{job_id}")
    assert poll.status_code == 200
    assert poll.json()["status"] == "done"
    assert "markdown" in poll.json()


def test_convert_async_file():
    r = client.post(
        "/convert/async",
        files={"file": ("test.txt", b"async file content", "text/plain")},
    )
    assert r.status_code == 202
    job_id = r.json()["job_id"]

    for _ in range(10):
        poll = client.get(f"/tasks/{job_id}")
        status = poll.json()["status"]
        if status in ("done", "failed"):
            break
        time.sleep(1)

    assert poll.json()["status"] == "done"


def test_task_not_found():
    r = client.get("/tasks/nonexistent-task-id")
    assert r.status_code == 404
