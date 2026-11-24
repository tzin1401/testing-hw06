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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_

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
- **Human review:** _(để trống – sinh viên tự điền)_
