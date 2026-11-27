# Phản biện quy trình AI sinh test

Quy trình trong `agent_skill/pseudocode.md` có ba guardrail đáng giá: audit bằng model khác, `STATIC_CHECK` trước khi chạy Newman, và triage tách bug thật khỏi giả định. Chúng xử lý đúng loại lỗi AI hay mắc: case trùng, expected mâu thuẫn, false-pass do assertion lỏng. Việc buộc ghi nguồn expected và đánh dấu GIẢ ĐỊNH cũng giúp người đọc biết chỗ nào spec chưa nói.

Nhưng audit không tạo ra góc nhìn mới. Trên 252 case, audit loại 20 INVALID và 14 INCOMPLETE, chủ yếu nhờ so trùng request/expected; nó không phát hiện lớp lỗi chỉ lộ khi đọc code như SQLite tự ép `+1`, `1.0`, `01`, JWT không có `exp`, secret hardcode, `login_attempts` tăng 2, hay `1e309` thành `null`. Vì generator và auditor dùng chung bộ tiêu chí và cùng không đọc backend, blind spot của bên này là blind spot của bên kia. Bộ Extend 16 case sau đó bắt được các lỗi này, cho thấy giá trị nằm ở nguồn oracle mới, không phải ở vòng lặp audit.

Điểm yếu thứ hai là giả định. Nhiều expected 400/401/404 không có trong spec; nếu triage không tách chúng, báo cáo sẽ biến sắc thái thành bug. Ngược lại, các case crash SUT được giữ fail thay vì vá expected, đó là hành vi đúng.

Tóm lại, guardrail làm AI nhất quán và trung thực hơn, nhưng không thay được người đọc code, chọn oracle và quyết định đâu là bug.
