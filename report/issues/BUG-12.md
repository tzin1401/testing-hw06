# [BUG][Product] Thêm/sửa/xóa sản phẩm không cần đăng nhập hay quyền admin (BUG-12)

- **ID:** BUG-12 | **API:** `POST/PUT/DELETE /api/products[/:id]` | **Test case:** PR-G3-01..PR-G3-12, PR-G6-16..PR-G6-21, PR-G6-30..PR-G6-32
- **Phát hiện bởi:** AI-generated
- **Labels:** `type: bug`, `severity: blocker`, `priority: P0`, `module: product`, `status: new` _(severity/priority: đề xuất của AI, sinh viên review)_

## Mô tả lỗi
Thêm/sửa/xóa sản phẩm không cần đăng nhập hay quyền admin. Vi phạm: README FR-12: POST/PUT/DELETE `/api/products` phải yêu cầu JWT hợp lệ và `role = 'admin'`. SEC-02, SEC-03.

## Môi trường
- OS: Linux 7.0 (Ubuntu), Node v22.22.1
- SUT: eshop-sut commit `85af3ba`, backend `http://localhost:3000` (reset bằng `scripts/reset_sut.sh`)
- Công cụ: Postman/Newman 6.2.3, curl; header `X-Student-Id: 23120190`
- Tài khoản: user test tự đăng ký trong bước tái hiện; admin seed `admin@eshop.com`
- Ngày chạy: 2026-11-25

## Steps to reproduce
1. `scripts/reset_sut.sh` để seed lại DB.
2. Chạy `./scripts/repro_bugs.sh BUG-12` (hoặc gửi lần lượt các request trong transcript bên dưới bằng Postman/curl).
3. Đọc status và body của request cuối.

## Actual result
Không token: POST 200 "Product created", PUT 200, DELETE 200. Token user thường: POST 200, sản phẩm được tạo.

## Expected result
Không token: 401. Token user thường: 403. Dữ liệu không đổi.

Căn cứ: README FR-12: POST/PUT/DELETE `/api/products` phải yêu cầu JWT hợp lệ và `role = 'admin'`. SEC-02, SEC-03.

## Root cause (tham khảo)
`server.js:167`, `179`, `191` không có middleware `authenticateToken` và không kiểm tra role.

## Evidence
- Newman: `results/newman/23120190_API3_ProductCRUD_20261125.html` (tìm theo test case ID ở trên)
- Transcript curl thật: `evidence/issues/BUG-12_curl.txt`
- Screenshot: _Ảnh chụp Postman: `evidence/issues/BUG-12.png` (sinh viên chụp và đính kèm)._

<details><summary>Transcript tái hiện (nguyên văn, JWT đã che)</summary>

```text
# BUG-12 – transcript tái hiện thật, 2026-11-25 16:29:59 +07, SUT eshop-sut@85af3ba

# FR-12/SEC-02/SEC-03: POST/PUT/DELETE /api/products phải cần JWT admin
$ scripts/reset_sut.sh   # SUT seed lại

# Không có token

$ curl -X POST 'http://localhost:3000/api/products' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"name":"No Auth","price":100,"category_id":1}'
HTTP 200
{"message":"Product created","id":6}


$ curl -X PUT 'http://localhost:3000/api/products/6' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"name":"No Auth edited","price":200,"category_id":1}'
HTTP 200
{"message":"Product updated"}


$ curl -X DELETE 'http://localhost:3000/api/products/6' -H 'X-Student-Id: 23120190'
HTTP 200
{"message":"Product deleted"}


# Token user thường

$ curl -X POST 'http://localhost:3000/api/register' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"name":"Bug User","email":"bug-1795599001042759738@test.com","password":"Test1234!"}'
HTTP 200
{"message":"User registered successfully","id":3}


$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"bug-1795599001042759738@test.com","password":"Test1234!"}'
HTTP 200
{"message":"Login successful","token":"eyJ***(JWT đã che)","user":{"id":3,"name":"Bug User","email":"bug-1795599001042759738@test.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}


$ curl -X POST 'http://localhost:3000/api/products' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $TOKEN_A' -H 'Content-Type: application/json' -d '{"name":"User Created","price":100,"category_id":1}'
HTTP 200
{"message":"Product created","id":7}


$ curl -X GET 'http://localhost:3000/api/products/7' -H 'X-Student-Id: 23120190'
HTTP 200
{"id":7,"name":"User Created","price":100,"description":null,"imageUrl":null,"category_id":1}
```
</details>
