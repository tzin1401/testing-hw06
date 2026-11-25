#!/usr/bin/env python3
"""Sinh report/issues/BUG-xx.md và report/bug_report.md từ bảng BUGS + transcript thật evidence/issues/BUG-xx_curl.txt."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/tzin1401/testing-hw06/blob/main"
N1, N2, N3 = (f"results/newman/23120190_{x}_20261125.html" for x in ("API1_Login", "API2_CancelOrder", "API3_ProductCRUD"))

# id, module, title, api, cases, found_by, severity, priority, spec, expected, actual, root, newman
BUGS = [
 ("01", "Login", "Mỗi lần đăng nhập sai tăng bộ đếm 2 thay vì 1", "POST /api/login",
  "LG-G2-01, LG-G2-04, LG-G2-05, LG-G2-06, LG-G2-08, LG-EX-02", "cả hai", "major", "P1",
  "README FR-02 (R:41): \"Sau mỗi lần đăng nhập sai, hệ thống tăng bộ đếm lên đúng 1 đơn vị.\"",
  "Sau một lần sai, `login_attempts = 1`. Tài khoản chỉ bị khóa sau 3 lần sai liên tiếp.",
  "Sau MỘT lần sai, `GET /api/users/me` trả `login_attempts: 2`. Lần sai thứ hai đã khóa tài khoản.",
  "`server.js:54` dùng `user.login_attempts + 2`.", N1),
 ("02", "Login", "Tài khoản bị khóa 180 giây thay vì 30 giây", "POST /api/login",
  "LG-G2-07, LG-G2-11, LG-G3-09, LG-G6-03", "AI-generated", "major", "P1",
  "README FR-02 (R:42): sai từ 3 lần liên tiếp thì tạm khóa 30 giây.",
  "Sau 30 giây, đăng nhập đúng mật khẩu thành công (200 + JWT).",
  "`locked_until` = thời điểm khóa + 180 giây. Login đúng sau 31 giây vẫn trả 403 \"Tài khoản đã bị khóa\".",
  "`server.js:57` đặt `Date.now() + 180000`.", N1),
 ("03", "Login", "Response login trả về mật khẩu dạng plaintext", "POST /api/login",
  "LG-G4-01, LG-G4-02, LG-G4-03, LG-G4-07", "AI-generated", "critical", "P0",
  "README SEC-01: mật khẩu không được lưu dạng plaintext. FR-02 chỉ yêu cầu trả JWT, không yêu cầu trả thông tin nhạy cảm.",
  "Response không chứa `password` (cũng không chứa `reset_token`, `login_attempts`).",
  "`user.password` trong response là đúng mật khẩu người dùng vừa nhập (`Test1234!`). Mật khẩu được lưu và so sánh dạng plaintext.",
  "`server.js:46` so sánh `user.password === password` (plaintext). `server.js:52` trả nguyên object `user` từ DB.", N1),
 ("04", "Login", "Body không phải JSON gây lỗi 500 và lộ stack trace", "POST /api/login",
  "LG-G1-24", "AI-generated", "minor", "P2",
  "README FR-02 (R:42): thông báo lỗi phù hợp, không để lộ chi tiết.",
  "Trả 4xx (ví dụ 400/415) với JSON lỗi ngắn gọn.",
  "HTTP 500, trang HTML có `TypeError: Cannot destructure property 'email' of 'req.body'` kèm đường dẫn file và stack trace của server.",
  "`server.js:33` destructure `req.body` mà không kiểm tra; Express trả stack trace mặc định.", N1),
 ("05", "Login", "Thông báo khóa tiết lộ email nào đã đăng ký", "POST /api/login",
  "LG-G6-03", "AI-generated", "minor", "P3",
  "README FR-02 (R:42): \"Hệ thống trả về thông báo lỗi phù hợp; không để lộ chi tiết nguyên nhân.\"",
  "Cùng một input sai, email tồn tại và email không tồn tại nhận phản hồi giống nhau.",
  "Email đã đăng ký (sau khi sai) nhận 403 \"Tài khoản đã bị khóa\". Email không tồn tại nhận 401 \"Invalid email or password\". Kẻ tấn công dò được email hợp lệ.",
  "`server.js:37-43`: kiểm tra khóa chỉ chạy khi email tồn tại.", N1),
 ("06", "Auth", "JWT ký bằng secret hardcode, token tự ký được chấp nhận", "POST /api/login, PUT /api/orders/:id/cancel",
  "LG-EX-05, CN-EX-05", "Human Extend (AI bỏ sót)", "critical", "P0",
  "README SEC-02: các API bảo mật phải yêu cầu JWT hợp lệ. FR-12: thao tác admin cần `role = 'admin'` trong token.",
  "Token không do server cấp bị từ chối (401). Secret không nằm trong source.",
  "Token tự ký bằng secret đọc từ source với payload `{id:1, role:\"admin\"}` được chấp nhận: `GET /api/users/me` trả 200 với dữ liệu admin. Token tự ký cho user A hủy được đơn của A.",
  "`server.js:9` `const SECRET_KEY = \"super_secret_key_that_should_not_be_here\"`.", N1),
 ("07", "Auth", "JWT không có hạn và không bị thu hồi khi đổi mật khẩu hoặc xóa user", "POST /api/login, PUT /api/orders/:id/cancel",
  "LG-EX-03, CN-EX-02, CN-G3-06", "cả hai", "major", "P2",
  "README SEC-02: API bảo mật yêu cầu JWT hợp lệ. Token của mật khẩu cũ hoặc của user đã bị xóa không còn hợp lệ.",
  "JWT có `exp`. Token cấp trước khi đổi mật khẩu, hoặc của user đã bị xóa, bị từ chối.",
  "Payload JWT chỉ có `{id, role, iat}`, không có `exp`. Sau `reset-password`, token cũ vẫn hủy được đơn (200). Sau khi admin xóa user B, token của B vẫn hủy được đơn (200).",
  "`server.js:51` `jwt.sign` không có `expiresIn`. `server.js:100-110` không kiểm tra user còn tồn tại hay token cấp trước lần đổi mật khẩu.", N2),
 ("08", "Auth", "Header Authorization scheme Basic vẫn được chấp nhận", "PUT /api/orders/:id/cancel",
  "CN-G1-13", "AI-generated", "minor", "P3",
  "README FR-02 (R:43): token gửi qua header `Authorization: Bearer <token>`.",
  "Scheme khác `Bearer` bị từ chối (401).",
  "`Authorization: Basic <jwt>` vẫn hủy được đơn (200, đơn chuyển `canceled`).",
  "`server.js:102` lấy `split(\" \")[1]` mà không kiểm tra phần đầu là `Bearer`.", N2),
 ("09", "Order", "User hủy được đơn đang shipping", "PUT /api/orders/:id/cancel",
  "CN-G2-03", "AI-generated", "critical", "P1",
  "README FR-10: \"Khi đơn hàng đã ở trạng thái shipping, User không được phép tự hủy\". R:236: chỉ được hủy khi `pending` hoặc `confirmed`.",
  "Trả lỗi 4xx, đơn giữ trạng thái `shipping`.",
  "HTTP 200 \"Order canceled successfully\". GET đơn trả `status: canceled`.",
  "`server.js:329` chỉ chặn `delivered`/`canceled` (chính code có comment ghi điều kiện đúng là `pending`/`confirmed`).", N2),
 ("10", "Order", "Admin chuyển được đơn canceled sang delivered", "PUT /api/admin/orders/:id/status",
  "CN-G2-10", "AI-generated", "major", "P1",
  "README FR-10: `delivered` và `canceled` là trạng thái kết thúc, không được chuyển sang trạng thái khác.",
  "HTTP 400 \"Invalid state transition\", đơn giữ `canceled`.",
  "HTTP 200 \"Order status updated\". GET đơn trả `status: delivered`.",
  "`server.js:550` cho phép `canceled → delivered`.", N2),
 ("11", "Order/Product", "Path id dạng +1, 2.0, 03 vẫn khớp bản ghi", "PUT /api/orders/:id/cancel, DELETE/PUT /api/products/:id",
  "CN-EX-01, CN-EX-03, CN-EX-04, PR-EX-01, PR-EX-02, PR-EX-05, PR-EX-06", "Human Extend (AI bỏ sót)", "minor", "P3",
  "Spec dùng `:id` là mã định danh của đơn/sản phẩm (A:90, A:146). Không quy định ép kiểu; nhiều chuỗi khác nhau trỏ cùng một bản ghi là hành vi không mong muốn (đề xuất: chỉ chấp nhận số nguyên dương dạng chuẩn).",
  "`+1`, `2.0`, `03` bị từ chối (400 hoặc 404), dữ liệu không đổi.",
  "`PUT /api/orders/%2B1/cancel`, `/2.0/cancel`, `/03/cancel` đều 200 và đơn bị hủy. `DELETE /api/products/2.0` xóa sản phẩm id 2.",
  "`server.js:323`, `181`, `192` truyền thẳng `req.params.id` (chuỗi) vào SQLite; type affinity của cột INTEGER ép `'2.0'`, `'+1'`, `'03'` thành số.", N2),
 ("12", "Product", "Thêm/sửa/xóa sản phẩm không cần đăng nhập hay quyền admin", "POST/PUT/DELETE /api/products[/:id]",
  "PR-G3-01..PR-G3-12, PR-G6-16..PR-G6-21, PR-G6-30..PR-G6-32", "AI-generated", "blocker", "P0",
  "README FR-12: POST/PUT/DELETE `/api/products` phải yêu cầu JWT hợp lệ và `role = 'admin'`. SEC-02, SEC-03.",
  "Không token: 401. Token user thường: 403. Dữ liệu không đổi.",
  "Không token: POST 200 \"Product created\", PUT 200, DELETE 200. Token user thường: POST 200, sản phẩm được tạo.",
  "`server.js:167`, `179`, `191` không có middleware `authenticateToken` và không kiểm tra role.", N3),
 ("13", "Product", "Không validate name/price/category khi thêm và sửa sản phẩm", "POST /api/products, PUT /api/products/:id",
  "PR-G1-*, PR-G2-16, PR-G4-04, PR-G4-05, PR-G6-01..PR-G6-15, PR-EX-03, PR-EX-04", "cả hai", "major", "P1",
  "README FR-15: tên bắt buộc, tối đa 255 ký tự; giá bắt buộc, số dương (> 0); danh mục bắt buộc, phải chọn từ danh sách có sẵn.",
  "Trả 400 với thông báo lỗi, không tạo hoặc sửa sản phẩm.",
  "Thiếu name, price = -5, 0, -0, 1e309, category_id = 9999 đều trả 200 \"Product created\". `PUT` chỉ gửi `name` ghi đè `price`, `description`, `imageUrl`, `category_id` thành `null`.",
  "`server.js:167-189` chèn/cập nhật thẳng giá trị từ body, không có validation; PUT cập nhật mọi cột kể cả cột không gửi.", N3),
 ("14", "Product", "GET chi tiết sản phẩm làm sập server khi price null", "GET /api/products/:id (sau PUT/POST /api/products)",
  "PR-G6-09, PR-G6-15, PR-G6-31", "AI-generated", "blocker", "P0",
  "README FR-15: giá bắt buộc là số dương. Server không được dừng vì dữ liệu đầu vào.",
  "PUT với `price: null` bị từ chối (400). Nếu dữ liệu đã lỗi, GET vẫn trả response, server tiếp tục chạy.",
  "PUT `price: null` lên sản phẩm id 2 trả 200. Sau đó `GET /api/products/2` không có response (curl HTTP 000), mọi request tiếp theo đều thất bại. Log server: `TypeError: Cannot read properties of null (reading 'toString')`, process thoát.",
  "`server.js:162` gọi `row.price.toString()` cho id chẵn mà không kiểm tra null; kết hợp BUG-13 (không validate price).", N3),
 ("15", "Profile", "User thường tự nâng quyền admin qua API cập nhật hồ sơ", "PUT /api/users/me",
  "PR-G3-07, PR-G3-08, PR-G3-09", "AI-generated", "critical", "P0",
  "README SEC-06: \"API cập nhật hồ sơ không được cho phép thay đổi trường role từ client.\"",
  "Trường `role` bị bỏ qua hoặc bị từ chối; role giữ `user`.",
  "`PUT /api/users/me` với `{\"role\":\"admin\"}` trả 200. `GET /api/users/me` và lần login sau đều trả `role: admin`.",
  "`server.js:118-128` thêm `role = ?` vào câu UPDATE khi body có `role`.", N3),
 ("16", "Product", "Giá sản phẩm trả về kiểu chuỗi với id chẵn", "GET /api/products/:id",
  "PR-G4-02, PR-G4-07", "AI-generated", "minor", "P3",
  "README FR-15: giá là số dương. Ví dụ body product trong api_specification.md (A:95, A:124) dùng `price` là số (`100000`).",
  "`price` luôn là number.",
  "`GET /api/products/1` trả `price` kiểu number. `GET /api/products/2` trả `price: \"28000000\"` kiểu string.",
  "`server.js:162` `if (row.id % 2 === 0) row.price = row.price.toString();`.", N3),
]

MOD_LABEL = {"Login": "login", "Auth": "auth", "Order": "order", "Order/Product": "order", "Product": "product", "Profile": "profile"}

def labels(b):
    ls = ["type: bug", f"severity: {b[6]}", f"priority: {b[7]}", f"module: {MOD_LABEL[b[1]]}", "status: new"]
    if b[1] == "Order/Product": ls.append("module: product")
    if "Human" in b[5]: ls.append("found-by: human-extend")
    return ls

ENV = ("- OS: Linux 7.0 (Ubuntu), Node v22.22.1\n- SUT: eshop-sut commit `85af3ba`, backend `http://localhost:3000` (reset bằng `scripts/reset_sut.sh`)\n"
       "- Công cụ: Postman/Newman 6.2.3, curl; header `X-Student-Id: 23120190`\n- Tài khoản: user test tự đăng ký trong bước tái hiện; admin seed `admin@eshop.com`\n- Ngày chạy: 2026-11-25")

def body(b, issue_mode=False):
    i, mod, title, api, cases, found, sev, pri, spec, exp, act, root, newman = b
    bid = f"BUG-{i}"
    tr = (ROOT / f"evidence/issues/{bid}_curl.txt").read_text()
    steps = "\n".join(f"{n}. {s}" for n, s in enumerate(
        ["`scripts/reset_sut.sh` để seed lại DB.",
         f"Chạy `./scripts/repro_bugs.sh {bid}` (hoặc gửi lần lượt các request trong transcript bên dưới bằng Postman/curl).",
         "Đọc status và body của request cuối."], 1))
    link = (lambda p: f"[{p}]({REPO}/{p})") if issue_mode else (lambda p: f"`{p}`")
    has_png = (ROOT / f"evidence/issues/{bid}.png").exists()
    shot = (f"_Ảnh chụp Postman: `evidence/issues/{bid}.png` (sinh viên chụp và đính kèm)._" if not has_png
            else f"![{bid}](https://raw.githubusercontent.com/tzin1401/testing-hw06/main/evidence/issues/{bid}.png)" if issue_mode
            else f"![{bid}](../../evidence/issues/{bid}.png)")
    return f"""- **ID:** {bid} | **API:** `{api}` | **Test case:** {cases}
- **Phát hiện bởi:** {found}
- **Labels:** {", ".join(f"`{l}`" for l in labels(b))} _(severity/priority: đề xuất của AI, sinh viên review)_

## Mô tả lỗi
{title}. Vi phạm: {spec}

## Môi trường
{ENV}

## Steps to reproduce
{steps}

## Actual result
{act}

## Expected result
{exp}

Căn cứ: {spec}

## Root cause (tham khảo)
{root}

## Evidence
- Newman: {link(newman)} (tìm theo test case ID ở trên)
- Transcript curl thật: {link(f"evidence/issues/{bid}_curl.txt")}
- Screenshot: {shot}

<details><summary>Transcript tái hiện (nguyên văn, JWT đã che)</summary>

```text
{tr.rstrip()}
```
</details>
"""

def issue_title(b): return f"[BUG][{b[1]}] {b[2]} (BUG-{b[0]})"

import sys
if __name__ == "__main__":
    import json, sys
    out = ROOT / "report/issues"
    for b in BUGS:
        (out / f"BUG-{b[0]}.md").write_text(f"# {issue_title(b)}\n\n" + body(b))
    if len(sys.argv) > 1 and sys.argv[1] == "--issues":  # in JSON cho bước tạo GitHub Issue
        print(json.dumps([{"id": f"BUG-{b[0]}", "title": issue_title(b), "labels": labels(b), "body": body(b, True)} for b in BUGS], ensure_ascii=False))

TRIAGE = {"01": "a: BUG-LG-01", "02": "a: BUG-LG-01", "03": "a: BUG-LG-02", "04": "b: LG-03", "05": "b: LG-08",
          "06": "a: BUG-LG-03", "07": "b: LG-09, CN-04, CN-07", "08": "a: BUG-CN-01", "09": "a: BUG-CN-02",
          "10": "a: BUG-CN-03", "11": "b: CN-06, PR-06", "12": "a: BUG-PR-02", "13": "a: BUG-PR-01",
          "14": "a: BUG-PR-04", "15": "a: BUG-PR-03", "16": "b: PR-05"}

def summary(issue_nums=None):
    issue_nums = issue_nums or {}
    from collections import Counter
    rows = "\n".join(
        f"| [BUG-{b[0]}](issues/BUG-{b[0]}.md) | {b[2]} | `{b[3]}` | {b[6]} | {b[7]} | {b[4]} | {b[5]} | {TRIAGE[b[0]]} | "
        + (f"[#{issue_nums[b[0]]}](https://github.com/tzin1401/testing-hw06/issues/{issue_nums[b[0]]})" if b[0] in issue_nums else "#TBD") + " |"
        for b in BUGS)
    api = Counter(("API 1 Login" if b[4].startswith("LG") else "API 2 Cancel" if b[4].startswith("CN") else "API 3 Product") for b in BUGS)
    sev = Counter(b[6] for b in BUGS)
    human = [f"BUG-{b[0]}" for b in BUGS if "Human" in b[5]]
    both = [f"BUG-{b[0]}" for b in BUGS if b[5] == "cả hai"]
    return f"""# Bug report – HW06 (23120190)

{len(BUGS)} bug, mỗi bug là một nguyên nhân gốc và một GitHub Issue. Mọi Actual result lấy từ request thật: transcript ở `evidence/issues/BUG-xx_curl.txt` (sinh bằng `scripts/repro_bugs.sh`, SUT reset trước mỗi bug) và Newman report ở `results/newman/`.
Severity/Priority là **đề xuất của AI**, sinh viên review. Triage gốc: [00_triage.md](issues/00_triage.md) (cột "Triage" chỉ bảng a = đề xuất bug, b = cần sinh viên quyết định).

| Bug | Tiêu đề | API | Severity | Priority | Test case | Phát hiện bởi | Triage | GitHub Issue |
|---|---|---|---|---|---|---|---|---|
{rows}

## Thống kê

- Theo API (theo test case đầu tiên): {", ".join(f"{k}: {v}" for k, v in sorted(api.items()))}
- Theo severity: {", ".join(f"{k}: {v}" for k, v in sorted(sev.items()))}
- **AI bỏ sót** (chỉ case Human Extend phát hiện): {len(human)} – {", ".join(human)}
- AI và Human cùng phát hiện: {len(both)} – {", ".join(both)}

## Không đưa thành bug (giữ ở bảng b của triage)

- LG-01 chuẩn hóa email (viết hoa/khoảng trắng): spec không quy định normalization.
- LG-02 JSON sai cú pháp trả HTML 400: chỉ khác định dạng lỗi, không lộ thông tin như BUG-04.
- LG-06 request thiếu password bị tính là lần sai: spec không phân biệt.
- CN-05 admin hủy đơn người khác qua endpoint user: quyền và mã status đều là giả định.
- PR-06 phần id vắng trả `{{}}` 200: mã status là giả định (phần ép kiểu id đã thành BUG-11).
"""

if __name__ == "__main__" and "--summary" in sys.argv:
    import json as _j
    nums = _j.loads(pathlib.Path(sys.argv[-1]).read_text()) if sys.argv[-1].endswith(".json") else {}
    (ROOT / "report/bug_report.md").write_text(summary(nums))
