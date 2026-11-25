# [BUG][Order] User hủy được đơn đang shipping (BUG-09)

- **ID:** BUG-09 | **API:** `PUT /api/orders/:id/cancel` | **Test case:** CN-G2-03
- **Phát hiện bởi:** AI-generated
- **Labels:** `type: bug`, `severity: critical`, `priority: P1`, `module: order`, `status: new` _(severity/priority: đề xuất của AI, sinh viên review)_

## Mô tả lỗi
User hủy được đơn đang shipping. Vi phạm: README FR-10: "Khi đơn hàng đã ở trạng thái shipping, User không được phép tự hủy". R:236: chỉ được hủy khi `pending` hoặc `confirmed`.

## Môi trường
- OS: Linux 7.0 (Ubuntu), Node v22.22.1
- SUT: eshop-sut commit `85af3ba`, backend `http://localhost:3000` (reset bằng `scripts/reset_sut.sh`)
- Công cụ: Postman/Newman 6.2.3, curl; header `X-Student-Id: 23120190`
- Tài khoản: user test tự đăng ký trong bước tái hiện; admin seed `admin@eshop.com`
- Ngày chạy: 2026-11-25

## Steps to reproduce
1. `scripts/reset_sut.sh` để seed lại DB.
2. Chạy `./scripts/repro_bugs.sh BUG-09` (hoặc gửi lần lượt các request trong transcript bên dưới bằng Postman/curl).
3. Đọc status và body của request cuối.

## Actual result
HTTP 200 "Order canceled successfully". GET đơn trả `status: canceled`.

## Expected result
Trả lỗi 4xx, đơn giữ trạng thái `shipping`.

Căn cứ: README FR-10: "Khi đơn hàng đã ở trạng thái shipping, User không được phép tự hủy". R:236: chỉ được hủy khi `pending` hoặc `confirmed`.

## Root cause (tham khảo)
`server.js:329` chỉ chặn `delivered`/`canceled` (chính code có comment ghi điều kiện đúng là `pending`/`confirmed`).

## Evidence
- Newman: `results/newman/23120190_API2_CancelOrder_20261125.html` (tìm theo test case ID ở trên)
- Transcript curl thật: `evidence/issues/BUG-09_curl.txt`
- Screenshot: _Ảnh chụp Postman: `evidence/issues/BUG-09.png` (sinh viên chụp và đính kèm)._

<details><summary>Transcript tái hiện (nguyên văn, JWT đã che)</summary>

```text
# BUG-09 – transcript tái hiện thật, 2026-11-25 16:30:14 +07, SUT eshop-sut@85af3ba

# FR-10: đơn shipping user không được tự hủy
$ scripts/reset_sut.sh   # SUT seed lại

$ curl -X POST 'http://localhost:3000/api/register' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"name":"Bug User","email":"bug-1795599016096072893@test.com","password":"Test1234!"}'
HTTP 200
{"message":"User registered successfully","id":3}


$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"bug-1795599016096072893@test.com","password":"Test1234!"}'
HTTP 200
{"message":"Login successful","token":"eyJ***(JWT đã che)","user":{"id":3,"name":"Bug User","email":"bug-1795599016096072893@test.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}


$ curl -X POST 'http://localhost:3000/api/checkout' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $TOKEN_A' -H 'Content-Type: application/json' -d '{"total_amount":100000,"shipping_address":"HCM"}'
HTTP 200
{"message":"Checkout successful","orderId":1}


$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"admin@eshop.com","password":"Admin123!"}'
HTTP 200
{"message":"Login successful","token":"eyJ***(JWT đã che)","user":{"id":1,"name":"Admin User","email":"admin@eshop.com","password":"Admin123!","role":"admin","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}


$ curl -X PUT 'http://localhost:3000/api/admin/orders/1/status' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $ADMIN' -H 'Content-Type: application/json' -d '{"status":"confirmed"}'
HTTP 200
{"message":"Order status updated"}


$ curl -X PUT 'http://localhost:3000/api/admin/orders/1/status' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $ADMIN' -H 'Content-Type: application/json' -d '{"status":"shipping"}'
HTTP 200
{"message":"Order status updated"}


$ curl -X PUT 'http://localhost:3000/api/orders/1/cancel' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $TOKEN_A'
HTTP 200
{"message":"Order canceled successfully"}


$ curl -X GET 'http://localhost:3000/api/orders/1' -H 'X-Student-Id: 23120190'
HTTP 200
{"id":1,"user_id":3,"total_amount":100000,"status":"canceled","shipping_address":"HCM","created_at":"2026-11-25 09:30:16"}

=> status = canceled (expected shipping)
```
</details>
