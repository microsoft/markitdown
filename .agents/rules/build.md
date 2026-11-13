# Quy tắc môi trường, test và build của dự án

Quy tắc này áp dụng cho mọi AI agent làm việc trong repository `D:\dvtools\markitdown` (fork của `microsoft/markitdown`).

## 1. Môi trường Python

| Thành phần | Giá trị |
|---|---|
| Python | 3.14 (`py -3.14`). Package `markitdown` yêu cầu `>=3.10,<3.15`; **không dùng Python 3.15** đang là mặc định của máy |
| Virtualenv | `D:\dvtools\markitdown\.venv` (đã có trong `.gitignore`) |
| Cài đặt | editable từ mã nguồn, đủ extras và phụ thuộc test của `hatch-test` |
| ffmpeg | Cần cho audio. Script và test phải tìm được `ffmpeg.exe` trong PATH (WinGet hoặc Chocolatey) |

Tạo lại môi trường khi `.venv` không tồn tại hoặc hỏng:

```powershell
py -3.14 -m venv D:\dvtools\markitdown\.venv
D:\dvtools\markitdown\.venv\Scripts\python.exe -m pip install --upgrade pip
D:\dvtools\markitdown\.venv\Scripts\python.exe -m pip install -e "D:\dvtools\markitdown\packages\markitdown[all]" pytest openai pyyaml
```

Package phụ (`markitdown-mcp`, `markitdown-ocr`, `markitdown-sample-plugin`) chỉ cài khi người dùng yêu cầu hoặc step đang làm cần đến.

## 2. Chạy test

Test do agent tự chạy (debug, review, xác minh step):

```powershell
$env:PYTHONUTF8 = "1"
cd D:\dvtools\markitdown\packages\markitdown
D:\dvtools\markitdown\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
```

- Luôn đặt `PYTHONUTF8=1`. Không có cờ này, test CLI in tiếng Nhật/emoji ra stdout bị lỗi do Windows dùng cp1252.
- Có thể giới hạn test theo file (`tests/test_pdf.py`) hoặc `-k` khi làm một step cụ thể; trước khi đóng step phải chạy toàn bộ test suite của package bị sửa.
- Bộ test đầy đủ mất khoảng 5 phút; chạy ở chế độ nền nếu công cụ có giới hạn thời gian.
- Một số test cần mạng (`test_convert_http_uri`, YouTube, speech). Lỗi do mạng phải ghi rõ là lỗi môi trường, không được báo là PASS.

### Ngoại lệ đã được người dùng chấp nhận

| Test | Lý do | Quyết định |
|---|---|---|
| `tests/test_cli_vectors.py` — test vector bảng tiếng Nhật (`test_vector13`) khi chạy **không có** `PYTHONUTF8=1` | Encoding console Windows | Bỏ qua theo yêu cầu người dùng ngày 2026-11-13 |

Không được thêm ngoại lệ mới khi chưa có đồng ý của người dùng.

## 3. Build do người dùng yêu cầu

Khi người dùng gửi lệnh độc lập `Build`, `Build lại` hoặc `Build dự án`, agent build wheel và sdist cho package `markitdown`:

```powershell
D:\dvtools\markitdown\.venv\Scripts\python.exe -m pip install --upgrade build
D:\dvtools\markitdown\.venv\Scripts\python.exe -m build D:\dvtools\markitdown\packages\markitdown --outdir D:\dvtools\markitdown\dist
```

- `Build lại`: xóa nội dung cũ trong `D:\dvtools\markitdown\dist` trước khi build.
- Nếu người dùng nêu tên package khác (`markitdown-mcp`, `markitdown-ocr`...), build đúng package đó vào cùng `dist`.
- Sau khi build, liệt kê file `.whl` và `.tar.gz` với đường dẫn tuyệt đối.
- Build không đồng nghĩa với publish lên PyPI hay cài đặt toàn cục. Chỉ publish khi người dùng yêu cầu riêng.

## 4. Build do agent tự chạy

- Không ghi vào `D:\dvtools\markitdown\dist`.
- Dùng `D:\dvtools\markitdown\.artifacts\work\<mục-đích>\` làm output (thêm `.artifacts/` vào `.gitignore` nếu chưa có).
- Báo mục đích, package và vị trí artifact trong kết quả.

## 5. Ưu tiên và ngoại lệ

- Chỉ dẫn cụ thể của người dùng (Python version, package, output path) được ưu tiên hơn mặc định trong tài liệu này.
- Nếu người dùng nhắc từ `Build` trong ngữ cảnh hỏi khái niệm, không tự chạy build.
- Cài thêm phần mềm hệ thống (ffmpeg, Python khác, exiftool) cần đồng ý của người dùng.
