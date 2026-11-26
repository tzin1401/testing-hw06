# 01 – Phân tích spec: POST /api/login

Nguồn: A = `eshop-sut/api_specification.md`, R = `eshop-sut/README.md`.

## Endpoint
| Mục | Nội dung | Nguồn |
|---|---|---|
| Method/path | `POST /api/login` | A:23-24 |
| Auth | Không cần token (đây là API cấp token) | A:24, R:43 |
| Body | `{"email": string, "password": string}` | A:25-31 |
| 200 OK | Trả JWT `token` (string) và object `user` | A:32, R:43 |
| Header client gửi về sau | `Authorization: Bearer <token>` | R:43, A:59 |
| Tài khoản mẫu | admin@eshop.com / Admin123!, test@eshop.com / Test1234! (không dùng trong case vì dùng chung) | R:23-24 |

## Yêu cầu liên quan
| ID | Nội dung | Nguồn |
|---|---|---|
| FR-02a | Nhập Email + Mật khẩu | R:40 |
| FR-02b | Mỗi lần sai, bộ đếm tăng **đúng 1** | R:41 |
| FR-02c | Sai **≥3 lần liên tiếp** → khóa **30 giây**; thông báo lỗi phù hợp, không lộ chi tiết nguyên nhân | R:42 |
| FR-02d | Thành công trả JWT, dùng qua `Authorization: Bearer` | R:43 |
| FR-02e | Email phải đúng format (`type="email"`) | R:44, R:33 |
| SEC-01 | Mật khẩu không lưu plaintext (→ response không được trả password) | R:278 |
| SEC-02 | API bảo mật cần JWT hợp lệ (token login cấp phải dùng được) | R:279 |
| SEC-05 | Parameterized query (→ SQLi trên email/password không bypass được) | R:282 |
| SEC-03 | Role nằm trong token (→ client không tự nâng role qua body login) | R:280 |
| FR-03 | Đổi mật khẩu qua reset (dùng cho case token cũ / mật khẩu cũ) | R:46-60, A:34-53 |

## State machine (FR-02, R:41-42)
```
Normal(n=0) --sai--> Normal(n=1) --sai--> Normal(n=2) --sai--> Locked(30s)
Normal(n<3) --đúng--> Normal(n=0) + token
Locked --đúng/sai (trong 30s)--> Locked, không token
Locked --hết 30s, đúng--> Normal(n=0) + token
```
"Liên tiếp" (R:42) ⇒ đăng nhập đúng sẽ reset bộ đếm.

## GIẢ ĐỊNH (spec không nêu)
| # | Giả định |
|---|---|
| GD1 | Sai email hoặc mật khẩu → **401** + field `error` |
| GD2 | Thiếu field / rỗng / sai format email / body `{}` → **400 hoặc 401** (không 200, không 500) |
| GD3 | JSON sai cú pháp → **400**, không lộ stack trace (`node_modules`) |
| GD4 | Content-Type không phải JSON → **400/401/415** |
| GD5 | Tài khoản bị khóa → **401/403/423/429**, không có `token` |
| GD6 | Field thừa trong body bị bỏ qua → 200 |
| GD7 | Thông báo lỗi khi sai email và khi sai mật khẩu phải giống nhau (chống dò user, R:42 "không lộ chi tiết") |
| GD8 | Email so khớp không phân biệt hoa thường; khoảng trắng đầu/cuối không được trim (ambiguous → chỉ GIẢ ĐỊNH) |
| GD9 | Thời gian phản hồi < 2000 ms |
| GD10 | Token login cấp phải có `exp` hoặc bị vô hiệu sau khi đổi mật khẩu (P3) |
| GD11 | Thông báo khi bị khóa không lộ số lần sai / thời điểm mở khóa (không chứa `locked_until`, `login_attempts`) |
| GD12 | `user` trong response 200 có `id` (number), `email`, `name`, `role` (string); response là `application/json` |
| GD13 | Bộ đếm FR-02 quan sát được qua field `login_attempts` của `GET /api/admin/users` (tên field không có trong spec; lấy từ response thật của admin API) |
| GD14 | User thường gọi API admin (`/api/admin/*`) bị từ chối **401/403** (A:173, R:177-179; mã cụ thể không nêu) |
