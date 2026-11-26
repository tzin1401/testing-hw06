# Định dạng `cases.json`

```json
{
  "api": "API1_Login",
  "prefix": "LG",
  "endpoint": "POST /api/login",
  "cases": [
    {
      "id": "LG-G1-01",
      "group": "G1",
      "technique": "EP",
      "requirement": "FR-02",
      "purpose": "Email tồn tại, password đúng",
      "source": "A:24-32; R:40,43",
      "label": "VALID",
      "label_reason": "",
      "crashes_sut": false,
      "vars": { "email": "lg-{{$guid}}@test.com" },
      "setup": [
        { "name": "đăng ký", "method": "POST", "path": "/api/register",
          "body": { "name": "U", "email": "{{email}}", "password": "Test1234!" },
          "expect_status": 200, "capture": { "uid": "id" } }
      ],
      "request": {
        "method": "POST", "path": "/api/login",
        "headers": { },
        "body": { "email": "{{email}}", "password": "Test1234!" }
      },
      "expect": {
        "status": 200, "assumed": false,
        "checks": [
          { "path": "token", "type": "string" },
          { "path": "user.password", "absent": true }
        ]
      }
    }
  ]
}
```

## Trường

| Trường | Ý nghĩa |
|---|---|
| `id` | `<PREFIX>-<G1..G6|EX>-<NN>` |
| `label` | `PENDING` khi mới sinh; auditor đổi thành `VALID` / `INVALID` / `INCOMPLETE`. Case `INVALID` không vào collection |
| `vars` | Biến của case, set trước request đầu tiên. Chuỗi có `{{$guid}}` sẽ được thay bằng UUID |
| `setup[]` | Các request chuẩn bị. `expect_status` sai thì case coi là setup lỗi. `capture`: `{biến: "đường.dẫn.json"}` lưu vào biến collection |
| `request` | Request chính. Dùng `body` (JSON) **hoặc** `raw` (chuỗi gửi nguyên văn) và `content_type` nếu không phải JSON. Header `Authorization` ghi như `"Bearer {{token}}"` |
| `expect.status` | Số, hoặc mảng số nếu chấp nhận nhiều mã |
| `expect.assumed` | `true` nếu status lấy từ GIẢ ĐỊNH; assertion sẽ có nhãn `(GIẢ ĐỊNH)` để `triage.py` nhận diện |
| `expect.checks[]` | Gồm: `{path, type}` với type `string`/`number`/`boolean`/`object`/`array`; `{path, equals}`; `{path, absent: true}`; `{path, exists: true}`; `{no_text: "chuỗi"}` (body không chứa chuỗi, vd `"password"`, `"at "` của stack trace) |
| `after[]` | Tùy chọn: request kiểm tra sau (oracle), cùng dạng với `setup` nhưng có thêm `checks` |
| `crashes_sut` | `true` nếu case có thể làm sập server; case sẽ được chạy riêng sau khi reset |

Mỗi case phải tự tạo dữ liệu riêng (user, đơn hàng, sản phẩm) trong `setup` và không dựa vào case khác.
