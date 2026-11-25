# API 3 – Product CRUD: mapping test case → collection (bước PR-X4, review tĩnh)

- Collection: `collections/23120190_API3_ProductCRUD.postman_collection.json` (tên `23120190_API3_ProductCRUD`, Postman v2.1)
- Nguồn: `report/testcases/API3_product_generated.md` (bảng G1–G4, G6, mục Audit và Extend – Human)
- Reviewer: Claude Code, model thực tế `anthropic/claude-sonnet-5-5` (không phải worker Codex), 2026-11-25 (review tĩnh ban đầu). Phụ lục runtime (mục 1, 3, 4, 6, 7, 8 cập nhật sau khi tách PR-G6-09/15/31 sang `G6-isolated`): cũng do Claude Code, model thực tế `anthropic/claude-sonnet-5-5`; chỉ đọc lại collection, `scripts/run_newman.sh` và log CLI thật do Manager cung cấp, không chạy lại test hay SUT
- Phạm vi: đối chiếu tĩnh từng ID (method, path, header, raw body, setup độc lập, status, nhãn GIẢ ĐỊNH, schema, điều kiện core, kiểm tra "S không đổi"/"chỉ P đổi"). Số liệu đếm và so khớp lấy bằng script đọc JSON collection và bảng markdown (chỉ đọc). Reviewer không reset SUT, không chạy Newman (theo hợp đồng Manager), không sửa collection, test case, SUT, script, environment; `report/AI_LOG.md` do Manager ghi. Số liệu runtime ở mục 6 lấy từ log CLI thật (chỉ `--reporters cli`) do người khác chạy, dùng làm chẩn đoán.

> Kết quả chạy thử chỉ để kiểm collection; kết quả chính thức xem results/newman/ do sinh viên chạy.

## 1. Bảng mapping (133 ID nguồn: 127 trong G1–G4, G6 và 6 EX; 125 có folder, 8 INVALID không có folder)

Quy ước:
- Request = số request trong folder case, gồm setup và GET xác minh. Assertion = số `pm.test(` trong mọi script của folder; không có `pm.test` ở pre-request (0 trên 258 script pre-request), nên toàn bộ nằm ở test script.
- Chuỗi `status` trong cột Khớp là thứ tự các assertion `status N (GIẢ ĐỊNH)` trong folder, gồm cả GET xác minh sau request chính. File nguồn ghi 100% status là GIẢ ĐỊNH nên mọi assertion status đều mang nhãn này.
- Khớp = method, path, header, body, status, điều kiện core và nhãn khớp cột Request và cột Expected của file nguồn. Tên đầy đủ của body (B, B2, V…) nằm ở cột Request của file nguồn; bảng chỉ chép lại cột đó để đối chiếu.
- Cả 125 folder case đều có ít nhất một assertion `core:` và một assertion `status N (GIẢ ĐỊNH)`; mọi `pm.test` đều có tiền tố `[ID]` đúng ID folder.

### G1 – Domain partition + boundary (41 case)

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| PR-G1-01 | VALID | G1 / [PR-G1-01] Thiếu name | 5 | 6 | Có: POST /api/products; Bearer T; JSON B-name; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-02 | VALID | G1 / [PR-G1-02] Name rỗng | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[name]=""; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-03 | VALID | G1 / [PR-G1-03] Name khoảng trắng | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[name]="   "; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-05 | VALID | G1 / [PR-G1-05] Name 254 ký tự | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[name]=tên 254; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-06 | VALID | G1 / [PR-G1-06] Name 255 ký tự | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[name]=tên 255; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-07 | VALID | G1 / [PR-G1-07] Name 256 ký tự | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[name]=tên 256; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-08 | VALID | G1 / [PR-G1-08] Name tiếng Việt | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[name]="Sản phẩm {{K}}"; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-09 | VALID | G1 / [PR-G1-09] Name null | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[name]=null; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-10 | VALID | G1 / [PR-G1-10] Name số | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[name]=123; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-11 | VALID | G1 / [PR-G1-11] Thiếu price | 5 | 6 | Có: POST /api/products; Bearer T; JSON B-price; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-12 | VALID | G1 / [PR-G1-12] Price bằng 0 | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]=0; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-13 | VALID | G1 / [PR-G1-13] Price âm | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]=-1; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-14 | VALID | G1 / [PR-G1-14] Price 0.01 | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]=0.01; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-15 | VALID | G1 / [PR-G1-15] Price 1 | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]=1; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-16 | VALID | G1 / [PR-G1-16] Price rất lớn | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]=1e15; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-17 | VALID | G1 / [PR-G1-17] Price chuỗi số | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]="100000"; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-18 | VALID | G1 / [PR-G1-18] Price chuỗi chữ | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]="abc"; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-19 | VALID | G1 / [PR-G1-19] Price null | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]=null; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-20 | VALID | G1 / [PR-G1-20] Price boolean | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[price]=true; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-21 | VALID | G1 / [PR-G1-21] Thiếu category_id | 5 | 6 | Có: POST /api/products; Bearer T; JSON B-category_id; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-23 | VALID | G1 / [PR-G1-23] Category không tồn tại | 5 | 8 | Có: POST /api/products; Bearer T; JSON B[category_id]=99999; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-24 | VALID | G1 / [PR-G1-24] Category 0 | 5 | 8 | Có: POST /api/products; Bearer T; JSON B[category_id]=0; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-25 | VALID | G1 / [PR-G1-25] Category âm | 5 | 8 | Có: POST /api/products; Bearer T; JSON B[category_id]=-1; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-26 | VALID | G1 / [PR-G1-26] Category chuỗi | 5 | 8 | Có: POST /api/products; Bearer T; JSON B[category_id]="abc"; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-27 | VALID | G1 / [PR-G1-27] Thiếu description | 5 | 6 | Có: POST /api/products; Bearer T; JSON B-description; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-28 | VALID | G1 / [PR-G1-28] Description rỗng | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[description]=""; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-29 | VALID | G1 / [PR-G1-29] Description rất dài | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[description]=a×10000; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-30 | VALID | G1 / [PR-G1-30] Thiếu imageUrl | 5 | 6 | Có: POST /api/products; Bearer T; JSON B-imageUrl; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-31 | VALID | G1 / [PR-G1-31] Image rỗng | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[imageUrl]=""; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-32 | VALID | G1 / [PR-G1-32] Image rất dài | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[imageUrl]=a×10000; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-33 | VALID | G1 / [PR-G1-33] Image không phải URL | 5 | 6 | Có: POST /api/products; Bearer T; JSON B[imageUrl]="not-a-url"; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi |
| PR-G1-34 | VALID | G1 / [PR-G1-34] PUT id tồn tại | 8 | 8 | Có: PUT /api/products/{{P}}; Bearer T; JSON B[price]=1; status 200 (GIẢ ĐỊNH); core: P đúng body; sản phẩm khác không đổi |
| PR-G1-36 | VALID | G1 / [PR-G1-36] PUT id 0 | 5 | 8 | Có: PUT /api/products/0; Bearer T; JSON B; status 404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-37 | VALID | G1 / [PR-G1-37] PUT id âm | 5 | 8 | Có: PUT /api/products/-1; Bearer T; JSON B; status 404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-38 | VALID | G1 / [PR-G1-38] PUT id chữ | 5 | 8 | Có: PUT /api/products/abc; Bearer T; JSON B; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-41 | VALID | G1 / [PR-G1-41] DELETE id 0 | 5 | 8 | Có: DELETE /api/products/0; Bearer T; không body; status 404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-42 | VALID | G1 / [PR-G1-42] DELETE id âm | 5 | 8 | Có: DELETE /api/products/-1; Bearer T; không body; status 404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-43 | VALID | G1 / [PR-G1-43] DELETE id chữ | 5 | 8 | Có: DELETE /api/products/abc; Bearer T; không body; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-44 | VALID | G1 / [PR-G1-44] Body rỗng | 5 | 6 | Có: POST /api/products; Bearer T; JSON {}; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-45 | VALID | G1 / [PR-G1-45] JSON sai cú pháp | 5 | 6 | Có: POST /api/products; Bearer T; raw JSON {"name":; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G1-46 | VALID | G1 / [PR-G1-46] Field id thừa | 5 | 9 | Có: POST /api/products; Bearer T; JSON B thêm "id":99999; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi; id mới khác 99999 |

### G2 – State transition (13 case)

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| PR-G2-02 | VALID | G2 / [PR-G2-02] GET id chưa tồn tại | 6 | 7 | Có: GET /api/products/{{A}}; Bearer T; không body; status 404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G2-03 | VALID | G2 / [PR-G2-03] PUT id chưa tồn tại không tạo mới | 6 | 7 | Có: PUT /api/products/{{A}}; Bearer T; JSON B2; status 404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G2-04 | VALID | G2 / [PR-G2-04] DELETE id chưa tồn tại | 6 | 7 | Có: DELETE /api/products/{{A}}; Bearer T; không body; status 404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G2-05 | VALID | G2 / [PR-G2-05] POST khi sản phẩm mục tiêu đang tồn tại | 7 | 9 | Có: POST /api/products; Bearer T; JSON Bnew; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi; id mới khác P |
| PR-G2-06 | VALID | G2 / [PR-G2-06] GET sản phẩm đang tồn tại | 7 | 8 | Có: GET /api/products/{{P}}; Bearer T; không body; status 200 (GIẢ ĐỊNH); core: detail P đúng B; list không đổi |
| PR-G2-08 | VALID | G2 / [PR-G2-08] DELETE sản phẩm tồn tại | 8 | 9 | Có: DELETE /api/products/{{P}}; Bearer T; không body; status 200→404 (GIẢ ĐỊNH); core: sản phẩm khác không đổi; P đã xóa |
| PR-G2-10 | VALID | G2 / [PR-G2-10] GET sản phẩm đã xóa | 9 | 11 | Có: GET /api/products/{{P}}; Bearer T; không body; status 404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G2-11 | VALID | G2 / [PR-G2-11] PUT sản phẩm đã xóa | 10 | 12 | Có: PUT /api/products/{{P}}; Bearer T; JSON B2; status 404→404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G2-12 | VALID | G2 / [PR-G2-12] DELETE hai lần | 10 | 12 | Có: DELETE /api/products/{{P}}; Bearer T; không body; status 404→404 (GIẢ ĐỊNH); core: error không rỗng; list không đổi |
| PR-G2-13 | VALID | G2 / [PR-G2-13] Vòng đời đầy đủ | 11 | 15 | Có: POST /api/products JSON B → GET /api/products/{{P}} → PUT /api/products/{{P}} JSON B2 → GET /api/products/{{P}} → DELETE /api/products/{{P}} → GET /api/products/{{P}} → GET /api/products; tất cả Bearer T; GET/DELETE không body; sau POST lấy P duy nhất theo K từ GET list, dừng nếu P thuộc 1..5; status 200→200→200→200→200→404→200 (GIẢ ĐỊNH); core: unique non-seed P; detail matches expected; error không rỗng; list không đổi |
| PR-G2-14 | VALID | G2 / [PR-G2-14] Chỉ sản phẩm đích thay đổi | 10 | 10 | Có: PUT /api/products/{{P}}; Bearer T; JSON B2; status 200 (GIẢ ĐỊNH); core: P đúng body; sản phẩm khác không đổi |
| PR-G2-15 | VALID | G2 / [PR-G2-15] Hai sản phẩm trùng tên | 7 | 9 | Có: POST /api/products; Bearer T; JSON B; status 200 (GIẢ ĐỊNH); core: sản phẩm mới đúng yêu cầu; sản phẩm cũ không đổi; hai sản phẩm trùng tên khác id |
| PR-G2-16 | INCOMPLETE | G2 / [PR-G2-16] PUT một phần giữ field không gửi | 7 | 8 | Có: PUT /api/products/{{P}}; Bearer T; JSON {"price":150000}; status 400 (GIẢ ĐỊNH); core: error không rỗng; list không đổi. INCOMPLETE xử lý theo lý do audit: expected 200 cũ thay bằng 400 + `error` + list bằng S (quy tắc full PUT G6/G5); description ở folder và ở request chính ghi "INCOMPLETE" và nêu quy tắc thay thế |

### G3 – Security (22 case)

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| PR-G3-01 | VALID | G3 / [PR-G3-01] Thiếu token tạo | 11 | 12 | Có: POST /api/products; không Authorization; JSON B2; status 401 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-02 | VALID | G3 / [PR-G3-02] Thiếu token sửa | 11 | 12 | Có: PUT /api/products/{{P}}; không Authorization; JSON B2; status 401 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-03 | VALID | G3 / [PR-G3-03] Thiếu token xóa | 11 | 12 | Có: DELETE /api/products/{{P}}; không Authorization; không body; status 401 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-04 | VALID | G3 / [PR-G3-04] User thường tạo | 11 | 12 | Có: POST /api/products; Authorization: Bearer {{V}}; JSON B2; status 403 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-05 | VALID | G3 / [PR-G3-05] User thường sửa | 11 | 12 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{V}}; JSON B2; status 403 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-06 | VALID | G3 / [PR-G3-06] User thường xóa | 11 | 12 | Có: DELETE /api/products/{{P}}; Authorization: Bearer {{V}}; không body; status 403 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-07 | VALID | G3 / [PR-G3-07] Tự nâng role rồi tạo | 16 | 16 | Có: POST /api/products; Authorization: Bearer {{W2}}; JSON B2; status 403 (GIẢ ĐỊNH); core: profile không phải admin; error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list. setup đăng ký user riêng dùng `oneOf([200,201])` (md không quy định status register; chỉ là setup); `PUT /api/users/me` không assert (md: "bất kể response") |
| PR-G3-08 | VALID | G3 / [PR-G3-08] Tự nâng role rồi sửa | 16 | 16 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{W2}}; JSON B2; status 403 (GIẢ ĐỊNH); core: profile không phải admin; error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list. như PR-G3-07 (setup E); request chính PUT |
| PR-G3-09 | VALID | G3 / [PR-G3-09] Tự nâng role rồi xóa | 16 | 16 | Có: DELETE /api/products/{{P}}; Authorization: Bearer {{W2}}; không body; status 403 (GIẢ ĐỊNH); core: profile không phải admin; error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list. như PR-G3-07 (setup E); request chính DELETE |
| PR-G3-10 | VALID | G3 / [PR-G3-10] JWT tự ký tạo | 11 | 12 | Có: POST /api/products; Authorization: Bearer {{H}}; JSON B2; status 401 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-11 | VALID | G3 / [PR-G3-11] JWT tự ký sửa | 11 | 12 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{H}}; JSON B2; status 401 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-12 | VALID | G3 / [PR-G3-12] JWT tự ký xóa | 11 | 12 | Có: DELETE /api/products/{{P}}; Authorization: Bearer {{H}}; không body; status 401 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-13 | VALID | G3 / [PR-G3-13] SQL injection name khi tạo | 11 | 11 | Có: POST /api/products; Authorization: Bearer {{T}}; JSON B2[name]="{{K}}' OR 1=1 --"; status 200 (GIẢ ĐỊNH); core: đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-14 | VALID | G3 / [PR-G3-14] SQL injection description khi tạo | 11 | 11 | Có: POST /api/products; Authorization: Bearer {{T}}; JSON B2[description]="' OR 1=1 --"; status 200 (GIẢ ĐỊNH); core: đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-15 | VALID | G3 / [PR-G3-15] SQL injection name khi sửa | 11 | 11 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{T}}; JSON B2[name]="{{K}}' OR 1=1 --"; status 200 (GIẢ ĐỊNH); core: đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-16 | VALID | G3 / [PR-G3-16] SQL injection description khi sửa | 11 | 11 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{T}}; JSON B2[description]="' OR 1=1 --"; status 200 (GIẢ ĐỊNH); core: đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-17 | VALID | G3 / [PR-G3-17] SQL injection path sửa | 11 | 12 | Có: PUT /api/products/{{I}}; Authorization: Bearer {{T}}; JSON B2; status 400 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-18 | VALID | G3 / [PR-G3-18] SQL injection path xóa | 11 | 12 | Có: DELETE /api/products/{{I}}; Authorization: Bearer {{T}}; không body; status 400 (GIẢ ĐỊNH); core: error không rỗng; đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-19 | VALID | G3 / [PR-G3-19] Stored XSS name khi tạo | 11 | 11 | Có: POST /api/products; Authorization: Bearer {{T}}; JSON B2[name]="<script>alert(1)</script>"; status 200 (GIẢ ĐỊNH); core: đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-20 | VALID | G3 / [PR-G3-20] Stored XSS name khi sửa | 11 | 11 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{T}}; JSON B2[name]="<img src=x onerror=alert(1)>"; status 200 (GIẢ ĐỊNH); core: đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-21 | VALID | G3 / [PR-G3-21] Mass assignment id và field lạ khi tạo | 11 | 11 | Có: POST /api/products; Authorization: Bearer {{T}}; JSON B2 thêm "id":{{Q}},"unexpected":"overwrite"; status 200 (GIẢ ĐỊNH); core: đối chiếu S và payload; detail P bằng list; detail Q bằng list |
| PR-G3-22 | VALID | G3 / [PR-G3-22] Mass assignment id và field lạ khi sửa | 11 | 11 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{T}}; JSON B2 thêm "id":{{Q}},"unexpected":"overwrite"; status 200 (GIẢ ĐỊNH); core: đối chiếu S và payload; detail P bằng list; detail Q bằng list |

### G4 – Schema validation (8 case)

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| PR-G4-01 | VALID | G4 / [PR-G4-01] Schema tạo và round-trip price | 5 | 14 | Có: POST /api/products; Bearer T; JSON B; GET /api/products lấy P duy nhất theo K, dừng nếu P thuộc 1..5; GET /api/products/{{P}}; Bearer T; không body; status 200→200→200 (GIẢ ĐỊNH); core: JSON và thời gian dưới 2000ms; schema S1; message và id; id POST bằng P; schema S4; product và giá trị |
| PR-G4-02 | VALID | G4 / [PR-G4-02] Schema sửa và kiểm tra giá trị mới | 6 | 12 | Có: PUT /api/products/{{P}}; Bearer T; JSON B2; GET /api/products/{{P}}; Bearer T; không body; status 200→200 (GIẢ ĐỊNH); core: JSON và thời gian dưới 2000ms; schema S2; message; schema S4; product và giá trị |
| PR-G4-03 | VALID | G4 / [PR-G4-03] Schema xóa | 6 | 12 | Có: DELETE /api/products/{{P}}; Bearer T; không body; GET /api/products/{{P}}; Bearer T; không body; status 200→404 (GIẢ ĐỊNH); core: JSON và thời gian dưới 2000ms; schema S2; message; schema S3; error không rỗng |
| PR-G4-04 | VALID | G4 / [PR-G4-04] Lỗi tạo thiếu name | 5 | 10 | Có: POST /api/products; Bearer T; JSON {"price":12345,"description":"Mô tả {{K}}","imageUrl":"https://example.com/initial.png","category_id":{{C}}}; GET /api/products; Bearer T; không body; status 400→200 (GIẢ ĐỊNH); core: JSON và thời gian dưới 2000ms; schema S3; error không rỗng; list bằng S |
| PR-G4-05 | VALID | G4 / [PR-G4-05] Lỗi sửa price không dương | 7 | 12 | Có: PUT /api/products/{{P}}; Bearer T; JSON {"name":"{{K}}","price":0,"description":"Mô tả {{K}}","imageUrl":"https://example.com/initial.png","category_id":{{C}}}; GET /api/products; Bearer T; không body; status 400→200 (GIẢ ĐỊNH); core: JSON và thời gian dưới 2000ms; schema S3; error không rỗng; list bằng S |
| PR-G4-06 | VALID | G4 / [PR-G4-06] Lỗi xóa id không tồn tại | 6 | 11 | Có: DELETE /api/products/{{A}}; Bearer T; không body; GET /api/products; Bearer T; không body; status 404→200 (GIẢ ĐỊNH); core: JSON và thời gian dưới 2000ms; schema S3; error không rỗng; list bằng S |
| PR-G4-07 | INCOMPLETE | G4 / [PR-G4-07] Kiểu price trên product id chẵn và lẻ | 24 | 33 | Có: GET /api/products/{{E}}; Bearer T; không body; GET /api/products/{{O}}; Bearer T; không body; status 200→200 (GIẢ ĐỊNH); core: JSON và thời gian dưới 2000ms; schema S4; product và giá trị. INCOMPLETE: description ở folder, ở setup parity 10 và ở hai GET ghi "INCOMPLETE: cần tạo được id chẵn và lẻ lớn hơn 5 trong tối đa 10 sản phẩm; thiếu parity thì setup thất bại, không gửi GET kiểm tra". Vòng lặp dùng `pm.execution.setNextRequest` (10 chỗ): đủ parity thì nhảy tới GET even; sau sản phẩm 10 mà thiếu thì nhảy tới PR-G4-08. Số assertion là số tĩnh; lúc chạy ít hơn nếu thoát sớm |
| PR-G4-08 | VALID | G4 / [PR-G4-08] Kiểm tra GET object đầy đủ | 5 | 8 | Có: GET /api/products/{{P}}; Bearer T; không body; status 200 (GIẢ ĐỊNH); core: JSON và thời gian dưới 2000ms; schema S4; product và giá trị |

### G6 – Bổ sung theo G5 (35 case: 32 trong folder `G6`, 3 trong folder `G6-isolated`)

PR-G6-09, PR-G6-15, PR-G6-31 nằm trong folder `G6-isolated` (đặt trước `EX`), không còn nằm trong `G6`. Request, script, assertion và expected của ba case giữ nguyên.

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| PR-G6-01 | VALID | G6 / [PR-G6-01] H1, H8: thiếu name PUT | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V-name; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-02 | VALID | G6 / [PR-G6-02] H1: name rỗng PUT | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[name]=""; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-03 | VALID | G6 / [PR-G6-03] H1: name sai kiểu số | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[name]=123; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-04 | VALID | G6 / [PR-G6-04] H1: name 255 ký tự | 9 | 12 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[name]=a×255; status 200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thay đổi P; detail P đúng mong đợi |
| PR-G6-05 | VALID | G6 / [PR-G6-05] H1: name 256 ký tự | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[name]=a×256; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-06 | VALID | G6 / [PR-G6-06] H1: name null | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[name]=null; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-07 | VALID | G6 / [PR-G6-07] H2: price âm | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[price]=-1; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-08 | VALID | G6 / [PR-G6-08] H2: price chuỗi | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[price]="150000"; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-09 | VALID | G6-isolated / [PR-G6-09] H2: price null | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[price]=null; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi. Nội dung case không đổi, chỉ chuyển folder; chạy riêng một lượt có reset trước (mục 6) |
| PR-G6-10 | VALID | G6 / [PR-G6-10] H2: price dương 0.01 | 9 | 12 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[price]=0.01; status 200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thay đổi P; detail P đúng mong đợi |
| PR-G6-11 | VALID | G6 / [PR-G6-11] H3, H8: thiếu category | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V-category_id; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-12 | VALID | G6 / [PR-G6-12] H3: category 99999 không tồn tại | 10 | 14 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[category_id]=99999; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-13 | VALID | G6 / [PR-G6-13] H3: category 0 | 10 | 14 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[category_id]=0; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-14 | VALID | G6 / [PR-G6-14] H3: category âm | 10 | 14 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[category_id]=-1; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-15 | VALID | G6-isolated / [PR-G6-15] H8: thiếu riêng price | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V-price; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi. Nội dung case không đổi, chỉ chuyển folder; chạy riêng một lượt có reset trước (mục 6) |
| PR-G6-16 | VALID | G6 / [PR-G6-16] H4: alg none tạo | 9 | 13 | Có: POST /api/products; Authorization: Bearer {{N}}; JSON V; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-17 | VALID | G6 / [PR-G6-17] H4: alg none sửa | 9 | 13 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{N}}; JSON V; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-18 | VALID | G6 / [PR-G6-18] H4: alg none xóa | 9 | 13 | Có: DELETE /api/products/{{P}}; Authorization: Bearer {{N}}; không body; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-19 | VALID | G6 / [PR-G6-19] H5: JWT sai cấu trúc tạo | 9 | 13 | Có: POST /api/products; Authorization: Bearer {{M}}; JSON V; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-20 | VALID | G6 / [PR-G6-20] H5: JWT sai cấu trúc sửa | 9 | 13 | Có: PUT /api/products/{{P}}; Authorization: Bearer {{M}}; JSON V; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-21 | VALID | G6 / [PR-G6-21] H5: JWT sai cấu trúc xóa | 9 | 13 | Có: DELETE /api/products/{{P}}; Authorization: Bearer {{M}}; không body; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-22 | VALID | G6 / [PR-G6-22] H6: XSS description POST | 10 | 14 | Có: POST /api/products; Bearer T; JSON V[description]="<script>alert(1)</script>"; status 200→200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thêm một id và giữ nguyên S; detail P đúng mong đợi; detail id mới đúng body |
| PR-G6-23 | VALID | G6 / [PR-G6-23] H6: XSS description PUT | 9 | 12 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[description]="<script>alert(1)</script>"; status 200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thay đổi P; detail P đúng mong đợi |
| PR-G6-24 | VALID | G6 / [PR-G6-24] H6: XSS imageUrl POST | 10 | 14 | Có: POST /api/products; Bearer T; JSON V[imageUrl]="javascript:alert(1)"; status 200→200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thêm một id và giữ nguyên S; detail P đúng mong đợi; detail id mới đúng body |
| PR-G6-25 | VALID | G6 / [PR-G6-25] H6: XSS imageUrl PUT | 9 | 12 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[imageUrl]="javascript:alert(1)"; status 200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thay đổi P; detail P đúng mong đợi |
| PR-G6-26 | VALID | G6 / [PR-G6-26] H6: SQL imageUrl POST | 10 | 14 | Có: POST /api/products; Bearer T; JSON V[imageUrl]="' OR 1=1 --"; status 200→200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thêm một id và giữ nguyên S; detail P đúng mong đợi; detail id mới đúng body |
| PR-G6-27 | VALID | G6 / [PR-G6-27] H6: SQL imageUrl PUT | 9 | 12 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[imageUrl]="' OR 1=1 --"; status 200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thay đổi P; detail P đúng mong đợi |
| PR-G6-28 | VALID | G6 / [PR-G6-28] H7: name một ký tự, xác nhận identity | 10 | 14 | Có: POST /api/products; Bearer T; JSON V[name]="a"; status 200→200→200→200→200 (GIẢ ĐỊNH); core: list chỉ thêm một id và giữ nguyên S; detail P đúng mong đợi; detail id mới đúng body |
| PR-G6-29 | VALID | G6 / [PR-G6-29] H9: schema list sản phẩm | 9 | 14 | Có: GET /api/products; Bearer T; không body; status 200→200→200→200 (GIẢ ĐỊNH); core: schema list; P đủ field và đúng B; list bằng S; detail P đúng mong đợi |
| PR-G6-30 | VALID | G6 / [PR-G6-30] H10: auth-first POST body rỗng | 9 | 13 | Có: POST /api/products; không Authorization; JSON {}; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-31 | VALID | G6-isolated / [PR-G6-31] H10: auth-first PUT body rỗng | 9 | 13 | Có: PUT /api/products/{{P}}; không Authorization; JSON {}; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi. Nội dung case không đổi, chỉ chuyển folder; chạy riêng một lượt có reset trước (mục 6) |
| PR-G6-32 | VALID | G6 / [PR-G6-32] H5: JWT thiếu dấu phân cách | 9 | 13 | Có: POST /api/products; Authorization: Bearer {{M2}}; JSON V; status 200→401→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-33 | VALID | G6 / [PR-G6-33] H1: name kiểu array | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[name]=["abc"]; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-34 | VALID | G6 / [PR-G6-34] H1: name kiểu boolean | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[name]=true; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-G6-35 | VALID | G6 / [PR-G6-35] H2: price kiểu boolean | 9 | 13 | Có: PUT /api/products/{{P}}; Bearer T; JSON V[price]=true; status 200→400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |

### EX – Extend (6 case: 5 trong folder `EX`, PR-EX-05 trong folder `EX-last`)

| ID | Nhãn audit | Folder trong collection | Request | Assertion | Khớp file? |
|---|---|---|---|---|---|
| PR-EX-01 | EX | EX / [PR-EX-01] ID có dấu `+` không được sửa sản phẩm | 8 | 11 | Có: PUT /api/products/%2B{{P}}; Bearer T; JSON V; status 400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-EX-02 | EX | EX / [PR-EX-02] ID dạng `P.0` không được sửa sản phẩm | 8 | 11 | Có: PUT /api/products/{{P}}.0; Bearer T; JSON V; status 400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-EX-03 | EX | EX / [PR-EX-03] Price vượt giới hạn double phải bị từ chối | 5 | 7 | Có: POST /api/products; Bearer T; JSON B[price]=1e309; status 400→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S |
| PR-EX-04 | EX | EX / [PR-EX-04] Price `-0` phải bị từ chối | 5 | 7 | Có: POST /api/products; Bearer T; JSON B[price]=-0; status 400→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S |
| PR-EX-06 | EX | EX / [PR-EX-06] ID có dấu `+` không được xóa sản phẩm | 8 | 11 | Có: DELETE /api/products/%2B{{P}}; Bearer T; không body; status 400→200→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S; detail P đúng mong đợi |
| PR-EX-05 | EX | EX-last / [PR-EX-05] ID không nguyên không được xóa sản phẩm | 5 | 7 | Có: DELETE /api/products/2.0; Bearer T; không body; status 400→200 (GIẢ ĐỊNH); core: error không rỗng; list bằng S. folder `EX-last`, nằm sau `_smoke`; là case cuối cùng và request cuối cùng của collection; request DELETE có description "chạy cuối vì xóa dữ liệu seed; reset SUT ngay sau case"; setup xác nhận id 2 có trong snapshot |

### Ngoài nguồn (fixture chẩn đoán X0)

| Mục | Folder | Request | Assertion | Ghi chú |
|---|---|---|---|---|
| [SMOKE] GET /api/products | _smoke | 1 | 1 | Không áp dụng "Khớp": fixture chẩn đoán X0, không thuộc tập case nguồn (cùng cách xử lý như API 1). Nằm giữa `EX` và `EX-last`; `scripts/run_newman.sh` chọn từng folder (lượt chính `--folder G1 G2 G3 G4 G6 EX EX-last`, ba lượt riêng chỉ chọn case trong `G6-isolated`) nên `_smoke` không vào báo cáo nào. Test tên `[SMOKE] status 200`, không có `(GIẢ ĐỊNH)` vì không phải case nguồn |

## 2. ID bị bỏ qua (INVALID theo audit)

- PR-G1-04 – INVALID theo audit: false-pass, nhận diện theo name `a` có thể khớp sản phẩm khác; PR-G6-28 thay thế
- PR-G1-22 – INVALID theo audit: trùng D1 với PR-G2-05
- PR-G1-35 – INVALID theo audit: trùng D3 với PR-G2-03
- PR-G1-39 – INVALID theo audit: trùng D5 với PR-G2-08
- PR-G1-40 – INVALID theo audit: trùng D4 với PR-G2-04
- PR-G2-01 – INVALID theo audit: trùng D1 với PR-G2-05
- PR-G2-07 – INVALID theo audit: trùng D2 với PR-G2-14
- PR-G2-09 – INVALID theo audit: trùng D1 với PR-G2-05

Cả 8 ID không có folder trong collection và đều có trong `info.description` ("Bỏ qua INVALID theo audit: …", kèm lý do ngắn).

## 3. Tổng

| Folder | Case | Request | Assertion |
|---|---|---|---|
| G1 | 41 | 208 | 271 |
| G2 | 13 | 104 | 124 |
| G3 | 22 | 257 | 268 |
| G4 | 8 | 64 | 112 |
| G6 | 32 | 295 | 419 |
| G6-isolated | 3 | 27 | 39 |
| EX | 5 | 34 | 47 |
| EX-last | 1 | 5 | 7 |
| **Tổng nguồn** | **125** | **994** | **1287** |
| `_smoke` (ngoài nguồn) | 1 | 1 | 1 |
| **Tổng trong file** | 126 | **995** | **1288** |

Số case chuyển = 125 = 117 VALID + 2 INCOMPLETE + 6 EX. Số ID nguồn = 133 (gồm 8 INVALID không có folder); audit 127 ID = 117 VALID + 2 INCOMPLETE + 8 INVALID. Phân theo nguồn: G1 46−5 INVALID = 41; G2 16−3 = 13; G3 22; G4 8; G6 35 (32 trong `G6` + 3 trong `G6-isolated`); EX 6. Số 125 khớp số folder đếm được từ JSON (41 + 13 + 22 + 8 + 32 + 3 + 5 + 1).

Số assertion là số tĩnh. Riêng PR-G4-07 (33 assertion, 24 request) có thể ít hơn lúc chạy vì `setNextRequest` thoát vòng setup sớm. Tổng nguồn 994 request / 1287 assertion tĩnh không đổi so với trước khi tách. Lượt chính của `scripts/run_newman.sh` chỉ có 967 request / 1248 assertion tĩnh (G1 208 + G2 104 + G3 257 + G4 64 + G6 295 + EX 34 + EX-last 5 request; 271 + 124 + 268 + 112 + 419 + 47 + 7 assertion); 27 request / 39 assertion tĩnh còn lại thuộc ba lượt riêng của `G6-isolated`. Số chạy thực ở lượt chính là 951 request / 1231 assertion, thấp hơn số tĩnh 16 request / 17 assertion vì luồng điều khiển parity của PR-G4-07 (mục 6.5). Mô tả cũ "runner chạy cả 994 request" không còn đúng.

## 4. Kiểm tra cấu trúc

- Pre-request cấp collection: đúng 1 event, đúng 2 dòng, so sánh chuỗi với hai dòng người dùng cung cấp cho kết quả bằng nhau. Không folder hay request nào có `auth` hoặc ghi đè `X-Student-Id` (0 lần xuất hiện ngoài event collection). Không hardcode `localhost` (0 lần); mọi URL dùng `{{baseUrl}}`.
- `pm.sendRequest`: 0. `try/catch`: 0. `skip`: 0. `setTimeout`: 0 (API 3 không có case chờ). `setNextRequest`: 10 lần, chỉ ở PR-G4-07 (vòng lấy id chẵn/lẻ); id đích có trong collection (`GET .../even` và request đầu của PR-G4-08), nên không nhảy tới target không tồn tại; sandbox của Newman 6.2.3 (postman-sandbox) có `pm.execution.setNextRequest`.
- Không có assertion bị nới lỏng. Quét từ khóa `oneOf|within|.or(|\|\||include|satisfy|below|above|match`:
  - `oneOf([200,201])` chỉ ở setup đăng ký user của PR-G3-07..09 (file không quy định status register).
  - `.include` chỉ ở PR-G6-29 (`P đủ field và đúng B`, so từng thuộc tính bằng giá trị).
  - `.satisfy(Number.isInteger)` chỉ ở PR-G4-01 (id integer).
  - `.match` và `.below(2000)` chỉ ở G4, đúng điều kiện Content-Type `application/json` (cho phép charset) và dưới 2000 ms của file.
  - `.above(5)` chỉ ở bước xác định P/Q trong setup (file: dừng nếu P thuộc 1..5).
  - Không có assertion nào chấp nhận hai status.
- Status: mọi `status N` có nhãn `(GIẢ ĐỊNH)` và mã trong tên bằng mã trong `have.status(N)` (script quét, 0 lệch). Chuỗi status của case chính khớp cột Expected status của file cho mọi case ngoài G4 (script) và G4 đã đối chiếu tay (PR-G4-01 200→200→200, 02 200→200, 03 200→404, 04 400→200, 05 400→200, 06 404→200, 07 200→200, 08 200).
- Schema G4: bốn schema S1–S4 nằm nguyên văn (`$schema` draft-07, `exclusiveMinimum: 0` ở S4, `error` string ở S3) trong `pm.response.to.have.jsonSchema`; PR-G6-29 dùng S4 làm `items` của mảng, đúng "mọi phần tử khớp S4". Không bớt field.
- Độ dài chuỗi đo bằng script: PR-G1-05/06/07 = 254/255/256 ký tự (khóa K tính 45 ký tự), PR-G1-29/32 = 10000, PR-G6-04/05 = 255/256 và verify của PR-G6-04 = 255.
- Số nguyên và literal đặc biệt: PR-G1-16 `1000000000000000`, PR-EX-03 `1e309`, PR-EX-04 `-0` ghi nguyên văn trong raw body; đường dẫn `%2B{{P}}`, `{{P}}.0`, `2.0`, `1%20OR%201%3D1` đúng cột Request.
- Dữ liệu độc lập: mỗi folder tự login admin, lấy category, tạo P (và Q nếu cần) với tên chứa `{{$guid}}`; mọi biến `collectionVariables` có tiền tố ID case (script: 0 vi phạm, 0 tham chiếu chéo case).
- G3 tạo user riêng bằng `/api/register` (email theo uuid) cho SEC-06; dùng `userEmail` của environment cho user thường; token giả HS256 tính bằng CryptoJS với secret `wrong-secret-<uuid>`, payload `{"id":1,"role":"admin"}`; token G6 `alg none` ghi `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpZCI6MSwicm9sZSI6ImFkbWluIn0.` (đã giải mã đúng `{"alg":"none","typ":"JWT"}` và `{"id":1,"role":"admin"}`), cộng `not.a.jwt` và `not-a-jwt`.
- INCOMPLETE: PR-G2-16 và PR-G4-07 có description trên folder và trên request nêu phần thiếu hoặc quy tắc thay thế.
- PR-G2-16: bảng nguồn vẫn ghi 200 (giữ để truy vết); collection dùng 400 + error + không đổi theo quy tắc full PUT của G6/G5 và lý do audit "phải sửa expected". Đây là quy ước thay thế do file nêu, không phải nới lỏng.
- Thứ tự folder: G1, G2, G3, G4, G6, `G6-isolated`, EX, `_smoke`, `EX-last`. PR-EX-05 là case cuối cùng và request cuối cùng của collection (và là case cuối của lượt chính); description của request DELETE ghi "chạy cuối vì xóa dữ liệu seed; reset SUT ngay sau case". `G6-isolated` có description: tách riêng vì PUT với price null hoặc thiếu có thể lưu price null và GET detail sau đó làm SUT dừng; reset trước mỗi case.
- Routing trong `scripts/run_newman.sh` (đọc, không sửa) cho API 3: với từng tên trong ba tên folder con đúng nguyên văn (`[PR-G6-09] H2: price null`, `[PR-G6-15] H8: thiếu riêng price`, `[PR-G6-31] H10: auth-first PUT body rỗng`) chạy `scripts/reset_sut.sh` rồi một lần `newman run --folder <tên>` ra `results/newman/23120190_API3_ProductCRUD_isolated-<ID>_<YYYYMMDD>.html` và `.json`, cộng dồn cờ fail; sau cả ba chạy reset rồi lượt chính `--folder G1 G2 G3 G4 G6 EX EX-last` ra `23120190_API3_ProductCRUD_<YYYYMMDD>.html` và `.json` (tên file chính không đổi); cuối cùng reset lần nữa. Ba tên folder trong script khớp ba folder trong `G6-isolated`; folder `G6` không còn ba case này nên không chạy hai lần. Script chỉ ghi file khi người dùng tự chạy; review này không chạy nó.
- `results/newman/` chỉ có `.gitkeep`; review này không tạo file ở đó.

## 5. Kiểm tra mutation ("S không đổi" / "chỉ P đổi")

Mọi case có thay đổi dữ liệu hoặc có khả năng thay đổi đều có kiểm tra theo file. Phân loại lấy từ tên assertion trong collection:

| Kiểu kiểm tra | Assertion trong collection | Case |
|---|---|---|
| Từ chối, list bằng S (so theo id, bỏ qua thứ tự) | `core: list không đổi` / `core: list bằng S` | PR-G1-01..03, 07, 09..13, 17..21, 23..26, 36..38, 41..45; PR-G2-02, 03, 04, 06, 10, 11, 12, 16; PR-G4-04, 05, 06; PR-EX-03, 04, 05 |
| Từ chối, list bằng S và detail P bằng D (hoặc bằng bản trong S) | `core: list bằng S` + `core: detail P đúng mong đợi` | PR-G6-01..03, 05..09, 11..21, 29..35; PR-EX-01, 02, 06 |
| Từ chối hoặc thành công, đối chiếu S gồm P, Q, seed, số lượng N | `core: đối chiếu S và payload` + `core: detail P bằng list` + `core: detail Q bằng list` | PR-G3-01..22 (từ chối: N và mọi id bằng S; thành công: N+1 hoặc chỉ P đổi) |
| POST thành công: đúng một id mới, mọi id cũ không đổi | `core: sản phẩm mới đúng yêu cầu` + `core: sản phẩm cũ không đổi` (+ detail id mới ở G6) | PR-G1-05, 06, 08, 14, 15, 16, 27..33, 46; PR-G2-05, 15; PR-G6-22, 24, 26, 28 |
| PUT thành công: chỉ P đổi | `core: sản phẩm khác không đổi` / `core: list chỉ thay đổi P` + detail P đúng body | PR-G1-34; PR-G2-14 (có thêm Q); PR-G6-04, 10, 23, 25, 27 |
| DELETE thành công: P không còn, id khác bằng S | `core: P đã xóa` + `core: sản phẩm khác không đổi` + GET P 404 | PR-G2-08; PR-G2-13 (list cuối bằng S) |
| Không có snapshot theo file | G4-01, 02, 03, 07, 08 chỉ kiểm response/detail như cột Expected | PR-G4-01, 02, 03, 07, 08 (file không yêu cầu S) |

Ghi nhận: PR-G1-04 (INVALID) không có; thay bằng PR-G6-28 nhận diện bằng delta id thay vì name.

## 6. Runtime (log CLI thật, chỉ để chẩn đoán)

### 6.1 Phạm vi và nguồn

- Reviewer không reset SUT và không chạy Newman. Số liệu dưới đây lấy từ log CLI thật (`--reporters cli`, mỗi lượt có `scripts/reset_sut.sh` trước) do Manager và worker chạy sau khi tách case, model chạy bước cuối `openai-codex/gpt-6-luna`. Log nằm ở artifact phiên làm việc: `product-before-isolation-cli.log` / `-server.log` (trước khi tách), `product-isolate-PR-G6-09-cli.log` / `-server.log` (cùng mẫu cho PR-G6-15 và PR-G6-31), `product-regular-G1-G2-G3-G4-G6-EX-EX-last-cli.log` / `-server.log`, `product-final-server.log`.
- Đây là chẩn đoán kỹ thuật, không phải kết quả chính thức: không có file HTML/JSON, `results/newman/` chỉ có `.gitkeep`. Người dùng cho phép giữ log thật của sự cố này; đây không phải bug report chính thức. Bug report chính thức phải lấy response từ lần chạy chính thức do sinh viên thực hiện.

### 6.2 Chẩn đoán trước khi tách case (PR-G6-09/15/31 còn nằm trong `G6`)

Một lượt liên tục trên collection cũ: 979 request, 77 request lỗi, 1234 assertion (341 fail), 1m24.4s.

- PR-G6-09: `PUT /api/products/121` với `price: null` trả `200 OK` (296B), expected 400. Id 121 là số lẻ nên `GET /api/products/121` vẫn trả `200 OK` (488B); SUT chưa dừng ở case này. Vì vậy nhận định cũ rằng SUT dừng ngay tại PR-G6-09 (lịch sử X3, AI_LOG #31, và suy luận id chẵn của bản review trước) không đúng cho lần chạy này; không dùng lại.
- Lần dừng đầu tiên: PR-G6-31. `PUT /api/products/150` (không Authorization, body `{}`) trả `200 OK` (296B), expected 401; request kế tiếp `GET /api/products/150` báo `[errored] socket hang up`. Log server tại thời điểm đó:

```
/…/eshop-sut/backend/server.js:162
    if (row.id % 2 === 0) row.price = row.price.toString();
TypeError: Cannot read properties of null (reading 'toString')
    at Statement.<anonymous> (…/server.js:162:49)
```

  Sau đó mọi request báo `connect ECONNREFUSED 127.0.0.1:3000`, bắt đầu từ PR-G6-32 (setup login), tới hết lượt. Đó là nguồn của 77 request lỗi.
- Cơ chế (đọc `server.js`): `POST/PUT /api/products` ghi `price` không kiểm tra nên cột nhận null; `GET /api/products/:id` gọi `row.price.toString()` khi `row.id` chẵn, ném TypeError trong callback sqlite, không có handler nên Node dừng. Id lẻ (121) không vào nhánh đó nên sống. Sau reset DB có 5 sản phẩm seed, sản phẩm đầu tiên một case tạo ra có id 6 (chẵn), nên khi chạy riêng cả ba case đều chạm nhánh này.
- Trong cùng log server có một `SyntaxError: Unexpected end of JSON input` từ body-parser: đó là phản hồi cho request JSON sai cú pháp, SUT không dừng vì nó.

### 6.3 Cách chạy hiện tại: bốn lượt độc lập

1. Ba lượt riêng, mỗi lượt reset SUT trước rồi chạy đúng một folder con của `G6-isolated`: PR-G6-09, PR-G6-15, PR-G6-31.
2. Một lượt chính sau reset: G1, G2, G3, G4, G6 (32 case), EX, EX-last.
3. Reset lần cuối (log `product-final-server.log`: khởi động bình thường).

Tên file chính thức khi sinh viên tự chạy: lượt chính `results/newman/23120190_API3_ProductCRUD_<YYYYMMDD>.html/.json`; lượt riêng `results/newman/23120190_API3_ProductCRUD_isolated-PR-G6-09_<YYYYMMDD>.html/.json` (tương tự PR-G6-15, PR-G6-31).

### 6.4 Kết quả log CLI

| Lượt | Request | Request lỗi | Test script lỗi | Pre-request script lỗi | Assertion | Pass | Fail | Thời gian |
|---|---|---|---|---|---|---|---|---|
| Riêng PR-G6-09 | 9 | 1 | 0 / 9 | 0 / 10 | 13 | 8 | 5 | 292 ms |
| Riêng PR-G6-15 | 9 | 1 | 0 / 9 | 0 / 10 | 13 | 8 | 5 | 297 ms |
| Riêng PR-G6-31 | 9 | 1 | 0 / 9 | 0 / 10 | 13 | 8 | 5 | 342 ms |
| Chính (G1, G2, G3, G4, G6, EX, EX-last) | 951 | 0 | 0 / 948 | 0 / 1198 | 1231 | 938 | 293 | 1m 22.1s |
| **Cộng bốn lượt** | **978** | **3** | | | **1270** | **962** | **308** | |

Dòng cộng là tổng của bốn lượt độc lập (951+27, 1231+39, 938+24, 293+15), không phải một lượt chạy duy nhất. Ba request lỗi đều đến từ SUT dừng ở ba lượt riêng.

Ba lượt riêng có cùng mẫu: `PUT` trả `200 OK` (296B) thay vì 400 (PR-G6-09, PR-G6-15) hoặc 401 (PR-G6-31); `GET /api/products/6` xác minh detail báo `[errored] socket hang up`; log server là `TypeError: Cannot read properties of null (reading 'toString')` tại `server.js:162`. Chi tiết PR-G6-09: assertion fail là `status 400`, `core: error không rỗng` (response không có `error`), `core: list bằng S`, `status 200` và `core: detail P đúng mong đợi` của GET detail (không có response); cộng 1 request lỗi `socket hang up`.

Lượt chính: 0 request lỗi, 0 lỗi script, chạy tới PR-G6-32..35 và PR-EX-05 (case cuối) trọn vẹn. Server log chỉ có `SyntaxError` JSON parse của body-parser ứng với request JSON sai cú pháp (theo mapping, case duy nhất gửi raw JSON sai cú pháp là PR-G1-45), không có crash. 293 assertion fail là kết quả test (SUT khác expected hoặc mã status giả định), chưa phân loại ở đây.

### 6.5 Vì sao lượt chính là 951 / 1231, không phải 967 / 1248

Số tĩnh lượt chính là 967 request / 1248 assertion. Chênh 16 request / 17 assertion đến từ PR-G4-07: vòng parity thoát khi đã có id chẵn và lẻ (`setNextRequest`), nên log chỉ chạy 8 trong 24 request và 16 trong 33 assertion của case (đếm trực tiếp từ log: 8 request, 16 assertion). Không thiếu case ở lượt chính.

### 6.6 Bao phủ 125 folder case

- Lượt chính chạy 122 folder case: G1 41, G2 13, G3 22, G4 8, G6 32, EX 5, EX-last 1.
- Ba lượt riêng chạy 3 folder còn lại: PR-G6-09, PR-G6-15, PR-G6-31.
- Hợp lại đủ 125 folder case nguồn, mỗi case đúng một lần, qua bốn lượt chạy.

### 6.7 Kết luận runtime

- "Runtime sạch" chỉ áp cho lượt chính: không request lỗi, không lỗi script, SUT sống tới hết. Không có nghĩa là mọi test pass (293 fail).
- Ba case riêng tái hiện lỗi SUT (price null/thiếu được lưu, rồi GET detail trên id chẵn làm SUT dừng) và vẫn fail. Không khẳng định runtime sạch toàn cục và không khẳng định test all pass.
- Không sửa expected, không bỏ case, không bỏ assertion để lượt riêng pass.
- Hệ quả cho X5: báo cáo/tổng hợp phải gộp JSON của lượt chính và cả 3 JSON lượt riêng; chỉ dùng JSON lượt chính sẽ thiếu 3 case. Số liệu chính thức chỉ lấy từ file do sinh viên chạy `scripts/run_newman.sh`.

## 7. Finding tĩnh cho Manager

Không có dòng "Khớp file? Không". Không cần giao prompt sửa expected, request hay assertion. Các mục dưới đây là quan sát, không chặn:

1. **Rủi ro runtime (mục 6):** đã xử lý bằng cách tách PR-G6-09/15/31 sang `G6-isolated`, mỗi case một lượt có reset trước. Lượt chính chạy hết tới PR-EX-05 không crash; ba lượt riêng vẫn làm SUT dừng ở GET detail và vẫn fail (đúng kỳ vọng, bug SUT). Không phải lỗi collection hay runner; không thấy lỗi trong `scripts/run_newman.sh`.
2. **Tên request xác minh:** ở G3 (3 request mỗi case), G6 (2–3 mỗi case) và EX (1–2 mỗi case), GET xác minh mang tên `[ID] setup: kiểm tra/xác minh …` nhưng chứa assertion `core:`. Tên assertion vẫn đúng quy ước `[ID] core: …`; chỉ tên request mơ hồ trong báo cáo (setup fail hay core fail). Không đổi kết quả. Quy ước X0 chỉ định nghĩa request `setup:` và request chính.
3. **Tên request chính:** G3, G4, G6, EX đặt id biến trong path (`PUT /api/products/{pr_g3_02_p}`), G1 và G2 dùng `{P}`. Chỉ khác về hình thức.
4. **PR-G3-07..09:** setup đăng ký chấp nhận 200 hoặc 201 (file không quy định); `PUT /api/users/me` không có assertion (file: "bất kể response"). Không nới expected của case.
5. **PR-G4-07:** dùng `setNextRequest` để thoát vòng khi đủ id chẵn và lẻ; thiếu parity thì nhảy qua hai GET kiểm tra (file: setup thất bại, không gửi GET). Số assertion thực tế lúc chạy nhỏ hơn 33 (log: 16).
6. **Assertion chặt hơn cột Expected (không phải nới):** `core: sản phẩm mới đúng yêu cầu` ở G1/G2 so mọi field đã gửi (file chỉ nêu name hoặc vài field). Nếu SUT lưu sai field khác, test này fail dù cột Expected chưa nhắc field đó. Giữ nguyên vì chặt hơn không vi phạm quy tắc.
7. **PR-G2-16:** collection theo expected 400 thay thế, bảng nguồn vẫn ghi 200 chỉ để truy vết; sinh viên nên biết khi đọc report.
8. **`_smoke`:** chấp nhận như fixture X0; không đưa vào số liệu nguồn.
9. **Gộp kết quả ở X5:** vì ba case chạy ở file riêng, mọi số liệu tổng (số case, assertion, fail) phải cộng lượt chính và ba lượt riêng; không đọc riêng file chính.

## 8. Đối chiếu "Xong khi"

| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| Mọi ID của file có trong bảng mapping | Đạt | 133 ID: 125 dòng bảng (G1 41, G2 13, G3 22, G4 8, G6 35 gồm 3 dòng `G6-isolated`, EX 6) + 8 INVALID ở mục 2; script đối chiếu lần review đầu: thiếu 0, thừa 0, INVALID có folder 0. Folder và tổng đã đối chiếu lại bằng jq trên collection hiện tại: G6 32 case 295 request 419 assertion; `G6-isolated` 3 case 27 request 39 assertion; tổng nguồn 994 / 1287 |
| Không còn dòng "Khớp file? Không" | Đạt | 0 dòng; chỉ có quan sát ở mục 7, đã báo Manager |
| Không có file mới trong `results/newman/` | Đạt | thư mục chỉ có `.gitkeep`; không có file HTML/JSON, review này không tạo file |
| Runtime sạch (PR-X4 mục 2) | **Đạt có điều kiện, không khẳng định sạch toàn cục** | Lượt chính sạch về kỹ thuật (951 request, 0 lỗi request, 0 lỗi script, tới hết PR-EX-05; 938 pass / 293 fail). Ba lượt riêng tái hiện lỗi SUT (mỗi lượt 1 request lỗi, 5 assertion fail) và vẫn fail. Cộng bốn lượt độc lập: 978 request, 3 request lỗi, 1270 assertion, 962 pass, 308 fail. Chưa phải kết quả chính thức |

Phần tĩnh của "Xong khi" đạt. Phần runtime là chẩn đoán từ log CLI thật, không phải kết quả chính thức, và không được ghi là "sạch toàn cục" hay "all pass".
