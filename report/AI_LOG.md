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
- **Human review:** Đã đọc lại bảng tham số và các response happy path; chấp nhận dùng làm nguồn expected. Phần status/schema lỗi còn mơ hồ giữ nguyên để các bước sau ghi GIẢ ĐỊNH.

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
- **Human review:** Duyệt 25 case LG-G1: đủ lớp email/password/body. Đồng ý LG-G1-14 trùng LG-G1-01; các giả định trim, không phân biệt hoa-thường và mốc 4096 là chưa có trong spec nên chỉ dùng để thăm dò.

## #3 – 2026-11-24 14:51 (giờ VN)
- **AI tool:** LGG2 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** LG-G2 – Generate
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
  > . API 1 – Login – G2: sinh test case chuyển trạng thái cho FR-02 (bộ đếm sai và khóa tài khoản).
  > Input: report/01_spec_analysis.md (mục API 1) và mục G1 đã có trong report/testcases/API1_login_generated.md (đọc để KHÔNG trùng).
  > 1. Vẽ bảng trạng thái (dạng bảng Markdown, không cần hình): trạng thái = số lần sai liên tiếp (0, 1, 2, khóa); sự kiện = login sai, login đúng, hết 30 giây. Ghi rõ trạng thái kế tiếp và response mong đợi cho từng cặp (trạng thái, sự kiện), kể cả cặp KHÔNG hợp lệ.
  > 2. Từ bảng, sinh test case phủ:
  >    - Mọi chuyển trạng thái hợp lệ (0-switch coverage).
  >    - Các chuỗi 2 bước quan trọng (1-switch), ví dụ: sai 2 lần → đúng → sai 2 lần → vẫn chưa khóa.
  >    - Biên của bộ đếm: sai đúng 2 lần thì chưa khóa; lần thứ 3 thì khóa; bộ đếm tăng đúng 1 mỗi lần sai.
  >    - Biên thời gian: đăng nhập đúng ngay khi bị khóa; ở giây ~29 vẫn khóa; sau 30 giây (dùng ~31 giây) mở khóa.
  >    - Thông báo khi bị khóa không lộ nguyên nhân chi tiết (FR-02).
  >    - Khóa của user A không ảnh hưởng user B.
  > Cột Precondition ghi rõ chuỗi request và thời gian chờ (ví dụ "đợi 31 giây"), để sau này làm được bằng Postman (setTimeout) hoặc Collection Runner.
  > Append mục "## G2 – State transition" vào report/testcases/API1_login_generated.md.
  > Xong khi: có bảng trạng thái, mọi ô của bảng có ít nhất 1 test case phủ, tối thiểu 8 test case, ID LG-G2-xx, không trùng G1.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API1_login_generated.md
- **AI output:**
  > Append G2: 12 case ST LG-G2-01–12; ma trận 4×3 có ID từng ô, ngưỡng 2/3 lần, chờ 29/31 giây, reset/cách ly tài khoản. Manager đọc phần mới và kiểm tra tĩnh đạt; không gọi SUT, các điểm spec chưa rõ ghi GIẢ ĐỊNH.
- **Human review:** Duyệt 12 case LG-G2: ngưỡng 2/3 lần và chờ 29/31 giây đúng FR-02. Đồng ý LG-G2-02 trùng LG-G2-01; chấp nhận giả định không gia hạn khóa để chạy.

## #4 – 2026-11-24 14:51 (giờ VN)
- **AI tool:** CNG1 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** CN-G1 – Generate
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
  > . API 2 – Hủy đơn – G1: sinh test case EP và BVA cho PUT /api/orders/:id/cancel.
  > Input: mục API 2 trong report/01_spec_analysis.md.
  > Làm lần lượt từng tham số, trước hết liệt kê lớp hợp lệ/không hợp lệ:
  >   - Path :id: đơn của chính user (dùng trạng thái pending ở bước này); id không tồn tại; 0; số âm; số rất lớn (2147483648, 9999999999); số thập phân 1.5; chuỗi chữ "abc"; ký tự đặc biệt; khoảng trắng.
  >   - Header Authorization: token user hợp lệ; thiếu header; "Bearer " không có token; sai scheme (Basic ...); token sai chữ ký; token rác.
  >   - Body: không cần body; gửi body thừa (ví dụ {"status":"delivered"}) không được làm đổi kết quả.
  > Mỗi lớp ít nhất 1 test; lớp không hợp lệ thì mỗi test chỉ sai MỘT tham số.
  > Precondition mẫu: đăng ký user mới → login lấy token → POST /api/cart (sản phẩm id 1) → POST /api/checkout → lấy orderId.
  > Tạo file report/testcases/API2_cancel_generated.md, có tiêu đề "# API 2 – PUT /api/orders/:id/cancel – Test case do AI sinh", rồi append mục "## G1 – Domain partition + boundary". Bảng EP/BVA đặt trước bảng test case.
  > Xong khi: mỗi tham số có bảng lớp và test cho từng lớp, tối thiểu 12 test case, ID CN-G1-xx, có Nguồn expected hoặc GIẢ ĐỊNH.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Tạo API2_cancel_generated.md với 16 case (12 EP, 4 BVA), bảng lớp path/auth/body có ánh xạ; setup đơn riêng và xác minh ID vắng mặt, kiểm tra trạng thái sau request. Manager đọc và kiểm tra 9 cột/ID/request/nguồn đạt; không gọi SUT.
- **Human review:** Duyệt 16 case CN-G1: phủ đủ path id, Authorization và body. Các case 02/05/06 cần xác minh ID vắng qua danh sách admin nên sẽ ghi chú điều kiện khi chạy.

## #5 – 2026-11-24 14:52 (giờ VN)
- **AI tool:** PRG1 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-G1 – Generate
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
  > . API 3 – Product CRUD – G1: sinh test case EP và BVA cho POST /api/products và PUT /api/products/:id (DELETE chỉ có path id, gộp vào đây).
  > Input: mục API 3 trong report/01_spec_analysis.md.
  > Làm lần lượt từng tham số, trước hết liệt kê lớp hợp lệ/không hợp lệ và giá trị biên:
  >   - name (FR-15: bắt buộc, tối đa 255): thiếu; rỗng ""; chỉ khoảng trắng; 1 ký tự; 254; 255; 256 ký tự; tiếng Việt có dấu; null; kiểu số.
  >   - price (FR-15: bắt buộc, > 0): thiếu; 0; -1; 0.01; 1; số rất lớn (1e15); chuỗi số "100000"; chuỗi chữ "abc"; null; boolean.
  >   - category_id (FR-15: bắt buộc, phải có sẵn): thiếu; id có trong GET /api/categories; id không tồn tại (99999); 0; âm; chuỗi.
  >   - description, imageUrl: thiếu; rỗng; rất dài; imageUrl không phải URL.
  >   - Path :id cho PUT và DELETE: id tồn tại; không tồn tại; 0; âm; "abc".
  >   - Body tổng thể: {} ; JSON sai cú pháp; field thừa (ví dụ "id": 1 trong body POST).
  > Mỗi lớp ít nhất 1 test; lớp không hợp lệ thì mỗi test chỉ sai MỘT tham số. Dùng token admin (admin@eshop.com) cho mọi test ở bước này. Với PUT, gửi đủ các field khác hợp lệ.
  > Tạo file report/testcases/API3_product_generated.md, có tiêu đề "# API 3 – Product CRUD – Test case do AI sinh", rồi append mục "## G1 – Domain partition + boundary". Bảng EP/BVA đặt trước bảng test case; cột Request ghi rõ endpoint nào.
  > Xong khi: mỗi tham số có bảng lớp/biên và test cho từng lớp, phủ cả POST, PUT, DELETE, tối thiểu 15 test case, ID PR-G1-xx, có Nguồn expected hoặc GIẢ ĐỊNH.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API3_product_generated.md
- **AI output:**
  > Tạo API3_product_generated.md với 46 case EP/BVA, phủ mọi lớp name/price/category/description/imageUrl/path/body và POST/PUT/DELETE. Setup admin, sản phẩm riêng, ID vắng mặt xác minh, snapshot dữ liệu. Manager đọc và kiểm tra tĩnh đạt; không gọi SUT.
- **Human review:** Duyệt 46 case PR-G1: phủ name/price/category/description/imageUrl/path/body. Loại PR-G1-04 vì nhận diện theo tên 'a' dễ pass nhầm; 22/35/39/40 trùng case khác.

## #6 – 2026-11-24 14:53 (giờ VN)
- **AI tool:** LGG3 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** LG-G3 – Generate
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
  > . API 1 – Login – G3: sinh test case bảo mật cho POST /api/login.
  > Input: report/01_spec_analysis.md (mục API 1, phần c) và các mục G1, G2 đã có (đọc để không trùng).
  > Đi lần lượt từng yêu cầu. Với mỗi yêu cầu, viết 1 dòng "áp dụng cho login như thế nào" rồi sinh test case:
  >   - SEC-05 SQL injection: payload ở email và ở password (ví dụ ' OR '1'='1, admin@eshop.com'--, UNION). Expected: không đăng nhập được, không trả lỗi CSDL thô.
  >   - SEC-01: response login thành công KHÔNG được chứa mật khẩu (dù plaintext hay hash).
  >   - FR-02 không lộ nguyên nhân: email không tồn tại và mật khẩu sai phải trả CÙNG status và CÙNG thông điệp (chống dò email).
  >   - Token: JWT có 3 phần; payload chứa id và role đúng với user (decode base64, không cần secret); user thường thì role = "user".
  >   - Brute force: khóa theo FR-02 có thật sự chặn thử tiếp không.
  >   - Input độc hại khác: chuỗi rất dài (10.000 ký tự), ký tự điều khiển, kiểu object/array thay cho string (ví dụ {"$ne": null}).
  > Append mục "## G3 – Security" vào report/testcases/API1_login_generated.md.
  > Xong khi: mỗi yêu cầu ở trên có ít nhất 1 test case, tối thiểu 8 test case, ID LG-G3-xx, cột Requirement ghi SEC-xx hoặc FR-02.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API1_login_generated.md
- **AI output:**
  > Append G3: 17 case SEC, gồm SQLi email/password, rò password, chống dò email, JWT, brute force, input 10000 ký tự/control/object/array. Setup riêng và kiểm tra tài khoản sau tấn công. Manager đọc và kiểm tra tĩnh đạt; không request SUT, các diễn giải bảo mật ghi giả định.
- **Human review:** Duyệt 17 case LG-G3: SQLi, JWT, brute force, input dài/điều khiển/object/array đủ. Đồng ý LG-G3-06 trùng LG-G4-03.

## #7 – 2026-11-24 14:54 (giờ VN)
- **AI tool:** PRG2 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-G2 – Generate
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
  > . API 3 – Product CRUD – G2: sinh test case chuyển trạng thái theo vòng đời sản phẩm.
  > Input: report/01_spec_analysis.md (mục API 3), mục G1 đã có (đọc để không trùng).
  > 1. Lập bảng trạng thái: trạng thái = chưa tồn tại, đang tồn tại, đã xóa; sự kiện = POST, GET /api/products/:id, PUT, DELETE. Ghi trạng thái kế tiếp và response mong đợi cho từng cặp, kể cả cặp không hợp lệ (PUT/DELETE sản phẩm đã xóa, xóa 2 lần).
  > 2. Sinh test phủ mọi ô của bảng, và các chuỗi:
  >    - POST → GET thấy đúng dữ liệu vừa tạo → PUT → GET thấy dữ liệu mới → DELETE → GET và GET /api/products không còn.
  >    - FR-15 "khi sửa một sản phẩm, chỉ sản phẩm đó bị thay đổi": lưu snapshot GET /api/products trước, PUT 1 sản phẩm, so sánh các sản phẩm khác giữ nguyên.
  >    - Tạo 2 sản phẩm trùng tên (spec có cấm không? ghi GIẢ ĐỊNH nếu mơ hồ).
  >    - PUT chỉ gửi một phần field: các field không gửi có bị xóa trắng không (spec có nói không?).
  > Precondition: tự tạo sản phẩm bằng POST với token admin. KHÔNG sửa/xóa sản phẩm seed id 1..5, trừ test so sánh snapshot (chỉ GET).
  > Append mục "## G2 – State transition (vòng đời sản phẩm)" vào report/testcases/API3_product_generated.md.
  > Xong khi: có bảng trạng thái, mọi ô có ít nhất 1 test, có test FR-15 "chỉ sản phẩm đó bị thay đổi", tối thiểu 8 test case, ID PR-G2-xx.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API3_product_generated.md
- **AI output:**
  > Append G2: 16 case ST, bảng 3 trạng thái×4 sự kiện gắn ID từng ô; vòng đời đầy đủ, snapshot FR-15 chỉ sửa đích, trùng tên và partial PUT. Manager yêu cầu chuyển bullets thành bảng đúng tiêu chí rồi kiểm tra tĩnh đạt; không gọi SUT, lifecycle/status chưa quy định ghi GIẢ ĐỊNH.
- **Human review:** Duyệt 16 case PR-G2: 12 ô chuyển trạng thái đều có case. 01/07/09 trùng; PR-G2-16 (PUT một phần) sẽ đổi expected sang 400 theo quy ước full PUT.

## #8 – 2026-11-24 14:54 (giờ VN)
- **AI tool:** LGG4 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** LG-G4 – Generate
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
  > . API 1 – Login – G4: sinh test case kiểm tra schema response cho POST /api/login.
  > Input: report/01_spec_analysis.md (mục API 1, phần d và response quan sát ở mục 3) và các mục G1–G3.
  > 1. Viết JSON Schema (draft-07) cho:
  >    a) response 200: theo spec "trả về chuỗi JWT token và thông tin user". Field nào spec nói thì required; field nào chỉ thấy khi quan sát thì ghi chú "quan sát, spec không nói". Ghi rõ những field KHÔNG được có (password).
  >    b) response lỗi (401/403/400): object có field error kiểu string.
  >    Đặt schema trong khối ```json để sau này dán vào Postman (pm.response.to.have.jsonSchema).
  > 2. Sinh test case kiểm tra: status code; header Content-Type là application/json; body khớp schema; kiểu từng field (id là integer, token là string không rỗng, role thuộc {"user","admin"}); không có field thừa nhạy cảm; response lỗi cũng khớp schema lỗi; thời gian phản hồi < 2000 ms.
  > Append mục "## G4 – Schema validation" vào report/testcases/API1_login_generated.md.
  > Xong khi: có 2 JSON Schema hợp lệ (parse được), tối thiểu 5 test case, ID LG-G4-xx.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API1_login_generated.md
- **AI output:**
  > Append G4: 7 case SCH và 2 JSON Schema draft07 (success/error), kiểm tra status/media type/kiểu user/sensitive/error/timing. Chỉ token,user required theo spec; field quan sát tùy chọn, các ràng buộc khác ghi giả định. Manager đọc và kiểm tra parse/meta-schema đạt, không gọi SUT.
- **Human review:** Duyệt 7 case LG-G4: schema 200/lỗi và timing rõ. LG-G4-04/05 phải đọc status 400/423 theo quy ước G6 thay vì 401/403.

## #9 – 2026-11-24 14:54 (giờ VN)
- **AI tool:** CNG2 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** CN-G2 – Generate
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
  > . API 2 – Hủy đơn – G2: sinh test case chuyển trạng thái theo FR-10 cho thao tác User hủy đơn.
  > Input: report/01_spec_analysis.md (mục API 2), sơ đồ FR-10 trong eshop-sut/README.md, mục G1 đã có (đọc để không trùng).
  > 1. Lập bảng chuyển trạng thái đầy đủ 5×5: hàng = trạng thái hiện tại (pending, confirmed, shipping, delivered, canceled); cột = trạng thái đích; ô = hợp lệ/không hợp lệ và AI ĐƯỢC chuyển (User qua /cancel, Admin qua /api/admin/orders/:id/status). Trích dòng spec cho từng ô.
  > 2. Sinh test case cho thao tác User hủy (PUT /api/orders/:id/cancel) ở TỪNG trạng thái nguồn: pending, confirmed, shipping, delivered, canceled. Ghi rõ expected status và trạng thái đơn sau đó (kiểm tra lại bằng GET /api/orders/:id hoặc GET /api/orders/my-orders).
  > 3. Sinh test chuỗi (1-switch): hủy 2 lần liên tiếp; pending → confirmed → hủy; confirmed → shipping → hủy (User không được hủy); sau khi hủy, Admin thử chuyển canceled → confirmed / shipping / delivered (trạng thái kết thúc phải bị từ chối).
  > 4. Sinh test "hủy không làm đổi đơn khác": user có 2 đơn, hủy 1 đơn thì đơn kia giữ nguyên trạng thái.
  > Precondition: dựng trạng thái bằng token admin (admin@eshop.com) gọi PUT /api/admin/orders/:id/status lần lượt theo đúng đường đi hợp lệ.
  > Append mục "## G2 – State transition (FR-10)" vào report/testcases/API2_cancel_generated.md.
  > Xong khi: có bảng 5×5, đủ 5 trạng thái nguồn cho User hủy, có test chuỗi và test trạng thái kết thúc, tối thiểu 10 test case, ID CN-G2-xx.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Append G2: 13 case ST, ma trận 5×5 đủ nguồn/actor/ID từng ô; User cancel từ 5 trạng thái, chuỗi, final states, cách ly hai đơn. Request macros U/A/K được định nghĩa đầy đủ; manager đọc và kiểm tra tĩnh đạt. Shipping Admin/self-transition/status giả định, không gọi SUT.
- **Human review:** Duyệt 13 case CN-G2: ma trận 5×5 có ID từng ô, self-transition ghi giả định. 01/11/12 trùng case khác.

## #10 – 2026-11-24 14:56 (giờ VN)
- **AI tool:** PRG3 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-G3 – Generate
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
  > . API 3 – Product CRUD – G3: sinh test case bảo mật cho POST/PUT/DELETE /api/products.
  > Input: report/01_spec_analysis.md (mục API 3, phần c), các mục G1, G2 đã có.
  > Đi lần lượt từng yêu cầu, mỗi yêu cầu viết 1 dòng "áp dụng thế nào" rồi sinh test cho CẢ 3 method:
  >   - FR-12 + SEC-02: không có token → bị từ chối, sản phẩm không được tạo/sửa/xóa (kiểm tra lại bằng GET).
  >   - FR-12 + SEC-03 leo quyền: token của user thường (test@eshop.com) → bị từ chối. Thêm: user tự sửa role bằng PUT /api/users/me {"role":"admin"} rồi login lại và gọi API sản phẩm (SEC-06 kết hợp SEC-03).
  >   - Token giả mạo: JWT tự ký với {"id":1,"role":"admin"} bằng secret đoán, hoặc token alg "none" → bị từ chối.
  >   - SEC-05 SQL injection ở name, description và path id (ví dụ 1 OR 1=1 cho DELETE) → không làm hỏng/xóa dữ liệu khác; kiểm tra lại số sản phẩm.
  >   - SEC-04 stored XSS: name = <script>alert(1)</script> hoặc <img src=x onerror=alert(1)>. Ở mức API: ghi expected theo spec (từ chối hoặc lưu nguyên văn để UI escape) và GIẢ ĐỊNH nếu spec mơ hồ.
  >   - Mass assignment: gửi "id" hoặc field lạ trong body POST/PUT để ghi đè sản phẩm khác.
  > Append mục "## G3 – Security" vào report/testcases/API3_product_generated.md.
  > Xong khi: mỗi yêu cầu trên có test cho cả POST, PUT, DELETE nếu áp dụng, tối thiểu 10 test case, ID PR-G3-xx, có bước kiểm tra lại dữ liệu sau tấn công.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API3_product_generated.md
- **AI output:**
  > Append G3: 22 case SEC; no-token/user-role/profile-escalation/forged-JWT phủ 3 methods; SQLi name/description/path, XSS và mass assignment khi áp dụng. Snapshot và GET kiểm tra dữ liệu sau từng tấn công, không tác động seed trực tiếp; manager đọc và kiểm tra tĩnh đạt, không gọi SUT.
- **Human review:** Duyệt 22 case PR-G3: đủ thiếu token, user thường, token giả, SQLi, XSS và mass assignment. Thiếu alg none đã được bổ sung ở G6.

## #11 – 2026-11-24 14:56 (giờ VN)
- **AI tool:** CNG3 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** CN-G3 – Generate
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
  > . API 2 – Hủy đơn – G3: sinh test case bảo mật cho PUT /api/orders/:id/cancel.
  > Input: report/01_spec_analysis.md (mục API 2, phần c), các mục G1, G2 đã có.
  > Đi lần lượt từng yêu cầu, mỗi yêu cầu viết 1 dòng "áp dụng thế nào" rồi sinh test:
  >   - IDOR / FR-11: user B hủy đơn của user A → bị từ chối, đơn của A giữ nguyên trạng thái (kiểm tra lại). Thử cả với đơn A ở trạng thái pending và confirmed.
  >   - SEC-02: không token, token hết hạn/sai chữ ký, token của user đã bị admin xóa (DELETE /api/admin/users/:id).
  >   - Token giả mạo: JWT tự ký với {"id": <id của A>, "role":"user"} bằng secret đoán (ví dụ "secret") → phải bị từ chối.
  >   - SEC-05: SQL injection ở path id (1 OR 1=1, 1;DROP TABLE orders, 1' --) → không hủy đơn nào, không lộ lỗi CSDL; kiểm tra các đơn khác vẫn nguyên.
  >   - Admin dùng endpoint của user để hủy đơn người khác: spec có cho phép không? Ghi GIẢ ĐỊNH nếu mơ hồ.
  >   - Dò ID: id liên tiếp của người khác trả mã khác với id không tồn tại có làm lộ thông tin không.
  > Append mục "## G3 – Security" vào report/testcases/API2_cancel_generated.md.
  > Xong khi: mỗi yêu cầu trên có ít nhất 1 test, tối thiểu 8 test case, ID CN-G3-xx, có bước kiểm tra lại trạng thái đơn sau mỗi tấn công.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Append G3: 12 case SEC (IDOR pending/confirmed, JWT absent/expired/signature/deleted/forged, 3 SQLi, admin route, enumeration). Setup hai user/hai đơn độc lập, GET sau từng tấn công; điều kiện exp và deleted-user ghi rõ. Manager đọc và kiểm tra tĩnh đạt; không gọi SUT.
- **Human review:** Duyệt 12 case CN-G3: IDOR, token, SQLi và dò ID đủ. 03/05 trùng; 01/02 đổi 403 thành 404 theo quy ước G6.

## #12 – 2026-11-24 14:57 (giờ VN)
- **AI tool:** CNG4 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** CN-G4 – Generate
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
  > . API 2 – Hủy đơn – G4: sinh test case kiểm tra schema cho PUT /api/orders/:id/cancel và response GET /api/orders/:id dùng để kiểm tra lại.
  > Input: report/01_spec_analysis.md (mục API 2, phần d và response quan sát), các mục G1–G3.
  > 1. Viết JSON Schema (draft-07) cho: response hủy thành công; response lỗi ({error: string}); object đơn hàng (id, user_id, total_amount, status thuộc enum 5 trạng thái, shipping_address, created_at). Field nào spec không nói thì ghi chú "quan sát, spec không nói".
  > 2. Sinh test: status code; Content-Type JSON; body khớp schema; sau khi hủy, đơn có status đúng bằng "canceled" (đúng chính tả của spec); lỗi 4xx cũng khớp schema lỗi; thời gian phản hồi < 2000 ms.
  > Append mục "## G4 – Schema validation" vào report/testcases/API2_cancel_generated.md.
  > Xong khi: có 3 JSON Schema parse được, tối thiểu 5 test case, ID CN-G4-xx.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Append G4: 6 case SCH và 3 JSON Schema draft07 cho cancel success/error/order GET; kiểm tra status/media/schema/canceled spelling/error/timing. Phân biệt field message quan sát và field GET chưa quan sát. Manager đọc, parse và Draft7 metaschema đạt; không gọi SUT.
- **Human review:** Duyệt 6 case CN-G4: schema success/error/GET và timing rõ. 03/04 trùng; các case phụ thuộc exp hoặc xóa user sẽ đánh dấu không chạy được nếu setup không đạt.

## #13 – 2026-11-24 14:57 (giờ VN)
- **AI tool:** PRG4 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-G4 – Generate
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
  > . API 3 – Product CRUD – G4: sinh test case kiểm tra schema cho POST/PUT/DELETE /api/products và GET /api/products/:id dùng để kiểm tra lại.
  > Input: report/01_spec_analysis.md (mục API 3, phần d và response quan sát), các mục G1–G3.
  > 1. Viết JSON Schema (draft-07) cho: response POST thành công (theo response quan sát, ghi chú field nào spec không nói); response PUT và DELETE thành công; response lỗi ({error: string}); object sản phẩm (id integer, name string, price NUMBER > 0, description, imageUrl, category_id integer).
  > 2. Sinh test: status code; Content-Type JSON; body khớp schema; GET sau POST trả price đúng KIỂU number (không phải chuỗi) và đúng giá trị đã gửi; GET sau PUT trả đúng giá trị mới; kiểm tra kiểu price trên nhiều sản phẩm khác nhau (cả id chẵn và lẻ) vì spec mục 3.3 dùng price dạng số; lỗi 4xx khớp schema lỗi; thời gian < 2000 ms.
  > Append mục "## G4 – Schema validation" vào report/testcases/API3_product_generated.md.
  > Xong khi: có 4 JSON Schema parse được, tối thiểu 6 test case, ID PR-G4-xx.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API3_product_generated.md
- **AI output:**
  > Append G4: 8 case SCH, 4 Draft07 schemas (POST, PUT/DELETE, error, product), price number/round-trip và id chẵn/lẻ từ sản phẩm tự tạo, 4xx và timing. Manager đọc và kiểm tra parse/metaschema đạt, không gọi SUT; response chưa đặc tả ghi giả định.
- **Human review:** Duyệt 8 case PR-G4: schema POST/PUT/DELETE/lỗi và kiểu price. Case 07 phụ thuộc id chẵn-lẻ nên chỉ chạy khi setup đủ.

## #14 – 2026-11-24 14:59 (giờ VN)
- **AI tool:** LGG5 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** LG-G5 – Generate
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
  > . API 1 – Login – G5: rà soát độ phủ bộ test case AI đã sinh cho POST /api/login. KHÔNG đánh nhãn VALID/INVALID/INCOMPLETE, đó là việc của sinh viên.
  > Input: report/testcases/API1_login_generated.md, report/01_spec_analysis.md, eshop-sut/README.md (FR-02, SEC-01..07).
  > 1. Tìm test case trùng hoặc gần trùng giữa các mục G1–G4. Liệt kê cặp ID và lý do; không xóa.
  > 2. Lập ma trận độ phủ: hàng = từng yêu cầu (mỗi gạch đầu dòng FR-02, mỗi SEC áp dụng, mỗi tham số); cột = EP, BVA, ST, SEC, SCH; ô = các ID phủ. Đánh dấu ô trống quan trọng.
  > 3. Kiểm tra định dạng: mỗi test có đủ cột, Request đủ để chạy, Expected cụ thể, có Nguồn expected.
  > 4. Đếm: tổng số test case (đã trừ trùng), số theo từng kỹ thuật.
  > Append mục "## G5 – Tổng hợp độ phủ (reviewer)" gồm: bảng đếm, ma trận, danh sách trùng, danh sách lỗ hổng độ phủ (mỗi lỗ hổng: yêu cầu nào, vì sao quan trọng, gợi ý 1 test case).
  > Xong khi: có bảng đếm, ma trận, kết luận rõ "ĐỦ ≥ 35" hoặc "THIẾU n case", và danh sách lỗ hổng (có thể rỗng).
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API1_login_generated.md
- **AI output:**
  > Append G5: tổng thô61, trừ3 nhóm trùng còn58 (EP20/BVA4/ST11/SEC16/SCH7), kết luận ĐỦ≥35; ma trận18×5 và danh sách5 lỗH1–H5. Phát hiện mâu thuẫn giả định statusF1 giữa G1–G3 vàG4 cần thống nhất trước Execute. Manager đọc báo cáo và kiểm tra ID tham chiếu đạt; không Audit hay SUT.
- **Human review:** Đọc báo cáo G5: đồng ý 58/61 sau khi trừ D1–D3, giữ case trùng để truy vết. F1/F2 chuyển sang G6 xử lý.

## #15 – 2026-11-24 15:01 (giờ VN)
- **AI tool:** LGG6 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** LG-G6 – Generate
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
  > . API 1 – Login – G6 bổ sung: mục G5 trong report/testcases/API1_login_generated.md báo ĐỦ 58 case nhưng còn thiếu độ phủ kỹ thuật và các lỗ hổng độ phủ sau: H1 FR-02: sau 31 giây hết khóa gửi sai trước mọi login đúng để phân biệt reset do expiry với do thành công. H2 FR-02/SEC-02: dùng JWT vừa cấp làm Bearer GET /api/users/me và kiểm danh tính. H3 chống dò email sau 3/4 lần sai: so sánh chuỗi status/message email tồn tại và email UUID chưa đăng ký. H4 login với Authorization Bearer invalid.token.value vẫn cấp token khi credentials đúng (GIẢ ĐỊNH). H5 role admin trong body login không nâng quyền user; chọn kỳ vọng cụ thể kèm giả định. F1/F2 nhất quán suite: trước bảng G6 ghi quy tắc giả định hợp nhất cho toàn tài liệu: sai credentials/input dùng400, đang khóa dùng423, error string không rỗng là giả định schema chung. Ghi rõ LG-G4-04 status401 vàLG-G4-05 status403 là các lựa chọn cũ không áp dụng khi chuyển sang Execute; không sửa hay xóa các mục cũ. Không coi các lựa chọn cũ là quy định spec. Các field/claim khác chưa nêu ghi GIẢ ĐỊNH. Đừng thêm test chỉ để echo wiring; nếu cần thêm case chứng minh schema lỗi với status400/423 thì một case chuỗi riêng cụ thể, không trùng assertions cũ. Bảo toàn G1–G5, append chỉ G6..
  > Sinh test case bổ sung để lấp ĐÚNG các lỗ hổng trên, không sinh lại case đã có. Mỗi test ghi rõ lấp lỗ hổng nào.
  > Append mục "## G6 – Bổ sung theo G5" vào report/testcases/API1_login_generated.md, ID LG-G6-xx, cùng định dạng bảng ở Bối cảnh chung.
  > Xong khi: mọi lỗ hổng được liệt kê có ít nhất 1 test, tổng số test (đã trừ trùng) ≥ 35.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API1_login_generated.md
- **AI output:**
  > Append G6: 5 case mới lấp H1–H5 (expiry reset không qua login đúng, Bearer dùng được, anti-enumeration lockout, auth header sai tại login, role injection). Quy tắc hợp nhất status400/423 và error string thay giả định cũ LG-G4-04/05 mà không sửa G1–G5. Manager đọc/check tĩnh đạt; 66 thô, dự kiến63 sau trùng chờ reviewer xác nhận; không gọi SUT.
- **Human review:** Duyệt 5 case LG-G6: lấp đúng H1–H5. Đồng ý cách so sánh lỗi tương đối ở H3 và dùng GET /api/users/me để kiểm token.

## #16 – 2026-11-24 15:03 (giờ VN)
- **AI tool:** PRG5 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-G5 – Generate
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
  > . API 3 – Product CRUD – G5: rà soát độ phủ bộ test case AI đã sinh cho Product CRUD. KHÔNG đánh nhãn VALID/INVALID/INCOMPLETE.
  > Input: report/testcases/API3_product_generated.md, report/01_spec_analysis.md, eshop-sut/README.md (FR-12, FR-15, SEC-02..06).
  > 1. Liệt kê test trùng hoặc gần trùng giữa G1–G4 (cặp ID và lý do; không xóa).
  > 2. Ma trận độ phủ: hàng = mỗi ràng buộc FR-15 (name, price, category, chỉ sửa 1 sản phẩm) + mỗi SEC áp dụng + mỗi method POST/PUT/DELETE; cột = EP, BVA, ST, SEC, SCH; ô = các ID phủ. Đánh dấu ô trống quan trọng.
  > 3. Kiểm tra định dạng: đủ cột, Request ghi rõ method, Expected cụ thể, có Nguồn expected.
  > 4. Đếm tổng (đã trừ trùng), theo kỹ thuật và theo method.
  > Append mục "## G5 – Tổng hợp độ phủ (reviewer)": bảng đếm, ma trận, danh sách trùng, danh sách lỗ hổng (yêu cầu, vì sao quan trọng, gợi ý 1 test).
  > Xong khi: có bảng đếm, ma trận, kết luận "ĐỦ ≥ 35" hoặc "THIẾU n case", và danh sách lỗ hổng.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API3_product_generated.md
- **AI output:**
  > Append G5: 92 thô, 5 nhóm trùng loại7 còn85; bảng đếm theo kỹ thuật/method, ma trận18×5, format92/92 đủ cột, 10 lỗH1–H10. Thiếu PUT validation/token none, các vấn đề XSS/identity/partialPUT/list/auth-first. Manager đọc và kiểm tra tham chiếu đạt; chuyển G6, không Audit hay gọi SUT.
- **Human review:** Đọc G5 của API 3: 92→85 và H1–H10 hợp lý; chấp nhận chuyển toàn bộ lỗ hổng sang G6.

## #17 – 2026-11-24 15:04 (giờ VN)
- **AI tool:** CNG5 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** CN-G5 – Generate
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
  > . API 2 – Hủy đơn – G5: rà soát độ phủ bộ test case AI đã sinh cho PUT /api/orders/:id/cancel. KHÔNG đánh nhãn VALID/INVALID/INCOMPLETE.
  > Input: report/testcases/API2_cancel_generated.md, report/01_spec_analysis.md, eshop-sut/README.md (FR-10, FR-11, FR-20, SEC-02, SEC-05).
  > 1. Liệt kê test trùng hoặc gần trùng giữa G1–G4 (cặp ID và lý do; không xóa).
  > 2. Ma trận độ phủ: hàng = mỗi ô của bảng 5×5 FR-10 liên quan tới User hủy + mỗi yêu cầu bảo mật + mỗi tham số; cột = EP, BVA, ST, SEC, SCH; ô = các ID phủ. Đánh dấu ô trống quan trọng.
  > 3. Kiểm tra định dạng: đủ cột, Precondition dựng được trạng thái, Expected cụ thể, có Nguồn expected.
  > 4. Đếm tổng (đã trừ trùng) và theo kỹ thuật.
  > Append mục "## G5 – Tổng hợp độ phủ (reviewer)": bảng đếm, ma trận, danh sách trùng, danh sách lỗ hổng (yêu cầu, vì sao quan trọng, gợi ý 1 test).
  > Xong khi: có bảng đếm, ma trận, kết luận "ĐỦ ≥ 35" hoặc "THIẾU n case", và danh sách lỗ hổng.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Append G5: 47 thô, 5 nhóm trùng loại5 còn42 (EP12/BVA4/ST10/SEC10/SCH6); ma trận User-cancel×5states + FR/SEC/params, 9 lỗH1–H9. Phát hiện403/404 ownership xung đột và error predicates yếu, chuyểnG6 hợp nhất giả định/schema. Manager đọc/check tham chiếu đạt; không SUT/Audit.
- **Human review:** Đọc G5 của API 2: 47→42 và H1–H9 hợp lý; ưu tiên H1–H3, chấp nhận 403/404 là giả định chờ G6 chốt.

## #18 – 2026-11-24 15:05 (giờ VN)
- **AI tool:** LGG5R2 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** LG-G5R2 – Generate
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
  > . API 1 – Login – G5: rà soát độ phủ bộ test case AI đã sinh cho POST /api/login. KHÔNG đánh nhãn VALID/INVALID/INCOMPLETE, đó là việc của sinh viên.
  > Input: report/testcases/API1_login_generated.md, report/01_spec_analysis.md, eshop-sut/README.md (FR-02, SEC-01..07).
  > 1. Tìm test case trùng hoặc gần trùng giữa các mục G1–G4. Liệt kê cặp ID và lý do; không xóa.
  > 2. Lập ma trận độ phủ: hàng = từng yêu cầu (mỗi gạch đầu dòng FR-02, mỗi SEC áp dụng, mỗi tham số); cột = EP, BVA, ST, SEC, SCH; ô = các ID phủ. Đánh dấu ô trống quan trọng.
  > 3. Kiểm tra định dạng: mỗi test có đủ cột, Request đủ để chạy, Expected cụ thể, có Nguồn expected.
  > 4. Đếm: tổng số test case (đã trừ trùng), số theo từng kỹ thuật.
  > Append mục "## G5 – Tổng hợp độ phủ (reviewer)" gồm: bảng đếm, ma trận, danh sách trùng, danh sách lỗ hổng độ phủ (mỗi lỗ hổng: yêu cầu nào, vì sao quan trọng, gợi ý 1 test case).
  > Xong khi: có bảng đếm, ma trận, kết luận rõ "ĐỦ ≥ 35" hoặc "THIẾU n case", và danh sách lỗ hổng (có thể rỗng).
  > 
  > Rà lại sau G6: đọc cả G6 vừa bổ sung; append một mục ## G5 – Tổng hợp độ phủ (reviewer) mới ở cuối, ghi rõ bản rà lại sau G6 là kết luận hiện hành. Giữ nguyên G5 trước đó và G1–G6. Đếm cả G6, cập nhật ma trận/tổng/trùng, đối chiếu từng H1–H5 và F1/F2 được lấp bằng case/quy tắc mới; không phát minh requirement hoặc lỗ hổng ngoài phạm vi những kỹ thuật đã giao. Không làm Audit, không nhãn. Nếu chỉ còn giới hạn spec không rõ đã ghi giả định thì phân biệt với thiếu case. Trả số cuối và lỗ hổng còn lại (nếu có).
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API1_login_generated.md
- **AI output:**
  > Append bản G5 cuối sau G6:66 thô,3nhómtrùng còn63 (EP21/BVA4/ST12/SEC19/SCH7), H1–H5 vàF1/F2 đóng, không còn thiếu case. Ngoại lệmedia415 nêu rõ trongbảncuối; các status/schema khác là giảđịnh. Manager đọc báo cáo, xácnhận1dòngclarification và kiểmtra thamchiếu đạt; không SUT/Audit.
- **Human review:** Đọc lại G5 API 1: 66→63, F1/F2 đã có quy tắc thay thế. Đồng ý không sửa dòng cũ, chỉ áp quy ước khi Execute.

## #19 – 2026-11-24 15:07 (giờ VN)
- **AI tool:** PRG6 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-G6 – Generate
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
  > . API 3 – Product CRUD – G6 bổ sung: mục G5 trong report/testcases/API3_product_generated.md báo ĐỦ 85 case nhưng còn thiếu độ phủ kỹ thuật và các lỗ hổng độ phủ sau: H1: PUT name thiếu/rỗng/sai kiểu và biên255/256 chưa phủ. H2: PUT price âm, chuỗi/null, 0.01 chưa phủ. H3: PUT category thiếu, không tồn tại99999 (xác minh GET categories),0/âm chưa phủ. Các case validation chỉ sai1field, còn lại body đầy đủ. H4: JWT alg none/chữ ký rỗng chưa có; cover POST/PUT/DELETE theo yêu cầu G3 cả3method. H5: malformedJWT cover cả3method. H6: XSS description/imageUrl và SQL imageUrl còn thiếu ở POST/PUT; expected literal accept hoặc reject phải chọn cụ thể có GIẢ ĐỊNH, không kết luận UI. H7: name1ký tự a cần snapshot before/after, exactly1newID và mọi trường đúng; bổ sung case snapshot-identity, không sửa G1-04. H8: chọn thống nhất full PUT bắt buộc name/price/category theo FR15; viết quy tắc G6 thay lựa chọn partial200 ở PR-G2-16 bằng400, giữ nguyên mục cũ để truy vết, giữ dữ liệu không đổi. Mỗi missing-field PUT đã có H1/H3 và price thêm1case để phủ policy. H9: GET list schema array of product, fields/spec chưanêu giảđịnh; không hardcode chứa seed1..5 thành spec, kiểm list chứa sảnphẩm tựtạo của case và items theo S4. Có thể thêm schema draft07 riêng G6 không sửa4schema G4. H10: khôngtoken+body{} auth-first401, snapshot khôngđổi, thứtự/statusGIẢĐỊNH. Cả10lỗ từ mục5.6G5 phải được map cụ thể vào case mới. Chỉ lấp các lỗ trên; mọi case độc lập admin setup, dữliệu riêng, auth/body đầyđủ, snapshot & GET sau tấn công. Không sửa/xóa G1–G5 hoặc seed. Ma trận H1..H10→IDs trước bảng. Bảng9cột, concrete method/path/body/status; macro cùngmục đầyđủ. Không bỏ lỗ vì thấp; no SUT. Không dùng alias B2 chưa định nghĩa. POST /products là collection không POST/:id..
  > Sinh test case bổ sung để lấp ĐÚNG các lỗ hổng trên, không sinh lại case đã có. Mỗi test ghi rõ lấp lỗ hổng nào.
  > Append mục "## G6 – Bổ sung theo G5" vào report/testcases/API3_product_generated.md, ID PR-G6-xx, cùng định dạng bảng ở Bối cảnh chung.
  > Xong khi: mọi lỗ hổng được liệt kê có ít nhất 1 test, tổng số test (đã trừ trùng) ≥ 35.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API3_product_generated.md
- **AI output:**
  > Append G6:35case lấpH1–H10, PUTvalidation, unsigned/malformedJWT cả3methods, XSSdescription/imageUrl/javascript và SQLimageUrl, snapshotname1ký tự, fullPUT policy toànAPI3, list schema, auth-first. Manager yêu cầu rõ precedence và javascriptvector rồi đọc/check9cột/IDs/nguồn đạt; không gọiSUT. Tổng127thô, chờreviewertrừtrùng.
- **Human review:** Duyệt 35 case PR-G6: phủ H1–H10, chọn full PUT và bỏ qua field thừa. Đồng ý D6 thay PR-G1-04 bằng PR-G6-28.

## #20 – 2026-11-24 15:07 (giờ VN)
- **AI tool:** CNG6 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** CN-G6 – Generate
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
  > . API 2 – Hủy đơn – G6 bổ sung: mục G5 trong report/testcases/API2_cancel_generated.md báo ĐỦ 42 case nhưng còn thiếu độ phủ kỹ thuật và các lỗ hổng độ phủ sau: H1 thiếu token trên IDvắng đã xácminh, expected401 (auth-first GIẢĐỊNH), đơnriêng khôngđổi. H2 JWT alg:none header/payload userA, chữkýrỗng,401. H3 path <O1>abc với O1 làđơnthậtpending,400 và khônghủy O1/O2. H4 BVA2147483647 xácminh khôngtồn tại qua adminlist,404; đây chỉmốc32bit giảđịnh không trần spec. H5 Userchủđơn cancelshipping400 + ContentTypeJSON + schemaerror. H6 Admin token dùng User /cancel trên delivered400 và shipping400 (shipping là GIẢĐỊNH vìdiagramkhôngcạnh và prosekhôngrõ). H7 UserB hủyđơnA shipping/delivered/canceled: chọn404đồngnhất choownership và trạngthái giữnguyên; từngbiếnthể độc lập. H8 User thường gọi PUT /api/admin/orders/<O1>/status body{"status":"canceled"} vớiđơnshipping:403,checksJSON/error và trạngthái khôngđổi; gián tiếpFR12. H9 IDvắng với ownertoken404khớpschemaerror; 403schemađược H8kiểm.
  > F1/Expected yếu: trước bảngG6 viết quyước GIẢĐỊNHhợpnhất toànAPI2 đểchuyểnsangExecute: errorJSONobject error:string nonempty, khôngJWT, mediaapplication/json; áp dụngmọi dòngcũ 'biểu thị lỗi'; cancel successJSONobject message:string nonempty (GIẢĐỊNH dựatrênquan sátkhôngphảispec), trạngthái đích canceled. Invalidbody/path/state400; auth401; roleAdmin403; missing/foreignorder404. Chỉ đổighi chú nghĩa cho CN-G3-01/02 từ403sang404 theoquyước này;giữnguyên G1–G5. CN-G3-12 ba404 giữ nguyên. Ưutiên auth→ownership→state làGIẢĐỊNH, không specfact. Giữvai tròG6 làbổsungkhôngauditlabels. Caseexpired/deleteuser conditional do spec khôngbảođảm không giả làm chạyđược.
  > Mỗi case setupriêng registerA/B+loginadmin+2đơn, điđúngcạnhpendingconfirmedshippingdelivered, khôngdùng kếtquảcasekhác, khônggọiSUT. Headers/body/macro đầyđủtrongG6. MapH1..H9→IDs, đủ9cột. Không sửaG1–G5, không tạo collection/script. Chỉlấpđúnglỗtrên, khôngthêmscope..
  > Sinh test case bổ sung để lấp ĐÚNG các lỗ hổng trên, không sinh lại case đã có. Mỗi test ghi rõ lấp lỗ hổng nào.
  > Append mục "## G6 – Bổ sung theo G5" vào report/testcases/API2_cancel_generated.md, ID CN-G6-xx, cùng định dạng bảng ở Bối cảnh chung.
  > Xong khi: mọi lỗ hổng được liệt kê có ít nhất 1 test, tổng số test (đã trừ trùng) ≥ 35.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Append G6:12case lấpH1–H9 (auth-firstmissingID, algnone, Oabc,2147483647, shippingschema, Adminstate,foreignshipping/finals,adminrole,404schema). Hợpnhất error/success predicates,status; Userforeign404, Adminbypassownership làgiảđịnh vẫnstate400. Manager đọc/checktĩnh đạt;59thô chờreviewertrừtrùng; khôngSUT.
- **Human review:** Duyệt 12 case CN-G6: phủ H1–H9. Chốt 404 cho đơn người khác, 400/403/401 theo actor; các case cần V(X) sẽ ghi chú điều kiện.

## #21 – 2026-11-24 15:13 (giờ VN)
- **AI tool:** PRG5R2 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-G5R2 – Generate
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
  > . API 3 – Product CRUD – G5: rà soát độ phủ bộ test case AI đã sinh cho Product CRUD. KHÔNG đánh nhãn VALID/INVALID/INCOMPLETE.
  > Input: report/testcases/API3_product_generated.md, report/01_spec_analysis.md, eshop-sut/README.md (FR-12, FR-15, SEC-02..06).
  > 1. Liệt kê test trùng hoặc gần trùng giữa G1–G4 (cặp ID và lý do; không xóa).
  > 2. Ma trận độ phủ: hàng = mỗi ràng buộc FR-15 (name, price, category, chỉ sửa 1 sản phẩm) + mỗi SEC áp dụng + mỗi method POST/PUT/DELETE; cột = EP, BVA, ST, SEC, SCH; ô = các ID phủ. Đánh dấu ô trống quan trọng.
  > 3. Kiểm tra định dạng: đủ cột, Request ghi rõ method, Expected cụ thể, có Nguồn expected.
  > 4. Đếm tổng (đã trừ trùng), theo kỹ thuật và theo method.
  > Append mục "## G5 – Tổng hợp độ phủ (reviewer)": bảng đếm, ma trận, danh sách trùng, danh sách lỗ hổng (yêu cầu, vì sao quan trọng, gợi ý 1 test).
  > Xong khi: có bảng đếm, ma trận, kết luận "ĐỦ ≥ 35" hoặc "THIẾU n case", và danh sách lỗ hổng.
  > 
  > Rà lại sau G6: đọc cả G6, append một mục ## G5 – Tổng hợp độ phủ (reviewer) mới cuối file, ghi kết luận hiện hành thay số liệu G5 cũ. Không sửa/xóa G1–G6 cũ. Đếm cả G6, kỹ thuật và method, nhóm trùng hợp/near-duplicates; map H1..H10 sang case/quy tắc mới. FullPUT G6 là giả định hiện hành cho cả file, thay PR-G2-16 status400+unchanged; giữ oldcase để trace. Không tạo lỗ hổng ngoài phạm vi yêu cầu G1–G4 hay mở scope mới; phân biệt giới hạn spec đã ghi giả định với thiếu case. G6 H9 array each item S4 là schema mô tả được dùng, không cần tạo schema mới riêng nếu rõ. H7 case28 snapshotdelta lấp falsepass. H4 unsignedvsmalformed3methods và H6XSSjavascript/literal không chứng minhUI đều đã định nghĩa. Chỉ báo lỗ hổng thật còn lại nếu có. No tests/build/lint/formatters/SUT. MUST edit existing file, not shell/python mutations. Return actual tool/model/date and final counts.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API3_product_generated.md
- **AI output:**
  > Append G5cuối sauG6:127thô,6nhómtrùng hợp loại8 còn119 (EP40/BVA20/ST13/SEC37/SCH9); H1–H10đóng, khôngcònthiếucase. G6-28thayoracleweakG1-04, fullPUT400 làhiệnhànhchoG2-16. Manager đọc/check ID vàtự tínhhợpnhómtrùng từlabelsthậtđạt; khôngSUT/Audit.
- **Human review:** Đọc lại G5 API 3: 127→119, không còn lỗ hổng thật. Đồng ý giữ D1–D6 để truy vết, không xóa case.

## #22 – 2026-11-24 15:15 (giờ VN)
- **AI tool:** CNG5R2 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol)
- **API / Bước:** CN-G5R2 – Generate
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
  > . API 2 – Hủy đơn – G5: rà soát độ phủ bộ test case AI đã sinh cho PUT /api/orders/:id/cancel. KHÔNG đánh nhãn VALID/INVALID/INCOMPLETE.
  > Input: report/testcases/API2_cancel_generated.md, report/01_spec_analysis.md, eshop-sut/README.md (FR-10, FR-11, FR-20, SEC-02, SEC-05).
  > 1. Liệt kê test trùng hoặc gần trùng giữa G1–G4 (cặp ID và lý do; không xóa).
  > 2. Ma trận độ phủ: hàng = mỗi ô của bảng 5×5 FR-10 liên quan tới User hủy + mỗi yêu cầu bảo mật + mỗi tham số; cột = EP, BVA, ST, SEC, SCH; ô = các ID phủ. Đánh dấu ô trống quan trọng.
  > 3. Kiểm tra định dạng: đủ cột, Precondition dựng được trạng thái, Expected cụ thể, có Nguồn expected.
  > 4. Đếm tổng (đã trừ trùng) và theo kỹ thuật.
  > Append mục "## G5 – Tổng hợp độ phủ (reviewer)": bảng đếm, ma trận, danh sách trùng, danh sách lỗ hổng (yêu cầu, vì sao quan trọng, gợi ý 1 test).
  > Xong khi: có bảng đếm, ma trận, kết luận "ĐỦ ≥ 35" hoặc "THIẾU n case", và danh sách lỗ hổng.
  > 
  > Rà lại sau G6: đọc G6, append mục ## G5 – Tổng hợp độ phủ (reviewer) mới cuối file, ghi kết luận hiện hành. Giữ G1–G6/G5cũ nguyên để trace. Đếm cảG6, nhómtrùng hợp không trừnear-duplicates; map H1..H9, F403/404 vàerrorpredicate sang case/quy tắc mới. G6 toànAPI2: Userforeign404, Adminbypassownership giảđịnh nhưng state400; CN-G3-01/02 old403 superseded404, giữoldcellsprovenance; CN-G3-12 ba404 đúng. Errorstringnonempty/JSON/noJWT áp dụngcác oracle cũ yếu. No need Audit labels. Điều kiện expiredJWT exp / deleteduser / listabsence do spec khôngnêu đã gắnGIẢĐỊNH phải phânbiệt với thiếucase, không bịa khả năngthực thi. Không phátminh scope mới/gap ngoài G1–G4; chỉ báo lỗhổngthật nếu còn. MUST edit not shell/python mutation. No tests/build/lint/formatters/SUT. Return actual model,date,finalcounts.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): User explicitly requests completing three parallel Generate chains through G5; one task assignment per step, sequential within each chain. Read skill://ponytail first and obey throughout; reviewers also read skill://ponytail-review. Relevant repo rules are already supplied: do NOT discover/read agent/context files. Only spec documents named above and your own API testcase file may be read; NEVER implementation backend/frontend or HTTP/SUT requests. Expected must come ONLY from spec, not observed behavior. Treat all unspecified statuses, error schema, timing<2000ms, JWT claim types, lifecycle details, counter reset, IDOR cancellation ownership as GIẢ ĐỊNH with reason. No audit labels, no fabricated observations. No nested delegation. Skip build/lint/tests/formatters/static-check scripts mid-flight; manager checks once step is ready.
  > Scope: own ONLY assigned API file, append only assigned section; do not edit earlier sections. New files via write; existing files MUST edit. No other repo changes. Manager exclusively writes report/AI_LOG.md and commits sequentially: DO NOT touch AI_LOG or git. Return actual agent/model id, date from TZ=Asia/Ho_Chi_Minh date "+%Y-%m-%d %H:%M", count added, and acceptance evidence. Original common+step prompt retained by manager for verbatim append log. No helper scripts/docs/collections.
  > Each testcase exactly 9 Markdown columns (escape any pipe inside cell), explicit method/path/header/body (setup macros allowed if completely defined in SAME step); status concrete with assumptions, body concrete predicates, source citations. Unique per-case fresh data (include case ID + UUID), never cross-case state. All security attacks check data afterward. Do not use reserved absent IDs without ensuring absence via GET/list in setup. Never update/delete seed products1..5. CN setups fetch actual product details and derive checkout total, with admin transitions only legal edges. Error payloads/status unspecified are assumptions not fabricated facts.
  > For matrices, every cell has direct case references. ST impossible/no-op/undefined events must be explicit assumptions and a test verifying no undesired change. Product POST is collection creation, never invented POST /:id. Login reset after success/expiry inferred from consecutive/duration not explicitly stated. CN shipping Admin action ambiguous, do NOT silently infer shipping→canceled permission.
  > G4 schema properties: spec-guaranteed required only; observations optional and labeled, unobserved fields must say GIẢ ĐỊNH not 'observed'. Password exclusion a security inference. Draft07 schemas in json code blocks with $schema; no literal pipes in cells. G5 count genuine semantic duplicate groups (union, not subtract each pair), not near-duplicates or shared successful setup/assertions; matrix every applies SEC including indirect/not-applicable explanation. Check Request executability as document; do not send it. Report actionable exact holes for G6 if any. Reviewer may append coverage REPORT ONLY, no edits/testcase generation or earlier section mutations; any gaps return for task G6.
  > 
  > OWN FILE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Append G5cuối sauG6:59thô,7nhómtrùng hợp loại9 còn50 (EP12/BVA5/ST10/SEC19/SCH4); H1–H9đóng, schema-error dedup phản ánh predicateEtoànfile. Manager đọc và chỉnh4dòngbáocáo: successpredicatehiệnhành, deleteduser tokenvẫn dùngđược làtestfailkhôngskip, phânbiệtFR10specvớigiảđịnh. CheckID/cột vàtự tínhhợpnhómtrùngđạt; không SUT/Audit.
- **Human review:** Đọc lại G5 API 2: 59→50, không còn lỗ hổng thật. Các case điều kiện (exp, xóa user, V(X)) sẽ báo không chạy được thay vì pass.

## #23 – 2026-11-24 22:08 (giờ VN)
- **AI tool:** task ExecuteX0 (openai-codex/gpt-6.1-terra); omp Manager (openai-codex/gpt-6.1-sol); sonic kiểm tra CLI (worker không cung cấp model id)
- **API / Bước:** Execute – X0: Hạ tầng dùng chung
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.request.url.toString());
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > Execute – X0: dựng hạ tầng chạy test cho 3 API. Chưa thêm test case nào.
  > 1. Tạo 3 file collection rỗng (Postman v2.1) đúng tên trong bảng phạm vi:
  >    collections/23120190_API1_Login.postman_collection.json
  >    collections/23120190_API2_CancelOrder.postman_collection.json
  >    collections/23120190_API3_ProductCRUD.postman_collection.json
  >    Mỗi collection có:
  >    - Pre-request script cấp collection đúng 2 dòng ở Phần B (upsert X-Student-Id + console.log).
  >    - Folder rỗng: G1, G2, G3, G4, G6, EX.
  >    - Description: API, endpoint, file test case nguồn, quy ước assertion "core" / "status (GIẢ ĐỊNH)".
  >    - Một request mẫu "[SMOKE] GET /api/products" trong folder riêng "_smoke", có test status 200, để kiểm pre-request.
  > 2. Tạo scripts/run_newman.sh (chmod +x) cho NGƯỜI DÙNG chạy bản chính thức:
  >    - set -e cho phần chuẩn bị; nhưng lỗi test của newman KHÔNG được dừng script (chạy đủ cả 3 collection, cuối cùng in tổng kết và exit 1 nếu có collection fail).
  >    - Với mỗi API: gọi scripts/reset_sut.sh, rồi
  >      newman run collections/23120190_<API>.postman_collection.json -e environments/local.postman_environment.json \
  >        --reporters cli,htmlextra,json \
  >        --reporter-htmlextra-export results/newman/23120190_<API>_$(date +%Y%m%d).html \
  >        --reporter-htmlextra-title "23120190 – <API> – localhost" \
  >        --reporter-json-export results/newman/23120190_<API>_$(date +%Y%m%d).json
  >    - Tham số tùy chọn: tên API (API1_Login | API2_CancelOrder | API3_ProductCRUD) để chạy riêng một API; không có tham số thì chạy cả 3.
  >    - Chừa sẵn chỗ (comment) cho run data-driven của X-DATA.
  > 3. Chạy thử: scripts/reset_sut.sh; newman run <từng collection> -e environments/local.postman_environment.json --reporters cli --folder _smoke. Xác nhận console in "X-Student-Id: 23120190".
  >    KHÔNG chạy scripts/run_newman.sh (script đó ghi report chính thức, chỉ người dùng chạy).
  > Xong khi: 3 collection import được (newman chạy _smoke pass), console in X-Student-Id cho request smoke, scripts/run_newman.sh có đủ các ý ở mục 2, results/newman/ không có file mới.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Load skill://ponytail first and obey whole session. Only X0 this turn, no X1–X5. Repo context rules are provided here: log only when prompt includes phrase; append only, timestamp Vietnam date command, quote prompt minus phrase, Human review blank. Manager is ONLY AI_LOG writer and committer; do not edit log/git. Return actual model/date and output summary to manager. Do not read agent/context files already supplied. No nested delegation.
  > Own only four NEW files: the three collections and scripts/run_newman.sh. They do not exist; use write. Any subsequent file edits MUST edit, never shell/python mutation. chmod +x runner allowed. Do not change testcases/environment/reset/SUT/results/newman. Skip ALL tests/build/lint/formatters/smoke commands: after files ready manager delegates execution to sonic. Hence X0 step3 handled separately; do NOT run runner officially or newman yourself.
  > Read environments/local.postman_environment.json, scripts/reset_sut.sh and README.md for existing conventions; source prompts provided verbatim. Skeleton only: folders G1,G2,G3,G4,G6,EX empty; separate _smoke with one actual GET {{baseUrl}}/api/products and status200 assertion. Collection-level prerequest exactly the supplied 2 lines, no scripts faking logs. Description endpoint/source and core/status conventions. BaseUrl variable used in request, no explicit X-Student-Id headers on request.
  > Runner minimal Bash; own root independent of invoking cwd, exact API selection with no-arg all3 and invalid usage rejected before work. set -e preparation; actual Newman nonzero captured without aborting remaining selected APIs. Reset before EACH API. CLI,htmlextra,json reporter options/naming/date/title exactly prompt. Summarize each selected API and overall exit1 if any newman fails. Do not swallow reset failure; do not forge reports or call any reporters during creation. Leave ONLY requested X-DATA integration comment, no fake execution. No retries/dependencies/abstractions/extraneous scripts/docs. Keep all errors observable. Return files ready for check; do not claim smoke pass.
- **AI output:**
  > Tạo 3 collection v2.1 đúng tên, pre-request cấp collection đúng 2 dòng X-Student-Id/console.log, G1/G2/G3/G4/G6/EX rỗng và mỗi collection 1 request _smoke GET {{baseUrl}}/api/products. Tạo scripts/run_newman.sh executable: chọn một/cả ba API, reset trước từng API, CLI+HTMLextra+JSON theo tên/ngày, tiếp tục sau lỗi Newman, tổng kết và exit1 nếu có fail; comment X-DATA. Cập nhật README cách chạy và giới hạn X0. Kiểm JSON, bash -n, Newman6.2.3/reporter htmlextra1.23.1 đạt. Reset riêng trước mỗi smoke; 3 lần Newman CLI thật đều 1 request/1 assertion/0 fail, console in X-Student-Id:23120190 (URL template ở console, HTTP GET thực tế localhost:3000 trả200). Harness bản sao tạm cô lập xác nhận fail giữa vẫn chạy đủ3, chọnAPI, invalidargs, lỗi reset, cwd và reporter argv; đã xóa fixtures. Không chạy runner chính thức; results/newman/ trước/sau chỉ .gitkeep cùng hash; không sửa test case/SUT, không tạo ảnh/report chính thức. Chưa thêm folder test case, chưa làm X1–X5.
- **Human review:** Đã mở 3 collection và run_newman.sh: đúng tên, folder G1..EX rỗng, _smoke và hai dòng pre-request giữ nguyên; runner reset trước từng API và không dừng khi Newman fail. Đồng ý X0 đạt; lưu ý bằng chứng chỉ là 3 lần smoke và bash -n vì worker chưa chạy runner chính thức.

## #24 – 2026-11-24 22:32 (giờ VN)
- **AI tool:** CN-X1 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** CN-X1 – Execute
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 2 – Execute – CN-X1: chuyển các case CN-G1-xx và CN-G2-xx thành request trong collections/23120190_API2_CancelOrder.postman_collection.json, folder G1 và G2.
  > Input: report/testcases/API2_cancel_generated.md (mục G1, G2, Audit). Tuân thủ Phần B.
  > Chú ý riêng:
  > - Setup đơn hàng: đăng ký user mới → login → POST /api/cart → POST /api/checkout → lấy order id từ response. Đổi trạng thái đơn bằng PUT /api/admin/orders/:id/status với token admin (login admin trong setup của từng case).
  > - Các macro trong file (S, S6, D(<trạng thái>), K(O), U, A[...]) phải được dịch thành request cụ thể đúng như định nghĩa trong file.
  > - G2 kiểm từng cạnh của máy trạng thái FR-10: mỗi đích trong A[...] là một case con riêng với đơn MỚI (đúng "D(...) riêng cho từng đích").
  > - Path dạng %2B, 1.5, %20 gửi nguyên văn, không để Postman tự chuẩn hóa.
  > Chạy thử: reset SUT, newman ... --reporters cli --folder G1, rồi --folder G2. Chỉ sửa lỗi kỹ thuật.
  > Xong khi: mọi case VALID/INCOMPLETE của G1, G2 có folder; mỗi cạnh của G2 có request và assertion riêng; chạy cli không lỗi script; báo số pass/fail.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X1: modify only G1/G2 items and info.description. Existing G3/G4/G6/EX empty remain unchanged. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API2_CancelOrder.postman_collection.json
  > SOURCE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Chuyển26foldercase G1=16/G2=10,493request,25cạnhAdmin G2 mỗiđích có register/checkout mới. BỏCN-G2-01/11/12 INVALID,3caseG1 INCOMPLETE ghidescription. Hookmới giữnguyên; pathencoded cấpitem. Debug CLI serialized: G1 requests135/assert183 pass172 fail11; G2 requests358/assert493 pass487 fail6; tổng659pass17fail. Khônglỗi script/biếnURLchưathay; failassertgiữtheofile, khôngđổiexpected. Khôngreportchínhthức/commit.
- **Human review:** Đối chiếu 26 folder với G1/G2: đủ case VALID/INCOMPLETE, CN-G2-01/11/12 bị bỏ đúng nhãn INVALID, path %2B/1.5/%20 giữ nguyên văn. Fail trong debug là do SUT/expected giả định, không phải lỗi script; đồng ý giữ nguyên và chuyển sang X2.

## #25 – 2026-11-24 22:32 (giờ VN)
- **AI tool:** LG-X1 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** LG-X1 – Execute
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 1 – Execute – LG-X1: chuyển các case LG-G1-xx và LG-G2-xx thành request trong collections/23120190_API1_Login.postman_collection.json, folder G1 và G2.
  > Input: report/testcases/API1_login_generated.md (mục G1, G2, bảng Audit). Tuân thủ Phần B (đặc biệt: bỏ INVALID, quy ước assertion core/status, không sửa expected).
  > Chú ý riêng:
  > - G1 dùng "Quy ước setup độc lập" trong file (đăng ký user lg-<id>-<guid>@test.com, password Test1234!). Các biến upperEmail, spaceLead, longEmail... tạo trong pre-request của request chính.
  > - LG-G1-23 (JSON sai cú pháp) và LG-G1-24 (text/plain) dùng body raw, gửi nguyên văn.
  > - G2 có chuỗi nhiều request (W, W, C, chờ 29/31 giây). Mỗi bước trong chuỗi là một request riêng trong folder case; assertion nằm ở đúng request của bước đó. Chờ bằng setTimeout đúng số giây trong file.
  > Chạy thử: scripts/reset_sut.sh rồi newman ... --reporters cli --folder G1, sau đó --folder G2. Sửa lỗi kỹ thuật cho đến khi mọi request chạy được (không có lỗi script, không có biến chưa định nghĩa). Test fail do SUT trả khác expected là BÌNH THƯỜNG, giữ nguyên.
  > Xong khi: mọi case VALID/INCOMPLETE của G1, G2 có folder riêng; ID INVALID được liệt kê trong description collection; chạy cli không còn lỗi script; báo số assertion pass/fail của lần chạy thử (chỉ báo, không ghi file).
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X1: modify only G1/G2 items and info.description. Existing G3/G4/G6/EX empty remain unchanged. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API1_Login.postman_collection.json
  > SOURCE: report/testcases/API1_login_generated.md
- **AI output:**
  > Chuyển35foldercase G1=24/G2=11,112request; bỏLG-G1-14/LG-G2-02 INVALID. Đổi biến dẫnxuấtG1 sangcollectionVariables cóprefixID, hookmớigiữnguyên; rawmalformedJSON/textplain vàtimer29/31 giữtheofile. Debug correctedG1:48requests/72assert pass46fail26/1.932s; unchangedG2:64requests/119assert pass61fail58/2m36.4s. Tổng107pass84fail, khônglỗiscriptchưabắt/unresolvedvars. JSONErrortrongpm.test làbodyassertfail, khôngnớiexpected. Khôngreportchínhthức/commit.
- **Human review:** Kiểm 35 folder G1/G2: LG-G1-14 và LG-G2-02 không có folder, raw malformed JSON/text-plain và timer 29/31 giữ đúng file. Biến đã đổi sang collectionVariables có prefix ID nên không lẫn giữa case; pass/fail debug chỉ dùng gỡ lỗi kỹ thuật.

## #26 – 2026-11-24 22:37 (giờ VN)
- **AI tool:** PR-X1 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-X1 – Execute
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 3 – Execute – PR-X1: chuyển các case PR-G1-xx và PR-G2-xx thành request trong collections/23120190_API3_ProductCRUD.postman_collection.json, folder G1 và G2.
  > Input: report/testcases/API3_product_generated.md (mục G1, G2, Audit). Tuân thủ Phần B.
  > Chú ý riêng:
  > - Token admin T và token user V lấy trong setup của từng case (login admin/user seed bằng biến environment).
  > - Snapshot S = GET /api/products trước request chính; kiểm "list không đổi" bằng so sánh với S trong test script.
  > - Các body macro (B, B2, B[field]=giá trị) dịch đúng như định nghĩa trong file; tên sản phẩm duy nhất theo {{$guid}}.
  > - PR-G2-16 có nhãn INCOMPLETE: dùng expected hiện hành theo lý do audit (quy ước full PUT của G6), ghi rõ trong description.
  > Chạy thử: reset SUT, newman ... --folder G1, rồi --folder G2. Chỉ sửa lỗi kỹ thuật.
  > Xong khi: mọi case VALID/INCOMPLETE của G1, G2 có folder; chạy cli không lỗi script; báo số pass/fail.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X1: modify only G1/G2 items and info.description. Existing G3/G4/G6/EX empty remain unchanged. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API3_ProductCRUD.postman_collection.json
  > SOURCE: report/testcases/API3_product_generated.md
- **AI output:**
  > Chuyển54foldercase/312requests: G1=41,G2=13; bỏ8IDINVALID theoaudit, G2-16INCOMPLETE ghi fullPUT400+unchanged. Sửa kỹthuật bindingdata xungđột sandbox vàthiếu) tạiG2-05, parseerrorbody trongcorecallback, khôngđổiexpected/hook. FinalCLI G1:208requests/271assert201pass70fail/6.2s; finalG2:104requests/123assert95pass28fail/2.4s; tổng296pass98fail. Khônglỗi scriptchưabắt/unresolvedvars/requesterrors ởfinalruns. Initialruns kỹthuật lỗikhôngdùnglàkếtquảbug. Khôngreportchínhthức/commit.
- **Human review:** Đối chiếu 54 folder G1/G2 với audit: 8 INVALID không có folder, PR-G2-16 ghi rõ INCOMPLETE theo quy ước full PUT 400. Hai lỗi kỹ thuật ở G2-05 và parse error body đã sửa mà không đổi expected; 98 fail còn lại là ứng viên bug/giả định, không phải lỗi collection.

## #27 – 2026-11-24 22:42 (giờ VN)
- **AI tool:** LG-X2 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** LG-X2 – Execute
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 1 – Execute – LG-X2: chuyển các case LG-G3-xx và LG-G4-xx thành request trong collection API 1, folder G3 và G4.
  > Input: report/testcases/API1_login_generated.md (mục G3, G4, Audit). Tuân thủ Phần B.
  > Chú ý riêng:
  > - G3: payload SQLi, object/array thay field, ký tự điều khiển (\u0000) phải gửi đúng nguyên văn trong body raw JSON. Case "duyệt đệ quy không lộ password" viết hàm duyệt trong test script.
  > - G4: dán NGUYÊN schema JSON trong file vào pm.response.to.have.jsonSchema(...). Không chỉnh schema.
  > Chạy thử: reset SUT, newman ... --reporters cli --folder G3, rồi --folder G4. Chỉ sửa lỗi kỹ thuật.
  > Xong khi: mọi case VALID/INCOMPLETE của G3, G4 có folder; schema dán đúng nguyên văn (đối chiếu từng schema với file); chạy cli không lỗi script; báo số pass/fail.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X2: modify only G3/G4 items and info.description; preserve all G1/G2/_smoke and protected collection hook. G6/EX remain empty. G4 schemas must be exact original JSON schema. Expired/deleted-user INCOMPLETE cases: do not invent exp/expired token or fake a pass; implement the feasible portion and describe exact missing prerequisite per audit. No skip swallowing failures; absent exp cannot be presented as actual expired-token exercise. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API1_Login.postman_collection.json
  > SOURCE: report/testcases/API1_login_generated.md
- **AI output:**
  > Thêm23folderG3=16/G4=7,68requests, bỏLG-G3-06INVALID; 2schemaunique khớpnguồn. SửatechnicalapplyAST/escape vàURL LG-G3-07 nhầmsangregister vìlabelchứa đăngký, naysanglogin. CLI G3trướcsửaURL:51req104assert81pass23fail/32.4s; G4:17req45assert34pass11fail/608ms. Rerunchỉcase07đãsửa:4req9assert7pass2fail/191ms;2failstatus400so401, coreequivalencepass. KhôngclaimtổngG3cuốitừrunold; fullcollectionX3sẽđếmlại. Khônglỗiscriptchưabắt; hookmới vàschema/status400/423theoauditgiữnguyên. Khôngreportchínhthức/commit.
- **Human review:** Kiểm G3/G4: 23 folder, LG-G3-06 bị bỏ đúng, schema G4 dán nguyên 2 schema nguồn. Việc sửa URL LG-G3-07 từ register về login là đúng endpoint; 2 fail status 400/401 ở case đó là giả định, không phải lỗi script.

## #28 – 2026-11-24 22:47 (giờ VN)
- **AI tool:** PR-X2 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** PR-X2 – Execute
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 3 – Execute – PR-X2: chuyển các case PR-G3-xx và PR-G4-xx thành request trong collection API 3, folder G3 và G4.
  > Input: report/testcases/API3_product_generated.md (mục G3, G4, Audit). Tuân thủ Phần B.
  > Chú ý riêng:
  > - Case thiếu token / user thường / JWT tự ký: mỗi case kiểm cả status VÀ "S không đổi" (GET list sau request).
  > - Case tự nâng role (PR-G3-07..09) gọi PUT /api/users/me trong setup đúng như file.
  > - Payload XSS/SQLi gửi nguyên văn; kiểm giá trị lưu là literal đúng như cột Expected.
  > - G4: dán NGUYÊN schema trong file vào jsonSchema.
  > Chạy thử: reset SUT, newman ... --folder G3, rồi --folder G4. Chỉ sửa lỗi kỹ thuật.
  > Xong khi: mọi case VALID/INCOMPLETE của G3, G4 có folder; schema đúng nguyên văn; chạy cli không lỗi script; báo số pass/fail.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X2: modify only G3/G4 items and info.description; preserve all G1/G2/_smoke and protected collection hook. G6/EX remain empty. G4 schemas must be exact original JSON schema. Expired/deleted-user INCOMPLETE cases: do not invent exp/expired token or fake a pass; implement the feasible portion and describe exact missing prerequisite per audit. No skip swallowing failures; absent exp cannot be presented as actual expired-token exercise. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API3_ProductCRUD.postman_collection.json
  > SOURCE: report/testcases/API3_product_generated.md
- **AI output:**
  > Thêm30folderG3=22/G4=8,321requestkhaitriển; khôngINVALIDở2nhóm. G4-07source-definedparityjump bằngstableID, max10, dừngsaukhiE/Ocómặt, giữmọimainassert; actualchỉ2POST+GETpairs. Exact4schemasS1–S4 với12occurrenceskhớpnguồn. CLI G3:257req268assert201pass67fail/8.1s; G4:48req95assert80pass15fail/1.301s; tổng281pass82fail/305requeststhựcthi. Khônglỗiscriptchưabắt/unresolvedvars; hookmớigiữnguyên, failauth/state/schema giữtheofile. Khôngreportchínhthức/commit.
- **Human review:** Đối chiếu G3/G4 API3: 30 folder, không bỏ case nào; PR-G4-07 chỉ chạy 2 cặp POST/GET nhưng giữ mọi assertion chính và dừng sau 10 vòng nên chấp nhận. Bốn schema S1–S4 khớp nguyên văn nguồn; 82 fail là bug/giả định cần triage.

## #29 – 2026-11-24 22:50 (giờ VN)
- **AI tool:** task CNX2 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** API 2 – Execute – CN-X2
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 2 – Execute – CN-X2: chuyển các case CN-G3-xx và CN-G4-xx thành request trong collection API 2, folder G3 và G4.
  > Input: report/testcases/API2_cancel_generated.md (mục G3, G4, Audit). Tuân thủ Phần B.
  > Chú ý riêng:
  > - Case hai user A/B (IDOR): mỗi case tự đăng ký cả A và B.
  > - Case JWT tự ký / alg none / sai cấu trúc: dựng token trong pre-request bằng CryptoJS, đúng header/payload/secret ghi trong file.
  > - CN-G3-06 (user đã bị xóa) gọi DELETE /api/admin/users/:id bằng token admin trong setup.
  > - G4: dán NGUYÊN schema trong file vào jsonSchema.
  > Chạy thử: reset SUT, newman ... --reporters cli --folder G3, rồi --folder G4. Chỉ sửa lỗi kỹ thuật.
  > Xong khi: mọi case VALID/INCOMPLETE của G3, G4 có folder; schema dán đúng nguyên văn; chạy cli không lỗi script; báo số pass/fail.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X2: modify only G3/G4 items and info.description; preserve all G1/G2/_smoke and protected collection hook. G6/EX remain empty. G4 schemas must be exact original JSON schema. Expired/deleted-user INCOMPLETE cases: do not invent exp/expired token or fake a pass; implement the feasible portion and describe exact missing prerequisite per audit. No skip swallowing failures; absent exp cannot be presented as actual expired-token exercise. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API2_CancelOrder.postman_collection.json
  > SOURCE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Thêm14folderG3=10/G4=4,192requestkhaitriển; bỏCN-G3-03/05,G4-03/04INVALID. Schemaunique khớpnguồn, owner404theoG6. CN-G3-04INCOMPLETE chỉkiểmexp thiếu, khônggiảtokenhếthạn. SửaguardG3-06: failedsetupassertvẫnghi, chưađủđiềukiệnđơnsaudelete thìjumpstableIDcase07; khitiềnđềđạt vẫnattack401. FinalcoherentG3CLI:158req205assert196pass9fail/3.8s, case07vàsaurunsvẫntiếptục; G4:32req46assert46pass0fail/903ms. Tổng242pass9fail, khônglỗiscriptchưabắt; guardcasekhôngđượcgiảpass/hayclaimđãchạyattack. Hookmớigiữnguyên, khôngreportchínhthức/commit.
- **Human review:** Kiểm G3/G4 API2: 14 folder, CN-G3-03/05 và G4-03/04 bị bỏ đúng INVALID, CN-G3-04 chỉ kiểm precondition exp và ghi rõ không giả token hết hạn. Guard CN-G3-06 không cho setup fail thành pass; đồng ý 9 fail còn lại là thật hoặc giả định.

## #30 – 2026-11-24 22:57 (giờ VN)
- **AI tool:** task LGX3 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** API 1 – Execute – LG-X3
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 1 – Execute – LG-X3: chuyển các case LG-G6-xx và LG-EX-xx thành request trong collection API 1, folder G6 và EX.
  > Input: report/testcases/API1_login_generated.md (mục G6, Extend – Human, Audit). Tuân thủ Phần B.
  > Chú ý riêng:
  > - LG-EX-03 decode base64url payload JWT trong test script (atob sau khi đổi -_ thành +/ và thêm padding), kiểm `exp`.
  > - LG-EX-04 đi qua POST /api/forgot-password và POST /api/reset-password; lấy resetToken từ response forgot-password như cột Precondition ghi.
  > - LG-EX-05 ký JWT HS256 bằng CryptoJS (có sẵn trong sandbox Postman): CryptoJS.HmacSHA256(header.payload, secret), chuyển base64url.
  > - Folder EX đặt sau G6.
  > Chạy thử: reset SUT, newman ... --reporters cli --folder G6, rồi --folder EX; sau đó chạy toàn collection một lần để chắc không có case nào phụ thuộc nhau. Chỉ sửa lỗi kỹ thuật.
  > Xong khi: mọi case G6 VALID/INCOMPLETE và đủ 5 case LG-EX có folder; chạy toàn collection không lỗi script; báo tổng số assertion pass/fail và thời gian chạy.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Never derive an endpoint from display-label substrings: earlier label contains "chưa đăng ký" wrongly mapped login to register; construct explicit method/path. Avoid top-level identifier data because Newman sandbox injects legacy data binding; use a case-specific/scoped response variable. For large one-line JSON, ast_edit exact folder node then resolve proposal; a staged or failed edit is NOT applied. Verify tool operation result before claiming ready (no runtime tests while coding). Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X3: modify only G6/EX and API3 EX-last ordering; preserve earlier completed G1/G2/G3/G4 folders and protected hook. EX-last containing PR-EX-05 must be last after _smoke; only its own verification requests may follow seed delete. Audit+Human Extend are authoritative. No expected changes. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API1_Login.postman_collection.json
  > SOURCE: report/testcases/API1_login_generated.md
- **AI output:**
  > Thêm10caseG6/EX5mỗi nhóm,49requests. Sửa11GUIDcallsdobuilderfstringmấtbrace; khôngđổi payload/expected/timert0+31/hook. G6debugtrướcfreshnessfix28req65assert44pass21fail; EX21req43assert30pass13fail; oldfullkhôngdùnglàprooffinal. FinalfullcorrectedCLI:230requests449assert299pass150fail/4m17.1s, zeroScriptErrors/requesterrors và properUUIDthật,localhost/XStudentId. Schema/status/corefailgiữnguyênfile, khôngofficialreport/commit. Đủ5EX, hmac/forgot/reset/exp theoHumanExtend.
- **Human review:** Kiểm G6/EX API1: đủ 10 case G6 và 5 EX, gồm decode exp, forgot/reset và HMAC bằng secret trong file. 11 GUID mất brace đã sửa trước lần chạy cuối; full run 230 request/449 assertion, 0 lỗi script, 150 fail là ứng viên bug nên giữ nguyên.

## #31 – 2026-11-24 23:03 (giờ VN)
- **AI tool:** task PRX3 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** API 3 – Execute – PR-X3
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 3 – Execute – PR-X3: chuyển các case PR-G6-xx và PR-EX-xx thành request trong collection API 3, folder G6 và EX.
  > Input: report/testcases/API3_product_generated.md (mục G6, Extend – Human, Audit). Tuân thủ Phần B.
  > Chú ý riêng:
  > - PR-EX-01/02/06: path %2B{{P}}, {{P}}.0 gửi nguyên văn; sau request kiểm GET /api/products/{{P}} và list bằng S.
  > - PR-EX-03 gửi body raw `"price": 1e309` đúng nguyên văn (không để script tính ra Infinity rồi stringify).
  > - PR-EX-04 gửi body raw `"price": -0`.
  > - PR-EX-05 xóa product seed id 2: đặt request này ở CUỐI CÙNG của collection (folder "EX-last" sau EX), description ghi "chạy cuối vì xóa dữ liệu seed".
  > Chạy thử: reset SUT, newman ... --folder G6, --folder EX, --folder EX-last, rồi toàn collection. Chỉ sửa lỗi kỹ thuật.
  > Xong khi: mọi case G6 VALID/INCOMPLETE và đủ 6 case PR-EX có folder; PR-EX-05 là request cuối; toàn collection chạy không lỗi script; báo tổng pass/fail và thời gian chạy.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Never derive an endpoint from display-label substrings: earlier label contains "chưa đăng ký" wrongly mapped login to register; construct explicit method/path. Avoid top-level identifier data because Newman sandbox injects legacy data binding; use a case-specific/scoped response variable. For large one-line JSON, ast_edit exact folder node then resolve proposal; a staged or failed edit is NOT applied. Verify tool operation result before claiming ready (no runtime tests while coding). Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X3: modify only G6/EX and API3 EX-last ordering; preserve earlier completed G1/G2/G3/G4 folders and protected hook. EX-last containing PR-EX-05 must be last after _smoke; only its own verification requests may follow seed delete. Audit+Human Extend are authoritative. No expected changes. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API3_ProductCRUD.postman_collection.json
  > SOURCE: report/testcases/API3_product_generated.md
- **AI output:**
  > Thêm41caseG6=35/EX=6,361requests; xóaemptyduplicateG6/EX, EX-lastchứaPR-EX-05sau_smoke vàrequestdescriptionriskreset. Literal1e309/-0 vàencodedpaths giữđúng. DebugG6:322requestattempts242requesterrors,351assert83pass268fail/6.8s; SUTchếtkhicaseG6-09price:nullđượcchấpnhậnrồiGETserializertoString(null). EXriêng34req47assert29pass18fail/856ms; EX-last5req7assert4pass3fail/221ms. Full:979attempts77requesterrors,1233assert892pass341fail/1m34.5s,51testscriptfailuresdoserverunavailable. server.logxácnhậnbackend/server.js:162TypeError, khôngorchestrationreset. TIÊUCHÍruntimecleanCHƯAĐẠTdoSUTcrash; oraclesphầnsaukhôngđượckiểmđầyđủ. KhôngváSUT/đổi expected/bỏcase/retryđểchecrash; X4mappingghirõgiớihạn, khôngreportchínhthức/commit.
- **Human review:** Đồng ý không vá SUT: crash tại server.js:162 do serialize price null, không phải lỗi setup; các case sau không quan sát được nên việc ghi tiêu chí runtime sạch chưa đạt là trung thực. Cần tách PR-G6-09/15/31 ở X4 và ghi crash thành bug.

## #32 – 2026-11-24 23:05 (giờ VN)
- **AI tool:** task CNX3 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol)
- **API / Bước:** API 2 – Execute – CN-X3
- **Prompt:**
  > BỐI CẢNH CHUNG – HW06 API Testing, bước Execute (đọc kỹ trước khi làm)
  > - Thư mục làm việc: /home/zinn/zinn/testing/hw06. Đề: "2026.HW06.API Testing_En.pdf". Quy tắc: agent.md (BẮT BUỘC đọc và tuân theo).
  > - KHÔNG push, KHÔNG tạo issue, KHÔNG commit (Manager tự commit ở X0 và X5).
  > - MSSV 23120190. SUT: EShop backend, base URL http://localhost:3000, reset bằng scripts/reset_sut.sh (khởi động lại server = DB seed lại, cart trong RAM bị xóa).
  > - Environment Postman: environments/local.postman_environment.json (baseUrl, studentId, adminEmail/adminPassword, userEmail/userPassword). Dùng {{baseUrl}}, không hardcode localhost trong request.
  > - Newman 6.2.3 + newman-reporter-htmlextra đã cài global.
  > 
  > NGUỒN TEST CASE
  > - Mỗi API có 1 file trong report/testcases/. Cuối file có mục "## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)" và mục "## Extend – Human".
  > - CHUYỂN THÀNH REQUEST: mọi case nhãn VALID, mọi case nhãn INCOMPLETE, và mọi case <tiền tố>-EX-xx.
  > - BỎ QUA: case nhãn INVALID. Liệt kê các ID bị bỏ trong description của collection kèm lý do "INVALID theo audit".
  > - Case INCOMPLETE: đọc lý do audit. Nếu lý do chỉ ra quy ước thay thế (ví dụ "phải sửa expected theo quy ước G6") thì dùng quy ước đó. Nếu case không thể tự động hóa đầy đủ thì làm phần làm được và ghi "INCOMPLETE: <phần thiếu>" trong description của request.
  > - Mục G5 chỉ là báo cáo, không có request.
  > 
  > QUY ƯỚC COLLECTION
  > - Postman Collection v2.1, tên collection trùng tên file (bỏ đuôi): 23120190_API1_Login, 23120190_API2_CancelOrder, 23120190_API3_ProductCRUD.
  > - Cấu trúc folder: G1, G2, G3, G4, G6, EX (theo mục trong file test case). Mỗi test case là MỘT folder con tên "[<ID>] <Mục đích>". Request setup nằm trong folder đó, tên "[<ID>] setup: <việc>"; request chính tên "[<ID>] <method> <path>".
  > - Pre-request script CẤP COLLECTION (đã có từ X0, không sửa):
  >     pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });
  >     console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));
  >   Vì header được thêm ở đây, KHÔNG dùng pm.sendRequest cho setup (request gửi bằng pm.sendRequest không đi qua pre-request này). Setup phải là request thật, hiện trong report.
  > - Dữ liệu độc lập: mỗi case tự tạo user/đơn/sản phẩm như cột Precondition. Email duy nhất dùng {{$guid}} hoặc Date.now(). Lưu biến bằng pm.collectionVariables với tên có tiền tố ID (ví dụ lg_g1_01_email) để case không dùng chung biến.
  > - Case cần chờ (ví dụ chờ 31 giây sau khóa): dùng setTimeout trong pre-request của request cần chờ. Thời gian chờ lấy ĐÚNG theo file test case (spec 30 giây). KHÔNG tăng thời gian chờ để khớp hành vi thực tế của SUT.
  > - Case xóa/sửa dữ liệu seed (ví dụ PR-EX-05 xóa product id 2) đặt ở CUỐI collection và ghi rõ trong description.
  > 
  > QUY ƯỚC ASSERTION (quan trọng nhất)
  > - Tên test: "[<ID>] <điều kiện>". Mỗi case có:
  >   * Assertion CỐT LÕI: điều spec nói chắc chắn hoặc điều kiện trong cột "Expected body / kiểm tra" (ví dụ: không có token, dữ liệu không đổi, không lộ password, schema đúng). Tên: "[<ID>] core: <điều kiện>".
  >   * Assertion STATUS: nếu status ghi trong file là spec nói rõ thì tên "[<ID>] status <n>". Nếu status là GIẢ ĐỊNH thì tên "[<ID>] status <n> (GIẢ ĐỊNH)" và VẪN kiểm đúng mã đó.
  >   Mục đích: khi chạy, người dùng tách được fail do bug thật (core) với fail do giả định mã lỗi.
  > - Schema (G4 và case SCH): dùng pm.response.to.have.jsonSchema(<schema trong file test case>), dán nguyên schema.
  > - Expected lấy từ file test case. TUYỆT ĐỐI KHÔNG sửa expected, mã status, schema hay thời gian chờ cho khớp response thực tế. Được phép đọc eshop-sut/backend/ ở bước này chỉ để hiểu vì sao REQUEST lỗi kỹ thuật (ví dụ tên field), không để đổi expected.
  > - Test fail là kết quả bình thường. Không thêm điều kiện bỏ qua (skip), không bọc assertion trong try/catch để nuốt lỗi.
  > 
  > CHẠY THỬ (chỉ để gỡ lỗi collection)
  > - Trước mỗi lần chạy thử: scripts/reset_sut.sh.
  > - Lệnh: newman run <collection> -e environments/local.postman_environment.json --reporters cli [--folder <tên>]
  > - CẤM ghi file vào results/newman/ và CẤM dùng reporter htmlextra/json. File report chính thức do người dùng tự chạy.
  > - Kết quả chạy thử chỉ dùng để sửa lỗi kỹ thuật. Không chép response vào report như bằng chứng bug.
  > 
  > QUY TẮC AI LOG
  > - Prompt có cụm "ghi vào log" thì sau khi xong PHẢI append một entry vào report/AI_LOG.md theo đúng định dạng agent.md mục 1. AI tool = tên agent + model của chính bạn. Giờ lấy bằng `date "+%Y-%m-%d %H:%M"`. Prompt ghi NGUYÊN VĂN, chỉ bỏ cụm "ghi vào log" ở câu đầu. Human review để trống. Nếu agent khác đang ghi log thì đợi.
  > - API / Bước ghi dạng "API 1 – Execute – LG-X1".
  > 
  > CẤM
  > - Bịa response SUT; sửa code SUT; sửa file test case (report/testcases/*); sửa collection của API khác; tạo/sửa file trong results/newman/.
  > 
  > CUỐI MỖI LẦN LÀM
  > - Báo lại cho Manager: file đã tạo/sửa, số folder case đã thêm, danh sách ID đã chuyển, ID bỏ qua kèm lý do, và bằng chứng cho từng tiêu chí "Xong khi".
  > 
  > API 2 – Execute – CN-X3: chuyển các case CN-G6-xx và CN-EX-xx thành request trong collection API 2, folder G6 và EX.
  > Input: report/testcases/API2_cancel_generated.md (mục G6, Extend – Human, Audit). Tuân thủ Phần B.
  > Chú ý riêng:
  > - CN-EX-01/03/04: path %2B{{O}}, {{O}}.0, 0{{O}} gửi nguyên văn. Sau request hủy, gọi GET /api/orders/{{O}} bằng token chủ đơn để kiểm đơn vẫn pending (oracle K).
  > - CN-EX-02 đi qua forgot-password → reset-password rồi dùng token CŨ.
  > - CN-EX-05 ký JWT HS256 bằng CryptoJS với secret ghi trong file.
  > Chạy thử: reset SUT, newman ... --folder G6, rồi --folder EX, rồi toàn collection. Chỉ sửa lỗi kỹ thuật.
  > Xong khi: mọi case G6 VALID/INCOMPLETE và đủ 5 case CN-EX có folder; toàn collection chạy không lỗi script; báo tổng pass/fail và thời gian chạy.
  > 
  > 
  > 
  > MANAGER CONTRACT (higher priority): Read skill://ponytail first; active throughout; reviewers also ponytail-review. User requests parallel chains X1→X4, then X-DATA, stop human gate, NO X5/commits. Only ONE assigned step per task. Manager owns AI_LOG; DO NOT edit log/git. Return actual model/date and exact case/request counts, skipped INVALID IDs/reasons and implementation evidence. Repo rules already supplied: no discovery/read of agent/context files.
  > CRITICAL USER UPDATE: collection-level prerequest two lines from NEW PartB are IMMUTABLE, especially console.log pm.variables.replaceIn(...). Do not modify, reformat or replace either line/event. If mismatch report immediately, NEVER repair. Manager verified starting hooks match user c7b77c2.
  > Own ONLY assigned collection; edit ONLY current step folders and description INVALID list, existing file MUST edit (never shell/Python overwrite/write whole existing JSON). No testcase/env/reset/runner/SUT/reports/other collection changes. New scratch generator files ONLY local:// if genuinely needed, delete afterward; don't leave generator/source scripts in repo. Shared language/helper patterns inside your own collection must be boring and request assertions explicit. No nested delegation.
  > IMPORTANT RUNTIME SERIALIZATION: skip all test/build/lint/formatters/static QA commands and ALL SUT/Newman/reset calls while coding. Manager delegates CLI checking to sonic afterward with shared SUT exclusive lock. Thus verbatim prompt's debug-run clauses handled by manager, not worker. Do not tune expected from SUT. Read spec/testcases only as necessary; backend only if later exact technical request defect cannot be resolved from docs.
  > Implement every VALID/INCOMPLETE case in assigned G sections; audit is source of truth, read its reason + G6 current convention and latest G5 for oracle precedence. INVALID IDs listed with 'INVALID theo audit', never folders. Copy request/expectation precisely, own case-prefixed collectionVariables, fresh setup per case, all actual setup requests (no pm.sendRequest). No skipRequest/setNextRequest skipping consumer failures; no swallowed assertions/try-catch suppression, no fake fallback tokens/IDs/data. Assert core and status separately; assumptions in status testnames. Assertions must be consumer meaningful, no always-true/not-throw/source echoes. Assertion fail due SUT/schema/status is normal, not 'technical error' to fix. Safe JSON field extraction cannot hide failed setup; requests missing identifiers must produce explicit failed setup assertions, not fake success.
  > Use environment admin/user credentials. Never derive an endpoint from display-label substrings: earlier label contains "chưa đăng ký" wrongly mapped login to register; construct explicit method/path. Avoid top-level identifier data because Newman sandbox injects legacy data binding; use a case-specific/scoped response variable. For large one-line JSON, ast_edit exact folder node then resolve proposal; a staged or failed edit is NOT applied. Verify tool operation result before claiming ready (no runtime tests while coding). Every URL starts {{baseUrl}}; percent-encoded paths exact, disable URL encoding when needed using request.protocolProfileBehavior disableUrlEncoding. Postman sandbox CryptoJS built-in where needed; no added dependencies. Long JSON/control/raw values exact. Timers per source31/29 relative lock timestamp, no extending wait due SUT. Folder testcases [ID] purpose; all setup/main request/test names prefixed[ID]. Subedges for CN A[...] have NEW independent orders. Snapshot comparisons by ID with entire fields ignoring ordering; never accept additional statuses. Collections may include _smoke unchanged.
  > For X3: modify only G6/EX and API3 EX-last ordering; preserve earlier completed G1/G2/G3/G4 folders and protected hook. EX-last containing PR-EX-05 must be last after _smoke; only its own verification requests may follow seed delete. Audit+Human Extend are authoritative. No expected changes. Read complete setup definitions, not truncated lines. Preserve original hook lines bytes. Do not run commands merely to test generation; deliver and Manager checks.
  > 
  > OWN FILE: collections/23120190_API2_CancelOrder.postman_collection.json
  > SOURCE: report/testcases/API2_cancel_generated.md
- **AI output:**
  > Thêm15caseG6=10/EX=5,220requests; bỏG6-05/12INVALID vàemptyduplicates. Sửa24GUIDliteralsX2(thừa kỹthuật20G3/4G4)thànhdoublebrace, khôngexpected/hookchanges. G6CLI178req239assert234pass5fail/4.2s; EX42req63assert48pass15fail/1.101s. Finalfullverbatimlocal83:904req,904testscripts,1073prerequests,1230assert1184pass46fail/36.4s; khôngrequest/scriptfailures. Báocáo688/792banđầucủaverifierđãsửa theoartifact, khôngdùngsốsai. ProperUUID,percentencodedpaths vàStudentIDlocalhostverified. Expiry/deleteduserpreconditionsINCOMPLETE khônggiảpass. Khôngofficialreport/commit.
- **Human review:** Kiểm G6/EX API2: 15 folder, bỏ G6-05/12 đúng INVALID, 24 GUID thiếu brace đã sửa mà không đổi expected. Full run 904 request/1230 assertion, 0 lỗi request/script, 46 fail giữ nguyên. Không giả pass cho precondition exp/user bị xóa là đúng.


## #33 – 2026-11-25 03:07 (giờ VN)
- **AI tool:** Manager (openai-codex/gpt-6.1-sol)
- **API / Bước:** API 1 – Execute – LG-X4
- **Prompt:**
  > . Đội agent quay lại dùng Codex (quota 5h vừa hồi). Tiếp tục bước Execute đang dở theo EXECUTE_PROMPTS.md, đọc lại PHẦN A và PHẦN B trong file trước khi giao việc.
  > Trạng thái hiện tại (đã kiểm từ file và AI_LOG):
  > - Xong: X0 (commit c7b77c2), LG-X1..X3, CN-X1..X3, PR-X1..X3. Collection đã có đủ folder G1..EX.
  > - LG-X4: đã có report/execute/API1_login_mapping.md nhưng CHƯA có entry log. Kiểm file này đủ tiêu chí "Xong khi" của LG-X4; đạt thì ghi log, chưa đạt thì giao LG-X4 lại.
  > - X-DATA: đã có data/lg_g1_partition.csv, folder "DATA – LG-G1" và lệnh trong scripts/run_newman.sh nhưng CHƯA có log. Kiểm tiêu chí "Xong khi" của X-DATA rồi xử lý như trên.
  > - Chưa làm: CN-X4, PR-X4 → giao cho reviewer, chạy song song.
  > Giữ nguyên quy tắc: không commit trong X1–X4, không tạo file trong results/newman/, không sửa expected, không sửa 2 dòng pre-request. Xong hết thì dừng ở bước 🧑 và gửi tôi tin nhắn hướng dẫn chạy run_newman.sh.
- **AI output:**
  > Kiểm mapping hiện có đạt tiêu chí: 71/71 ID nguồn có dòng; 68 case chuyển (61 VALID, 2 INCOMPLETE, 5 EX), 3 INVALID không có folder; 229 request/473 assertion nguồn, cộng smoke 230/474. Các số từng folder khớp collection hiện tại. Bằng chứng CLI LG-X4 đã có trong mapping: 322 pass/152 fail, 230 request, không lỗi script/request, 4m17s; không chạy lại. Bổ sung mô tả phạm vi tổng đếm trước X-DATA và ngoại lệ skipRequest hợp lệ khi DATA không có caseId. Không finding mở; hai dòng pre-request giữ nguyên; results/newman chỉ có .gitkeep. Không commit/report chính thức.
- **Human review:** Mở mapping API1: 71/71 ID có dòng, 68 case được chuyển, 3 INVALID không có folder, số request/assertion khớp collection. Chấp nhận dùng lại bằng chứng CLI cũ thay vì chạy lại; ngoại lệ skipRequest khi DATA thiếu caseId đã ghi rõ nên không che fail.


## #34 – 2026-11-25 03:07 (giờ VN)
- **AI tool:** Manager (openai-codex/gpt-6.1-sol); sonic ExecuteProof (openai-codex/gpt-6-luna)
- **API / Bước:** Execute – X-DATA
- **Prompt:**
  > . Đội agent quay lại dùng Codex (quota 5h vừa hồi). Tiếp tục bước Execute đang dở theo EXECUTE_PROMPTS.md, đọc lại PHẦN A và PHẦN B trong file trước khi giao việc.
  > Trạng thái hiện tại (đã kiểm từ file và AI_LOG):
  > - Xong: X0 (commit c7b77c2), LG-X1..X3, CN-X1..X3, PR-X1..X3. Collection đã có đủ folder G1..EX.
  > - LG-X4: đã có report/execute/API1_login_mapping.md nhưng CHƯA có entry log. Kiểm file này đủ tiêu chí "Xong khi" của LG-X4; đạt thì ghi log, chưa đạt thì giao LG-X4 lại.
  > - X-DATA: đã có data/lg_g1_partition.csv, folder "DATA – LG-G1" và lệnh trong scripts/run_newman.sh nhưng CHƯA có log. Kiểm tiêu chí "Xong khi" của X-DATA rồi xử lý như trên.
  > - Chưa làm: CN-X4, PR-X4 → giao cho reviewer, chạy song song.
  > Giữ nguyên quy tắc: không commit trong X1–X4, không tạo file trong results/newman/, không sửa expected, không sửa 2 dòng pre-request. Xong hết thì dừng ở bước 🧑 và gửi tôi tin nhắn hướng dẫn chạy run_newman.sh.
- **AI output:**
  > Kiểm CSV đủ 20 dòng lớp email/password VALID LG-G1-01..21 trừ INVALID LG-G1-14; các lớp body/media LG-G1-22..25 nằm ngoài phạm vi CSV và vẫn có trong G1. Folder DATA có setup độc lập UUID và login dựng body bằng iterationData, giữ expected/core/GIẢ ĐỊNH. CLI thực chạy bởi sonic openai-codex/gpt-6-luna: 20 iterations, 40 requests, 76 assertions = 54 pass/22 fail, không lỗi request/script, 1009 ms. Chạy DATA không CSV: 0 request/0 assertion, guard hoạt động, 40 ms. Runner chính thức lọc G1..EX (API3 thêm EX-last), có lần chạy DATA riêng với -d và reset trước mỗi run; bash -n đạt. Không chạy runner chính thức, không tạo report, không commit. Đạt tiêu chí X-DATA; giữ nguyên hai dòng pre-request.
- **Human review:** Kiểm CSV 20 dòng phủ LG-G1-01..21 trừ LG-G1-14, folder DATA dùng iterationData và giữ expected/core. Chạy không CSV ra 0 request chứng minh guard đúng; 22 fail là do SUT/giả định. Lưu ý chỉ có HTML DATA, không có JSON nên số liệu DATA lấy từ HTML.

## #35 – 2026-11-25 15:23 (giờ VN)
- **AI tool:** Manager (openai-codex/gpt-6.1-sol)
- **API / Bước:** API 2 – Execute – CN-X4
- **Prompt:**
  > . Tiếp tục bước Execute theo EXECUTE_PROMPTS.md. Đọc lại PHẦN A, PHẦN B và agent.md trước khi giao việc. Giữ model của các agent đúng như config hiện tại, không đổi model.
  >
  > Trạng thái (đã kiểm từ file và AI_LOG):
  > - Xong và đã có log: X0 (commit c7b77c2), LG/CN/PR-X1..X3, LG-X4 (#33), X-DATA (#34).
  > - CN-X4: đã có report/execute/API2_cancel_mapping.md nhưng CHƯA có log. Kiểm tiêu chí "Xong khi" của CN-X4: đạt thì ghi log, chưa đạt thì giao reviewer làm lại phần thiếu. Các điểm F1–F7 trong mục 7 của file cần Manager quyết định; ghi quyết định vào log.
  > - PR-X4: đã có report/execute/API3_product_mapping.md nhưng CHƯA có log. Phần tĩnh đạt; phần runtime "chưa khẳng định" vì lần chạy thử SUT dừng ở PR-G6-09.
  >   → Giao task: reset SUT bằng scripts/reset_sut.sh, chạy collection PR bằng newman --reporters cli để tìm nguyên nhân dừng ở PR-G6-09 (SUT crash hay lỗi script/setup). Nếu do script thì sửa script/setup của collection; nếu SUT crash thật thì đó là bug: ghi lại response/log thật, để case đó fail, xếp nó chạy cuối hoặc tách để các case sau vẫn chạy. Không sửa expected để cho pass.
  >   → Sau đó reviewer cập nhật mục "Runtime sạch" trong API3_product_mapping.md theo kết quả chạy thật, rồi ghi log PR-X4.
  >
  > Quy tắc giữ nguyên: không commit, không tạo file trong results/newman/, không sửa expected, không sửa 2 dòng pre-request cấp collection, không dùng htmlextra/json reporter. Commit message không ghi tên AI.
  >
  > Xong hết thì dừng ở bước 🧑 và gửi tôi tin nhắn hướng dẫn chạy ./scripts/run_newman.sh và chụp console X-Student-Id vào evidence/xstudentid_console.png.
- **AI output:**
  > Đọc lại PHẦN A/B và agent.md. CN-X4 đạt: 64/64 ID nguồn được mapping, 55 case nguồn + 25 sub-folder cạnh trạng thái; 9 INVALID bỏ đúng; 906 request/1233 assertion tĩnh gồm smoke khớp mapping. Không cần giao reviewer làm lại. Dùng bằng chứng CLI đã có, không chạy lại để xác nhận: 906 request, 1233 assertion = 1185 pass/48 fail, 31.6 s, không lỗi request/script. results/newman/ chỉ có .gitkeep; hook đúng hai dòng.
  > Quyết định Manager F1: giữ tên oracle “setup” lần này; assertion core và ID vẫn phân biệt được lỗi, không ảnh hưởng expected. F2: chấp nhận INCOMPLETE CN-G3-04 theo file và SUT hiện không có exp; đây chỉ là kiểm precondition, KHÔNG tuyên bố đã kiểm token hết hạn; nếu sau này có exp thì phải bổ sung nhánh chờ/PUT/K trước khi tuyên bố đầy đủ. F3: giữ điều hướng dừng case theo precondition xóa user của file; đây không phải bỏ qua assertion request chính; lần chạy quan sát không kích hoạt, request đích tồn tại; ràng buộc ID cứng được ghi nhận, không coi case đạt khi setup fail. F4: giữ kiểm JWT chặt hơn; nếu thông báo chứa a.b.c thì cần human review false positive, không nới regex theo response. F5: giữ bước lưu baseline, chỉ request 2/3 chứng minh so sánh; assertion đầu không được diễn giải là bằng chứng chống dò ID độc lập. F6: giữ oracle dùng token cũ đúng file; khi token bị vô hiệu, oracle không quan sát được trạng thái đơn, không suy diễn lỗi dữ liệu từ 401. F7: giữ tên folder hiện tại vì ID duy nhất và mapping mô tả rõ mục đích; không đổi tên thuần hình thức trong lượt này. Không sửa collection/expected, không commit, không tạo report chính thức.
- **Human review:** Đối chiếu mapping API2: 64/64 ID, 55 case + 25 sub-folder cạnh, 9 INVALID bị bỏ, 906 request/1233 assertion khớp. F2/F5/F6 giữ đúng giới hạn quan sát, không tuyên bố đã kiểm token hết hạn và không suy diễn khi oracle 401; F1/F7 chỉ là đặt tên nên không ảnh hưởng kết quả.

## #36 – 2026-11-25 15:33 (giờ VN)
- **AI tool:** Manager (openai-codex/gpt-6.1-sol); task ProductIsolation (openai-codex/gpt-6.1-terra); sonic ProductRuntime/ProductProof (openai-codex/gpt-6-luna); reviewer ProductMappingReview (anthropic/claude-sonnet-5-5)
- **API / Bước:** API 3 – Execute – PR-X4
- **Prompt:**
  > . Tiếp tục bước Execute theo EXECUTE_PROMPTS.md. Đọc lại PHẦN A, PHẦN B và agent.md trước khi giao việc. Giữ model của các agent đúng như config hiện tại, không đổi model.
  >
  > Trạng thái (đã kiểm từ file và AI_LOG):
  > - Xong và đã có log: X0 (commit c7b77c2), LG/CN/PR-X1..X3, LG-X4 (#33), X-DATA (#34).
  > - CN-X4: đã có report/execute/API2_cancel_mapping.md nhưng CHƯA có log. Kiểm tiêu chí "Xong khi" của CN-X4: đạt thì ghi log, chưa đạt thì giao reviewer làm lại phần thiếu. Các điểm F1–F7 trong mục 7 của file cần Manager quyết định; ghi quyết định vào log.
  > - PR-X4: đã có report/execute/API3_product_mapping.md nhưng CHƯA có log. Phần tĩnh đạt; phần runtime "chưa khẳng định" vì lần chạy thử SUT dừng ở PR-G6-09.
  >   → Giao task: reset SUT bằng scripts/reset_sut.sh, chạy collection PR bằng newman --reporters cli để tìm nguyên nhân dừng ở PR-G6-09 (SUT crash hay lỗi script/setup). Nếu do script thì sửa script/setup của collection; nếu SUT crash thật thì đó là bug: ghi lại response/log thật, để case đó fail, xếp nó chạy cuối hoặc tách để các case sau vẫn chạy. Không sửa expected để cho pass.
  >   → Sau đó reviewer cập nhật mục "Runtime sạch" trong API3_product_mapping.md theo kết quả chạy thật, rồi ghi log PR-X4.
  >
  > Quy tắc giữ nguyên: không commit, không tạo file trong results/newman/, không sửa expected, không sửa 2 dòng pre-request cấp collection, không dùng htmlextra/json reporter. Commit message không ghi tên AI.
  >
  > Xong hết thì dừng ở bước 🧑 và gửi tôi tin nhắn hướng dẫn chạy ./scripts/run_newman.sh và chụp console X-Student-Id vào evidence/xstudentid_console.png.
- **AI output:**
  > Giữ nguyên model theo config, không đổi model. Đọc PHẦN A/B và agent.md trước giao việc; ghép PHẦN B nguyên văn qua local://execute_worker_context.txt. Sonic reset rồi chạy full PR CLI để chẩn đoán: 979 request/77 lỗi, 1234 assertion/341 fail, 1m24.4s. PR-G6-09 PUT price:null trên id121 lẻ trả 200, chưa crash; lần crash đầu của lượt này ở PR-G6-31 GET id150 sau PUT body {} trả 200. Log thật server.js:162: TypeError: Cannot read properties of null (reading 'toString'); sau đó ECONNREFUSED. Đây là bug SUT, không phải lỗi setup. Giữ artifact CLI/server trước reset trong local://product-before-isolation-{cli,server}.log; không coi là report chính thức.
  > Task chuyển nguyên vẹn PR-G6-09/15/31 (price null, thiếu price, body rỗng) sang G6-isolated trong collection API3; không sửa request/expected/assertion/hook. scripts/run_newman.sh chạy mỗi case riêng với reset trước từng lượt, ghi trạng thái fail nhưng tiếp tục; reset rồi chạy lượt chính G1/G2/G3/G4/G6/EX/EX-last. PR-EX-05 vẫn cuối lượt chính và collection. Manager đổi dấu phân tách tên report riêng thành API3_ProductCRUD_isolated-<ID>_<ngày>.html/json để khớp wildcard API3_ProductCRUD_* của X5. Agent không chạy runner hay reporter chính thức; các file đó chỉ sinh khi sinh viên chạy.
  > Kiểm CLI sau sửa bởi sonic: bash -n đạt. Ba lượt riêng mỗi lượt 9 request/1 lỗi request, 13 assertion = 8 pass/5 fail, không lỗi script; thời gian PR-G6-09/15/31 lần lượt 292/297/342ms. Cả ba GET detail id6 báo socket hang up và log TypeError null.toString; giữ fail, không nuốt lỗi. Lượt chính reset độc lập: 951 request/0 lỗi, 948 test script/0 lỗi, 1198 pre-request script/0 lỗi, 1231 assertion = 938 pass/293 fail, 1m22.1s; chạy tới PR-G6-32..35 và PR-EX-05, không crash. Cộng bốn lượt độc lập: 978 request, 3 lỗi request, 1270 assertion = 962 pass/308 fail. Reset cuối đã hoàn thành. Artifact local://product-isolate-PR-G6-<09|15|31>-{cli,server}.log và local://product-regular-G1-G2-G3-G4-G6-EX-EX-last-{cli,server}.log lưu số liệu thật.
  > Reviewer cập nhật report/execute/API3_product_mapping.md: mapping đủ 133 ID (125 case + 8 INVALID), G6 còn 32 case/295 request/419 assertion; G6-isolated 3/27/39; tổng tĩnh nguồn giữ 994 request/1287 assertion. Lượt chính tĩnh 967/1248, thực chạy 951/1231 do parity PR-G4-07 thoát setup sớm đúng file. Đủ 125 case qua bốn lượt; runtime sạch chỉ cho lượt chính về request/script, KHÔNG sạch toàn cục và KHÔNG all pass. X5 phải gộp JSON chính và cả ba JSON isolated. Không finding chặn; giữ các quan sát tĩnh không đổi expected. Reviewer báo không có edit tool nên đã sửa mapping bằng scripted replacement trái chỉ dẫn edit-only; Manager đã report_issue về bất nhất tool, không lặp lại thao tác đó. results/newman/ chỉ có .gitkeep; không commit, không tạo report chính thức, không sửa SUT/testcase/hai dòng pre-request. Dừng ở bước người dùng tự chạy và chụp console, chưa làm X5.
- **Human review:** Chấp nhận tách 3 case sang G6-isolated và reset từng lượt: lượt chính 951 request/1231 assertion, 938 pass, không lỗi script, chạy tới PR-EX-05. Ba lượt isolated đều tái hiện TypeError null.toString nên đó là bug SUT, phải giữ fail. Việc reviewer sửa mapping bằng script trái quy ước đã được báo; số liệu vẫn khớp artifact.

## #37 – 2026-11-25 16:05 (giờ VN)
- **AI tool:** Manager (openai-codex/gpt-6.1-sol); task LoginResults/CancelResults/ProductResults (openai-codex/gpt-6.1-terra); sonic OfficialManifest (openai-codex/gpt-6-luna); reviewer ResultsReview (anthropic/claude-sonnet-5-5)
- **API / Bước:** API 1, API 2, API 3 – Execute – X5
- **Prompt:**
  > . Tôi đã chạy ./scripts/run_newman.sh và chụp evidence/xstudentid_console.png. Làm X5 theo EXECUTE_PROMPTS.md: đọc JSON thật trong results/newman/ (gộp cả 3 file isolated của API3), viết report/execute/API<n>_*_results.md, rồi tạo 3 commit execute như prompt X5. Không sửa file trong results/newman/. Commit message không ghi tên AI. Chưa push.
  > Lưu ý: results/newman/23120190_API3_ProductCRUD_20261125.json nặng 190MB, vượt giới hạn 100MB của GitHub; KHÔNG commit file này (thêm vào .gitignore), chỉ commit file HTML. Ghi rõ lý do trong results.md.
- **AI output:**
  > Chỉ đọc sáu JSON Newman chính thức ngày 20261125, đủ HTML tương ứng và DATA HTML; mọi request host localhost. Không chạy lại Newman/SUT/runner. Đã xem ảnh evidence/xstudentid_console.png: console có X-Student-Id: 23120190 và localhost. Tạo report/execute/API1_login_results.md, API2_cancel_results.md, API3_product_results.md: số liệu run.stats/timings, bảng đủ failure nối đúng execution/cursor, expected từ testcase/audit/G6, body thật che token/mật khẩu, nhóm ứng viên theo hiện tượng và phần status GIẢ ĐỊNH cần sinh viên quyết định. Không severity, không bug report.
  > API1 JSON: 229 request, 473 assertion = 321 pass/152 fail, 257312ms, 10 nhóm ứng viên. DATA HTML riêng: 20 iteration, 40 request, 76 assertion = 54 không fail/22 fail, 1078ms; runner không sinh JSON DATA, không giả số liệu hay response JSON DATA và không cộng vào JSON chính. API2: 905 request, 1232 assertion = 1184 pass/48 fail, 34558ms, 8 nhóm ứng viên; 17 fail chỉ status giả định, 1 setup INCOMPLETE exp không phải tấn công hết hạn đã chạy.
  > API3 gộp bốn lượt: 978 request/3 lỗi request, 1270 assertion = 962 pass/308 fail, tổng thời lượng 83153ms không gồm reset, 7 nhóm ứng viên. Lượt chính 951 request, 1231 assertion = 938 pass/293 fail, 82173ms; isolated PR-G6-09/15/31 mỗi lượt 9 request/1 lỗi, 13 assertion = 8 pass/5 fail, 321/347/312ms. Bảng đủ 311 failure records = 308 assertion + 3 lỗi request. Không cộng trùng setup parity bị bỏ qua. Trích mảng là phần tử thật nhưng không luôn là phần tử chứng minh thay đổi; xem full JSON để đối chiếu snapshot.
  > Main JSON API3 chính xác 189863153 byte, SHA256 b9cccdbf68c595cd12868289b5032cab2f2ef44143f732f3cf50df3dead31eae: giữ local, thêm đúng đường dẫn vào .gitignore, loại khỏi commit vì vượt giới hạn GitHub100MB; báo cáo ghi rõ lý do/hash/kích thước. HTML chính và cả HTML/JSON của ba isolated vẫn thuộc commit API3. Không sửa bất kỳ file trong results/newman; đã lấy manifest hash/kích thước các artifact gốc. Reviewer độc lập ACCEPT, không lỗi thực tế chặn. Ứng viên chỉ là nhóm cần điều tra, không phải số bug đã xác nhận.
  > Thực hiện ba commit riêng theo X5 qua selective commit: API1 kèm DATA, runner chung, AI_LOG và ảnh; API2 kèm collection/mapping/results/HTML/JSON; API3 kèm collection/mapping/results/HTML chính/ba cặp isolated và quy tắc ignore main JSON lớn. Giữ nguyên thay đổi .gitignore có sẵn ngoài quy tắc được yêu cầu. Không push. Artifact chính thức và ảnh gốc có thể chứa token/password local; không chỉnh bằng chứng theo yêu cầu người dùng.
- **Human review:** Đã đối chiếu 3 results.md với JSON/HTML: API1 229/473, API2 905/1232, API3 gộp 978 request/1270 assertion, đúng 311 failure record. Token/password trong body đã che; JSON 190MB không commit nhưng có hash/kích thước trong báo cáo và .gitignore. Các nhóm chỉ là ứng viên, chưa chốt bug.

## #38 – 2026-11-25 16:17 (giờ VN)
- **AI tool:** Manager (openai-codex/gpt-6.1-sol); scout BugTriage (openai-codex/gpt-6-luna); task CorrectTriage (openai-codex/gpt-6.1-terra)
- **API / Bước:** API 1, API 2, API 3 – Bug report – B0
- **Prompt:**
  > . Làm bước Bug report theo BUGREPORT_PROMPTS.md. Đọc PHẦN A, PHẦN B và agent.md trước khi giao việc. Bắt đầu từ B0 và dừng ở 🧑1.
- **AI output:**
  > Đã đọc PHẦN A/B và agent.md trước giao việc; ghép PHẦN B và prompt B0 nguyên văn vào assignment. Scout chỉ đọc, không gọi SUT. Manager từ chối draft scout do trùng root cause JWT xuyên API, phân loại và ledger mâu thuẫn, đếm sai, xếp nhầm crash vào không phải bug; giao task sửa phần thiếu B0, không chuyển sang B1.
  > Tạo report/issues/00_triage.md sau khi đối chiếu ba results.md, testcase, README/api_specification và backend. Bảng (a): 10 dòng đề xuất nguyên nhân gốc, bao phủ 13 nhóm nguồn; bảng (b): 12 nhóm cần sinh viên quyết định với hai cách hiểu; bảng (c): failure setup CN-G3-04 INCOMPLETE ngoài 25 nhóm, không kết luận đã thực thi token hết hạn. Đủ 25/25 nhóm, mỗi nhóm đúng một bảng. Giữ mơ hồ về status, wire type/schema, normalization, thu hồi JWT, ID canonical và media-type/JSON lỗi ở phần cần quyết định; ghi giới hạn case validation trong ghi chú, không sửa expected.
  > Bug ID đề xuất: BUG-LG-01 đếm sai/thời lượng khóa, BUG-LG-02 lộ password, BUG-LG-03 secret JWT cố định (gộp LG-EX-05 và CN-EX-05 một nguyên nhân xuyên API); BUG-CN-01 scheme Basic, BUG-CN-02 user hủy shipping, BUG-CN-03 canceled→delivered; BUG-PR-01 thiếu validation POST/PUT, BUG-PR-02 thiếu JWT/admin middleware, BUG-PR-03 tự sửa role, BUG-PR-04 GET detail null.toString gây mất kết nối. AI bỏ sót: 1 nguyên nhân Human Extend-only (BUG-LG-03); các nhóm có cả AI-generated và Extend không tính bỏ sót. Severity/priority đều là đề xuất của AI, chưa chốt.
  > Manager đối chiếu trực tiếp R:41–43,158–162,177–179,195–198,278–283 và các nhánh backend liên quan; xác nhận code +2/180000ms, thiếu validation/middleware, sửa role và chuyển canceled→delivered tại server.js:550–551. Kiểm cấu trúc bằng đọc Markdown: 25 khóa nhóm xuất hiện đúng một lần trong hai bảng phân loại, 10 dòng đề xuất, 1 Human Extend-only, mọi ô “Sinh viên xác nhận” trống. Không chạy SUT/curl/Newman/reset, không sửa kết quả Newman, testcase, collection, SUT hay ảnh; không commit/push/tạo issue, không làm B1. Dừng ở 🧑1 để sinh viên xác nhận triage.
- **Human review:** Đọc 00_triage.md: đủ 25 nhóm, 10 nguyên nhân gốc, 12 nhóm cần sinh viên quyết định, 1 failure setup tách riêng. Đồng ý gộp secret JWT của LG-EX-05 và CN-EX-05 thành một root cause xuyên API; BUG-LG-03 đúng là lỗ hổng chỉ Extend bắt được. Severity/priority vẫn là đề xuất, dừng ở 🧑1 là đúng.
