# HW06 – Phân chia API cho nhóm 5 người

SUT: [ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut), commit `85af3ba`. Endpoint lấy từ `api_specification.md`, yêu cầu lấy từ `README.md` (FR, SEC).

## Bảng phân chia

Mỗi người 3 API (Pool A, B, C). **Không có API nào trùng giữa 2 người**, nên bộ ba và prompt chắc chắn khác nhau.

| # | Họ tên | MSSV | Pool A | Pool B | Pool C |
|---|---|---|---|---|---|
| 1 | | | **FR-02 Login**<br>`POST /api/login` | **FR-10 User hủy đơn**<br>`PUT /api/orders/:id/cancel` | **FR-15 Product CRUD**<br>`POST/PUT/DELETE /api/products[/:id]` |
| 2 | | | **FR-01 Đăng ký**<br>`POST /api/register` | **FR-08 Checkout**<br>`POST /api/checkout` | **FR-18 Admin đổi trạng thái đơn**<br>`PUT /api/admin/orders/:id/status` |
| 3 | | | **FR-03 Quên/đặt lại mật khẩu**<br>`POST /api/forgot-password` + `POST /api/reset-password` | **FR-11 Xem đơn hàng**<br>`GET /api/orders/:id` + `GET /api/orders/my-orders` | **FR-16 Import CSV**<br>`POST /api/admin/import-products` |
| 4 | | | **FR-04 Hồ sơ cá nhân**<br>`GET/PUT /api/users/me` | **FR-09 Áp mã giảm giá**<br>`POST /api/apply-coupon` | **FR-17 Admin coupon**<br>`POST /api/admin/coupons` + `DELETE /api/admin/coupons/:id` |
| 5 | | | **FR-05/06 Tìm kiếm & chi tiết SP**<br>`GET /api/products?search=` + `GET /api/products/:id` | **FR-07 Giỏ hàng**<br>`POST /api/cart` + `GET /api/cart` | **FR-19 Admin user**<br>`GET /api/admin/users` + `DELETE /api/admin/users/:id` |

Dự phòng nếu có người cần đổi: **FR-14 Category CRUD** (`/api/categories`, Pool C).

## Vì sao mỗi người đều có thể đạt đủ điểm

Đề chấm mỗi API theo: ≥ 35 test case phủ **domain partition, state transition, security, schema**, cộng ≥ 5 case tự thêm và **bug thật**. Mọi API ở trên đều thỏa cả bốn:

| API | Tham số để chia partition | State transition | Security (SEC) | Bug tiềm năng (đã xem code) |
|---|---|---|---|---|
| Login | email, password | Bộ đếm sai → khóa → hết khóa (FR-02) | SQLi, lộ password, SEC-01 | Có, nhiều |
| Hủy đơn | id, token | pending/confirmed/shipping/delivered/canceled (FR-10) | IDOR, thiếu token | Có |
| Product CRUD | name, price, category_id, id | Tạo → sửa → xóa → xem lại | Role (SEC-03), thiếu token (SEC-02) | Có, nhiều |
| Đăng ký | name, email, password | Đăng ký → trùng email → login | SQLi, SEC-01, role injection | Có, nhiều |
| Checkout | total_amount, shipping_address, cart | Giỏ → đơn pending → giỏ sau checkout | Sửa tổng tiền, thiếu token | Có |
| Admin đổi trạng thái | id, status | Toàn bộ FR-10 | Role (SEC-03) | Có |
| Quên/đặt lại MK | email, resetToken, newPassword | Xin OTP → dùng → dùng lại → OTP cũ | SEC-07 entropy/hết hạn | Có |
| Xem đơn hàng | id, token | Đơn ở từng trạng thái hiển thị đúng | IDOR, thiếu token (SEC-02) | Có |
| Import CSV | mảng products, name, price | All-or-nothing rollback (FR-16) | Role (SEC-03) | Có, nhiều |
| Hồ sơ | name, phone, shipping_address, role | Cập nhật → đọc lại | Leo quyền role (SEC-06), lộ password | Có |
| Áp mã giảm giá | code, total_amount, user_id | Dùng mã → hết lượt (C5) | Thiếu token (C4), user_id giả | Có, nhiều |
| Admin coupon | code, type, discount_value, min, expired_at, max_uses | Tạo → áp dụng → xóa → áp lại | Role (SEC-03) | Có, nhiều |
| Tìm kiếm & chi tiết SP | search, id | Sản phẩm bị sửa/xóa thì kết quả đổi | SQLi (SEC-05), XSS (SEC-04) | Có |
| Giỏ hàng | id, name, price, quantity | Thêm → thêm trùng → checkout → giỏ | Giá do client gửi, thiếu token | Có, nhiều |
| Admin user | id, token | Xóa → login lại → xóa lần 2 | Role (SEC-03), tự xóa mình | Có |

Cách chia giữ cân bằng: ai cũng có ít nhất một API dính trạng thái đơn hàng (FR-10) hoặc trạng thái khóa/OTP, và có ít nhất một API admin cần kiểm tra role.

## Lưu ý chung

- Mỗi người chạy SUT trên máy mình (`localhost`). Không dùng chung server.
- **Không chia sẻ prompt, collection hay bug report.** Đề ghi copy (kể cả prompt) thì 0 điểm cả hai người.
- Bảng "Bug tiềm năng" chỉ nói là có bug, không nói bug gì. Mỗi người tự tìm, tự chứng minh bằng request thật.
