# API 2 – Cancel Order: mapping test case → collection (bước X4, review tĩnh)

- Collection: `collections/23120190_API2_CancelOrder.postman_collection.json` (tên `23120190_API2_CancelOrder`, Postman v2.1)
- Nguồn: `report/testcases/API2_cancel_generated.md` (mục Audit và Extend – Human; quy ước hợp nhất ở G6)
- Reviewer: Claude (anthropic/claude-sonnet-5-5), 2026-11-25. Không phải Codex worker.
- Phạm vi: đối chiếu tĩnh từng ID (method, path, header/token, raw body, setup độc lập, oracle K, status, nhãn GIẢ ĐỊNH, schema, thời gian). Không sửa collection, không chạy SUT/Newman ở bước này.

> Kết quả chạy thử chỉ để kiểm collection; kết quả chính thức xem results/newman/ do sinh viên chạy.

## 1. Bảng mapping (64 ID nguồn: 59 gốc + 5 EX; 55 có folder, 9 INVALID không có folder)

Quy ước: Request = số request trong folder case (gồm setup, kể cả request trong sub-folder). Assertion = số `pm.test(` trong folder case (đếm cả pre-request: kết quả 0 `pm.test` ở pre-request). Khớp = request, token, status, điều kiện core, oracle K, nhãn (GIẢ ĐỊNH) và schema khớp file nguồn. "E" = predicate hợp nhất của G6: `Content-Type` JSON, body object có `error` string không rỗng, không chứa JWT (G1–G3, G2, EX gộp trong một assertion `core: E ...` kèm jsonSchema S-error; G6/EX tách thành 3–4 assertion `core:` tương đương).

### G1 – Domain partition + boundary

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| CN-G1-01 | VALID | G1 / [CN-G1-01] Hủy pending | 8 | 11 | Có: PUT chủ đơn (T), không body; 200 (GIẢ ĐỊNH) + `message` string (quy ước G6); K GET Bearer T: `canceled` |
| CN-G1-02 | INCOMPLETE | G1 / [CN-G1-02] ID dương vắng | 10 | 13 | Có: V(X) qua `GET /api/admin/orders` chọn `max+1` vắng; PUT Bearer T; 404 (GIẢ ĐỊNH) + E + schema S-error; K pending. Description INCOMPLETE có (phân trang) |
| CN-G1-03 | VALID | G1 / [CN-G1-03] ID bằng 0 | 8 | 11 | Có: `PUT /api/orders/0/cancel`, Bearer T; 400 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-04 | VALID | G1 / [CN-G1-04] ID âm | 8 | 11 | Có: `/-1/cancel`; 400 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-05 | INCOMPLETE | G1 / [CN-G1-05] ID vượt 32 bit | 10 | 13 | Có: V(X) xác nhận 2147483648 vắng; 404 (GIẢ ĐỊNH) + E; K pending. Description INCOMPLETE có |
| CN-G1-06 | INCOMPLETE | G1 / [CN-G1-06] ID rất lớn | 10 | 13 | Có: V(X) xác nhận 9999999999 vắng; 404 (GIẢ ĐỊNH) + E; K pending. Description INCOMPLETE có |
| CN-G1-07 | VALID | G1 / [CN-G1-07] ID thập phân | 8 | 11 | Có: `/1.5/cancel`; 400 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-08 | VALID | G1 / [CN-G1-08] ID chữ | 8 | 11 | Có: `/abc/cancel`; 400 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-09 | VALID | G1 / [CN-G1-09] ID đặc biệt | 8 | 11 | Có: `/%40/cancel`; 400 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-10 | VALID | G1 / [CN-G1-10] ID khoảng trắng | 8 | 11 | Có: `/%20/cancel`; 400 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-11 | VALID | G1 / [CN-G1-11] Thiếu Authorization | 8 | 11 | Có: PUT không có header Authorization; 401 (GIẢ ĐỊNH) + E; K pending (Bearer T) |
| CN-G1-12 | VALID | G1 / [CN-G1-12] Bearer rỗng | 8 | 11 | Có: header đúng `Authorization: Bearer ` (rỗng); 401 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-13 | VALID | G1 / [CN-G1-13] Sai scheme | 8 | 11 | Có: `Authorization: Basic {T}`; 401 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-14 | VALID | G1 / [CN-G1-14] JWT sai chữ ký | 9 | 12 | Có: Tbad = T với ký tự đầu chữ ký đổi `A`↔`B` (giữ 2 phần đầu); 401 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-15 | VALID | G1 / [CN-G1-15] Token rác | 8 | 11 | Có: `Bearer not-a-jwt`; 401 (GIẢ ĐỊNH) + E; K pending |
| CN-G1-16 | VALID | G1 / [CN-G1-16] Body thừa | 8 | 11 | Có: Content-Type JSON + body `{"status":"delivered"}`; 200 (GIẢ ĐỊNH) + `message`; K `canceled` (nên không thể là delivered) |

### G2 – State transition

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| CN-G2-01 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D1 với CN-G1-01: cùng request/expected, chỉ khác nhãn ST.); có trong `info.description` |
| CN-G2-02 | VALID | G2 / [CN-G2-02] User hủy confirmed | 11 | 15 | Có: Admin token `A(confirmed)` + K(confirmed) làm setup; U Bearer T 200 + `message`; K canceled |
| CN-G2-03 | VALID | G2 / [CN-G2-03] User không hủy shipping | 13 | 18 | Có: D(shipping) = A(confirmed), K, A(shipping), K (token admin); U Bearer T 400 (GIẢ ĐỊNH) + E; K shipping |
| CN-G2-04 | VALID | G2 / [CN-G2-04] User không hủy delivered | 15 | 21 | Có: D(delivered) 3 cạnh Admin + K sau từng cạnh; U 400 (GIẢ ĐỊNH) + E; K delivered |
| CN-G2-05 | VALID | G2 / [CN-G2-05] Hủy hai lần | 11 | 16 | Có: U 200 + `message`, K canceled, U lần hai 400 (GIẢ ĐỊNH) + E, K canceled |
| CN-G2-06 | VALID | G2 / [CN-G2-06] Các cạnh từ pending | 45 | 58 | Có: 5 sub-folder (mỗi đích có S riêng, user/admin/đơn riêng); Admin A(s): 400,200,400,400,200 khớp thứ tự file; K pending,confirmed,pending,pending,canceled; các 400 có E |
| CN-G2-07 | VALID | G2 / [CN-G2-07] Các cạnh từ confirmed | 55 | 73 | Có: 5 sub-folder; A(s): 400,400,200,400,200; K confirmed,confirmed,shipping,confirmed,canceled; dựng bằng admin qua K từng bước |
| CN-G2-08 | VALID | G2 / [CN-G2-08] Các cạnh từ shipping | 65 | 89 | Có: 5 sub-folder; A(s): 400,400,400,200,400; K shipping,shipping,shipping,delivered,shipping; Admin→canceled từ shipping 400 (GIẢ ĐỊNH) đúng file |
| CN-G2-09 | VALID | G2 / [CN-G2-09] Các cạnh từ delivered | 75 | 105 | Có: 5 sub-folder; cả 5 A(s) 400 + E; mỗi K delivered |
| CN-G2-10 | VALID | G2 / [CN-G2-10] Các cạnh từ canceled | 55 | 80 | Có: 5 sub-folder; dựng canceled bằng U (user token, 200 + K canceled); A(s) 400 + E; mỗi K canceled |
| CN-G2-11 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D4 với CN-G2-02: cùng đơn confirmed, cùng hủy, cùng 200.); có trong `info.description` |
| CN-G2-12 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D5 với CN-G2-03: cùng chuỗi tới shipping rồi hủy, cùng 400.); có trong `info.description` |
| CN-G2-13 | VALID | G2 / [CN-G2-13] Hủy không đổi đơn khác | 13 | 18 | Có: O và O2 cùng T (checkout 2 lần, O2 xác nhận pending); U trên O 200 + `message`; K O canceled; K O2 pending |

### G3 – Security

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| CN-G3-01 | INCOMPLETE | G3 / [CN-G3-01] B hủy đơn A pending | 15 | 19 | Có: PUT Bearer TB trên O1; 404 (GIẢ ĐỊNH, quy ước G6 thay 403) + JSON error; K O1, O2 pending (Bearer TA). Description INCOMPLETE nêu quy ước G6 |
| CN-G3-02 | INCOMPLETE | G3 / [CN-G3-02] B hủy đơn A confirmed | 17 | 22 | Có: Admin A(confirmed) + K O1 confirmed; TB hủy O1 404 (GIẢ ĐỊNH, quy ước G6) + JSON error; K O1 confirmed, O2 pending. Description INCOMPLETE có |
| CN-G3-03 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D2 với CN-G1-11: cùng không Authorization, cùng 401.); có trong `info.description` |
| CN-G3-04 | INCOMPLETE | G3 / [CN-G3-04] Token hết hạn | 13 | 14 | Có, phần làm được: dựng S3 + kiểm `exp` trong payload TA (setup assert `exp` là number); KHÔNG có request tấn công/chờ/K vì file cho phép không thực thi khi không có `exp`. Description INCOMPLETE có (xem phát hiện F2) |
| CN-G3-05 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D3 với CN-G1-14: cùng cách tạo JWT sai chữ ký, cùng 401.); có trong `info.description` |
| CN-G3-06 | INCOMPLETE | G3 / [CN-G3-06] Token user đã bị xóa | 18 | 20 | Có: snapshot admin, `DELETE /api/admin/users/<idA>`, xác nhận A vắng, snapshot sau; PUT Bearer TA 401 (GIẢ ĐỊNH) + JSON error; K qua `GET /api/admin/orders` (hai đơn pending, so snapshot). Description INCOMPLETE có (xem F3) |
| CN-G3-07 | VALID | G3 / [CN-G3-07] JWT tự ký secret đoán | 15 | 19 | Có: Tforge HS256 `{"id":<idA>,"role":"user"}` ký `secret`, base64url không padding (pre-request CryptoJS); 401 (GIẢ ĐỊNH) + JSON error; K O1, O2 pending |
| CN-G3-08 | VALID | G3 / [CN-G3-08] SQL OR ở path | 15 | 20 | Có: `/1%20OR%201%3D1/cancel` Bearer TA; 400 (GIẢ ĐỊNH) + JSON error + không lộ SQL/SQLite/stack trace; K hai đơn pending |
| CN-G3-09 | VALID | G3 / [CN-G3-09] SQL DROP ở path | 15 | 20 | Có: `/1%3BDROP%20TABLE%20orders/cancel`; 400 (GIẢ ĐỊNH) + JSON error + không lộ SQL; K hai đơn pending và GET 200 |
| CN-G3-10 | VALID | G3 / [CN-G3-10] SQL comment ở path | 15 | 20 | Có: `/1%27%20--/cancel`; 400 (GIẢ ĐỊNH) + JSON error + không lộ SQL; K hai đơn pending |
| CN-G3-11 | VALID | G3 / [CN-G3-11] Admin hủy đơn A | 15 | 19 | Có: PUT Bearer TM (Admin) trên O1 của A; 200 (GIẢ ĐỊNH) + `message`; K O1 canceled, O2 pending |
| CN-G3-12 | INCOMPLETE | G3 / [CN-G3-12] Dò ID liên tiếp và ID vắng mặt | 22 | 35 | Có: setup kiểm O2=O1+1 và chọn X vắng từ danh sách admin; 3 PUT Bearer TB (O1, O2, X) đều 404 (GIẢ ĐỊNH) + JSON error + so body sau khi thay ID bằng `<ID>`; K O1, O2 pending sau từng request. Description INCOMPLETE có |

### G4 – Schema validation

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| CN-G4-01 | VALID | G4 / [CN-G4-01] Schema response hủy pending | 8 | 11 | Có: U 200 (GIẢ ĐỊNH) + Content-Type JSON + jsonSchema S-success (dán nguyên); K 200 + status canceled |
| CN-G4-02 | VALID | G4 / [CN-G4-02] Schema GET sau hủy | 8 | 11 | Có: setup hủy (200); GET: 200 (GIẢ ĐỊNH) + Content-Type JSON + jsonSchema S-order (đủ 6 field, enum 5 trạng thái) + status canceled |
| CN-G4-03 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D7 với CN-G2-05: cùng hủy rồi hủy lại, 200 rồi 400.); có trong `info.description` |
| CN-G4-04 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D2 với CN-G1-11; schema lỗi nằm trong predicate E của G6.); có trong `info.description` |
| CN-G4-05 | VALID | G4 / [CN-G4-05] Thời gian hủy thành công | 8 | 12 | Có: U 200 + Content-Type + S-success + `responseTime < 2000`; K 200 + canceled |
| CN-G4-06 | VALID | G4 / [CN-G4-06] Thời gian GET sau hủy | 8 | 12 | Có: setup hủy; GET 200 + Content-Type + S-order + canceled + `responseTime < 2000` |

### G6 – Bổ sung theo G5

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| CN-G6-01 | INCOMPLETE | G6 / [CN-G6-01] bảo vệ đơn pending | 16 | 22 | Có: V(X) từ danh sách admin; PUT không Authorization trên X; 401 (GIẢ ĐỊNH) + Content-Type + `error` không rỗng + không lộ JWT; K O1, O2 pending. Description INCOMPLETE có |
| CN-G6-02 | VALID | G6 / [CN-G6-02] bảo vệ đơn pending | 15 | 21 | Có: token `alg:none` + payload gốc TA + chữ ký rỗng (header base64url của `{"alg":"none","typ":"JWT"}`); 401 (GIẢ ĐỊNH) + E; K hai đơn pending |
| CN-G6-03 | VALID | G6 / [CN-G6-03] bảo vệ đơn pending | 15 | 21 | Có: `/<O1>abc/cancel` Bearer TA; 400 (GIẢ ĐỊNH) + E; K hai đơn pending |
| CN-G6-04 | INCOMPLETE | G6 / [CN-G6-04] bảo vệ đơn pending | 16 | 22 | Có: V(2147483647) vắng qua danh sách admin; PUT Bearer TA; 404 (GIẢ ĐỊNH) + E; K hai đơn pending. Description INCOMPLETE có |
| CN-G6-05 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D5 với CN-G2-03; E và S-error đã nằm trong predicate G6.); có trong `info.description` |
| CN-G6-06 | VALID | G6 / [CN-G6-06] bảo vệ đơn delivered | 21 | 27 | Có: D(delivered) bằng TM + K từng bước; PUT Bearer TM 400 (GIẢ ĐỊNH) + E; K O1 delivered, O2 pending |
| CN-G6-07 | VALID | G6 / [CN-G6-07] bảo vệ đơn shipping | 19 | 25 | Có: D(shipping); PUT Bearer TM 400 (GIẢ ĐỊNH) + E; K O1 shipping, O2 pending |
| CN-G6-08 | VALID | G6 / [CN-G6-08] bảo vệ đơn shipping | 19 | 25 | Có: D(shipping); PUT Bearer TB 404 (GIẢ ĐỊNH) + E; K O1 shipping, O2 pending |
| CN-G6-09 | VALID | G6 / [CN-G6-09] bảo vệ đơn delivered | 21 | 27 | Có: D(delivered); PUT Bearer TB 404 + E; K O1 delivered, O2 pending |
| CN-G6-10 | VALID | G6 / [CN-G6-10] bảo vệ đơn canceled | 17 | 23 | Có: D(canceled) bằng TA (200 + K canceled); PUT Bearer TB 404 + E; K O1 canceled, O2 pending |
| CN-G6-11 | VALID | G6 / [CN-G6-11] bảo vệ đơn shipping | 19 | 26 | Có: D(shipping); `PUT /api/admin/orders/<O1>/status` Bearer TA (user thường), body `{"status":"canceled"}`; 403 (GIẢ ĐỊNH) + E + jsonSchema S-error; K O1 shipping, O2 pending |
| CN-G6-12 | INVALID | (không có folder – đúng) | 0 | 0 | Có: bỏ theo audit (Trùng D6 với CN-G1-02; chỉ khác nhãn SCH và thêm đơn thứ hai trong K.); có trong `info.description` |

### EX – Extend

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| CN-EX-01 | (Extend – không nhãn) | EX / [CN-EX-01] bảo vệ đơn pending | 8 | 12 | Có: `PUT /api/orders/%2B<O>/cancel` Bearer T; 400 (GIẢ ĐỊNH) + E; K O pending |
| CN-EX-02 | (Extend – không nhãn) | EX / [CN-EX-02] bảo vệ đơn pending | 10 | 14 | Có: forgot-password lấy `resetToken`, reset-password `New1234!`; PUT với T cũ; 401 (GIẢ ĐỊNH) + E; K O pending dùng T cũ đúng như file (xem F6) |
| CN-EX-03 | (Extend – không nhãn) | EX / [CN-EX-03] bảo vệ đơn pending | 8 | 12 | Có: `/<O>.0/cancel`; 400 (GIẢ ĐỊNH) + E; K O pending |
| CN-EX-04 | (Extend – không nhãn) | EX / [CN-EX-04] bảo vệ đơn pending | 8 | 12 | Có: `/0<O>/cancel`; 400 (GIẢ ĐỊNH) + E; K O pending |
| CN-EX-05 | (Extend – không nhãn) | EX / [CN-EX-05] bảo vệ đơn pending | 8 | 13 | Có: JWT HS256 `{"id":<idA>,"role":"user"}` ký `super_secret_key_that_should_not_be_here`; 401 (GIẢ ĐỊNH) + E; K O pending |

### Ngoài nguồn (fixture chẩn đoán X0)

| Mục | Folder | Request | Assertion | Ghi chú |
|---|---|---|---|---|
| [SMOKE] GET /api/products | _smoke | 1 | 1 | Không áp dụng "Khớp": fixture chẩn đoán từ X0 (giống collection API 1), không thuộc tập case nguồn. Runner chính thức lọc G1..EX nên không vào báo cáo chính |

## 2. ID bỏ qua (INVALID theo audit)

- CN-G2-01 – INVALID theo audit: trùng CN-G1-01
- CN-G2-11 – INVALID theo audit: trùng CN-G2-02
- CN-G2-12 – INVALID theo audit: trùng CN-G2-03
- CN-G3-03 – INVALID theo audit: trùng CN-G1-11
- CN-G3-05 – INVALID theo audit: trùng CN-G1-14
- CN-G4-03 – INVALID theo audit: trùng CN-G2-05
- CN-G4-04 – INVALID theo audit: trùng CN-G1-11 (schema lỗi nằm trong E)
- CN-G6-05 – INVALID theo audit: trùng CN-G2-03
- CN-G6-12 – INVALID theo audit: trùng CN-G1-02

Cả 9 ID không có folder trong collection và đều có trong `info.description` (chuỗi "Bỏ qua ... INVALID theo audit").

## 3. Tổng

| Folder | Case | Request | Assertion |
|---|---|---|---|
| G1 | 16 | 135 | 183 |
| G2 | 10 | 358 | 493 |
| G3 | 10 | 160 | 208 |
| G4 | 4 | 32 | 46 |
| G6 | 10 | 178 | 239 |
| EX | 5 | 42 | 63 |
| **Tổng nguồn** | **55** | **905** | **1232** |
| `_smoke` (ngoài nguồn) | 1 | 1 | 1 |
| **Tổng trong file** | 56 | **906** | **1233** |

Số case chuyển = 55 = 40 VALID + 10 INCOMPLETE + 5 EX. Số ID nguồn = 64 (gồm 9 INVALID không có folder). Request lớn vì G2-06..10 gồm 25 sub-folder, mỗi sub-folder dựng đơn riêng. Khớp với quan sát Newman (906 request, 1233 assertion; 1075 pre-request script = 906 collection-level + 169 request-level).

INCOMPLETE (10) – mỗi ID có description trên request: CN-G1-02, G1-05, G1-06 (V(X) phân trang), CN-G3-01, G3-02 (403→404 theo G6), CN-G3-04 (exp), CN-G3-06 (xóa user), CN-G3-12 (V(X) + liên tiếp), CN-G6-01, G6-04 (V(X)).

## 4. Kiểm tra cấu trúc

- Pre-request cấp collection: đúng 2 dòng, đúng 2 câu lệnh `pm.request.headers.upsert(...)` và `console.log('X-Student-Id: ...')` như quy ước; collection có đúng 1 `event` cấp collection.
- `pm.sendRequest`: 0. `try/catch`: 0. `skipRequest`: 0. `setTimeout`: 0 (không có case nào cần chờ ở API 2). `localhost` hardcode: 0 (mọi URL dùng `{{baseUrl}}`). Header `X-Student-Id` chỉ xuất hiện trong pre-request cấp collection (2 lần trong cùng script).
- `pm.execution.setNextRequest`: 4 lần, chỉ ở các setup của CN-G3-06 (xem F3).
- Biến trạng thái dùng `pm.collectionVariables` với tiền tố `cn_<g>_<nn>_`; không có biến tham chiếu chéo case. Email dùng `{{$guid}}` (95 lần) qua `pm.variables.replaceIn`.
- Tên assertion: mọi `pm.test` (trừ `[SMOKE]`) bắt đầu `[CN-...]`; có 266 assertion `status N (GIẢ ĐỊNH)` (mọi status của request chính đều gắn GIẢ ĐỊNH, spec không nêu mã) và 219 assertion `core:`.
- Schema G4: S-success, S-order, S-error dán nguyên văn từ file nguồn (S-order đủ 6 field, enum 5 trạng thái, không field bắt buộc).
- Token (tiêu chí bổ sung): 75 request `PUT /api/admin/orders/<id>/status`; 74 dùng token admin (`CN-G2-02/03/04/06..10`, `CN-G3-02`, `CN-G6-06..09`, `CN-G6-11` setup), ngoại lệ duy nhất CN-G6-11 request chính dùng token user TA đúng như file (User gọi API Admin → 403). Request hủy dùng đúng token file: chủ đơn (G1, G2, G4, G3-06 TA đã xóa, G3-08..10, G6-03/04, EX-01..04), B (G3-01, G3-02, G3-12, G6-08..10), admin TM (G3-11, G6-06, G6-07), không Authorization (G1-11, G6-01), header rỗng/Basic/sửa chữ ký/rác/none/tự ký (G1-12..15, G6-02, G3-07, EX-05).
- Oracle K (tiêu chí bổ sung): case nào file có K thì collection có GET `/api/orders/<O>` (hoặc `GET /api/admin/orders` ở G3-06) sau request; trạng thái đúng bảng file (pending sau mọi lỗi; canceled sau hủy thành công; G2-03 shipping; G2-04 delivered; G2-05 canceled hai lần; G3-02 confirmed + O2 pending; G3-11 O1 canceled + O2 pending; G6-06..11 theo trạng thái dựng, O2 luôn pending). Case hai đơn (G3, G6) GET cả O1 và O2; G3-12 GET sau từng request trong ba request. CN-G3-04 là ngoại lệ không có K (xem F2).
- Không assertion nào bị nới lỏng: mọi status khớp cột Expected (hoặc quy ước G6: CN-G3-01/02 đã dùng 404); schema không bớt field; không có thời gian chờ nào thay đổi; mọi "biểu thị lỗi" chuyển thành E.
- `results/newman/` chỉ có `.gitkeep`; không có report mới.

## 5. Phát hiện tĩnh (danh sách cho Manager)

Không có dòng "Khớp file? Không". Các điểm dưới đây không làm sai expected, nhưng Manager nên quyết định có giao prompt sửa không (không ảnh hưởng assertion core).

| # | ID | Mức | Mô tả | Bằng chứng |
|---|---|---|---|---|
| F1 | CN-G6-01..04, 06..11, CN-EX-01..05 | Thấp (đặt tên) | Request oracle K đặt tên `[ID] setup: oracle đơn 1/2` nhưng chứa assertion `core: đơn N pending/canceled/...`. Quy ước nói setup chỉ là bước dựng; trong report fail của oracle sẽ hiện như "setup" (ví dụ lỗi 36, 39, 42, 45, 48 trong lần chạy thử đều là `core: đơn 1 pending` nằm trong request tên "setup: oracle đơn 1") |  request `[ID] setup: oracle đơn 1` / `setup: oracle đơn 2` trong folder G6 và EX |
| F2 | CN-G3-04 | Thấp (INCOMPLETE, đúng quy ước) | Folder chỉ có setup + assertion `setup: claim exp có thể chờ`; không có nhánh chờ → PUT token cũ → K khi payload có `exp`. Hiện chạy là fail ở setup (token SUT không có `exp`), không có request tấn công nào. Description INCOMPLETE đã nêu. Nếu SUT sau này cấp `exp` thì case vẫn không chờ và không gửi PUT | folder 11 request, 0 request PUT cancel |
| F3 | CN-G3-06 | Thấp (quy ước) | 4 setup dùng `pm.execution.setNextRequest('c7b6dcf4-…0307')` khi `ready` false để "dừng case" theo file. Đích là `id` gắn vào request đầu của CN-G3-07 (có trong collection, hợp lệ) nhưng buộc cứng id và khác quy ước "không thêm điều kiện bỏ qua". Lần chạy thử không kích hoạt (906/906 request chạy) | grep `setNextRequest` = 4, `"id":"c7b6dcf4-…0307"` = 1 |
| F4 | CN-G6-xx, CN-EX-xx | Thông tin | Assertion "không lộ JWT" ở G6/EX dùng regex rộng `x.y.z` (mọi chuỗi 3 phần ngăn bằng dấu chấm), còn G1–G3 dùng regex bắt đầu `eyJ`. Không yếu hơn file; chỉ có thể báo false positive nếu thông báo lỗi chứa chuỗi dạng `a.b.c` | request chính G6/EX so với request chính G3 |
| F5 | CN-G3-12 | Thông tin | Assertion `core: body giống sau loại ID` ở request thứ nhất chỉ lưu baseline, luôn pass; so sánh thật ở request 2 và 3. Đúng ý file nhưng assertion đầu không kiểm gì | request `[CN-G3-12] PUT .../<order1>/cancel` |
| F6 | CN-EX-02 | Thông tin (đúng file) | K dùng token T cũ như file ghi `K(O) = ... Bearer {{T}}`. Nếu SUT vá và vô hiệu token cũ sau reset password thì K GET trả 401 và `core: đơn 1 pending` fail vì lý do khác. Hiện SUT còn chấp nhận T cũ nên K hoạt động | request `[CN-EX-02] setup: oracle đơn 1` dùng `{{cn_ex_02_token_a}}` |
| F7 | CN-G6-01..04, 06..11, CN-EX-01..05 | Thông tin (đặt tên) | Tên folder case của G6/EX chung chung (`bảo vệ đơn pending/shipping/delivered/canceled`), không nêu mục đích của file (ví dụ CN-G6-02 là JWT `alg:none`, CN-EX-02 là token cũ sau reset mật khẩu). Quy ước: `[<ID>] <Mục đích>` | tên folder trong collection |

## 6. Quan sát chạy X4

Không do reviewer này chạy. Manager đã giao worker khác chạy một lần Newman CLI đầy đủ có reset SUT, không lọc folder, không xuất report; artifact công cụ debug `local://3.log` (tóm tắt dòng 7667–7685). Worker thực thi: openai-codex/gpt-6-luna (theo Manager). Reviewer chỉ đọc lại bảng tóm tắt và danh sách lỗi trong artifact.

|Chỉ số|Quan sát thực tế|
|---|---|
|Iteration|1|
|Request|906, 0 lỗi request|
|Test script|906, 0 lỗi script|
|Pre-request script|1075, 0 lỗi script|
|Assertion|1233: 1185 pass, 48 fail|
|Thời gian|31.6 s|

Console có `X-Student-Id: 23120190 -> ... http://localhost:3000/...` (quan sát ở request `[SMOKE]` trong artifact) và hostname `localhost`. 48 failure đều là AssertionError, không có lỗi request hay script; không sửa status, schema hay core để làm xanh.

Tóm tắt 48 fail theo ID (expected so với thực tế, chỉ để kiểm collection):

- Status GIẢ ĐỊNH lệch (SUT trả 404/403 thay 400/401 hoặc ngược lại): CN-G1-03, 04, 07, 08, 09, 10 (400 vs 404); CN-G1-14, 15, CN-G3-07, CN-G6-02 (401 vs 403); CN-G3-08, 09, 10, CN-G6-03 (400 vs 404); CN-G6-06, 07 (400 vs 404); CN-G6-11 (403 vs 400).
- Fail kèm core (dữ liệu/oracle): CN-G1-13 (200, không có `error`, đơn bị `canceled`); CN-G2-03 (hủy shipping trả 200, đơn `canceled`); CN-G2-10 sub-folder `canceled → delivered` (Admin đổi trạng thái 200, đơn `delivered`); CN-G3-06 (token user đã xóa trả 200, đơn `canceled`); CN-G3-11 (Admin hủy trả 404, đơn O1 vẫn pending); CN-EX-01..05 (mỗi case 3 fail: status, `error`, đơn `canceled` thay `pending`).
- Setup: CN-G3-04 `setup: claim exp có thể chờ` (payload không có `exp`).

Đây không phải kết quả Execute chính thức; kết quả chính thức xem `results/newman/` do sinh viên chạy.

## 7. Kết luận X4 cho CN

- Mọi ID của file có trong bảng (64/64); 9 INVALID không có folder và đều trong danh sách bỏ qua; 10 INCOMPLETE đều có description; 5 EX đủ.
- Không còn dòng "Khớp file? Không". F1–F7 là điểm cần Manager quyết định; không có điểm nào nới lỏng expected.
- `results/newman/` không có file mới.
