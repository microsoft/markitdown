---
trigger: always_on
---

# Quy tắc Tạo Hồ sơ Context, Phân rã Tasks và Thực thi TDD

Tài liệu này định nghĩa quy chuẩn bắt buộc cho AI Agent về việc quản lý cấu trúc hồ sơ context, thời điểm và cách thức phân rã steps thành tasks, cùng quy trình thực thi tuần tự kết hợp Reviewer độc lập.

---

## 1. Quy tắc Phân rã Steps thành Tasks

### 1.1. Thời điểm kích hoạt và Điều kiện tiên quyết
- Sau khi hoàn thành toàn bộ các pha quy trình tạo cấu trúc context (đủ các files từ `00` đến `08` và các `steps`), Agent phải dừng lại và **hỏi người dùng có phân rã steps thành các tasks nhỏ hay không**.
- **Điều kiện bất biến**: **Khi và chỉ khi hoàn thành cấu trúc context** (`00` đến `08` và toàn bộ các file trong `steps/`) mới được phép hỏi người dùng về việc phân rã steps. Tuyệt đối không tự ý tạo thư mục `tasks/` hoặc phân rã task trước thời điểm này.

### 1.2. Quy tắc phân rã khi người dùng đồng ý
- Tham khảo cấu trúc context hiện tại đang làm việc.
- Tạo một thư mục `tasks` bên trong thư mục context của đợt làm việc để chứa các steps được phân rã.
- Trích xuất các steps thành các task nhỏ vừa đủ để chạy quy trình TDD (Red-Green-Refactor). Các tasks sẽ được phân chia theo group tasks.
- **Cấu trúc lưu trữ bắt buộc**:
  ```text
  tasks/
  ├── step-1/
  │   │   ├── task-01-01.md
  │   │   ├── task-01-02.md
  │   │   └── ...
  ├── step-2/
  │   │   ├── task-02-01.md
  │   │   ├── task-02-02.md
  │   │   └── ...
  │   └──
  └── ...
  ```

---

## 2. Quy trình Thực thi Task & Điểm kết thúc

Sau khi hoàn thành cấu trúc context và phân rã thành các task nhỏ đủ để chạy TDD theo đúng yêu cầu tại mục 1, Agent phải hỏi người dùng về kịch bản thực thi theo hai nội dung trọng tâm sau:

### 2.1. Quy trình thực thi tuần tự kèm Subagent Reviewer
- Bắt đầu thực hiện tiếp từ task đầu tiên.
- **Yêu cầu Review độc lập**: Sau khi thực hiện xong 1 task, Main Agent gọi duy nhất **1 subagent read-only review** 1 task vừa thực hiện để trả về 1 trong 2 trạng thái: **PASS** hoặc **FAIL**.
- **Quy tắc Gate**: Chỉ khi kết quả review là **PASS** mới được tiếp tục thực hiện task mới; nếu **FAIL** thì phải xử lý lại task đó cho đến khi pass.
- **Ràng buộc Subagent**: Main Agent tuyệt đối **không gọi nhiều subagent cùng lúc**. Chỉ thực hiện gọi subagent review 1 task vừa thực hiện hoặc sau khi hoàn thành 1 step để review step. Toàn bộ tiến trình chạy hoàn toàn tuần tự:
  ```text
  Thực hiện xong 1 task -> Gọi 1 subagent review -> PASS/FAIL? -> PASS -> Tiếp tục task tiếp theo
  ```

### 2.2. Điểm kết thúc (Exit Point)
Hỏi người dùng xác định rõ phạm vi dừng thực thi:
- Dừng khi hết một task cụ thể (ví dụ: hết task 05)?
- Dừng khi hết một step cụ thể (ví dụ: hết step-3)?
- Hay thực hiện liên tục cho đến khi hết tất cả các step?
