# MarkItDown API 接口文档

**Base URL：** `http://localhost:8000`

---

## 目录

- [通用说明](#通用说明)
- [GET /health](#get-health)
- [POST /convert](#post-convert)
- [POST /convert/async](#post-convertasync)
- [GET /tasks/{job_id}](#get-tasksjob_id)
- [错误码说明](#错误码说明)
- [完整调用示例](#完整调用示例)

---

## 通用说明

### 请求格式

所有文件上传接口均使用 `multipart/form-data`。

### 响应格式

所有响应均为 JSON，`Content-Type: application/json`。

### 文件大小策略

`POST /convert` 接口会**自动判断文件大小**，无需客户端手动选择同步/异步：

| 文件大小 | 行为 | 响应状态码 |
|---------|------|-----------|
| < 10 MB | 同步处理，直接返回 Markdown | `200` |
| ≥ 10 MB | 自动转异步，返回任务 ID | `202` |

---

## GET /health

健康检查，用于确认服务是否正常运行。

**请求**

```
GET /health
```

**响应** `200 OK`

```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

**示例**

```bash
curl http://localhost:8000/health
```

---

## POST /convert

将文件或 URL 转换为 Markdown。服务端自动根据文件大小决定同步或异步处理。

**请求**

```
POST /convert
Content-Type: multipart/form-data
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | 二进制文件 | `file` 和 `url` 二选一 | 要转换的文件 |
| `url` | 字符串（表单字段） | `file` 和 `url` 二选一 | 要抓取并转换的 URL |

> 注意：`file` 和 `url` 不能同时为空，也不需要同时传。

---

### 场景一：小文件（< 10 MB）同步响应

**响应** `200 OK`

```json
{
  "markdown": "# 文档标题\n\n正文内容..."
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `markdown` | string | 转换后的 Markdown 文本 |

---

### 场景二：大文件（≥ 10 MB）自动转异步

**响应** `202 Accepted`

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "poll_url": "/tasks/550e8400-e29b-41d4-a716-446655440000",
  "detail": "文件较大，已提交后台转换，请轮询 poll_url 查询结果"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `job_id` | string | 任务唯一 ID（UUID） |
| `poll_url` | string | 轮询结果的相对路径 |
| `detail` | string | 提示信息 |

---

### 场景三：URL 转换（同步）

**响应** `200 OK`

```json
{
  "markdown": "# Example Domain\n\nThis domain is for use in illustrative examples..."
}
```

---

**示例**

```bash
# 上传文件
curl -X POST http://localhost:8000/convert \
  -F "file=@/path/to/document.pdf"

# 转换 URL
curl -X POST http://localhost:8000/convert \
  -F "url=https://example.com"

# 上传 Word 文档
curl -X POST http://localhost:8000/convert \
  -F "file=@/path/to/report.docx"
```

---

## POST /convert/async

强制异步处理，不论文件大小，立即返回 `job_id`，适合批量任务场景。

**请求**

```
POST /convert/async
Content-Type: multipart/form-data
```

**请求参数**

与 `POST /convert` 相同。

**响应** `202 Accepted`

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "poll_url": "/tasks/550e8400-e29b-41d4-a716-446655440000"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `job_id` | string | 任务唯一 ID（UUID） |
| `poll_url` | string | 轮询结果的相对路径 |

**示例**

```bash
# 强制异步上传
curl -X POST http://localhost:8000/convert/async \
  -F "file=@/path/to/large-file.pdf"

# 强制异步转换 URL
curl -X POST http://localhost:8000/convert/async \
  -F "url=https://example.com/long-page"
```

---

## GET /tasks/{job_id}

查询异步任务的处理状态和结果。

**请求**

```
GET /tasks/{job_id}
```

**路径参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| `job_id` | string | 提交任务时返回的 UUID |

---

### 状态说明

**排队中** `200 OK`

```json
{
  "status": "pending"
}
```

**处理中** `200 OK`

```json
{
  "status": "running"
}
```

**完成** `200 OK`

```json
{
  "status": "done",
  "markdown": "# 文档标题\n\n正文内容..."
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | 任务状态：`pending` / `running` / `done` / `failed` |
| `markdown` | string | 转换结果（仅 `done` 时存在） |

**失败** `200 OK`

```json
{
  "status": "failed",
  "error": "PdfConverter threw MissingDependencyException..."
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `failed` |
| `error` | string | 错误详情（仅 `failed` 时存在） |

**任务不存在** `404 Not Found`

```json
{
  "detail": "任务 xxx 不存在"
}
```

**示例**

```bash
curl http://localhost:8000/tasks/550e8400-e29b-41d4-a716-446655440000
```

---

## 错误码说明

| HTTP 状态码 | 含义 | 场景 |
|------------|------|------|
| `200` | 成功 | 同步转换完成 |
| `202` | 已接受 | 任务已提交后台处理 |
| `404` | 不存在 | `job_id` 无效或已过期 |
| `422` | 请求参数错误 | 未提供 `file`/`url`，或转换失败 |
| `500` | 服务内部错误 | 未预期的异常 |

---

## 完整调用示例

### Shell（Bash）

```bash
#!/bin/bash
BASE_URL="http://localhost:8000"
FILE_PATH="/path/to/document.pdf"

# 上传文件
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/convert" \
  -F "file=@$FILE_PATH")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
  # 同步完成，直接提取 markdown
  echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['markdown'])"

elif [ "$HTTP_CODE" = "202" ]; then
  # 异步，开始轮询
  JOB_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
  echo "任务已提交，job_id: $JOB_ID，开始轮询..."

  while true; do
    sleep 3
    RESULT=$(curl -s "$BASE_URL/tasks/$JOB_ID")
    STATUS=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")

    if [ "$STATUS" = "done" ]; then
      echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['markdown'])"
      break
    elif [ "$STATUS" = "failed" ]; then
      echo "转换失败：$(echo $RESULT | python3 -c "import sys,json; print(json.load(sys.stdin)['error'])")"
      break
    else
      echo "状态：$STATUS，继续等待..."
    fi
  done
fi
```

### Python

```python
import time
import requests

def convert_to_markdown(file_path: str = None, url: str = None, base_url: str = "http://localhost:8000") -> str:
    """将文件或 URL 转换为 Markdown，自动处理同步/异步。"""
    if file_path:
        with open(file_path, "rb") as f:
            res = requests.post(f"{base_url}/convert", files={"file": f})
    elif url:
        res = requests.post(f"{base_url}/convert", data={"url": url})
    else:
        raise ValueError("file_path 和 url 必须提供一个")

    if res.status_code == 200:
        return res.json()["markdown"]

    if res.status_code == 202:
        job_id = res.json()["job_id"]
        print(f"大文件已提交，轮询 job_id: {job_id}")
        while True:
            time.sleep(2)
            poll = requests.get(f"{base_url}/tasks/{job_id}").json()
            status = poll["status"]
            print(f"  状态: {status}")
            if status == "done":
                return poll["markdown"]
            if status == "failed":
                raise RuntimeError(f"转换失败: {poll['error']}")

    raise RuntimeError(f"意外响应: {res.status_code} {res.text}")


# 使用示例
md = convert_to_markdown(file_path="/path/to/report.pdf")
print(md[:500])

md = convert_to_markdown(url="https://example.com")
print(md[:500])
```

### JavaScript（fetch）

```javascript
async function convertToMarkdown({ file, url }, baseUrl = 'http://localhost:8000') {
  const form = new FormData()
  if (file) form.append('file', file)
  if (url) form.append('url', url)

  const res = await fetch(`${baseUrl}/convert`, { method: 'POST', body: form })
  const data = await res.json()

  // 同步完成
  if (res.status === 200) return data.markdown

  // 异步轮询
  if (res.status === 202) {
    const { job_id } = data
    console.log(`已提交，轮询 job_id: ${job_id}`)
    while (true) {
      await new Promise(r => setTimeout(r, 2000))
      const poll = await fetch(`${baseUrl}/tasks/${job_id}`).then(r => r.json())
      console.log(`状态: ${poll.status}`)
      if (poll.status === 'done') return poll.markdown
      if (poll.status === 'failed') throw new Error(poll.error)
    }
  }

  throw new Error(`意外响应: ${res.status}`)
}

// 使用示例
const fileInput = document.querySelector('input[type="file"]')
const markdown = await convertToMarkdown({ file: fileInput.files[0] })
console.log(markdown)
```
