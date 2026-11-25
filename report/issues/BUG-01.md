# [BUG][Login] Mỗi lần đăng nhập sai tăng bộ đếm 2 thay vì 1 (BUG-01)

- **ID:** BUG-01 | **API:** `POST /api/login` | **Test case:** LG-G2-01, LG-G2-04, LG-G2-05, LG-G2-06, LG-G2-08, LG-EX-02
- **Phát hiện bởi:** cả hai
- **Labels:** `type: bug`, `severity: major`, `priority: P1`, `module: login`, `status: new` _(severity/priority: đề xuất của AI, sinh viên review)_

## Mô tả lỗi
Mỗi lần đăng nhập sai tăng bộ đếm 2 thay vì 1. Vi phạm: README FR-02 (R:41): "Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên đúng 1 đơn vị."

## Môi trường
- OS: Linux 7.0 (Ubuntu), Node v22.22.1
- SUT: eshop-sut commit `85af3ba`, backend `http://localhost:3000` (reset bằng `scripts/reset_sut.sh`)
- Công cụ: Postman/Newman 6.2.3, curl; header `X-Student-Id: 23120190`
- Tài khoản: user test tự đăng ký trong bước tái hiện; admin seed `admin@eshop.com`
- Ngày chạy: 2026-11-25

## Steps to reproduce
1. `scripts/reset_sut.sh` để seed lại DB.
2. Chạy `./scripts/repro_bugs.sh BUG-01` (hoặc gửi lần lượt các request trong transcript bên dưới bằng Postman/curl).
3. Đọc status và body của request cuối.

## Actual result
Sau MỘT lần sai, `GET /api/users/me` trả `login_attempts: 2`. Lần sai thứ hai đã khóa tài khoản.

## Expected result
Sau một lần sai, `login_attempts = 1`. Tài khoản chỉ bị khóa sau 3 lần sai liên tiếp.

Căn cứ: README FR-02 (R:41): "Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên đúng 1 đơn vị."

## Root cause (tham khảo)
`server.js:54` dùng `user.login_attempts + 2`.

## Evidence
- Newman: `results/newman/23120190_API1_Login_20261125.html` (tìm theo test case ID ở trên)
- Transcript curl thật: `evidence/issues/BUG-01_curl.txt`
- Screenshot: ![BUG-01](../../evidence/issues/BUG-01.png)

<details><summary>Transcript tái hiện (nguyên văn, JWT đã che)</summary>

```text
# BUG-01 – transcript tái hiện thật, 2026-11-25 16:29:07 +07, SUT eshop-sut@85af3ba

# FR-02: mỗi lần sai phải tăng bộ đếm đúng 1
$ scripts/reset_sut.sh   # SUT seed lại

$ curl -X POST 'http://localhost:3000/api/register' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"name":"Bug User","email":"bug-1795598949965596729@test.com","password":"Test1234!"}'
HTTP 200
{"message":"User registered successfully","id":3}


$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"bug-1795598949965596729@test.com","password":"Test1234!"}'
HTTP 200
{"message":"Login successful","token":"eyJ***(JWT đã che)","user":{"id":3,"name":"Bug User","email":"bug-1795598949965596729@test.com","password":"Test1234!","role":"user","login_attempts":0,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}}


$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: application/json' -d '{"email":"bug-1795598949965596729@test.com","password":"Sai12345!"}'
HTTP 401
{"error":"Invalid email or password"}


# Đọc bộ đếm sau MỘT lần sai

$ curl -X GET 'http://localhost:3000/api/users/me' -H 'X-Student-Id: 23120190' -H 'Authorization: Bearer $TOKEN_A'
HTTP 200
{"id":3,"name":"Bug User","email":"bug-1795598949965596729@test.com","password":"Test1234!","role":"user","login_attempts":2,"locked_until":null,"reset_token":null,"shipping_address":null,"phone":null}

=> login_attempts = 2 (expected 1)
```
</details>
