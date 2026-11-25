# [BUG][Auth] JWT không có hạn và không bị thu hồi khi đổi mật khẩu hoặc xóa user (BUG-07)

- **ID:** BUG-07 | **API:** `POST /api/login, PUT /api/orders/:id/cancel` | **Test case:** LG-EX-03, CN-EX-02, CN-G3-06
- **Phát hiện bởi:** cả hai
- **Labels:** `type: bug`, `severity: major`, `priority: P2`, `module: auth`, `status: new` _(severity/priority: đề xuất của AI, sinh viên review)_

## Mô tả lỗi
JWT không có hạn và không bị thu hồi khi đổi mật khẩu hoặc xóa user. Vi phạm: README SEC-02: API bảo mật yêu cầu JWT hợp lệ. Token của mật khẩu cũ hoặc của user đã bị xóa không còn hợp lệ.

## Môi trường
- OS: Linux 7.0 (Ubuntu), Node v22.22.1
- SUT: eshop-sut commit `85af3ba`, backend `http://localhost:3000` (reset bằng `scripts/reset_sut.sh`)
- Công cụ: Postman/Newman 6.2.3, curl; header `X-Student-Id: 23120190`
- Tài khoản: user test tự đăng ký trong bước tái hiện; admin seed `admin@eshop.com`
- Ngày chạy: 2026-11-25

## Steps to reproduce
1. `scripts/reset_sut.sh` để seed lại DB.
2. Chạy `./scripts/repro_bugs.sh BUG-07` (hoặc gửi lần lượt các request trong transcript bên dưới bằng Postman/curl).
3. Đọc status và body của request cuối.

## Actual result
Payload JWT chỉ có `{id, role, iat}`, không có `exp`. Sau `reset-password`, token cũ vẫn hủy được đơn (200). Sau khi admin xóa user B, token của B vẫn hủy được đơn (200).

## Expected result
JWT có `exp`. Token cấp trước khi đổi mật khẩu, hoặc của user đã bị xóa, bị từ chối.

Căn cứ: README SEC-02: API bảo mật yêu cầu JWT hợp lệ. Token của mật khẩu cũ hoặc của user đã bị xóa không còn hợp lệ.

## Root cause (tham khảo)
`server.js:51` `jwt.sign` không có `expiresIn`. `server.js:100-110` không kiểm tra user còn tồn tại hay token cấp trước lần đổi mật khẩu.

## Evidence
- Newman: `results/newman/23120190_API2_CancelOrder_20261125.html` (tìm theo test case ID ở trên)
- Transcript curl thật: `evidence/issues/BUG-07_curl.txt`
- Screenshot: _Ảnh chụp Postman: `evidence/issues/BUG-07.png` (sinh viên chụp và đính kèm)._

<details><summary>Transcript tái hiện (nguyên văn, JWT đã che)</summary>

```text
# BUG-07 – transcript tái hiện thật, 2026-11-25 16:29:50 +07, SUT eshop-sut@85af3ba

# Token không có exp, không bị thu hồi khi đổi mật khẩu hoặc xóa user
$ scripts/reset_sut.sh   # SUT seed lại

$ curl -X POST 'http://localhost:3000/api/register' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"name":"Bug User","email":"bug-1795598992132607379@test.com","password":"Test1234!"}'
HTTP 200
{"message":"User registered successfully","id":3}


$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"bug-1795598992132607379@test.com","password":"Test1234!"}'
HTTP 200
{"message":"Login successful","token":"eyJ***(JWT đã che)","user":{"id":3,"name":"Bug User","email":"bug-1795598992132607379@test.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}

=> payload JWT: {"id":3,"role":"user","iat":1795598992}

$ curl -X POST 'http://localhost:3000/api/checkout' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $TOKEN_A' -H 'Content-Type: application/json' -d '{"total_amount":100000,"shipping_address":"HCM"}'
HTTP 200
{"message":"Checkout successful","orderId":1}


$ curl -X POST 'http://localhost:3000/api/forgot-password' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"bug-1795598992132607379@test.com"}'
HTTP 200
{"message":"Mã đặt lại mật khẩu đã được tạo","resetToken":"5509"}


$ curl -X POST 'http://localhost:3000/api/reset-password' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"bug-1795598992132607379@test.com","resetToken":"5509","newPassword":"NewPass123!"}'
HTTP 200
{"message":"Password reset successfully"}


# Token cũ (cấp trước khi đổi mật khẩu) vẫn dùng được

$ curl -X PUT 'http://localhost:3000/api/orders/1/cancel' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $TOKEN_A'
HTTP 200
{"message":"Order canceled successfully"}


# Xóa user B, token của B vẫn hủy được đơn

$ curl -X POST 'http://localhost:3000/api/register' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"name":"Bug User","email":"bug-1795598992273350455@test.com","password":"Test1234!"}'
HTTP 200
{"message":"User registered successfully","id":4}


$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"bug-1795598992273350455@test.com","password":"Test1234!"}'
HTTP 200
{"message":"Login successful","token":"eyJ***(JWT đã che)","user":{"id":4,"name":"Bug User","email":"bug-1795598992273350455@test.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}


$ curl -X POST 'http://localhost:3000/api/checkout' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $TOKEN_B' -H 'Content-Type: application/json' -d '{"total_amount":100000,"shipping_address":"HCM"}'
HTTP 200
{"message":"Checkout successful","orderId":2}


$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"admin@eshop.com","password":"Admin123!"}'
HTTP 200
{"message":"Login successful","token":"eyJ***(JWT đã che)","user":{"id":1,"name":"Admin User","email":"admin@eshop.com","password":"Admin123!","role":"admin","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}


$ curl -X DELETE 'http://localhost:3000/api/admin/users/4' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $ADMIN'
HTTP 200
{"message":"User deleted"}


$ curl -X PUT 'http://localhost:3000/api/orders/2/cancel' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $TOKEN_B'
HTTP 200
{"message":"Order canceled successfully"}
```
</details>
