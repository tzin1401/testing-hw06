#!/usr/bin/env python3
"""Sinh case cho POST /api/login, mỗi kỹ thuật một hàm / một file gen/<G>.json, rồi gộp vào cases.json.
Dùng: generate.py <G1|G2|G3|G4|G6|EX|merge>"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).parent
PW = "Test1234!"
EMAIL = "lg-{{$guid}}@test.com"
LOCK = [401, 403, 423, 429]       # GD5
REJECT = [400, 401]               # GD2


def reg(var="email", cap="uid", pw=PW, name="LG User"):
    return {"name": f"đăng ký {var}", "method": "POST", "path": "/api/register",
            "body": {"name": name, "email": "{{%s}}" % var, "password": pw},
            "expect_status": 200, "capture": {cap: "id"}}


def login_step(n, pw="Wrong1234!", var="email", expect=None, **kw):
    s = {"name": n, "method": "POST", "path": "/api/login",
         "body": {"email": "{{%s}}" % var, "password": pw}, "expect_status": expect or [401] + LOCK[1:]}
    s.update(kw)
    return s


def wrongs(k):
    return [login_step(f"sai mật khẩu lần {i}") for i in range(1, k + 1)]


def login(body=None, raw=None, ct=None, **kw):
    r = {"method": "POST", "path": "/api/login"}
    if raw is not None:
        r["raw"] = raw
        if ct:
            r["content_type"] = ct
    else:
        r["body"] = body if body is not None else {"email": "{{email}}", "password": PW}
    r.update(kw)
    return r


def me_oracle(tok="token", uid="{{uid}}"):
    return {"name": "dùng token gọi /api/users/me", "method": "GET", "path": "/api/users/me",
            "headers": {"Authorization": "Bearer {{%s}}" % tok}, "expect_status": 200,
            "checks": [{"path": "id", "equals": int(uid) if uid.isdigit() else uid}]}


def case(g, n, tech, req, purpose, source, request, status, checks, setup=None, after=None,
         assumed=False, vars=None, crashes=False):
    return {"id": f"LG-{g}-{n:02d}", "group": g, "technique": tech, "requirement": req,
            "purpose": purpose, "source": source, "label": "PENDING", "label_reason": "",
            "crashes_sut": crashes, "vars": vars if vars is not None else {"email": EMAIL},
            "setup": setup if setup is not None else [reg()],
            "request": request,
            "expect": {"status": status, "assumed": assumed, "checks": checks},
            **({"after": after} if after else {})}


NO_TOKEN = {"path": "token", "absent": True}
HAS_ERR = {"path": "error", "exists": True}
NO_STACK = {"no_text": "node_modules"}


def G1():
    # EP/BVA: mỗi case chỉ đổi 1 tham số so với request hợp lệ
    c = []
    c.append(case("G1", 1, "EP", "FR-02", "EP email hợp lệ + password đúng → 200 có token và user",
                  "A:24-32; R:43", login(), 200,
                  [{"path": "token", "type": "string"}, {"path": "user", "type": "object"},
                   {"path": "user.email", "equals": "{{email}}"}],
                  after=[me_oracle()]))
    c[-1]["request"]["capture"] = {"token": "token"}
    c.append(case("G1", 2, "EP", "FR-02", "EP email chưa đăng ký (đúng format) → từ chối",
                  "R:40-42; GD1", login({"email": "{{email}}", "password": PW}), 401, [NO_TOKEN, HAS_ERR],
                  setup=[], assumed=True))
    c.append(case("G1", 3, "BVA", "FR-02", "BVA email rỗng \"\" → từ chối",
                  "R:40,44; GD2", login({"email": "", "password": PW}), REJECT, [NO_TOKEN, HAS_ERR], assumed=True))
    c.append(case("G1", 4, "EP", "FR-02", "EP thiếu field email → từ chối",
                  "A:25-31; GD2", login({"password": PW}), REJECT, [NO_TOKEN, HAS_ERR], assumed=True))
    c.append(case("G1", 5, "EP", "FR-02", "EP email sai format \"lg-no-at\" → từ chối",
                  "R:44, R:33; GD2", login({"email": "lg-no-at", "password": PW}), REJECT, [NO_TOKEN, HAS_ERR],
                  setup=[{**reg(), "body": {"name": "LG User", "email": "lg-no-at", "password": PW},
                          "expect_status": [200, 400, 500]}], vars={}, assumed=True))
    c.append(case("G1", 6, "BVA", "FR-02", "BVA email rất dài (4096 ký tự) → từ chối, không 500",
                  "R:44; GD2", login({"email": "a" * 4084 + "@example.com", "password": PW}), REJECT,
                  [NO_TOKEN, HAS_ERR], assumed=True))
    c.append(case("G1", 7, "EP", "FR-02", "EP password sai (email đúng) → 401",
                  "R:41; GD1", login({"email": "{{email}}", "password": "Wrong1234!"}), 401, [NO_TOKEN, HAS_ERR],
                  assumed=True))
    c.append(case("G1", 8, "BVA", "FR-02", "BVA password rỗng \"\" → từ chối",
                  "R:40; GD2", login({"email": "{{email}}", "password": ""}), REJECT, [NO_TOKEN, HAS_ERR], assumed=True))
    c.append(case("G1", 9, "EP", "FR-02", "EP thiếu field password → từ chối",
                  "A:25-31; GD2", login({"email": "{{email}}"}), REJECT, [NO_TOKEN, HAS_ERR], assumed=True))
    c.append(case("G1", 10, "BVA", "FR-02", "BVA password rất dài (4096 ký tự) → từ chối, không 500",
                  "R:40; GD2", login({"email": "{{email}}", "password": "A" * 4096}), REJECT, [NO_TOKEN, HAS_ERR],
                  assumed=True))
    c.append(case("G1", 11, "EP", "FR-02", "EP password khác hoa/thường (\"test1234!\") → 401",
                  "R:40-41; GD1", login({"email": "{{email}}", "password": "test1234!"}), 401, [NO_TOKEN, HAS_ERR],
                  assumed=True))
    c.append(case("G1", 12, "EP", "FR-02", "Body rỗng {} → từ chối",
                  "A:25-31; GD2", login({}), REJECT, [NO_TOKEN, HAS_ERR], setup=[], vars={}, assumed=True))
    c.append(case("G1", 13, "EP", "FR-02", "JSON sai cú pháp → 400, không lộ stack trace",
                  "A:25; GD3", login(raw='{"email": "x@test.com", "password": '), 400, [NO_TOKEN, NO_STACK],
                  setup=[], vars={}, assumed=True))
    c.append(case("G1", 14, "EP", "FR-02", "Content-Type text/plain (thân là JSON hợp lệ) → từ chối",
                  "A:25; GD4", login(raw='{"email": "{{email}}", "password": "Test1234!"}', ct="text/plain"),
                  [400, 401, 415], [NO_TOKEN], assumed=True))
    c.append(case("G1", 15, "EP", "FR-02", "Field thừa trong body bị bỏ qua → 200 có token",
                  "A:25-32; GD6", login({"email": "{{email}}", "password": PW, "foo": "bar"}), 200,
                  [{"path": "token", "type": "string"}], assumed=True))
    return c


def G2():
    # FR-02 state machine; R:41-42
    c = []
    ok = [{"path": "token", "type": "string"}]
    cap = {"token": "token"}
    c.append(case("G2", 1, "ST", "FR-02", "Normal(n=1): sai 1 lần rồi đúng → 200 (chưa khóa)",
                  "R:41-43", login(capture=cap), 200, ok, setup=[reg()] + wrongs(1), after=[me_oracle()]))
    c.append(case("G2", 2, "ST", "FR-02", "Normal(n=2): sai 2 lần rồi đúng → 200 (biên dưới ngưỡng 3)",
                  "R:41-43", login(capture=cap), 200, ok, setup=[reg()] + wrongs(2), after=[me_oracle()]))
    c.append(case("G2", 3, "ST", "FR-02", "Normal(n=2)--sai-->Locked: sai 3 lần rồi đúng → bị khóa, không token",
                  "R:42; GD5", login(), LOCK, [NO_TOKEN, HAS_ERR], setup=[reg()] + wrongs(3), assumed=True,
                  after=[login_step("đúng mật khẩu lần nữa vẫn khóa", pw=PW, expect=LOCK, checks=[NO_TOKEN])]))
    c.append(case("G2", 4, "ST", "FR-02", "Locked--sai-->Locked: đã khóa, sai tiếp → vẫn khóa",
                  "R:42; GD5", login({"email": "{{email}}", "password": "Wrong1234!"}), LOCK, [NO_TOKEN],
                  setup=[reg()] + wrongs(3), assumed=True,
                  after=[login_step("đúng mật khẩu sau đó vẫn khóa", pw=PW, expect=LOCK, checks=[NO_TOKEN])]))
    c.append(case("G2", 5, "ST", "FR-02", "Locked--hết 30s, đúng-->Normal: chờ 31 s rồi đúng → 200",
                  "R:42-43", login(capture=cap, wait_ms=31000), 200, ok, setup=[reg()] + wrongs(3),
                  after=[me_oracle()]))
    c.append(case("G2", 6, "BVA-time", "FR-02", "Locked tại 25 s (< 30 s): đúng mật khẩu → vẫn khóa",
                  "R:42; GD5", login(wait_ms=25000), LOCK, [NO_TOKEN], setup=[reg()] + wrongs(3), assumed=True,
                  after=[login_step("chờ thêm 6 s (tổng > 30 s) rồi đúng → mở khóa", pw=PW, expect=200,
                                    wait_ms=6000, checks=[{"path": "token", "type": "string"}])]))
    c.append(case("G2", 7, "ST", "FR-02", "Đúng reset bộ đếm (\"liên tiếp\"): sai 2, đúng, sai 2, đúng → 200",
                  "R:41-42", login(capture=cap), 200, ok,
                  setup=[reg()] + wrongs(2) + [login_step("đăng nhập đúng (reset)", pw=PW, expect=200)]
                  + [login_step(f"sai lại lần {i}") for i in (1, 2)], after=[me_oracle()]))
    c.append(case("G2", 8, "ST", "FR-02", "Khóa theo từng tài khoản: A bị khóa, B đăng nhập đúng → 200",
                  "R:42", login({"email": "{{email_b}}", "password": PW}, capture=cap), 200, ok,
                  setup=[reg(), reg("email_b", "uid_b")] + wrongs(3),
                  vars={"email": EMAIL, "email_b": "lg-b-{{$guid}}@test.com"},
                  after=[me_oracle(uid="{{uid_b}}")]))
    return c


def G3():
    c = []
    sqli = [
        ("SQLi tautology ở email", {"email": "' OR '1'='1' --", "password": "x"}),
        ("SQLi comment ở email (vô hiệu điều kiện password)", {"email": "{{email}}' --", "password": "x"}),
        ("SQLi tautology ở password", {"email": "{{email}}", "password": "' OR '1'='1"}),
        ("SQLi UNION ở email", {"email": "x' UNION SELECT 1,'a','b','c','admin',0,null,null,null,null --", "password": "c"}),
    ]
    for i, (p, b) in enumerate(sqli, 1):
        c.append(case("G3", i, "SEC-05", "SEC-05", p + " → không bypass, không 500",
                      "R:282; GD1/GD2", login(b), REJECT, [NO_TOKEN, NO_STACK], assumed=True))
    c.append(case("G3", 5, "SEC-05", "SEC-05", "Object thay cho chuỗi: password = {\"$ne\": null} → từ chối",
                  "R:282; GD2", login({"email": "{{email}}", "password": {"$ne": None}}), REJECT, [NO_TOKEN],
                  assumed=True))
    c.append(case("G3", 6, "SEC-05", "SEC-05", "Mảng thay cho chuỗi: email = [\"{{email}}\"] → từ chối",
                  "R:282; GD2", login({"email": ["{{email}}"], "password": PW}), REJECT, [NO_TOKEN], assumed=True))
    c.append(case("G3", 7, "SEC-01", "SEC-01", "Login thành công không trả password trong body",
                  "R:278, R:226", login(), 200, [{"path": "user.password", "absent": True},
                                                 {"no_text": PW}]))
    c.append(case("G3", 8, "Enumeration", "FR-02", "Không lộ nguyên nhân: sai email và sai password trả cùng thông báo",
                  "R:42; GD7", login({"email": "{{email}}", "password": "Wrong1234!"}), 401,
                  [{"path": "error", "equals": "{{err_unknown}}"}],
                  setup=[reg(), {"name": "login email chưa có", "method": "POST", "path": "/api/login",
                                 "body": {"email": "nobody-{{email}}", "password": PW},
                                 "expect_status": 401, "capture": {"err_unknown": "error"}}],
                  assumed=True))
    c.append(case("G3", 9, "SEC-03", "SEC-03", "Client gửi role:\"admin\" trong body login không nâng quyền",
                  "R:280, R:67; A:25-31, A:173; GD14", login({"email": "{{email}}", "password": PW, "role": "admin"}, capture={"token": "token"}), 200,
                  [{"path": "token", "type": "string"}],
                  after=[{"name": "token vừa cấp gọi /api/admin/users → bị từ chối", "method": "GET", "path": "/api/admin/users",
                          "headers": {"Authorization": "Bearer {{token}}"}, "expect_status": [401, 403], "checks": []}]))
    c.append(case("G3", 10, "SEC-02", "SEC-02", "Tài khoản bị khóa không lộ lý do chi tiết (không lộ locked_until / số lần)",
                  "R:42; GD5, GD11", login(), LOCK, [NO_TOKEN, HAS_ERR, {"no_text": "locked_until"}, {"no_text": "login_attempts"}],
                  setup=[reg()] + wrongs(3), assumed=True))
    return c


def G4():
    c = []
    cap = {"token": "token"}
    c.append(case("G4", 1, "Schema", "FR-02", "Schema 200: Content-Type JSON, token string, user.id number, user.email string",
                  "A:32; R:43; GD12", login(capture=cap), 200,
                  [{"header": "Content-Type", "includes": "application/json"}, {"path": "token", "type": "string"},
                   {"path": "user.id", "type": "number"}, {"path": "user.id", "equals": "{{uid}}"},
                   {"path": "user.email", "type": "string"}, {"path": "user.name", "type": "string"},
                   {"path": "user.role", "type": "string"}],
                  after=[me_oracle()], assumed=True))
    c.append(case("G4", 2, "Schema", "FR-02", "Schema lỗi 401: Content-Type JSON, error là string, không token",
                  "R:42; GD1", login({"email": "{{email}}", "password": "Wrong1234!"}), 401,
                  [{"header": "Content-Type", "includes": "application/json"}, {"path": "error", "type": "string"},
                   NO_TOKEN], assumed=True))
    c.append(case("G4", 3, "Schema", "FR-02", "Không lộ trạng thái khóa trong user: không có login_attempts, locked_until",
                  "R:42; GD11, GD13", login(), 200,
                  [
                   {"path": "user.login_attempts", "absent": True}, {"path": "user.locked_until", "absent": True}], assumed=True))
    c.append(case("G4", 4, "Perf", "FR-02", "Thời gian phản hồi login < 2000 ms",
                  "GD9", login(), 200, [{"max_ms": 2000}], assumed=True))
    return c


def G6():
    c = []
    c.append(case("G6", 1, "Heuristic: null", "FR-02", "Heuristic null: email = null → từ chối, không 500",
                  "GD2", login({"email": None, "password": PW}), REJECT, [NO_TOKEN, NO_STACK], assumed=True))
    c.append(case("G6", 2, "Heuristic: kiểu sai", "FR-02", "Heuristic kiểu sai: password là số 12345678 → từ chối",
                  "GD2", login({"email": "{{email}}", "password": 12345678}), REJECT, [NO_TOKEN],
                  assumed=True))
    c.append(case("G6", 3, "Heuristic: hoa/thường", "FR-02", "Heuristic hoa/thường: email viết HOA vẫn đăng nhập đúng user",
                  "R:33; GD8", login({"email": "{{email_up}}", "password": PW}), 200,
                  [{"path": "user.id", "equals": "{{uid}}"}],
                  vars={"n": "{{$timestamp}}{{$randomInt}}", "email": "lg-up-{{n}}@test.com",
                        "email_up": "LG-UP-{{n}}@TEST.COM"}, assumed=True))
    c.append(case("G6", 4, "Heuristic: khoảng trắng", "FR-02", "Heuristic khoảng trắng: password có space cuối → 401",
                  "R:40; GD1/GD8", login({"email": "{{email}}", "password": PW + " "}), 401, [NO_TOKEN], assumed=True))
    c.append(case("G6", 5, "Heuristic: Unicode", "FR-02", "Heuristic Unicode/tiếng Việt: password \"MậtKhẩu1!\" đăng nhập đúng → 200",
                  "R:40,43", login({"email": "{{email}}", "password": "MậtKhẩu1!"}), 200,
                  [{"path": "token", "type": "string"}], setup=[reg(pw="MậtKhẩu1!")]))
    c.append(case("G6", 6, "Heuristic: gọi lặp", "FR-02", "Heuristic gọi lặp: login đúng 2 lần liên tiếp → cả 2 đều 200",
                  "R:43", login(capture={"token": "token"}), 200, [{"path": "token", "type": "string"}],
                  setup=[reg(), login_step("login đúng lần 1", pw=PW, expect=200)], after=[me_oracle()]))
    return c


def EX():
    # bug_patterns.md: P3, P4, P6, P7, P8, P9 liên quan; P1, P2, P5 không áp dụng (xem run_log)
    c = []
    c.append(case("EX", 1, "P3", "SEC-02", "P3: token cấp trước khi đặt lại mật khẩu phải bị từ chối sau khi đặt lại",
                  "R:43, R:279; A:34-53; GD10", {"method": "GET", "path": "/api/users/me",
                                                  "headers": {"Authorization": "Bearer {{old_token}}"}},
                  [401, 403], [{"path": "id", "absent": True}],
                  setup=[reg(), login_step("login lấy token cũ", pw=PW, expect=200, capture={"old_token": "token"}),
                         {"name": "forgot-password", "method": "POST", "path": "/api/forgot-password",
                          "body": {"email": "{{email}}"}, "expect_status": 200, "capture": {"otp": "resetToken"}},
                         {"name": "reset-password", "method": "POST", "path": "/api/reset-password",
                          "body": {"email": "{{email}}", "resetToken": "{{otp}}", "newPassword": "NewPass123!"},
                          "expect_status": 200}], assumed=True))
    c.append(case("EX", 2, "P4", "SEC-03", "P4: user đã đăng ký kèm role:\"admin\" thì login vẫn trả role user",
                  "R:280, R:67, A:173; GD14", login(capture={"token": "token"}), 200, [{"path": "token", "type": "string"}],
                  after=[{"name": "token vừa cấp gọi /api/admin/users → bị từ chối", "method": "GET", "path": "/api/admin/users",
                          "headers": {"Authorization": "Bearer {{token}}"}, "expect_status": [401, 403], "checks": []}],
                  setup=[{**reg(), "body": {"name": "LG User", "email": "{{email}}", "password": PW, "role": "admin"}}]))
    c.append(case("EX", 3, "P6", "SEC-01", "P6: response login không chứa chuỗi \"password\" ở bất kỳ đâu",
                  "R:278", login(), 200, [{"no_text": "\"password\""}]))
    c.append(case("EX", 4, "P7", "FR-02", "P7: sai 1 lần → login_attempts của user đúng bằng 1",
                  "R:41; GD1, GD13", login({"email": "{{email}}", "password": "Wrong1234!"}), 401, [NO_TOKEN],
                  setup=[reg(), {"name": "admin login (chỉ đọc)", "method": "POST", "path": "/api/login",
                                 "body": {"email": "admin@eshop.com", "password": "Admin123!"}, "expect_status": 200,
                                 "capture": {"admin_token": "token"}}],
                  after=[{"name": "đọc login_attempts qua /api/admin/users", "method": "GET", "path": "/api/admin/users",
                          "headers": {"Authorization": "Bearer {{admin_token}}"}, "expect_status": 200,
                          "checks": [{"path": "[id={{uid}}].login_attempts", "equals": 1}]}],
                  assumed=True))
    c.append(case("EX", 5, "P7", "FR-02", "P7: thời gian khóa thật ≤ 30 s – sai 3 lần, chờ 32 s, đúng → 200",
                  "R:42", login(capture={"token": "token"}, wait_ms=32000), 200, [{"path": "token", "type": "string"}],
                  setup=[reg()] + wrongs(3) + [login_step("ngay sau khi sai 3 lần: đúng → khóa", pw=PW, expect=LOCK)],
                  after=[me_oracle()]))
    c.append(case("EX", 6, "P8", "FR-02", "P8: password = null với email tồn tại không làm sập server",
                  "GD2", login({"email": "{{email}}", "password": None}), REJECT, [NO_TOKEN, NO_STACK],
                  after=[{"name": "server còn sống: GET /api/products", "method": "GET", "path": "/api/products",
                          "expect_status": 200, "checks": []}], assumed=True, crashes=True))
    c.append(case("EX", 7, "P9", "FR-02", "P9: user.id cùng kiểu number trên 2 user tạo liên tiếp (id chẵn/lẻ)",
                  "A:32", login(), 200, [{"path": "user.id", "type": "number"}, {"path": "user.id", "equals": "{{uid}}"}],
                  setup=[reg(), reg("email_b", "uid_b")],
                  vars={"email": EMAIL, "email_b": "lg-b-{{$guid}}@test.com"},
                  after=[{"name": "login user B, user.id là number", "method": "POST", "path": "/api/login",
                          "body": {"email": "{{email_b}}", "password": PW}, "expect_status": 200,
                          "checks": [{"path": "user.id", "type": "number"}, {"path": "user.id", "equals": "{{uid_b}}"}]}]))
    return c


GROUPS = {"G1": G1, "G2": G2, "G3": G3, "G4": G4, "G6": G6, "EX": EX}

if __name__ == "__main__":
    g = sys.argv[1]
    if g == "merge":
        cases = [c for k in GROUPS for c in json.loads((HERE / f"{k}.json").read_text())]
        out = {"api": "API1_Login", "prefix": "LG", "endpoint": "POST /api/login", "cases": cases}
        (HERE.parent / "cases.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
        print(len(cases), "case ->", HERE.parent / "cases.json")
    else:
        rows = GROUPS[g]()
        (HERE / f"{g}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
        print(g, len(rows))
