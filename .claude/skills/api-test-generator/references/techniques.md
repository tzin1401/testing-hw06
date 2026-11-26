# Template sinh test theo kỹ thuật

Mỗi nhóm là một lượt sinh riêng. Không gộp nhiều nhóm vào một prompt.
Mọi `expect` phải có `source` trỏ về dòng spec (A:xx / R:xx) hoặc ghi rõ GIẢ ĐỊNH.

## G1 – Domain partition + BVA
1. Với từng tham số (body, path, header), liệt kê lớp tương đương trước: hợp lệ, không hợp lệ, chưa xác định (sẽ là GIẢ ĐỊNH).
2. Thêm biên: rỗng, 1 ký tự, rất dài (4096), 0, âm, số thực, giá trị cực lớn.
3. Mỗi lớp một case; mỗi case chỉ đổi một tham số so với request hợp lệ.
4. Thêm các ngoại lệ ở mức toàn body: `{}`, JSON sai cú pháp, Content-Type không phải JSON, field thừa.

## G2 – State transition
1. Lấy state machine từ spec (vd FR-10 trạng thái đơn hàng, FR-02 khóa tài khoản / bộ đếm).
2. Liệt kê **mọi** cặp (trạng thái nguồn, sự kiện). Mỗi cạnh hợp lệ và mỗi cạnh không hợp lệ là một case.
3. Case phải có oracle sau hành động: dùng request `after` để đọc lại trạng thái thật.
4. Gồm cả chuỗi lặp: thao tác hai lần, sai N lần rồi đúng, hết thời gian khóa.

## G3 – Security (SEC-01..SEC-07)
- Thiếu token, token rỗng, sai scheme (Basic), token sai chữ ký, token hết hạn, token của user khác (IDOR).
- Role: user thường gọi API admin; client tự gửi `role`.
- Injection: SQL tautology/UNION/comment, XSS lưu trữ, object/array thay cho chuỗi.
- Lộ dữ liệu: response không chứa `password`, stack trace hay JWT của người khác.

## G4 – Schema
- Status, `Content-Type: application/json`, JSON schema của response thành công và response lỗi.
- Kiểu dữ liệu từng field (vd `price` là number), không có field nhạy cảm.
- Thời gian phản hồi (< 2000 ms).

## G6 – Heuristic
- `null`, kiểu sai, Unicode và tiếng Việt, khoảng trắng đầu/cuối, thứ tự gọi bất thường, gọi đồng thời hai lần.
- Ghi rõ heuristic nào sinh ra case trong `purpose`.
