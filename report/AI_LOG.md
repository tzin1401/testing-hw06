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

## #2 – 2026-11-24 14:41 (giờ VN)
- **AI tool:** task LoginG1 – OpenAI Codex (openai-codex/gpt-6.1-terra); Manager kiểm tra và ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** API 1 – Generate – LG-G1: Domain partition + boundary
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Generate (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - Repo: https://github.com/tzin1401/testing-hw06 (remote origin). KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit).
  > - Sinh viên: MSSV 23120190. Mọi request khi chạy sau này sẽ có header X-Student-Id: 23120190 (do pre-request script thêm, KHÔNG cần ghi vào từng test case).
  > - SUT: EShop backend, Node.js + Express + SQLite, base URL http://localhost:3000. Reset bằng scripts/reset_sut.sh (DB seed lại, cart trong RAM bị xóa).
  > - Tài khoản seed: admin@eshop.com / Admin123! (role admin); test@eshop.com / Test1234! (role user). Sản phẩm seed id 1..5, danh mục seed có sẵn.
  > - Nguồn yêu cầu DUY NHẤT để suy ra expected result: eshop-sut/README.md (FR-xx, SEC-01..SEC-07) và eshop-sut/api_specification.md, cùng report/01_spec_analysis.md (sau bước 0).
  > - CẤM đọc eshop-sut/backend/ và eshop-sut/frontend-*. Ở các bước G1–G5, CẤM gửi request vào SUT. Lý do: test case phải sinh từ spec, không chép theo code.
  > - 3 API được giao:
  >   API 1 – FR-02 Login: POST /api/login, tiền tố ID "LG", file report/testcases/API1_login_generated.md
  >   API 2 – FR-10 User hủy đơn: PUT /api/orders/:id/cancel, tiền tố "CN", file report/testcases/API2_cancel_generated.md
  >   API 3 – FR-15 Product CRUD: POST /api/products, PUT /api/products/:id, DELETE /api/products/:id, tiền tố "PR", file report/testcases/API3_product_generated.md
  > - Định dạng test case: mỗi bước nối thêm (append) MỘT mục "## <Gx> – <tên kỹ thuật>" vào file của API, chứa MỘT bảng Markdown với đúng các cột:
  >   | ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
  >   * ID: <tiền tố>-<G1|G2|G3|G4>-<2 chữ số>, ví dụ LG-G1-01. Không trùng.
  >   * Kỹ thuật: EP (phân hoạch tương đương), BVA (giá trị biên), ST (chuyển trạng thái), SEC, SCH (schema).
  >   * Requirement: FR-xx và/hoặc SEC-xx.
  >   * Precondition: phải TỰ TẠO dữ liệu của mình (ví dụ đăng ký user mới bằng POST /api/register với email duy nhất kiểu lg_{{timestamp}}@test.com, tạo đơn bằng POST /api/cart + POST /api/checkout, đổi trạng thái đơn bằng PUT /api/admin/orders/:id/status với token admin). Test này không được phụ thuộc kết quả test khác.
  >   * Request: method, path, header cần thiết (Authorization), body JSON cụ thể. Phải đủ để chuyển thẳng thành request Postman.
  >   * Expected: status code + điều kiện trên body. Không viết chung chung kiểu "trả lỗi".
  >   * Nguồn expected: trích dòng spec (ví dụ "README FR-02: khóa 30 giây"). Nếu spec KHÔNG nói rõ (ví dụ mã 400 hay 422), ghi "GIẢ ĐỊNH: <lý do>" để người dùng audit.
  > - Sau bảng, ghi 2–4 dòng "Ghi chú của AI": phần nào chưa chắc, phần nào spec mơ hồ. KHÔNG tự đánh nhãn VALID/INVALID/INCOMPLETE (đó là việc của sinh viên ở bước Audit).
  > - Quy tắc AI log: prompt có cụm "" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng trong agent.md mục 1. AI tool = tên agent + model của chính bạn. Thời gian lấy bằng lệnh `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN (bỏ cụm ""). Mục Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - Cấm: bịa response của SUT; sửa code SUT; sửa mục của bước khác trong file test case.
  > - Cuối mỗi lần làm: báo lại cho Manager file đã tạo/sửa, số test case đã thêm và bằng chứng cho từng tiêu chí "Xong khi".
  >
  > . API 1 – Login – G1: sinh test case bằng phân hoạch tương đương (EP) và giá trị biên (BVA) cho POST /api/login.
  > Input: mục API 1 trong report/01_spec_analysis.md.
  > Làm lần lượt từng tham số. Với MỖI tham số, trước khi viết test case, liệt kê các lớp hợp lệ và không hợp lệ:
  >   - email: đúng và tồn tại; đúng format nhưng không tồn tại; sai format (thiếu @, thiếu domain, có khoảng trắng); chuỗi rỗng; thiếu field; null; kiểu số; chữ hoa/thường khác với lúc đăng ký; khoảng trắng đầu/cuối; rất dài.
  >   - password: đúng; sai một ký tự; sai hoa/thường; rỗng; thiếu field; null; kiểu số; rất dài.
  >   - Body tổng thể: body rỗng {}; JSON sai cú pháp; Content-Type không phải JSON; field thừa.
  > Mỗi lớp ít nhất 1 test case. Lớp không hợp lệ thì mỗi test case chỉ sai MỘT tham số.
  > Precondition: mỗi test tự đăng ký user mới (email duy nhất) để không làm khóa tài khoản test@eshop.com.
  > Tạo file report/testcases/API1_login_generated.md, có tiêu đề "# API 1 – POST /api/login – Test case do AI sinh", rồi append mục "## G1 – Domain partition + boundary". Bảng EP/BVA đặt trước bảng test case.
  > Xong khi: mỗi tham số có bảng lớp và ít nhất 1 test case cho mỗi lớp, tối thiểu 14 test case, ID LG-G1-xx, cột "Nguồn expected" có trích spec hoặc ghi GIẢ ĐỊNH.
- **AI output:**
  > Tạo report/testcases/API1_login_generated.md với 25 test case LG-G1-01–25: 13 lớp email, 8 lớp password, 4 lớp body; bảng lớp ánh xạ ID trước bảng test 9 cột. Mỗi case đăng ký user riêng bằng email có case ID và UUID. Expected chưa được spec quy định được ghi GIẢ ĐỊNH. Manager yêu cầu bổ sung method/path/header trong từng Request và định nghĩa nguồn R/A. Không đọc implementation, không gọi SUT, không thực hiện bước tiếp theo.
- **Human review:** _(để trống – sinh viên tự điền)_
