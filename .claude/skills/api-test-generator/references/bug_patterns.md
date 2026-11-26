# Mẫu bug AI hay bỏ sót (nhóm EX)

Mỗi mẫu liên quan tới endpoint sinh **1 case EX**. Danh sách này được mở rộng sau mỗi lần chạy, dựa trên phần "đề xuất mẫu mới" trong `triage.md`.

| # | Mẫu | Cách thử | Nguồn |
|---|---|---|---|
| P1 | Secret JWT hardcode trong source | Đọc secret trong `server.js`, tự ký token `{id, role:"admin"}`, gọi API cần auth; kỳ vọng 401 | BUG-06 (người tìm, AI bỏ sót) |
| P2 | Path id bị ép kiểu | Dùng `%2B{{id}}`, `{{id}}.0`, `0{{id}}`; kỳ vọng 400/404 và bản ghi không đổi | BUG-11 (người tìm, AI bỏ sót) |
| P3 | JWT không có `exp`, không bị thu hồi | Decode payload kiểm tra `exp`; đổi mật khẩu hoặc xóa user rồi dùng token cũ | BUG-07 |
| P4 | Mass assignment `role` | Gửi `role:"admin"` khi đăng ký hoặc cập nhật hồ sơ, rồi đọc lại role | BUG-15 |
| P5 | Scheme Authorization khác Bearer | `Authorization: Basic <jwt>`; kỳ vọng 401 | BUG-08 |
| P6 | Response lộ password | Kiểm tra `absent` cho mọi field `password` trong body | BUG-03 |
| P7 | Bộ đếm / thời gian khóa sai | Sai 1 lần rồi đọc `login_attempts`; đo thời gian khóa thật | BUG-01, BUG-02 |
| P8 | Giá trị null làm sập server | Ghi field `null` rồi GET lại (đánh dấu `crashes_sut`) | BUG-14 |
| P9 | Kiểu field không nhất quán giữa các bản ghi | So kiểu của cùng field trên id chẵn và lẻ | BUG-16 |
