# [BUG][Product] GET chi tiết sản phẩm làm sập server khi price null (BUG-14)

- **ID:** BUG-14 | **API:** `GET /api/products/:id (sau PUT/POST /api/products)` | **Test case:** PR-G6-09, PR-G6-15, PR-G6-31
- **Phát hiện bởi:** AI-generated
- **Labels:** `type: bug`, `severity: blocker`, `priority: P0`, `module: product`, `status: new` _(severity/priority: đề xuất của AI, sinh viên review)_

## Mô tả lỗi
GET chi tiết sản phẩm làm sập server khi price null. Vi phạm: README FR-15: giá bắt buộc là số dương. Server không được dừng vì dữ liệu đầu vào.

## Môi trường
- OS: Linux 7.0 (Ubuntu), Node v22.22.1
- SUT: eshop-sut commit `85af3ba`, backend `http://localhost:3000` (reset bằng `scripts/reset_sut.sh`)
- Công cụ: Postman/Newman 6.2.3, curl; header `X-Student-Id: 23120190`
- Tài khoản: user test tự đăng ký trong bước tái hiện; admin seed `admin@eshop.com`
- Ngày chạy: 2026-11-25

## Steps to reproduce
1. `scripts/reset_sut.sh` để seed lại DB.
2. Chạy `./scripts/repro_bugs.sh BUG-14` (hoặc gửi lần lượt các request trong transcript bên dưới bằng Postman/curl).
3. Đọc status và body của request cuối.

## Actual result
PUT `price: null` lên sản phẩm id 2 trả 200. Sau đó `GET /api/products/2` không có response (curl HTTP 000), mọi request tiếp theo đều thất bại. Log server: `TypeError: Cannot read properties of null (reading 'toString')`, process thoát.

## Expected result
PUT với `price: null` bị từ chối (400). Nếu dữ liệu đã lỗi, GET vẫn trả response, server tiếp tục chạy.

Căn cứ: README FR-15: giá bắt buộc là số dương. Server không được dừng vì dữ liệu đầu vào.

## Root cause (tham khảo)
`server.js:162` gọi `row.price.toString()` cho id chẵn mà không kiểm tra null; kết hợp BUG-13 (không validate price).

## Evidence
- Newman: `results/newman/23120190_API3_ProductCRUD_20261125.html` (tìm theo test case ID ở trên)
- Transcript curl thật: `evidence/issues/BUG-14_curl.txt`
- Screenshot: _Ảnh chụp Postman: `evidence/issues/BUG-14.png` (sinh viên chụp và đính kèm)._

<details><summary>Transcript tái hiện (nguyên văn, JWT đã che)</summary>

```text
# BUG-14 – transcript tái hiện thật, 2026-11-25 16:30:02 +07, SUT eshop-sut@85af3ba

# GET detail làm sập server khi price null
$ scripts/reset_sut.sh   # SUT seed lại

$ curl -X PUT 'http://localhost:3000/api/products/2' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"name":"Price null","price":null,"category_id":1}'
HTTP 200
{"message":"Product updated"}


$ curl -X GET 'http://localhost:3000/api/products/2' -H 'X-Student-Id: 23120190'
HTTP 000



$ curl -X GET 'http://localhost:3000/api/products' -H 'X-Student-Id: 23120190'
HTTP 000



# Log server
                                                ^

TypeError: Cannot read properties of null (reading 'toString')
    at Statement.<anonymous> (/home/zinn/zinn/testing/hw06/eshop-sut/backend/server.js:162:49)
    at Statement.replacement (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/sqlite3/lib/trace.js:25:27)
    at Statement.replacement (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/sqlite3/lib/trace.js:25:27)

Node.js v22.22.1
```
</details>
