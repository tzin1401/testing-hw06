# Bước 0 — Phân tích spec: Login, Hủy đơn, Product CRUD

Sinh viên: **23120190**. Phạm vi: chuẩn bị Generate, chưa sinh test case, chưa Audit.

Nguồn yêu cầu duy nhất: `eshop-sut/README.md` (viết tắt **R**) và `eshop-sut/api_specification.md` (**A**). Dẫn nguồn `R:41` nghĩa là dòng 41 của README; số dòng theo bản hiện tại. Không đọc backend/frontend implementation. Scout phân tích spec; sonic thực thi happy path; Manager đối chiếu, ghi báo cáo/log và commit.

**Nguyên tắc:** chỉ suy expected từ spec. Ví dụ JSON không tự chứng minh mọi field bắt buộc hoặc mọi kiểu khác bị cấm. “GIẢ ĐỊNH” chỉ suy luận cần người dùng audit. HTTP status, error shape, thời gian < 2000 ms, coercion, giới hạn độ dài nếu spec chưa nói thì không được ghi thành yêu cầu chắc chắn. Mục 4 ghi response quan sát được, không phải expected.

## 1. API 1 — FR-02 Login: `POST /api/login`

### a) Bảng tham số

| Tên | Vị trí | Kiểu | Bắt buộc? | Ràng buộc theo spec | Trích dòng spec |
|---|---|---|---|---|---|
| email | body JSON | string trong ví dụ | Có theo thao tác nhập | Email đăng nhập; FR-02 yêu cầu `type="email"` và HTML5 validation trên UI, không khẳng định backend validate format | R:40,44; A:24–31 |
| password | body JSON | string trong ví dụ | Có theo thao tác nhập | Không nêu giới hạn password cho login; không áp đặt chính sách đăng ký cho login | R:40; A:24–31 |
| Authorization | header | Bearer JWT nếu có | Không yêu cầu cho login | Login sinh token; không có yêu cầu token đầu vào | R:43; A:23–32 |
| :id | path | Không có | Không áp dụng | Route không có path parameter | A:24 |

Content-Type JSON được thể hiện ở A:25; hành vi với malformed JSON, field thừa và media type khác chưa có đặc tả.

### b) Trạng thái và sự kiện

| Trạng thái / sự kiện | Kết quả theo spec | Nguồn |
|---|---|---|
| Sai khi chưa khóa | Mỗi lần sai tăng bộ đếm đúng 1 | R:41 |
| Sai liên tiếp từ 3 lần | Khóa tài khoản 30 giây; thông báo phù hợp, không lộ chi tiết nguyên nhân | R:42 |
| Login đúng khi không bị khóa | Trả JWT | R:43; A:32 |
| Login đúng sau 1–2 lần sai | Thành công trả JWT; reset bộ đếm là **GIẢ ĐỊNH** từ “liên tiếp”, không được nêu tường minh | R:41–43 |
| Hết 30 giây | Thời gian khóa kết thúc theo R:42; giá trị bộ đếm sau đó, mốc đo và cách mở khóa không được định nghĩa | R:42 |
| Đúng/sai trong lúc khóa | Khóa 30 giây là yêu cầu; status/body, có kéo dài khóa hoặc tăng bộ đếm không chưa rõ | R:41–43 |

Không biến counter nội bộ thành field response bắt buộc.

### c) SEC-01…SEC-07 và FR-12

| Yêu cầu | Áp dụng cho Login |
|---|---|
| SEC-01 (R:278) | Cấm lưu plaintext password. API black-box không tự chứng minh cách lưu; cấm lộ password trong response là suy luận bảo mật, không phải response schema được câu này nêu rõ. |
| SEC-02 (R:279) | JWT hợp lệ cho API bảo mật; login là bước cấp JWT (R:43), không đòi token trước khi login. |
| SEC-03 (R:280) | Không trực tiếp: login không phải API Admin; không cho suy luận rằng chỉ admin được login. |
| SEC-04 (R:281) | Gián tiếp khi giá trị nhập/thông tin user được hiển thị UI: escape. API-only không chứng minh UI render an toàn. |
| SEC-05 (R:282) | Truy vấn xác thực phải parameterized; có thể thiết kế input injection nhưng không đọc implementation. |
| SEC-06 (R:283) | Không trực tiếp: login không cập nhật profile; liên quan setup chống nâng role qua `PUT /api/users/me`. |
| SEC-07 (R:284) | Không trực tiếp: đây không phải reset OTP. |
| FR-12 (R:174–179) | Không trực tiếp: login không thuộc API Admin hoặc mutation product/category/coupon. |

### d) Response theo spec

A:32 ghi **200 OK**, JWT `token` và thông tin `user`; R:43 xác nhận JWT, không định nghĩa các field user, JWT claims/thuật toán/hạn dùng. R:42 yêu cầu thông báo lỗi phù hợp không lộ nguyên nhân nhưng không cho status hoặc JSON schema lỗi. `error: string`, role enum và integer id cần đánh dấu giả định nếu dùng làm schema bắt buộc; response thực tế xem 4.1–4.2.

### e) Mơ hồ / thiếu / mâu thuẫn

- Chưa quy định reset counter sau thành công/hết khóa, xử lý request trong lúc khóa, biên thời gian chính xác.
- HTML5 email validation là UI, không đồng nghĩa backend phải từ chối mọi email sai format.
- Chưa có quy tắc case-folding email, trim, null/object/array, field thiếu/thừa, input dài, error status/message cụ thể.
- So sánh lỗi email không tồn tại và password sai là diễn giải chống dò email từ R:42, chưa có chuỗi thông điệp chuẩn.
- R:35 yêu cầu xác nhận password khi đăng ký nhưng A:15–19 không có field tương ứng; không tự đặt tên field API.

### f) API phụ dựng precondition

`POST /api/register` body mẫu `{"name":"LG User","email":"lg_{{timestamp}}@test.com","password":"Test1234!"}` (A:12–21). Email phải hợp lệ/duy nhất, password tối thiểu 8 ký tự có hoa/thường/số/ký tự đặc biệt (R:32–35). Confirmation field chưa được API spec định nghĩa. Mỗi test độc lập tạo email mới; không làm khóa seed user. Sau đó login bằng chính credentials vừa tạo. Setup đăng ký chỉ được mô tả ở bước này, chưa gọi thực tế.

## 2. API 2 — FR-10 User hủy đơn: `PUT /api/orders/:id/cancel`

### a) Bảng tham số

| Tên | Vị trí | Kiểu | Bắt buộc? | Ràng buộc theo spec | Trích dòng spec |
|---|---|---|---|---|---|
| id | path | ID đơn; exact type chưa nêu | Có theo route | Xác định đơn cần hủy; chưa nêu integer/range/coercion | A:145–147 |
| Authorization | header | `Bearer <token>` | Có | Cart & Orders yêu cầu token; API bảo mật yêu cầu JWT hợp lệ | A:112; R:279 |
| body | body | Chưa nêu | Không có body được mô tả | Không tự coi `status` từ client là tham số hợp lệ | A:145–147 |

### b) Trạng thái và sự kiện

| Chuyển đổi | Actor / điều kiện | Nguồn |
|---|---|---|
| pending → confirmed | Admin xác nhận | R:145–156 |
| confirmed → shipping | Admin giao hàng | R:145–156 |
| shipping → delivered | Admin hoàn tất | R:145–156 |
| pending → canceled | User/Admin hủy | R:150–155 |
| confirmed → canceled | User/Admin hủy | R:150–155 |
| shipping → canceled qua User | User không được tự hủy | R:161; R:236 |
| delivered/canceled → trạng thái khác | Trạng thái kết thúc, cấm chuyển | R:158–162 |
| Chuyển đổi không hợp lệ khác | Lỗi với thông báo phù hợp | R:162 |

FR-20 (R:236) nhắc lại chỉ hủy khi pending/confirmed. A:147 dùng cụm “chưa giao”, chưa đủ để suy rằng shipping cũng cho User hủy. R:161 nói shipping chỉ Admin có thể thao tác, **không ghi rõ thao tác hủy**; sơ đồ không có cạnh shipping → canceled. Quyền Admin tại shipping cần audit, không tự thêm cạnh. Self-transition và initial status checkout không được mô tả tường minh.

### c) SEC-01…SEC-07 và FR-12

| Yêu cầu | Áp dụng cho Hủy đơn |
|---|---|
| SEC-01 (R:278) | Không xử lý password trực tiếp; yêu cầu storage toàn hệ thống, không chứng minh bằng cancel response. |
| SEC-02 (R:279) | Trực tiếp: JWT hợp lệ cùng A:112; hết hạn/sai chữ ký phải không được coi là token hợp lệ, nhưng status cụ thể chưa nêu. |
| SEC-03 (R:280) | Với API Admin dựng trạng thái phải kiểm tra role. Không tự yêu cầu role admin cho endpoint User cancel. |
| SEC-04 (R:281) | Gián tiếp khi thông tin đơn/địa chỉ được render UI; R:222 yêu cầu địa chỉ hiển thị an toàn. Không có cancel JSON escaping contract. |
| SEC-05 (R:282) | Trực tiếp với query chọn/cập nhật đơn theo path id. |
| SEC-06 (R:283) | Không trực tiếp; liên quan setup profile, không phải chức năng cancel. |
| SEC-07 (R:284) | Không trực tiếp; không có OTP trong cancel. |
| FR-12 (R:174–179) | Không trực tiếp liệt kê cancel; áp dụng cho `/api/admin/orders/:id/status` dùng dựng trạng thái. |

FR-11 (R:166) chỉ nêu User xem đơn của chính mình. Không cho User hủy đơn người khác là **GIẢ ĐỊNH bảo mật/ownership cần audit**, không trích FR-11 như quy định cancel tường minh.

### d) Response theo spec

A:147: trạng thái chuyển thành `canceled`, không có success status/body. R:162: chuyển không hợp lệ trả lỗi với thông báo phù hợp, không định nghĩa status/body. GET đơn có endpoint A:140,143; R:167 nói hiển thị mã/ngày/tổng/trạng thái nhưng chưa có schema JSON, tên `user_id`, `total_amount`, `created_at`, kiểu số/ngày. Không gọi GET đơn ở bước quan sát này; không ghi các field này là đã quan sát.

### e) Mơ hồ / thiếu / mâu thuẫn

- “Chưa giao” ở A:147 rộng/mơ hồ hơn điều kiện User pending/confirmed tại R:150–161,236.
- Quyền Admin hủy shipping và Admin dùng chính endpoint User chưa rõ.
- Chưa nêu cancel ownership tường minh, hành vi đối với id không tồn tại/sai type và thiếu token.
- Self-transition, idempotency hủy hai lần, error body/status, token của user đã bị xóa không được định nghĩa chi tiết.
- A:134 có `total_amount` client gửi, trong khi R:105–107 yêu cầu backend tính lại và không chấp nhận giá trị client: phân biệt body mẫu với business rule.

### f) API phụ dựng precondition

1. Register user riêng theo 1.f → `POST /api/login` lấy JWT (A:12–32).
2. `GET /api/products/:id` để biết sản phẩm (A:84–85); `POST /api/cart` kèm Bearer, body mẫu `{"id":1,"name":"Sản phẩm A","price":100000,"quantity":2}` (A:117–127).
3. `POST /api/checkout` cùng Bearer, body mẫu `{"total_amount":200000,"shipping_address":"123 Le Loi, TP.HCM"}` (A:129–137). R:105–108 yêu cầu backend tự tính tổng và xóa giỏ; không dùng giá client làm expected tổng đúng. Cách lấy orderId từ response là quan sát ở 4.4, không phải schema spec.
4. Login admin seed (R:23); `PUT /api/admin/orders/:id/status` body `{"status":"confirmed"}` rồi `{"status":"shipping"}` rồi `{"status":"delivered"}` tùy setup, đi đúng đường FR-10 (A:173,179–182; R:221).
5. Kiểm tra lại bằng `GET /api/orders/:id` hoặc `GET /api/orders/my-orders` với token chủ đơn (A:139–143; R:166). Dựng user B và đơn riêng để kiểm tra ownership/cách ly.
6. `DELETE /api/admin/users/:id` có Admin token để thiết kế token-deleted-user (A:173–177; R:227 cấm admin tự xóa mình). Không thực thi bước này trong Bước 0.

## 3. API 3 — FR-15 Product CRUD

### 3.1 POST `/api/products`

#### a) Bảng tham số

| Tên | Vị trí | Kiểu | Bắt buộc? | Ràng buộc theo spec | Trích dòng spec |
|---|---|---|---|---|---|
| Authorization | header | Bearer JWT | Có | JWT hợp lệ; role admin trong token | R:177–179 |
| name | body JSON | string trong ví dụ | Có | Tối đa 255 ký tự | R:195; A:94 |
| price | body JSON | number | Có | Số dương > 0 | R:196; A:95 |
| category_id | body JSON | số trong ví dụ; integer chưa ghi rõ | Có | Danh mục từ danh sách có sẵn | R:197; A:98 |
| description | body JSON | string trong ví dụ | Chưa nêu | Không có giới hạn/validation được mô tả | A:96 |
| imageUrl | body JSON | string trong ví dụ | Chưa nêu | Không định nghĩa URL validation/độ dài | A:97 |
| :id | path | Không có | Không áp dụng | POST route không có path id | A:88 |

#### b) Trạng thái / sự kiện

Admin tạo sản phẩm (R:193). Mô hình để thiết kế test: chưa tồn tại → tồn tại qua POST; đây là mô hình suy ra từ CRUD, không phải state machine tường minh. Chưa quy định uniqueness tên, id do ai cấp, trạng thái response sau tạo.

#### c) Bảo mật

Áp dụng bảng chung 3.4 cho **POST**: JWT + admin trước khi tạo; query parameterized; dữ liệu hiển thị phải an toàn. Không diễn giải SEC-04 thành bắt buộc từ chối chuỗi HTML ở API.

#### d) Response theo spec

A:87–100 chỉ cho endpoint và body thêm/sửa; R:191–198 cho quyền/ràng buộc. Không định nghĩa create status/success/error schema. `message`, `id` và HTTP 200 chỉ quan sát ở 4.5, không thành contract mặc định.

#### e) Mơ hồ

Không có response schema/status; không định nghĩa string trimming, đơn vị đếm 255 ký tự, null/coercion, field thừa, upper bound price, độ chính xác tiền, uniqueness tên. Description/imageUrl xuất hiện trong ví dụ nhưng chưa nêu bắt buộc. Chưa định nghĩa mass assignment id.

#### f) Setup

Login admin (R:23; A:23–32) → `GET /api/categories` chọn category hiện có (A:102–103) → POST với JSON đầy đủ hợp lệ (A:91–100); sau đó GET detail/list (A:80–85). Không dùng id category chưa biết là tồn tại. Request thực tế ở 4.5.

### 3.2 PUT `/api/products/:id`

#### a) Bảng tham số

| Tên | Vị trí | Kiểu | Bắt buộc? | Ràng buộc theo spec | Trích dòng spec |
|---|---|---|---|---|---|
| Authorization | header | Bearer JWT | Có | JWT hợp lệ, role admin | R:177–179 |
| id | path | ID sản phẩm, exact type chưa nêu | Có theo route | Chọn đúng sản phẩm sửa; format/range chưa nêu | A:89 |
| name | body JSON | string trong ví dụ | FR-15 ghi bắt buộc; partial PUT chưa rõ | Tối đa 255 ký tự | R:195; A:91–94 |
| price | body JSON | number | FR-15 ghi bắt buộc; partial PUT chưa rõ | > 0 | R:196; A:95 |
| category_id | body JSON | số trong ví dụ; integer chưa ghi rõ | FR-15 ghi bắt buộc; partial PUT chưa rõ | Danh mục có sẵn | R:197; A:98 |
| description | body JSON | string trong ví dụ | Chưa nêu | Không có constraints cụ thể | A:96 |
| imageUrl | body JSON | string trong ví dụ | Chưa nêu | Không có URL validation/length cụ thể | A:97 |

#### b) Trạng thái / sự kiện

Tồn tại → sửa → vẫn tồn tại là mô hình CRUD suy ra. **Chỉ sản phẩm được chọn thay đổi, các sản phẩm khác giữ nguyên** (R:198). PUT id chưa tồn tại/đã xóa không được định nghĩa tường minh; không tự suy upsert.

#### c) Bảo mật

Áp dụng bảng 3.4 cho **PUT**: kiểm tra JWT/admin trước sửa, parameterized query gồm path id và body, không để request ảnh hưởng sản phẩm khác (R:198).

#### d) Response theo spec

Không có status hoặc success/error schema cho PUT (A:87–100; R:191–198). Dữ liệu sau sửa kiểm tra qua GET detail/list, không suy message quan sát thành expected cố định.

#### e) Mơ hồ

Full replacement hay partial update; field không gửi có giữ lại không; id không tồn tại/đã xóa; extra body id và validation status đều chưa được mô tả. Các mơ hồ name/price/category của POST cũng áp dụng cho body thêm/sửa A:91.

#### f) Setup

Admin POST sản phẩm riêng trước (3.1.f), ghi snapshot GET list/detail, PUT chính id vừa tạo với body đầy đủ, GET lại để so sánh sản phẩm đích và các sản phẩm khác (A:81,85,88–100; R:198). Không sửa sản phẩm seed 1..5.

### 3.3 DELETE `/api/products/:id`

#### a) Bảng tham số

| Tên | Vị trí | Kiểu | Bắt buộc? | Ràng buộc theo spec | Trích dòng spec |
|---|---|---|---|---|---|
| Authorization | header | Bearer JWT | Có | JWT hợp lệ, role admin | R:177–179 |
| id | path | ID sản phẩm, exact type chưa nêu | Có theo route | Xác định sản phẩm cần xóa; format/range chưa nêu | A:90 |
| body | body | Chưa nêu | Không có body được mô tả | Không có body DELETE contract | A:90–91 |

#### b) Trạng thái / sự kiện

Admin được xóa sản phẩm (R:193). Tồn tại → đã xóa là mô hình CRUD; không quy định hard/soft delete, xóa lần hai, xóa khi đang được tham chiếu hoặc tái dùng id. GET/PUT/DELETE id đã xóa cần GIẢ ĐỊNH về status/chi tiết hành vi.

#### c) Bảo mật

Áp dụng bảng 3.4 cho **DELETE**: JWT/admin, parameterized query theo id; kiểm tra lại dữ liệu sau tấn công. Body-based XSS/mass assignment không trực tiếp áp dụng vì không có body contract.

#### d) Response theo spec

Không có status, success body hoặc error schema (A:90; R:193). Response ở 4.5 là quan sát, không phải quy định. Không khẳng định GET sau xóa phải 404 khi spec chưa nói status.

#### e) Mơ hồ

Hard/soft delete, nonexistent id, malformed id, idempotency và ràng buộc với đơn/giỏ chưa được định nghĩa. Không suy HTTP 200/204/404 thành chắc chắn.

#### f) Setup

Admin login → GET categories → POST sản phẩm riêng → DELETE id được cấp → GET detail/list để kiểm tra không còn được trả như sản phẩm hoạt động (**diễn giải CRUD cần audit**, A:81,85,88–90). Không xóa sản phẩm seed.

### 3.4 SEC-01…SEC-07 và FR-12 cho từng mutation

| Yêu cầu | POST | PUT | DELETE |
|---|---|---|---|
| SEC-01 (R:278) | Không xử lý password; storage toàn hệ thống | Không trực tiếp | Không trực tiếp |
| SEC-02 (R:279) | JWT hợp lệ trước tạo | JWT hợp lệ trước sửa | JWT hợp lệ trước xóa |
| SEC-03 (R:280) | Check role admin theo FR-12 | Check role admin theo FR-12 | Check role admin theo FR-12 |
| SEC-04 (R:281) | Input product được render phải escape; API accept/reject HTML chưa rõ | Tương tự POST | Gián tiếp UI hiển thị dữ liệu; không có body được đặc tả |
| SEC-05 (R:282) | Query insert phải parameterized | Query chọn/sửa theo id và body phải parameterized | Query chọn/xóa theo id phải parameterized |
| SEC-06 (R:283) | Không trực tiếp; chuỗi nâng role qua profile là precondition tấn công | Tương tự POST | Tương tự POST |
| SEC-07 (R:284) | Không trực tiếp: không OTP | Không trực tiếp | Không trực tiếp |
| FR-12 (R:177–179) | Trực tiếp: valid JWT + admin | Trực tiếp: valid JWT + admin | Trực tiếp: valid JWT + admin |

Setup SEC-06: `PUT /api/users/me` chỉ cho thông tin cơ bản (A:64–74), không cho đổi role (R:67,283); gửi `{"role":"admin"}` là input tấn công, không phải request hợp lệ theo spec. Tự ký token/alg none phải đánh giá theo yêu cầu JWT hợp lệ, không suy secret/algorithm thực tế từ code.

## 4. Response quan sát được — KHÔNG phải expected

Thời điểm thực thi: **2026-11-24 01:48 (giờ VN)**. Worker `HappyPathCapture` chạy `scripts/reset_sut.sh` một lần, nhận `SUT reset. Backend PID: 779986`, rồi gọi thật bằng curl tại `http://localhost:3000`. Tất cả request mang `X-Student-Id: 23120190`; body JSON dùng `Content-Type: application/json`. Token bên dưới chỉ giữ 10 ký tự đầu và thêm `...`; Authorization dùng token đầy đủ khi thực thi. Không suy luận bug từ các quan sát ở bước này.

### 4.1 API 1 — Login user

`POST http://localhost:3000/api/login` — không cần Authorization.

Request:
```json
{"email":"test@eshop.com","password":"Test1234!"}
```
HTTP **200**, response thực tế:
```json
{"message":"Login successful","token":"eyJhbGciOi...","user":{"id":2,"name":"Test User","email":"test@eshop.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}
```

### 4.2 Login admin — dựng precondition Product CRUD

`POST http://localhost:3000/api/login` — không cần Authorization.

Request:
```json
{"email":"admin@eshop.com","password":"Admin123!"}
```
HTTP **200**, response thực tế:
```json
{"message":"Login successful","token":"eyJhbGciOi...","user":{"id":1,"name":"Admin User","email":"admin@eshop.com","password":"Admin123!","role":"admin","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}
```

### 4.3 Categories — dựng precondition

`GET http://localhost:3000/api/categories` — không body, không Authorization.

HTTP **200**, response thực tế:
```json
[{"id":1,"name":"Điện thoại"},{"id":2,"name":"Laptop"},{"id":3,"name":"Phụ kiện"}]
```

### 4.4 API 2 — Cart → checkout → cancel

`POST http://localhost:3000/api/cart` — `Authorization: Bearer <token user ở 4.1>`.

Request:
```json
{"id":1,"name":"Sản phẩm A","price":100000,"quantity":2}
```
HTTP **200**, response thực tế:
```json
{"message":"Added to cart"}
```

`POST http://localhost:3000/api/checkout` — cùng token user.

Request:
```json
{"total_amount":200000,"shipping_address":"123 Le Loi, TP.HCM"}
```
HTTP **200**, response thực tế:
```json
{"message":"Checkout successful","orderId":1}
```

`PUT http://localhost:3000/api/orders/1/cancel` — cùng token user, không body; id lấy từ checkout vừa thực hiện.

HTTP **200**, response thực tế:
```json
{"message":"Order canceled successfully"}
```

### 4.5 API 3 — POST → PUT → DELETE sản phẩm mới

Cả ba request dùng `Authorization: Bearer <token admin ở 4.2>`. Không sửa/xóa sản phẩm seed 1..5.

`POST http://localhost:3000/api/products`

Request:
```json
{"name":"Execution Test Product","price":12345,"description":"temporary test product","imageUrl":"http://example.com/test.png","category_id":1}
```
HTTP **200**, response thực tế:
```json
{"message":"Product created","id":6}
```

`PUT http://localhost:3000/api/products/6` — id lấy từ POST vừa thực hiện.

Request:
```json
{"name":"Execution Test Product Updated","price":23456,"description":"updated temporary test product","imageUrl":"http://example.com/test-updated.png","category_id":1}
```
HTTP **200**, response thực tế:
```json
{"message":"Product updated"}
```

`DELETE http://localhost:3000/api/products/6` — không body.

HTTP **200**, response thực tế:
```json
{"message":"Product deleted"}
```

### 4.6 Giới hạn quan sát

Chín request happy path trên đều trả HTTP 200 trong lần thực thi này. Không gọi negative path, không thực hiện Audit/Extend/Execute bộ test, không gán nhãn audit. Không quan sát GET chi tiết đơn/sản phẩm: các field của chúng nếu chưa được spec định nghĩa vẫn là giả định, không được ghi là đã quan sát.
