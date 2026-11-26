# Triage – API1_Login

| Kết quả | Số case |
|---|---:|
| PASS | 33 |
| SPEC_AMBIGUOUS | 1 |
| BUG_CANDIDATE | 12 |
| SETUP_ERROR | 1 |
| NOT_RUN | 3 |

## Từng case

| ID | Kết quả | Assertion fail |
|---|---|---|
| LG-G1-01 | PASS |  |
| LG-G1-02 | PASS |  |
| LG-G1-03 | PASS |  |
| LG-G1-04 | PASS |  |
| LG-G1-05 | BUG_CANDIDATE | [LG-G1-05] status 400/401 (GIẢ ĐỊNH); [LG-G1-05] core: không có token; [LG-G1-05] core: có error |
| LG-G1-06 | PASS |  |
| LG-G1-07 | PASS |  |
| LG-G1-08 | PASS |  |
| LG-G1-09 | PASS |  |
| LG-G1-10 | PASS |  |
| LG-G1-11 | PASS |  |
| LG-G1-12 | PASS |  |
| LG-G1-13 | BUG_CANDIDATE | [LG-G1-13] core: body không chứa node_modules |
| LG-G1-14 | SPEC_AMBIGUOUS | [LG-G1-14] status 400/401/415 (GIẢ ĐỊNH) |
| LG-G1-15 | PASS |  |
| LG-G2-01 | PASS |  |
| LG-G2-02 | BUG_CANDIDATE | [LG-G2-02] status 200; [LG-G2-02] core: token là string; [LG-G2-02] oracle: dùng token gọi /api/users/me status 200; [LG-G2-02] oracle: id = {{uid}} |
| LG-G2-03 | PASS |  |
| LG-G2-04 | PASS |  |
| LG-G2-05 | BUG_CANDIDATE | [LG-G2-05] status 200; [LG-G2-05] core: token là string; [LG-G2-05] oracle: dùng token gọi /api/users/me status 200; [LG-G2-05] oracle: id = {{uid}} |
| LG-G2-06 | BUG_CANDIDATE | [LG-G2-06] oracle: chờ thêm 6 s (tổng > 30 s) rồi đúng → mở khóa status 200; [LG-G2-06] oracle: token là string |
| LG-G2-07 | SETUP_ERROR | [LG-G2-07] setup: đăng nhập đúng (reset) status 200; [LG-G2-07] status 200; [LG-G2-07] core: token là string; [LG-G2-07] oracle: dùng token gọi /api/users/me status 200; [LG-G2-07] oracle: id = {{uid} |
| LG-G2-08 | PASS |  |
| LG-G3-01 | PASS |  |
| LG-G3-02 | PASS |  |
| LG-G3-03 | PASS |  |
| LG-G3-04 | PASS |  |
| LG-G3-05 | PASS |  |
| LG-G3-06 | PASS |  |
| LG-G3-07 | BUG_CANDIDATE | [LG-G3-07] core: không có user.password; [LG-G3-07] core: body không chứa Test1234! |
| LG-G3-08 | PASS |  |
| LG-G3-09 | NOT_RUN | quá 2 vòng sinh lại vẫn INCOMPLETE: Status 200 với field thừa role chỉ có từ GD6 (như LG-G1-15) nhưng expect.assumed=false và source không trích GD6: đặt assumed=true và thêm GD6 vào source; phần after (admin 401/403, GD14) và setup độc lập đã đủ. |
| LG-G3-10 | PASS |  |
| LG-G4-01 | PASS |  |
| LG-G4-02 | PASS |  |
| LG-G4-03 | BUG_CANDIDATE | [LG-G4-03] core: không có user.login_attempts; [LG-G4-03] core: không có user.locked_until |
| LG-G4-04 | PASS |  |
| LG-G6-01 | PASS |  |
| LG-G6-02 | PASS |  |
| LG-G6-03 | BUG_CANDIDATE | [LG-G6-03] status 200 (GIẢ ĐỊNH); [LG-G6-03] core: user.id = {{uid}} |
| LG-G6-04 | PASS |  |
| LG-G6-05 | PASS |  |
| LG-G6-06 | PASS |  |
| LG-EX-01 | BUG_CANDIDATE | [LG-EX-01] status 401/403 (GIẢ ĐỊNH); [LG-EX-01] core: không có id |
| LG-EX-02 | BUG_CANDIDATE | [LG-EX-02] oracle: token vừa cấp gọi /api/admin/users → bị từ chối status 401/403 |
| LG-EX-03 | BUG_CANDIDATE | [LG-EX-03] core: body không chứa "password" |
| LG-EX-04 | BUG_CANDIDATE | [LG-EX-04] oracle: [id={{uid}}].login_attempts = 1 |
| LG-EX-05 | NOT_RUN | trùng LG-G2-05: cùng setup (đăng ký, sai 3 lần) và request (đúng sau chờ) + expected 200, chỉ khác wait 32s vs 31s và 1 lần đăng nhập thêm khi khóa; xóa hoặc đổi thành case khác biệt rõ (vd kiểm tra đăng nhập khi khóa không gia hạn khóa). |
| LG-EX-06 | PASS |  |
| LG-EX-07 | NOT_RUN | trùng LG-G4-01: request chính và expect (user.id number, equals uid) giống hệt; 'id chẵn/lẻ' không điều khiển được; nếu cần thì gộp login user B vào after của G4-01. |

## Ứng viên bug (bằng chứng từ Newman JSON)

### LG-G1-05 – EP email sai format "lg-no-at" → từ chối
- Assertion fail: [LG-G1-05] status 400/401 (GIẢ ĐỊNH); [LG-G1-05] core: không có token; [LG-G1-05] core: có error
- Request: `POST /api/login` body `{"email": "lg-no-at", "password": "Test1234!"}`
- Response thật: HTTP 200 `{"message":"Login successful","token":"eyJ***","user":{"id":6,"name":"LG User","email":"lg-no-at","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}`
- Severity (đề xuất của AI): Low – gốc ở /api/register không validate format email (FR-01, R:33); login chỉ chấp nhận user đã tồn tại

### LG-G1-13 – JSON sai cú pháp → 400, không lộ stack trace
- Assertion fail: [LG-G1-13] core: body không chứa node_modules
- Request: `POST /api/login` body `{"email": "x@test.com", "password": `
- Response thật: HTTP 400 `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>SyntaxError: Unexpected end of JSON input<br> &nbsp; &nbsp;at JSON.parse (&lt;anonymous&gt;)<br> &nbsp; &nbsp;at parse (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/body-parser/lib/types/json.js:72:19)<br> &nbsp; &nbsp;at /home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/body-parser/lib/read.js:162:18<br> &nbsp; &nbsp;at AsyncResource.runInAsyncScope (node:async_hooks:214:14)<br> &nbsp; &nbsp;at invokeCallback (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modu`
- Severity (đề xuất của AI): Low – trang lỗi HTML của Express lộ stack trace (đường dẫn node_modules)

### LG-G2-02 – Normal(n=2): sai 2 lần rồi đúng → 200 (biên dưới ngưỡng 3)
- Assertion fail: [LG-G2-02] status 200; [LG-G2-02] core: token là string; [LG-G2-02] oracle: dùng token gọi /api/users/me status 200; [LG-G2-02] oracle: id = {{uid}}
- Request: `POST /api/login` body `{"email": "lg-cd7b791a-14c0-4cdd-b4e1-0e91102514ad@test.com", "password": "Test1234!"}`
- Response thật: HTTP 403 `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}`
- Severity (đề xuất của AI): High – sai 2 lần đã bị khóa; bộ đếm tăng 2 thay vì 1 (R:41). Cùng gốc với LG-EX-04 và SETUP_ERROR của LG-G2-07

### LG-G2-05 – Locked--hết 30s, đúng-->Normal: chờ 31 s rồi đúng → 200
- Assertion fail: [LG-G2-05] status 200; [LG-G2-05] core: token là string; [LG-G2-05] oracle: dùng token gọi /api/users/me status 200; [LG-G2-05] oracle: id = {{uid}}
- Request: `POST /api/login` body `{"email": "lg-80c27720-e9a1-44ac-8f8e-f499f57e09b0@test.com", "password": "Test1234!"}`
- Response thật: HTTP 403 `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}`
- Severity (đề xuất của AI): High – sau 31 s vẫn khóa; thời gian khóa > 30 s (R:42)

### LG-G2-06 – Locked tại 25 s (< 30 s): đúng mật khẩu → vẫn khóa
- Assertion fail: [LG-G2-06] oracle: chờ thêm 6 s (tổng > 30 s) rồi đúng → mở khóa status 200; [LG-G2-06] oracle: token là string
- Request: `POST /api/login` body `{"email": "lg-7cbf0719-d01e-446e-81ab-53a9c12f0b19@test.com", "password": "Test1234!"}`
- Response thật: HTTP 403 `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}`
- Severity (đề xuất của AI): Medium – cùng gốc LG-G2-05 (tổng 31 s vẫn khóa)

### LG-G3-07 – Login thành công không trả password trong body
- Assertion fail: [LG-G3-07] core: không có user.password; [LG-G3-07] core: body không chứa Test1234!
- Request: `POST /api/login` body `{"email": "lg-5483787b-0c35-4816-b0e1-d7256fc40fb0@test.com", "password": "Test1234!"}`
- Response thật: HTTP 200 `{"message":"Login successful","token":"eyJ***","user":{"id":30,"name":"LG User","email":"lg-5483787b-0c35-4816-b0e1-d7256fc40fb0@test.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}`
- Severity (đề xuất của AI): Critical – response login trả `user.password` plaintext (SEC-01). Cùng gốc LG-EX-03

### LG-G4-03 – Không lộ trạng thái khóa trong user: không có login_attempts, locked_until
- Assertion fail: [LG-G4-03] core: không có user.login_attempts; [LG-G4-03] core: không có user.locked_until
- Request: `POST /api/login` body `{"email": "lg-98aa1efc-ea63-47af-9a41-68187b361ba4@test.com", "password": "Test1234!"}`
- Response thật: HTTP 200 `{"message":"Login successful","token":"eyJ***","user":{"id":35,"name":"LG User","email":"lg-98aa1efc-ea63-47af-9a41-68187b361ba4@test.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}`
- Severity (đề xuất của AI): Low – `user` lộ `login_attempts`, `locked_until` (GD11, GD13)

### LG-G6-03 – Heuristic hoa/thường: email viết HOA vẫn đăng nhập đúng user
- Assertion fail: [LG-G6-03] status 200 (GIẢ ĐỊNH); [LG-G6-03] core: user.id = {{uid}}
- Request: `POST /api/login` body `{"email": "LG-UP-1795689158397@TEST.COM", "password": "Test1234!"}`
- Response thật: HTTP 401 `{"error":"Invalid email or password"}`
- Severity (đề xuất của AI): Low – email phân biệt hoa/thường; chỉ dựa trên GD8, có thể coi là SPEC_AMBIGUOUS

### LG-EX-01 – P3: token cấp trước khi đặt lại mật khẩu phải bị từ chối sau khi đặt lại
- Assertion fail: [LG-EX-01] status 401/403 (GIẢ ĐỊNH); [LG-EX-01] core: không có id
- Request: `GET /api/users/me` body ``
- Response thật: HTTP 200 `{"id":43,"name":"LG User","email":"lg-385898c0-5fca-4286-a099-d9ffebea0092@test.com","password":"NewPass123!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}`
- Severity (đề xuất của AI): High – token cũ vẫn dùng được sau khi đặt lại mật khẩu (P3, GD10)

### LG-EX-02 – P4: user đã đăng ký kèm role:"admin" thì login vẫn trả role user
- Assertion fail: [LG-EX-02] oracle: token vừa cấp gọi /api/admin/users → bị từ chối status 401/403
- Request: `GET /api/admin/users` body ``
- Response thật: HTTP 200 `[{"id":1,"name":"Admin User","email":"admin@eshop.com","role":"admin","login_attempts":0,"locked_until":null,"shipping_address":null},{"id":2,"name":"Test User","email":"test@eshop.com","role":"user","login_attempts":0,"locked_until":null,"shipping_address":null},{"id":3,"name":"LG User","email":"lg-880dd9f1-3531-41c3-a405-eec1fba06f02@test.com","role":"user","login_attempts":0,"locked_until":null,"shipping_address":null},{"id":4,"name":"LG User","email":"lg-b9fc9394-9c41-4fc5-8c29-f51d790d54b1@test.com","role":"user","login_attempts":0,"locked_until":null,"shipping_address":null},{"id":5,"nam`
- Severity (đề xuất của AI): Critical – token user thường đọc được /api/admin/users (SEC-03). Lỗi nằm ở API admin, không phải /api/login; role trong body register thì bị bỏ qua đúng

### LG-EX-03 – P6: response login không chứa chuỗi "password" ở bất kỳ đâu
- Assertion fail: [LG-EX-03] core: body không chứa "password"
- Request: `POST /api/login` body `{"email": "lg-49c8b797-1c4c-4b6e-8316-4ccf7c4661de@test.com", "password": "Test1234!"}`
- Response thật: HTTP 200 `{"message":"Login successful","token":"eyJ***","user":{"id":45,"name":"LG User","email":"lg-49c8b797-1c4c-4b6e-8316-4ccf7c4661de@test.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}`
- Severity (đề xuất của AI): Critical – cùng gốc LG-G3-07

### LG-EX-04 – P7: sai 1 lần → login_attempts của user đúng bằng 1
- Assertion fail: [LG-EX-04] oracle: [id={{uid}}].login_attempts = 1
- Request: `GET /api/admin/users` body ``
- Response thật: HTTP 200 `[{"id":1,"name":"Admin User","email":"admin@eshop.com","role":"admin","login_attempts":0,"locked_until":null,"shipping_address":null},{"id":2,"name":"Test User","email":"test@eshop.com","role":"user","login_attempts":0,"locked_until":null,"shipping_address":null},{"id":3,"name":"LG User","email":"lg-880dd9f1-3531-41c3-a405-eec1fba06f02@test.com","role":"user","login_attempts":0,"locked_until":null,"shipping_address":null},{"id":4,"name":"LG User","email":"lg-b9fc9394-9c41-4fc5-8c29-f51d790d54b1@test.com","role":"user","login_attempts":0,"locked_until":null,"shipping_address":null},{"id":5,"nam`
- Severity (đề xuất của AI): High – sai 1 lần, login_attempts = 2 (R:41). Cùng gốc LG-G2-02

## Đề xuất mẫu mới cho bug_patterns.md

Bug chỉ case EX bắt được: LG-EX-01, LG-EX-02, LG-EX-03, LG-EX-04

Đề xuất của AI cho `references/bug_patterns.md`:

| # | Mẫu | Cách thử | Nguồn |
|---|---|---|---|
| P10 | API admin chỉ kiểm tra có token, không kiểm tra role | Login user thường, dùng token gọi `GET /api/admin/users`; kỳ vọng 401/403 | LG-EX-02 (chỉ EX bắt được) |
| P11 | Response lộ field trạng thái nội bộ (`login_attempts`, `locked_until`, `reset_token`) | Kiểm tra `absent` các field này trong `user` | LG-G4-03 |

LG-EX-01, LG-EX-03, LG-EX-04 khớp mẫu đã có (P3, P6, P7), không cần thêm mẫu mới.
