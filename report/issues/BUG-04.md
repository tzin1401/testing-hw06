# [BUG][Login] Body không phải JSON gây lỗi 500 và lộ stack trace (BUG-04)

- **ID:** BUG-04 | **API:** `POST /api/login` | **Test case:** LG-G1-24
- **Phát hiện bởi:** AI-generated
- **Labels:** `type: bug`, `severity: minor`, `priority: P2`, `module: login`, `status: new` _(severity/priority: đề xuất của AI, sinh viên review)_

## Mô tả lỗi
Body không phải JSON gây lỗi 500 và lộ stack trace. Vi phạm: README FR-02 (R:42): thông báo lỗi phù hợp, không để lộ chi tiết.

## Môi trường
- OS: Linux 7.0 (Ubuntu), Node v22.22.1
- SUT: eshop-sut commit `85af3ba`, backend `http://localhost:3000` (reset bằng `scripts/reset_sut.sh`)
- Công cụ: Postman/Newman 6.2.3, curl; header `X-Student-Id: 23120190`
- Tài khoản: user test tự đăng ký trong bước tái hiện; admin seed `admin@eshop.com`
- Ngày chạy: 2026-11-25

## Steps to reproduce
1. `scripts/reset_sut.sh` để seed lại DB.
2. Chạy `./scripts/repro_bugs.sh BUG-04` (hoặc gửi lần lượt các request trong transcript bên dưới bằng Postman/curl).
3. Đọc status và body của request cuối.

## Actual result
HTTP 500, trang HTML có `TypeError: Cannot destructure property 'email' of 'req.body'` kèm đường dẫn file và stack trace của server.

## Expected result
Trả 4xx (ví dụ 400/415) với JSON lỗi ngắn gọn.

Căn cứ: README FR-02 (R:42): thông báo lỗi phù hợp, không để lộ chi tiết.

## Root cause (tham khảo)
`server.js:33` destructure `req.body` mà không kiểm tra; Express trả stack trace mặc định.

## Evidence
- Newman: `results/newman/23120190_API1_Login_20261125.html` (tìm theo test case ID ở trên)
- Transcript curl thật: `evidence/issues/BUG-04_curl.txt`
- Screenshot: _Ảnh chụp Postman: `evidence/issues/BUG-04.png` (sinh viên chụp và đính kèm)._

<details><summary>Transcript tái hiện (nguyên văn, JWT đã che)</summary>

```text
# BUG-04 – transcript tái hiện thật, 2026-11-25 16:29:45 +07, SUT eshop-sut@85af3ba

# Content-Type không phải JSON
$ scripts/reset_sut.sh   # SUT seed lại

$ curl -X POST 'http://localhost:3000/api/login' -H 'X-Student-Id: 23120190' -H 'Content-Type: text/plain' -d '{"email":"test@eshop.com","password":"Test1234!"}'
HTTP 500
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>TypeError: Cannot destructure property &#39;email&#39; of &#39;req.body&#39; as it is undefined.<br> &nbsp; &nbsp;at /home/zinn/zinn/testing/hw06/eshop-sut/backend/server.js:33:11<br> &nbsp; &nbsp;at Layer.handleRequest (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/router/lib/layer.js:152:17)<br> &nbsp; &nbsp;at next (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/router/lib/route.js:157:13)<br> &nbsp; &nbsp;at Route.dispatch (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/router/lib/route.js:117:3)<br> &nbsp; &nbsp;at handle (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/router/index.js:435:11)<br> &nbsp; &nbsp;at Layer.handleRequest (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/router/lib/layer.js:152:17)<br> &nbsp; &nbsp;at /home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/router/index.js:295:15<br> &nbsp; &nbsp;at processParams (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/router/index.js:582:12)<br> &nbsp; &nbsp;at next (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/router/index.js:291:5)<br> &nbsp; &nbsp;at read (/home/zinn/zinn/testing/hw06/eshop-sut/backend/node_modules/body-parser/lib/read.js:62:5)</pre>
</body>
</html>
```
</details>
