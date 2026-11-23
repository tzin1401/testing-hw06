# AI Audit Log – HW06 API Testing

Sinh viên 23120190. Quy tắc ghi: xem [agent.md](../agent.md) mục 1.

## #1 – 2026-11-24 01:49 (giờ VN)
- **AI tool:** omp Manager (openai-codex/gpt-6.1-sol), phối hợp scout phân tích spec và sonic thực thi happy path
- **API / Bước:** API 1, API 2, API 3 – Bước 0: Phân tích spec
- **Prompt:**
  > . Bước 0 – Phân tích spec cho 3 API (API 1 Login, API 2 Hủy đơn, API 3 Product CRUD). Bước này ĐƯỢC gửi request vào SUT, nhưng VẪN KHÔNG đọc eshop-sut/backend/.
  > 1. Chạy scripts/reset_sut.sh.
  > 2. Đọc eshop-sut/README.md và eshop-sut/api_specification.md. Với MỖI API (Product CRUD tách 3 endpoint POST, PUT, DELETE), lập:
  >    a) Bảng tham số: tên | vị trí (path/header/body) | kiểu | bắt buộc? | ràng buộc theo spec | trích dòng spec.
  >       Tính cả header Authorization và path param :id.
  >    b) Các trạng thái và sự kiện liên quan:
  >       - Login: bộ đếm sai, khóa 30 giây, mở khóa, đăng nhập đúng reset bộ đếm (FR-02).
  >       - Hủy đơn: 5 trạng thái pending/confirmed/shipping/delivered/canceled, ai được hủy ở trạng thái nào (FR-10, FR-20).
  >       - Product: vòng đời tạo → sửa → xóa (FR-15).
  >    c) Yêu cầu bảo mật SEC-01..SEC-07 và FR-12 nào áp dụng cho API này, và áp dụng như thế nào.
  >    d) Hình dạng response theo spec. Spec nói gì, không nói gì.
  >    e) Danh sách chỗ spec MƠ HỒ hoặc mâu thuẫn (ví dụ: mã lỗi không ghi, api_specification.md và README khác nhau).
  >    f) Các API phụ cần để dựng precondition (register, cart, checkout, admin đổi trạng thái đơn, GET /api/products/:id, GET /api/categories).
  > 3. Gọi thật bằng curl chỉ các happy path sau, ghi lại status code và body THẬT (che token, chỉ giữ 10 ký tự đầu):
  >    POST /api/login (test@eshop.com); POST /api/cart rồi POST /api/checkout bằng user test; PUT /api/orders/<id vừa tạo>/cancel; POST /api/products, PUT /api/products/<id vừa tạo>, DELETE /api/products/<id vừa tạo> bằng token admin; GET /api/categories.
  >    Ghi rõ: đây là "response quan sát được", KHÔNG phải expected. Không suy luận bug ở bước này.
  > 4. Ghi tất cả vào report/01_spec_analysis.md, mỗi API một mục.
  > Xong khi: report/01_spec_analysis.md có đủ a)–f) cho 3 API (Product tách 3 endpoint), có response thật của mọi happy path ở mục 3, không có dòng nào lấy từ eshop-sut/backend/.
  >
  > Read-only deliverable: supply complete ready-to-save a–f markdown with accurate line citations for BOTH docs, full constraints and SEC-01..07 mapping per API (explicit indirect/not applicable). No observations invented. Steps 1/3 handled independently, step4 by manager.
- **AI output:**
  > Tạo report/01_spec_analysis.md: bảng tham số, trạng thái, bảo mật, response contract, điểm mơ hồ và API dựng precondition cho Login, Hủy đơn và từng endpoint Product CRUD. Reset SUT và ghi 9 response happy path localhost thực tế, token chỉ giữ 10 ký tự đầu. Tách quan sát khỏi expected; không đọc code SUT, không kết luận bug. Manager giữ quyền ghi file/log và commit; scout chỉ đọc spec, sonic chỉ thực thi. Dừng sau Bước 0, chưa sinh test case.
- **Human review:** _(để trống – sinh viên tự điền)_
