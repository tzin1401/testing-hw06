# AI-driven API Test Generator – Pseudocode

Bộ sinh test chạy tự động từ đầu đến cuối (không có human-in-the-loop) cho SUT EShop.
Đầu vào: đặc tả API. Đầu ra: test case, Postman collection, Newman report chạy thật, danh sách ứng viên bug.

Mỗi chỗ người duyệt trong quy trình làm tay được thay bằng một **guardrail tự động**: agent audit độc lập, kiểm tra cấu trúc, quy tắc phân loại kết quả và danh mục mẫu bug AI hay bỏ sót.

## Tham số thiết kế

```
CONFIG = {
  spec_files      : ["api_specification.md", "README.md"],   # A = API spec, R = FR/SEC
  target_endpoint : "POST /api/login",                         # một API mỗi lần chạy
  student_id      : "23120190",
  base_url        : "http://localhost:3000",
  techniques      : ["G1_partition_bva", "G2_state", "G3_security", "G4_schema", "G6_heuristic"],
  max_regen_round : 2,        # số vòng sinh lại khi audit còn INCOMPLETE
  generator_model : MODEL_A,
  auditor_model   : MODEL_B,  # khác generator để tránh tự chấm điểm
}
```

## Luồng chính

```
function GENERATE_API_TESTS(CONFIG):
    ctx        = ANALYSE_SPEC(CONFIG.spec_files, CONFIG.target_endpoint)
    cases      = []
    for tech in CONFIG.techniques:                       # mỗi kỹ thuật một lần sinh riêng, không gộp
        cases += GENERATE_BY_TECHNIQUE(tech, ctx)
    cases += GENERATE_FROM_BUG_PATTERNS(ctx)             # các mẫu bug AI từng bỏ sót

    for round in 1..CONFIG.max_regen_round:
        audited = AUDIT(cases, ctx)                      # agent thứ hai, model khác
        weak    = [c for c in audited if c.label == INCOMPLETE]
        if weak is empty: break
        cases   = REPLACE(audited, REGENERATE(weak, ctx, audited.findings))
    cases = [c for c in audited if c.label != INVALID]   # INVALID giữ lại trong log, không đưa vào collection

    collection = BUILD_COLLECTION(cases, CONFIG)
    assert STATIC_CHECK(collection, cases)               # dừng nếu cấu trúc sai, không chạy bừa

    RESET_SUT()
    run      = RUN_NEWMAN(collection, CONFIG.base_url)   # chạy thật, không bao giờ tự viết kết quả
    triage   = TRIAGE(run, cases)
    WRITE_OUTPUTS(cases, collection, run, triage)
    return triage
```

## 1. Phân tích spec

```
function ANALYSE_SPEC(files, endpoint):
    text  = READ(files)
    ep    = EXTRACT_ENDPOINT(text, endpoint)          # method, path, auth, body, response mẫu
    reqs  = EXTRACT_REQUIREMENTS(text, ep)            # FR-xx, SEC-xx liên quan, kèm số dòng nguồn
    state = EXTRACT_STATE_MACHINE(text, ep)           # vd FR-10 trạng thái đơn hàng, FR-02 khóa tài khoản
    gaps  = []
    for rule in ep.params + ep.responses:
        if rule.status is missing or rule.error_schema is missing:
            gaps += ASSUMPTION(rule, default=400)     # spec mơ hồ → ghi GIẢ ĐỊNH, không hỏi người
    return {ep, reqs, state, gaps, source_lines}
```

## 2. Sinh test theo kỹ thuật

```
function GENERATE_BY_TECHNIQUE(tech, ctx):
    prompt = TEMPLATE[tech].fill(ctx)                  # template riêng cho từng kỹ thuật
    rows   = LLM(CONFIG.generator_model, prompt)
    for r in rows:
        r.id     = NEXT_ID(prefix(ctx.ep), tech)       # vd LG-G1-01
        r.source = CITE(r.expected, ctx.source_lines)  # expected phải trỏ về dòng spec hoặc GIẢ ĐỊNH
        r.setup  = INDEPENDENT_SETUP(r)                # mỗi case tự tạo user/đơn riêng, không phụ thuộc case khác
    return rows

TEMPLATE = {
  G1_partition_bva : "Liệt kê lớp EP/BVA cho từng tham số rồi mới sinh case, 1 case / lớp",
  G2_state         : "Liệt kê mọi cạnh hợp lệ và không hợp lệ của state machine, 1 case / cạnh",
  G3_security      : "SEC-01..SEC-07: thiếu token, sai scheme, token giả, role, injection, lộ dữ liệu",
  G4_schema        : "Kiểm tra status, Content-Type, JSON schema và kiểu từng field của response",
  G6_heuristic     : "Heuristic: null, rỗng, kiểu sai, rất dài, ký tự đặc biệt, thứ tự gọi",
}
```

## 3. Mẫu bug AI hay bỏ sót

```
BUG_PATTERNS = [
  "secret JWT hardcode trong source → tự ký token và gọi API",
  "path id bị ép kiểu: +1, 1.0, 01",
  "token không có exp / không bị thu hồi sau đổi mật khẩu",
  "cập nhật hồ sơ kèm field role",
  "scheme Authorization khác Bearer",
  "response trả kèm password",
]

function GENERATE_FROM_BUG_PATTERNS(ctx):
    applicable = [p for p in BUG_PATTERNS if RELEVANT(p, ctx.ep)]
    return LLM(CONFIG.generator_model, "Sinh 1 case cho mỗi mẫu", applicable, ctx)   # gắn nhóm EX
```

`BUG_PATTERNS` được bổ sung sau mỗi lần chạy (xem bước 7).

## 4. Audit tự động

```
function AUDIT(cases, ctx):
    for c in cases:
        verdict  = LLM(CONFIG.auditor_model, AUDIT_PROMPT, c, ctx)   # model khác generator
        c.label  = verdict.label          # VALID | INVALID | INCOMPLETE
        c.reason = verdict.reason
    for (a, b) in PAIRS(cases):
        if SAME_REQUEST(a, b) and SAME_EXPECTED(a, b):
            b.label, b.reason = INVALID, "trùng " + a.id
    for c in cases:
        if CAN_FALSE_PASS(c):             # vd tìm sản phẩm theo name có thể khớp bản ghi khác
            c.label = INCOMPLETE
    return cases

AUDIT_PROMPT kiểm: expected có nguồn; setup độc lập; một mục đích / case;
                   assertion đủ mạnh (không chỉ status); GIẢ ĐỊNH được ghi rõ.
```

## 5. Dựng collection và kiểm tra tĩnh

```
function BUILD_COLLECTION(cases, CONFIG):
    col = NEW_COLLECTION("<MSSV>_<API>")
    col.prerequest = [
        "pm.request.headers.upsert({key:'X-Student-Id', value: pm.environment.get('studentId')})",
        "console.log('X-Student-Id: ' + ...)" ]
    for c in cases:
        folder = col.folder(c.group).add_folder("[" + c.id + "] " + c.purpose)
        folder.add(c.setup_requests)
        folder.add(c.request, tests = ASSERTIONS(c))      # status, body, schema, nhãn (GIẢ ĐỊNH)
    return col

function STATIC_CHECK(col, cases):
    return  every case id has exactly one folder
        and no INVALID case has a folder
        and every request carries X-Student-Id
        and every main request has ≥ 1 assertion
        and no hardcoded token / host other than {{baseUrl}}
```

## 6. Chạy thật

```
function RUN_NEWMAN(col, base_url):
    assert HOST(base_url) in {"localhost", "127.0.0.1"}
    for c in cases where c.crashes_sut:                   # case làm sập server chạy riêng
        RESET_SUT(); NEWMAN(col, folder=c.id)
    RESET_SUT()
    return NEWMAN(col, reporters=[cli, htmlextra, json])  # file report do Newman sinh, không chỉnh sửa
```

## 7. Phân loại kết quả và học lại

```
function TRIAGE(run, cases):
    result = {}
    for c in cases:
        fails = run.failed_assertions(c.id)
        if fails is empty:                  result[c.id] = PASS
        elif all(f.is_assumption for f in fails):
                                            result[c.id] = SPEC_AMBIGUOUS   # chỉ lệch GIẢ ĐỊNH
        else:                               result[c.id] = BUG_CANDIDATE
    candidates = GROUP_BY_ROOT_CAUSE([c for c in cases if result[c.id] == BUG_CANDIDATE], run)
    for bug in candidates:
        bug.evidence = run.real_request_response(bug.cases)   # lấy từ log Newman thật
        bug.severity = SUGGEST_SEVERITY(bug)                   # ghi rõ "đề xuất của AI"
        if bug.found_only_by_EX_pattern: BUG_PATTERNS.add(PATTERN_OF(bug))
    return {result, candidates}
```

## 8. Đầu ra

```
function WRITE_OUTPUTS(cases, col, run, triage):
    OUT = "skill_runs/<API>/"                                   # không ghi đè bài làm tay
    WRITE(OUT + "cases.json", cases)                            # gồm nhãn audit và lý do
    WRITE(OUT + "collection.json", col)
    KEEP (OUT + "newman/*.html", OUT + "newman/*.json")         # nguyên bản từ Newman
    WRITE(OUT + "triage.md", triage)
    WRITE(OUT + "run_log.md", tool, model, time, rounds, counts)
```

## Tiêu chí dừng

| Điều kiện | Hành động |
|---|---|
| Audit hết INCOMPLETE hoặc hết `max_regen_round` | Sang bước dựng collection |
| `STATIC_CHECK` sai | Dừng, ghi lỗi, không chạy Newman |
| Host không phải localhost | Dừng |
| Newman chạy xong | Phân loại kết quả, ghi đầu ra, kết thúc |
