# Quy tắc đặt tên (Naming Convention) — markitdown

Repository là fork của `microsoft/markitdown`. Quy tắc dưới đây ghi lại convention **đang có** của upstream; code mới phải theo đúng convention này để dễ đồng bộ với upstream.

Agent phải đọc toàn bộ tài liệu này trước khi tạo file, module, class, hàm, biến, lập plan hay đặc tả step.

---

## 1. Quy tắc chung Python

| Thành phần | Quy tắc | Ví dụ |
|---|---|---|
| Module / file | `snake_case.py` | `_markitdown.py` |
| Module nội bộ | Tiền tố `_` | `_base_converter.py`, `_stream_info.py` |
| Package | `snake_case` | `markitdown`, `markitdown_mcp` |
| Class | `PascalCase` | `MarkItDown`, `StreamInfo` |
| Exception | `PascalCase` + hậu tố `Exception` | `FileConversionException`, `UnsupportedFormatException` |
| Hàm, method, biến | `snake_case` | `convert_stream`, `file_stream` |
| Hằng số | `UPPER_SNAKE_CASE` | `ACCEPTED_MIME_TYPE_PREFIXES` |
| Thành phần private | Tiền tố `_` | `_get_mime_type` |

- Tuân theo PEP 8 và định dạng của `black` (repo có `.pre-commit-config.yaml`).
- Có type hint cho tham số và giá trị trả về của API public.
- Không đổi tên symbol public của upstream; nếu cần, thêm alias và ghi decision.

## 2. Converter

Mỗi định dạng đầu vào có một converter riêng trong `packages/markitdown/src/markitdown/converters/`.

| Thành phần | Quy tắc | Ví dụ |
|---|---|---|
| File | `_<format>_converter.py` | `_docx_converter.py`, `_pdf_converter.py` |
| Class | `<Format>Converter`, kế thừa `DocumentConverter` (hoặc converter gần nhất) | `DocxConverter`, `PdfConverter` |
| Method bắt buộc | `accepts(...)` và `convert(...)` theo signature của `DocumentConverter` | |
| Hằng số nhận diện | `ACCEPTED_MIME_TYPE_PREFIXES`, `ACCEPTED_FILE_EXTENSIONS` ở cấp module | |
| Helper không phải converter | `_<chức-năng>.py` | `_exiftool.py`, `_llm_caption.py` |

Khi thêm converter mới phải:

1. Export trong `converters/__init__.py`.
2. Đăng ký trong `MarkItDown.enable_builtins()` (`_markitdown.py`) với priority phù hợp.
3. Khai báo phụ thuộc tùy chọn mới trong `[project.optional-dependencies]` của `packages/markitdown/pyproject.toml` và thêm vào extra `all`.
4. Thêm file mẫu vào `tests/test_files/` và test vector vào `tests/_test_vectors.py`.

## 3. Plugin và package phụ

| Thành phần | Quy tắc | Ví dụ |
|---|---|---|
| Tên phân phối (PyPI) | `markitdown-<tên>` | `markitdown-ocr` |
| Tên package Python | `markitdown_<tên>` | `markitdown_ocr` |
| Thư mục | `packages/markitdown-<tên>/src/markitdown_<tên>/` | |
| Entry point plugin | nhóm `markitdown.plugin` | |

## 4. Test

| Thành phần | Quy tắc | Ví dụ |
|---|---|---|
| File test | `tests/test_<format-hoặc-chủ-đề>.py` | `tests/test_pdf.py` |
| Hàm test | `test_<hành-vi>_<điều-kiện>` (snake_case, mô tả hành vi) | `test_convert_local`, `test_missing_dependencies_and_legacy_xls_stay_separate` |
| File mẫu | `tests/test_files/<tên>.<ext>`; không chứa dữ liệu thật của người dùng | `test.docx` |
| Helper test dùng chung | module có tiền tố `_` | `_test_vectors.py` |

- Không xóa hoặc làm yếu test của upstream để test mới pass.
- Test cần mạng hoặc dịch vụ ngoài phải `skip` khi thiếu điều kiện, theo cách upstream đang làm.

## 5. File và thư mục ngoài mã nguồn

| Thành phần | Quy tắc |
|---|---|
| Hồ sơ workflow | `.ai-work/<yyyy-mm-dd>-<short-name>/` (xem `workflow.md`) |
| Kết quả chuyển đổi file | `.ai-work/conversions/<yyyy-mm-dd>-<short-name>/` (xem skill `file-to-md`) |
| Skill | `.agents/skills/<kebab-case>/SKILL.md` |
| Rule | `.agents/rules/<kebab-case>.md` |
| Script của skill | `.agents/skills/<skill>/scripts/<snake_case>.py` |

`<short-name>` dùng kebab-case, không dấu, ngắn gọn.

## 6. Ưu tiên và ngoại lệ

- Khi upstream có convention khác với tài liệu này, convention của upstream thắng; agent phải cập nhật tài liệu này.
- Chỉ dẫn cụ thể của người dùng được ưu tiên hơn mặc định.
