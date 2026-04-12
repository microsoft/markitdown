# markitdown-api

将任意文件或 URL 转换为 Markdown 的 FastAPI HTTP 服务，封装 [MarkItDown](https://github.com/microsoft/markitdown) 的所有格式转换能力。

---

## 功能特性

| 功能 | 说明 |
|------|------|
| 同步转换 | 文件 < 10 MB 时立即返回 Markdown 文本 |
| 自动升级异步 | 文件 ≥ 10 MB 自动提交后台任务，返回 `job_id` |
| 强制异步 | `POST /convert/async` 始终返回 `job_id` |
| 任务轮询 | `GET /tasks/{job_id}` 查询转换状态和结果 |
| URL 转换 | 直接传入 URL，服务抓取并转换 |
| 所有格式 | PDF、DOCX、PPTX、XLSX、HTML、MP3、MP4 等（依赖 `markitdown[all]`） |

---

## 快速开始

### 安装

```bash
# 在 markitdown 仓库根目录下，先创建虚拟环境
uv venv
uv pip install -e "packages/markitdown-api"
```

### 启动服务

```bash
# 方式一：使用脚本命令
markitdown-api

# 方式二：uvicorn（支持热重载，开发用）
uvicorn markitdown_api.app:app --reload --port 8000

# 方式三：Python 模块
python -m markitdown_api
```

服务默认监听 `http://0.0.0.0:8000`。

### 访问文档

启动后打开浏览器：

- Swagger UI：[http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc：[http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `HOST` | `0.0.0.0` | 监听地址 |
| `PORT` | `8000` | 监听端口 |
| `RELOAD` | `false` | 是否开启热重载（开发模式） |
| `ENABLE_PLUGINS` | `false` | 是否启用 MarkItDown 插件（如 markitdown-ocr） |

---

## 接口说明

### GET /health

健康检查。

**响应示例：**
```json
{ "status": "ok", "version": "0.1.0" }
```

---

### POST /convert

同步转换（文件 ≥ 10 MB 自动升级为异步）。

**请求（multipart/form-data）：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | 文件 | 二选一 | 上传的文件 |
| `url` | 字符串 | 二选一 | 目标 URL |

**响应（同步）：**
```json
{ "markdown": "# 标题\n\n正文内容..." }
```

**响应（大文件自动异步，HTTP 202）：**
```json
{
  "job_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "poll_url": "/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "detail": "文件较大，已提交后台转换，请轮询 poll_url 查询结果"
}
```

**示例：**
```bash
# 上传文件
curl -X POST http://localhost:8000/convert \
  -F "file=@/path/to/document.pdf"

# 转换 URL
curl -X POST http://localhost:8000/convert \
  -F "url=https://example.com"
```

---

### POST /convert/async

强制异步转换，立即返回 `job_id`。

**请求**：同 `POST /convert`

**响应（HTTP 202）：**
```json
{
  "job_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "poll_url": "/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**示例：**
```bash
curl -X POST http://localhost:8000/convert/async \
  -F "file=@/path/to/large-file.pdf"
```

---

### GET /tasks/{job_id}

查询异步任务状态和结果。

**响应示例：**

```json
// 排队中
{ "status": "pending" }

// 转换中
{ "status": "running" }

// 成功
{ "status": "done", "markdown": "# 标题\n\n正文..." }

// 失败
{ "status": "failed", "error": "错误信息" }
```

**示例：**
```bash
curl http://localhost:8000/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## 运行测试

```bash
uv pip install -e "packages/markitdown-api[dev]"
pytest packages/markitdown-api/tests/ -v
```

---

## 支持格式

依赖 `markitdown[all]`，支持：

| 格式 | 说明 |
|------|------|
| PDF | 文本层提取（含可选 OCR 插件） |
| DOCX | Word 文档 |
| PPTX | PowerPoint 演示文稿 |
| XLSX / XLS | Excel 表格 |
| HTML | 网页内容 |
| MP3 / WAV | 音频转写（Google Speech API） |
| MP4 | 视频（提取音频转写） |
| EPUB | 电子书 |
| ZIP | 压缩包内文件 |
| 图片 | EXIF 元数据（如启用 markitdown-ocr 则 OCR） |
| URL | 直接抓取网页 |

---

## 架构

```
Client
  │
  ├─ POST /convert (< 10MB)  ────► MarkItDown.convert ────► { markdown }
  │
  ├─ POST /convert (≥ 10MB)  ─┐
  │                           ├─► ThreadPoolExecutor ──► MarkItDown.convert
  └─ POST /convert/async    ─┘         │
                                        └─► task_store ──► GET /tasks/{id}
```
