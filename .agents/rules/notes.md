# Quy tắc Ghi nhận Sổ tay Lập trình viên (Developer Manual Notes) — markitdown

Tài liệu này định nghĩa quy chuẩn để AI Agent tiếp nhận, định dạng và lưu trữ các ghi chú viết tay (manual notes, dev scratchpad, insight kỹ thuật) của lập trình viên vào dự án **markitdown**.

---

## 1. Cú pháp kích hoạt (Invocation)
Bất cứ khi nào lập trình viên sử dụng một trong các cách diễn đạt sau trong khung chat:
- Nhắc đến `@notes.md` hoặc `@notes` (ví dụ: `@notes.md ghi chú lại cách dùng hàm này...`).
- Dùng tiền tố rõ ràng: `Note tay: <nội dung>`, `Ghi chú lại: <nội dung>`, `Lưu note: <nội dung>`, `NOTE: <nội dung>`.
- Chỉ định rõ ràng muốn lưu một phát hiện, ghi nhớ hoặc yêu cầu kỹ thuật cần lưu tâm.

AI Agent phải tự động kích hoạt quy trình định dạng và lưu trữ theo hướng dẫn dưới đây.

---

## 2. Vị trí lưu trữ & Phân hệ Dự án markitdown

Toàn bộ ghi chú được lưu theo cơ chế **nối tiếp vào cuối file (append-only)** tại:
- **Tệp lưu trữ chính của dự án**: `.ai-work/notes/notes.md`

### Bảng Ánh Xạ Phân Hệ (Modules Mapping)

| Mã Phân hệ | Phạm vi nghiệp vụ & Từ khóa nhận diện | Thành phần liên quan |
|---|---|---|
| `Core` | Lớp `MarkItDown`, `StreamInfo`, cơ chế chọn converter, exceptions, CLI (`__main__.py`). | `packages/markitdown/src/markitdown/*.py` |
| `Converters` | Các converter định dạng (`DocxConverter`, `PdfConverter`, `XlsxConverter`...), `_markdownify.py`, `_exiftool.py`, `_llm_caption.py`, `_transcribe_audio.py`. | `packages/markitdown/src/markitdown/converters/` |
| `Plugins` | MCP server, OCR, plugin mẫu, entry point `markitdown.plugin`. | `packages/markitdown-mcp`, `packages/markitdown-ocr`, `packages/markitdown-sample-plugin` |
| `Tests` | Test vectors, file mẫu, test CLI/module. | `packages/*/tests/` |
| `Conversions` | Quy trình chuyển file người dùng sang Markdown, skill `file-to-md`, kết quả trong `.ai-work/conversions`. | `.agents/skills/file-to-md/` |
| `Build & Env` | `.venv`, Python 3.14, ffmpeg, `PYTHONUTF8`, build wheel/sdist, đồng bộ upstream. | `.agents/rules/build.md`, `pyproject.toml` |
| `General` | Kiến trúc tổng thể, quy ước workflow, coding convention. | Toàn dự án |

---

## 3. Cấu trúc chuẩn của một Note Entry

Mỗi lần ghi một note mới, Agent nối thêm (append) vào cuối tệp `.ai-work/notes/notes.md` theo định dạng:

```markdown
### [YYYY-MM-DD HH:mm] <Tiêu đề súc tích tóm tắt nội dung note>
- **Chủ đề / Phân hệ**: <Mã phân hệ ở bảng trên>
- **Nội dung ghi chú**: <Nội dung ghi chú do lập trình viên diễn đạt>
- **File liên quan**: [tên_file](đường/dẫn/tương/đối) (nếu có)
```

---

## 4. Nguyên tắc bắt buộc dành cho Agent khi ghi Note
1. **Bảo tồn nội dung nguyên bản**: Không tự ý tóm tắt làm sai lệch hoặc lược bỏ ý nghĩa kỹ thuật mà lập trình viên đã diễn đạt.
2. **Không ghi đè (Append-Only)**: Tuyệt đối không xóa hay thay đổi các note đã ghi trước đó trong file. Luôn thêm vào cuối file.
3. **Liên kết mã nguồn chính xác**: Khi nhắc đến file trong repo, dùng link Markdown với đường dẫn tương đối từ gốc repo (ví dụ `packages/markitdown/src/markitdown/_markitdown.py`) để lập trình viên click mở trực tiếp.
4. **Phản hồi xác nhận**: Sau khi ghi xong, Agent thông báo ngắn gọn đường dẫn file đã ghi và trích dẫn nội dung vừa lưu để lập trình viên xác thực.
