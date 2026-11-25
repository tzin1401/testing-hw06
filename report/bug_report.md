# Bug report – HW06 (23120190)

16 bug, mỗi bug là một nguyên nhân gốc và một GitHub Issue. Mọi Actual result lấy từ request thật: transcript ở `evidence/issues/BUG-xx_curl.txt` (sinh bằng `scripts/repro_bugs.sh`, SUT reset trước mỗi bug) và Newman report ở `results/newman/`.
Severity/Priority là **đề xuất của AI**, sinh viên review. Triage gốc: [00_triage.md](issues/00_triage.md) (cột "Triage" chỉ bảng a = đề xuất bug, b = cần sinh viên quyết định).

| Bug | Tiêu đề | API | Severity | Priority | Test case | Phát hiện bởi | Triage | GitHub Issue |
|---|---|---|---|---|---|---|---|---|
| [BUG-01](issues/BUG-01.md) | Mỗi lần đăng nhập sai tăng bộ đếm 2 thay vì 1 | `POST /api/login` | major | P1 | LG-G2-01, LG-G2-04, LG-G2-05, LG-G2-06, LG-G2-08, LG-EX-02 | cả hai | a: BUG-LG-01 | [#1](https://github.com/tzin1401/testing-hw06/issues/1) |
| [BUG-02](issues/BUG-02.md) | Tài khoản bị khóa 180 giây thay vì 30 giây | `POST /api/login` | major | P1 | LG-G2-07, LG-G2-11, LG-G3-09, LG-G6-03 | AI-generated | a: BUG-LG-01 | [#2](https://github.com/tzin1401/testing-hw06/issues/2) |
| [BUG-03](issues/BUG-03.md) | Response login trả về mật khẩu dạng plaintext | `POST /api/login` | critical | P0 | LG-G4-01, LG-G4-02, LG-G4-03, LG-G4-07 | AI-generated | a: BUG-LG-02 | [#3](https://github.com/tzin1401/testing-hw06/issues/3) |
| [BUG-04](issues/BUG-04.md) | Body không phải JSON gây lỗi 500 và lộ stack trace | `POST /api/login` | minor | P2 | LG-G1-24 | AI-generated | b: LG-03 | [#4](https://github.com/tzin1401/testing-hw06/issues/4) |
| [BUG-05](issues/BUG-05.md) | Thông báo khóa tiết lộ email nào đã đăng ký | `POST /api/login` | minor | P3 | LG-G6-03 | AI-generated | b: LG-08 | [#5](https://github.com/tzin1401/testing-hw06/issues/5) |
| [BUG-06](issues/BUG-06.md) | JWT ký bằng secret hardcode, token tự ký được chấp nhận | `POST /api/login, PUT /api/orders/:id/cancel` | critical | P0 | LG-EX-05, CN-EX-05 | Human Extend (AI bỏ sót) | a: BUG-LG-03 | [#6](https://github.com/tzin1401/testing-hw06/issues/6) |
| [BUG-07](issues/BUG-07.md) | JWT không có hạn và không bị thu hồi khi đổi mật khẩu hoặc xóa user | `POST /api/login, PUT /api/orders/:id/cancel` | major | P2 | LG-EX-03, CN-EX-02, CN-G3-06 | cả hai | b: LG-09, CN-04, CN-07 | [#7](https://github.com/tzin1401/testing-hw06/issues/7) |
| [BUG-08](issues/BUG-08.md) | Header Authorization scheme Basic vẫn được chấp nhận | `PUT /api/orders/:id/cancel` | minor | P3 | CN-G1-13 | AI-generated | a: BUG-CN-01 | [#8](https://github.com/tzin1401/testing-hw06/issues/8) |
| [BUG-09](issues/BUG-09.md) | User hủy được đơn đang shipping | `PUT /api/orders/:id/cancel` | critical | P1 | CN-G2-03 | AI-generated | a: BUG-CN-02 | [#9](https://github.com/tzin1401/testing-hw06/issues/9) |
| [BUG-10](issues/BUG-10.md) | Admin chuyển được đơn canceled sang delivered | `PUT /api/admin/orders/:id/status` | major | P1 | CN-G2-10 | AI-generated | a: BUG-CN-03 | [#10](https://github.com/tzin1401/testing-hw06/issues/10) |
| [BUG-11](issues/BUG-11.md) | Path id dạng +1, 2.0, 03 vẫn khớp bản ghi | `PUT /api/orders/:id/cancel, DELETE/PUT /api/products/:id` | minor | P3 | CN-EX-01, CN-EX-03, CN-EX-04, PR-EX-01, PR-EX-02, PR-EX-05, PR-EX-06 | Human Extend (AI bỏ sót) | b: CN-06, PR-06 | [#11](https://github.com/tzin1401/testing-hw06/issues/11) |
| [BUG-12](issues/BUG-12.md) | Thêm/sửa/xóa sản phẩm không cần đăng nhập hay quyền admin | `POST/PUT/DELETE /api/products[/:id]` | blocker | P0 | PR-G3-01..PR-G3-12, PR-G6-16..PR-G6-21, PR-G6-30..PR-G6-32 | AI-generated | a: BUG-PR-02 | [#12](https://github.com/tzin1401/testing-hw06/issues/12) |
| [BUG-13](issues/BUG-13.md) | Không validate name/price/category khi thêm và sửa sản phẩm | `POST /api/products, PUT /api/products/:id` | major | P1 | PR-G1-*, PR-G2-16, PR-G4-04, PR-G4-05, PR-G6-01..PR-G6-15, PR-EX-03, PR-EX-04 | cả hai | a: BUG-PR-01 | [#13](https://github.com/tzin1401/testing-hw06/issues/13) |
| [BUG-14](issues/BUG-14.md) | GET chi tiết sản phẩm làm sập server khi price null | `GET /api/products/:id (sau PUT/POST /api/products)` | blocker | P0 | PR-G6-09, PR-G6-15, PR-G6-31 | AI-generated | a: BUG-PR-04 | [#14](https://github.com/tzin1401/testing-hw06/issues/14) |
| [BUG-15](issues/BUG-15.md) | User thường tự nâng quyền admin qua API cập nhật hồ sơ | `PUT /api/users/me` | critical | P0 | PR-G3-07, PR-G3-08, PR-G3-09 | AI-generated | a: BUG-PR-03 | [#15](https://github.com/tzin1401/testing-hw06/issues/15) |
| [BUG-16](issues/BUG-16.md) | Giá sản phẩm trả về kiểu chuỗi với id chẵn | `GET /api/products/:id` | minor | P3 | PR-G4-02, PR-G4-07 | AI-generated | b: PR-05 | [#16](https://github.com/tzin1401/testing-hw06/issues/16) |

## Thống kê

- Theo API (theo test case đầu tiên): API 1 Login: 7, API 2 Cancel: 4, API 3 Product: 5
- Theo severity: blocker: 2, critical: 4, major: 5, minor: 5
- **AI bỏ sót** (chỉ case Human Extend phát hiện): 2 – BUG-06, BUG-11
- AI và Human cùng phát hiện: 3 – BUG-01, BUG-07, BUG-13

## Không đưa thành bug (giữ ở bảng b của triage)

- LG-01 chuẩn hóa email (viết hoa/khoảng trắng): spec không quy định normalization.
- LG-02 JSON sai cú pháp trả HTML 400: chỉ khác định dạng lỗi, không lộ thông tin như BUG-04.
- LG-06 request thiếu password bị tính là lần sai: spec không phân biệt.
- CN-05 admin hủy đơn người khác qua endpoint user: quyền và mã status đều là giả định.
- PR-06 phần id vắng trả `{}` 200: mã status là giả định (phần ép kiểu id đã thành BUG-11).
