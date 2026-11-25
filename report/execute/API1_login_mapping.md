# API 1 – Login: mapping test case → collection (bước X4, review tĩnh)

- Collection: `collections/23120190_API1_Login.postman_collection.json` (tên `23120190_API1_Login`, Postman v2.1)
- Nguồn: `report/testcases/API1_login_generated.md` (mục Audit và Extend – Human)
- Reviewer: Claude (anthropic/claude-sonnet-5-5), 2026-11-24
- Phạm vi: đối chiếu tĩnh từng ID (method, path, header, raw body, setup độc lập, thứ tự bước, thời gian chờ, status, nhãn GIẢ ĐỊNH, schema, điều kiện core). Không sửa collection. Recheck tĩnh thực hiện sau bản sửa LGFixX4 và bước dọn cuối.

> Kết quả chạy thử chỉ để kiểm collection; kết quả chính thức xem results/newman/ do sinh viên chạy.

## 1. Bảng mapping (71 ID nguồn: 66 gốc + 5 EX; 68 có folder, 3 INVALID không có folder)

Quy ước: Request = số request trong folder case (gồm setup). Assertion = số `pm.test` trong folder case (kể cả `pm.test` ở pre-request). Khớp = request, status, điều kiện core, nhãn (GIẢ ĐỊNH) và thời gian chờ khớp file nguồn.

Điều kiện "không lộ nguyên nhân":
- Dòng E của G1 và bước L của G2 có assertion riêng "không lộ nguyên nhân" với regex `wrong password|incorrect password|sai mật khẩu|mật khẩu sai|email (exists|registered|tồn tại|đã đăng ký)|counter|số lần`.
- LG-G3-09 (bước W3 và bước C trong khóa) và LG-G4-05 (bước C chính) kiểm trong callback core `lỗi khóa không cấp token hoặc lộ nguyên nhân` với regex `password|mật khẩu|email|counter|attempt|tồn tại|không tồn tại|số lần`. Regex này bao hết từ khóa của regex trên nên không yếu hơn.

### G1 – Domain partition + boundary

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| LG-G1-01 | VALID | G1 / [LG-G1-01] Email tồn tại | 2 | 3 | Có: login email đã đăng ký, 200 (không GIẢ ĐỊNH), JWT 3 phần + `user` |
| LG-G1-02 | VALID | G1 / [LG-G1-02] Email chưa tồn tại | 2 | 4 | Có: `absent-`+email, 400 (GIẢ ĐỊNH), E |
| LG-G1-03 | VALID | G1 / [LG-G1-03] Email thiếu @ | 2 | 4 | Có: `email.replace('@','')`, 400 (GIẢ ĐỊNH), E |
| LG-G1-04 | VALID | G1 / [LG-G1-04] Email thiếu domain | 2 | 4 | Có: phần trước `@` + `@`, 400 (GIẢ ĐỊNH), E |
| LG-G1-05 | VALID | G1 / [LG-G1-05] Email có khoảng trắng trong | 2 | 4 | Có: `'x '+email`, 400 (GIẢ ĐỊNH), E |
| LG-G1-06 | VALID | G1 / [LG-G1-06] Email rỗng | 2 | 4 | Có: `"email":""`, 400 (GIẢ ĐỊNH), E |
| LG-G1-07 | VALID | G1 / [LG-G1-07] Thiếu email | 2 | 4 | Có: body chỉ có password, 400 (GIẢ ĐỊNH), E |
| LG-G1-08 | VALID | G1 / [LG-G1-08] Email null | 2 | 4 | Có: `"email":null`, 400 (GIẢ ĐỊNH), E |
| LG-G1-09 | VALID | G1 / [LG-G1-09] Email số | 2 | 4 | Có: `"email":12345`, 400 (GIẢ ĐỊNH), E |
| LG-G1-10 | VALID | G1 / [LG-G1-10] Email đổi chữ hoa/thường | 2 | 3 | Có: `email.toUpperCase()`, 200 (GIẢ ĐỊNH), S |
| LG-G1-11 | VALID | G1 / [LG-G1-11] Email có khoảng trắng đầu | 2 | 3 | Có: `' '+email`, 200 (GIẢ ĐỊNH), S |
| LG-G1-12 | VALID | G1 / [LG-G1-12] Email có khoảng trắng cuối | 2 | 3 | Có: `email+' '`, 200 (GIẢ ĐỊNH), S |
| LG-G1-13 | VALID | G1 / [LG-G1-13] Email rất dài | 2 | 4 | Có: `'a'.repeat(4087)+'@test.com'` = 4096 ký tự, 400 (GIẢ ĐỊNH), E |
| LG-G1-14 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (trùng LG-G1-01), có trong description collection |
| LG-G1-15 | VALID | G1 / [LG-G1-15] Password sai một ký tự | 2 | 4 | Có: `Test1235!`, 400 (GIẢ ĐỊNH), E |
| LG-G1-16 | VALID | G1 / [LG-G1-16] Password sai chữ hoa/thường | 2 | 4 | Có: `test1234!`, 400 (GIẢ ĐỊNH), E |
| LG-G1-17 | VALID | G1 / [LG-G1-17] Password rỗng | 2 | 4 | Có: `"password":""`, 400 (GIẢ ĐỊNH), E |
| LG-G1-18 | VALID | G1 / [LG-G1-18] Thiếu password | 2 | 4 | Có: body chỉ có email, 400 (GIẢ ĐỊNH), E |
| LG-G1-19 | VALID | G1 / [LG-G1-19] Password null | 2 | 4 | Có: `"password":null`, 400 (GIẢ ĐỊNH), E |
| LG-G1-20 | VALID | G1 / [LG-G1-20] Password số | 2 | 4 | Có: `"password":12345`, 400 (GIẢ ĐỊNH), E |
| LG-G1-21 | VALID | G1 / [LG-G1-21] Password rất dài | 2 | 4 | Có: `'a'.repeat(4096)`, 400 (GIẢ ĐỊNH), E |
| LG-G1-22 | VALID | G1 / [LG-G1-22] Body rỗng | 2 | 4 | Có: body `{}`, 400 (GIẢ ĐỊNH), E |
| LG-G1-23 | VALID | G1 / [LG-G1-23] JSON sai cú pháp | 2 | 4 | Có: raw thiếu `}`, 400 (GIẢ ĐỊNH), E |
| LG-G1-24 | VALID | G1 / [LG-G1-24] Media type khác JSON | 2 | 4 | Có: `Content-Type: text/plain`, raw JSON, 415 (GIẢ ĐỊNH), E |
| LG-G1-25 | VALID | G1 / [LG-G1-25] Field thừa | 2 | 3 | Có: thêm `"extra":"unused"`, 200 (GIẢ ĐỊNH), S |

### G2 – State transition

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| LG-G2-01 | VALID | G2 / [LG-G2-01] 0 → 1; kiểm tra không nhảy counter | 4 | 7 | Có: W, W, C → 400, 400 (GIẢ ĐỊNH), 200; không login trước |
| LG-G2-02 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (trùng LG-G2-01), có trong description |
| LG-G2-03 | VALID | G2 / [LG-G2-03] 2 → K; sai lần ba khóa | 5 | 11 | Có: setup W, W; W → 423; C → 423 (GIẢ ĐỊNH); L có "không lộ nguyên nhân" bước 3 và 4 |
| LG-G2-04 | VALID | G2 / [LG-G2-04] 0 → 0 khi đúng | 5 | 9 | Có: C, W, W, C → 200; 400, 400; 200 |
| LG-G2-05 | VALID | G2 / [LG-G2-05] 1 → 0 khi đúng | 6 | 11 | Có: setup W; C, W, W, C → 200; 400, 400; 200 |
| LG-G2-06 | VALID | G2 / [LG-G2-06] 2 → 0; sai hai → đúng → sai hai | 7 | 13 | Có: setup W, W; C, W, W, C → 200; 400, 400; 200 |
| LG-G2-07 | VALID | G2 / [LG-G2-07] Trong khóa sai và đúng bị từ chối, không kéo dài khóa | 7 | 16 | Có: setup W, W, W (423, ghi `t0`); W, C → 423, 423; chờ 31000 − (now − `t0`); C → 200; có "không lộ nguyên nhân" ở bước 3, 4, 5 |
| LG-G2-08 | VALID | G2 / [LG-G2-08] T không áp dụng tại 0 | 4 | 7 | Có: chờ 31000 ms ở pre-request của W đầu; W, W, C → 400, 400, 200 |
| LG-G2-09 | VALID | G2 / [LG-G2-09] T không áp dụng tại 1 | 5 | 11 | Có: setup W; chờ 31 s; W 400; W 423; C 423; L có "không lộ nguyên nhân" bước 3 và 4 |
| LG-G2-10 | VALID | G2 / [LG-G2-10] T không áp dụng tại 2 | 5 | 11 | Có: setup W, W; chờ 31 s; W 423; C 423; L có "không lộ nguyên nhân" bước 3 và 4 |
| LG-G2-11 | VALID | G2 / [LG-G2-11] Biên ~29 và ~31 giây; K → 0 | 9 | 19 | Có: setup W, W, W (ghi `t0`); chờ `t0`+29 s → C 423; `t0`+31 s → C 200; W 400; W 400; C 200; L bước 3 và 4 có "không lộ nguyên nhân" |
| LG-G2-12 | VALID | G2 / [LG-G2-12] Khóa A không ảnh hưởng B | 7 | 14 | Có: đăng ký A và B (`-b-`+guid); A bị khóa; CB → 200; C của A → 423; L bước 3 và 5 có "không lộ nguyên nhân" |

### G3 – Security

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| LG-G3-01 | VALID | G3 / [LG-G3-01] SQL tautology tại email | 3 | 6 | Có: `' OR '1'='1` ở email; 400 (GIẢ ĐỊNH), không token, không lộ SQL; C → 200 và `user.id` đúng |
| LG-G3-02 | VALID | G3 / [LG-G3-02] SQL comment tại email | 3 | 6 | Có: `admin@eshop.com'--`; như trên |
| LG-G3-03 | VALID | G3 / [LG-G3-03] SQL UNION tại email | 3 | 6 | Có: `' UNION SELECT NULL--`; như trên |
| LG-G3-04 | VALID | G3 / [LG-G3-04] SQL tautology tại password | 3 | 6 | Có: payload ở password; như trên |
| LG-G3-05 | VALID | G3 / [LG-G3-05] SQL UNION tại password | 3 | 6 | Có: payload ở password; như trên |
| LG-G3-06 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (trùng LG-G4-03), có trong description |
| LG-G3-07 | VALID | G3 / [LG-G3-07] Chống dò email bằng so sánh lỗi | 4 | 9 | Có: `absent-`+email → W → C; cùng status 400 (GIẢ ĐỊNH) và cùng `error`; C → 200 |
| LG-G3-08 | VALID | G3 / [LG-G3-08] JWT đúng cấu trúc và danh tính user | 2 | 5 | Có: 3 phần, decode payload; `id` = id đăng ký, `role` = `user`, `user.id` = id đăng ký |
| LG-G3-09 | VALID | G3 / [LG-G3-09] Khóa chặn mật khẩu đúng sau brute force | 6 | 12 | Có: W, W, W (423, ghi `t0`); C 423; chờ 31000 − (now − `t0`); C 200 và `user.id`; L (W3 và C) kiểm không token, `error` không rỗng và không lộ nguyên nhân (regex mở rộng thêm `số lần`) |
| LG-G3-10 | VALID | G3 / [LG-G3-10] Email độc hại 10.000 ký tự | 3 | 6 | Có: `'a'.repeat(9991)+'@test.com'` = 10000 ký tự; E; C 200 |
| LG-G3-11 | VALID | G3 / [LG-G3-11] Password độc hại 10.000 ký tự | 3 | 6 | Có: `'a'.repeat(10000)`; E; C 200 |
| LG-G3-12 | VALID | G3 / [LG-G3-12] Ký tự điều khiển trong email | 3 | 6 | Có: raw `"\u0000{{email}}\n"`; E; C 200 |
| LG-G3-13 | VALID | G3 / [LG-G3-13] Ký tự điều khiển trong password | 3 | 6 | Có: `"Test1234!\u0000\n"`; E; C 200 |
| LG-G3-14 | VALID | G3 / [LG-G3-14] Object kiểu toán tử thay email | 3 | 6 | Có: `{"$ne":null}` ở email; E; C 200 |
| LG-G3-15 | VALID | G3 / [LG-G3-15] Object kiểu toán tử thay password | 3 | 6 | Có: `{"$ne":null}` ở password; E; C 200 |
| LG-G3-16 | VALID | G3 / [LG-G3-16] Array thay email | 3 | 6 | Có: `["{{email}}"]`; E; C 200 |
| LG-G3-17 | VALID | G3 / [LG-G3-17] Array thay password | 3 | 6 | Có: `["Test1234!"]`; E; C 200 |

### G4 – Schema validation

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| LG-G4-01 | VALID | G4 / [LG-G4-01] Status, media type và schema thành công | 2 | 6 | Có: 200; schema 200 nguyên văn; Content-Type `application/json` (không phân biệt hoa thường, cho phép charset); token và user |
| LG-G4-02 | VALID | G4 / [LG-G4-02] Kiểu từng field user | 2 | 5 | Có: schema 200 + `id` integer, `name`/`email` string, `role` thuộc user/admin |
| LG-G4-03 | VALID | G4 / [LG-G4-03] Không lộ field nhạy cảm | 2 | 5 | Có: schema 200 + duyệt đệ quy key `password`/`passwd`/`hash`/`reset_token` và giá trị `Test1234!` |
| LG-G4-04 | INCOMPLETE | G4 / [LG-G4-04] Schema lỗi sai mật khẩu | 2 | 6 | Có: 400 (GIẢ ĐỊNH, G6 thay 401), schema lỗi nguyên văn, Content-Type JSON, không token; request chính có description INCOMPLETE |
| LG-G4-05 | INCOMPLETE | G4 / [LG-G4-05] Schema lỗi tài khoản khóa | 5 | 12 | Có: setup W, W, W (423); C → 423 (GIẢ ĐỊNH, G6 thay 403); schema lỗi, Content-Type JSON, không token, `error` không rỗng và không lộ nguyên nhân (regex mở rộng thêm `số lần`); request chính có description INCOMPLETE |
| LG-G4-06 | VALID | G4 / [LG-G4-06] Schema lỗi thiếu password | 2 | 6 | Có: body M chỉ có email; 400 (GIẢ ĐỊNH); schema lỗi; Content-Type JSON |
| LG-G4-07 | VALID | G4 / [LG-G4-07] Thời gian phản hồi login thành công | 2 | 5 | Có: 200; schema 200; `responseTime` < 2000 ms |

### G6 – Bổ sung theo G5

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| LG-G6-01 | VALID | G6 / [LG-G6-01] Hết khóa reset counter | 8 | 16 | Có: W, W, W (400, 400, 423, ghi `t0`); chờ `t0`+31 s; W, W, W, C → 400, 400, 423, 423 (GIẢ ĐỊNH); không login đúng trước ba lần sai sau chờ; không token ở mọi response |
| LG-G6-02 | VALID | G6 / [LG-G6-02] Token mới được API bảo mật chấp nhận | 3 | 6 | Có: C lưu token; ME 200 (GIẢ ĐỊNH) với `email` và `id` khớp |
| LG-G6-03 | VALID | G6 / [LG-G6-03] Chống dò email sau nhiều lần sai | 11 | 26 | Có: W×4 cho email thật rồi WA×4 cho email vắng (400, 400, 423, 423); so từng cặp `status` và `error`; chờ `t0`+31 s; C; ME. Ghi nhận lỗi gộp trong callback core, không còn assertion chỉ lưu biến |
| LG-G6-04 | VALID | G6 / [LG-G6-04] Bearer sai không chặn login | 3 | 6 | Có: `Authorization: Bearer invalid.token.value`; login 200 (GIẢ ĐỊNH); ME khớp danh tính |
| LG-G6-05 | VALID | G6 / [LG-G6-05] Role client không nâng quyền | 3 | 7 | Có: body thêm `"role":"admin"`; 200 (GIẢ ĐỊNH); payload JWT `role` = `user`; `user.role` (nếu có) = `user`; ME khớp |

### EX – Extend

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| LG-EX-01 | EX | EX / [LG-EX-01] Thiếu password không khóa tài khoản | 6 | 12 | Có: 3 lần thiếu password → 400 (GIẢ ĐỊNH); C → 200; ME 200 (GIẢ ĐỊNH) đúng email |
| LG-EX-02 | EX | EX / [LG-EX-02] Bộ đếm tăng đúng một | 4 | 8 | Có: login lấy token, W một lần, ME 200 (GIẢ ĐỊNH), `login_attempts` = 1 |
| LG-EX-03 | EX | EX / [LG-EX-03] JWT có hạn dùng | 3 | 7 | Có: login; payload có `exp` nguyên, `exp` > `iat`, có `id` và `role` |
| LG-EX-04 | EX | EX / [LG-EX-04] Đổi mật khẩu vô hiệu mật khẩu cũ | 6 | 11 | Có: forgot, reset, login cũ → 400 (GIẢ ĐỊNH), login mới → 200 (GIẢ ĐỊNH), ME đúng email |
| LG-EX-05 | EX | EX / [LG-EX-05] Token ký bằng secret source bị từ chối | 2 | 5 | Có: JWT HS256 tự ký, payload `{"id":idB,"role":"admin"}`, secret đúng như file; ME → 401 (GIẢ ĐỊNH); không trả dữ liệu nạn nhân. Gồm 1 `pm.test` ở pre-request (guard id) |

### Ngoài nguồn (fixture chẩn đoán X0)

| Mục | Folder | Request | Assertion | Ghi chú |
|---|---|---|---|---|
| [SMOKE] GET /api/products | _smoke | 1 | 1 | Không áp dụng "Khớp": fixture chẩn đoán bắt buộc từ X0 và là helper chụp console `X-Student-Id`, không thuộc tập case nguồn. Runner chính thức (XDATA) lọc G1..EX nên không vào báo cáo chính |

## 2. ID bị bỏ qua (INVALID theo audit)

- LG-G1-14 – INVALID theo audit: trùng ngữ nghĩa LG-G1-01
- LG-G2-02 – INVALID theo audit: trùng ngữ nghĩa LG-G2-01
- LG-G3-06 – INVALID theo audit: trùng ngữ nghĩa LG-G4-03

Cả 3 ID không có folder trong collection và đều có trong `info.description`.

## 3. Tổng

| Folder | Case | Request | Assertion |
|---|---|---|---|
| G1 | 24 | 48 | 91 |
| G2 | 11 | 64 | 129 |
| G3 | 16 | 51 | 104 |
| G4 | 7 | 17 | 45 |
| G6 | 5 | 28 | 61 |
| EX | 5 | 21 | 43 |
| **Tổng nguồn** | **68** | **229** | **473** |
| `_smoke` (ngoài nguồn) | 1 | 1 | 1 |
| **Tổng trong file** | 69 | **230** | **474** |

Tổng trên là phạm vi LG-X4 trước X-DATA, không gồm folder `DATA – LG-G1` thêm sau đó (2 request mẫu, lặp theo 20 dòng CSV). Runner chính thức tách DATA khỏi G1..EX; số assertion DATA phụ thuộc từng dòng và được kiểm riêng ở bước X-DATA.

Số case chuyển = 68 = 61 VALID + 2 INCOMPLETE + 5 EX. Số ID nguồn = 71 (gồm 3 INVALID không có folder).

## 4. Kiểm tra cấu trúc

- Pre-request cấp collection: đúng 2 dòng, dòng 2 dùng `pm.variables.replaceIn`, trùng đúng hai dòng người dùng cung cấp.
- Các folder nguồn G1..EX không có `pm.sendRequest`, `try/catch`, `skip`, `setNextRequest`. Folder DATA thêm sau LG-X4 dùng `pm.execution.skipRequest()` khi không có `caseId` trong iteration data, đúng ngoại lệ X-DATA; không bỏ qua case nguồn hay assertion fail.
- Biến trạng thái đều có tiền tố ID của case; không có biến tham chiếu chéo case; mọi `{{$guid}}` dùng ngoặc đôi.
- Schema G4 dán nguyên văn từ file nguồn.
- Thời gian chờ: 31000 ms và 29000 ms đặt ở pre-request của request cần chờ, đo từ `t0` ở các case nguồn yêu cầu.
- INCOMPLETE (LG-G4-04, LG-G4-05) có description trên request chính, nêu quy tắc G6 thay status.
- `results/newman/` không có report mới; chỉ có `.gitkeep`.

## 5. Finding tĩnh

Không còn finding mở. Các mục đã đóng: description INCOMPLETE cho LG-G4-04/05; assertion "không lộ nguyên nhân" cho dòng E của G1, bước L của G2, G3-09, G4-05 (regex G3-09/G4-05 hợp nhất, không yếu hơn); gộp ghi nhận lỗi của LG-G6-03 vào callback core; nhãn `(GIẢ ĐỊNH)` cho status ME của LG-EX-02. Folder `_smoke` được chấp nhận là fixture chẩn đoán X0.

## 6. Quan sát chạy X4

Đã reset SUT và chạy Newman CLI toàn collection sau sửa X4, không lọc folder, không xuất report. Artifact công cụ debug: `local://96.log`.

|Chỉ số|Quan sát thực tế|
|---|---|
|Iteration|1|
|Request|230, 0 lỗi request|
|Test script|230, 0 lỗi script|
|Pre-request script|335, 0 lỗi script|
|Assertion|474: 322 pass, 152 fail|
|Thời gian|4m 17s|

Console có `X-Student-Id: 23120190` và URL `http://localhost:3000` đã resolve. Các fail là expected-vs-actual thực tế; không sửa status, schema, thời gian chờ hoặc core để làm xanh. Đây không phải kết quả Execute chính thức.
