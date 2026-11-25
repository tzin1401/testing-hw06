# [BUG][Product] Giá sản phẩm trả về kiểu chuỗi với id chẵn (BUG-16)

- **ID:** BUG-16 | **API:** `GET /api/products/:id` | **Test case:** PR-G4-02, PR-G4-07
- **Phát hiện bởi:** AI-generated
- **Labels:** `type: bug`, `severity: minor`, `priority: P3`, `module: product`, `status: new` _(severity/priority: đề xuất của AI, sinh viên review)_

## Mô tả lỗi
Giá sản phẩm trả về kiểu chuỗi với id chẵn. Vi phạm: README FR-15: giá là số dương. Ví dụ body product trong api_specification.md (A:95, A:124) dùng `price` là số (`100000`).

## Môi trường
- OS: Linux 7.0 (Ubuntu), Node v22.22.1
- SUT: eshop-sut commit `85af3ba`, backend `http://localhost:3000` (reset bằng `scripts/reset_sut.sh`)
- Công cụ: Postman/Newman 6.2.3, curl; header `X-Student-Id: 23120190`
- Tài khoản: user test tự đăng ký trong bước tái hiện; admin seed `admin@eshop.com`
- Ngày chạy: 2026-11-25

## Steps to reproduce
1. `scripts/reset_sut.sh` để seed lại DB.
2. Chạy `./scripts/repro_bugs.sh BUG-16` (hoặc gửi lần lượt các request trong transcript bên dưới bằng Postman/curl).
3. Đọc status và body của request cuối.

## Actual result
`GET /api/products/1` trả `price` kiểu number. `GET /api/products/2` trả `price: "28000000"` kiểu string.

## Expected result
`price` luôn là number.

Căn cứ: README FR-15: giá là số dương. Ví dụ body product trong api_specification.md (A:95, A:124) dùng `price` là số (`100000`).

## Root cause (tham khảo)
`server.js:162` `if (row.id % 2 === 0) row.price = row.price.toString();`.

## Evidence
- Newman: `results/newman/23120190_API3_ProductCRUD_20261125.html` (tìm theo test case ID ở trên)
- Transcript curl thật: `evidence/issues/BUG-16_curl.txt`
- Screenshot: _Ảnh chụp Postman: `evidence/issues/BUG-16.png` (sinh viên chụp và đính kèm)._

<details><summary>Transcript tái hiện (nguyên văn, JWT đã che)</summary>

```text
# BUG-16 – transcript tái hiện thật, 2026-11-25 16:30:06 +07, SUT eshop-sut@85af3ba

# Kiểu price không nhất quán giữa các id
$ scripts/reset_sut.sh   # SUT seed lại

$ curl -X GET 'http://localhost:3000/api/products/1' -H 'X-Student-Id: 23120190'
HTTP 200
{"id":1,"name":"iPhone 15 Pro Max","price":30000000,"description":"Điện thoại cao cấp của Apple","imageUrl":"https://placehold.co/300x300/png?text=iPhone+15","category_id":1}

=> id 1 price type = number

$ curl -X GET 'http://localhost:3000/api/products/2' -H 'X-Student-Id: 23120190'
HTTP 200
{"id":2,"name":"Samsung Galaxy S24 Ultra","price":"28000000","description":"Màn hình hiển thị xuất sắc, camera siêu zoom","imageUrl":"https://placehold.co/300x300/png?text=Samsung+S24","category_id":1}

=> id 2 price type = string
```
</details>
