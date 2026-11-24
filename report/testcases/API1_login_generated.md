# API 1 – POST /api/login – Test case do AI sinh

## G1 – Domain partition + boundary

### Các lớp EP/BVA trước khi thiết kế test

| Tham số | Lớp | Phân loại | ID |
|---|---|---|---|
| email | Đúng format, đã đăng ký | Hợp lệ | LG-G1-01 |
| email | Đúng format, chưa tồn tại | Không hợp lệ | LG-G1-02 |
| email | Sai format: thiếu `@` | Không hợp lệ | LG-G1-03 |
| email | Sai format: thiếu domain | Không hợp lệ | LG-G1-04 |
| email | Sai format: khoảng trắng bên trong | Không hợp lệ | LG-G1-05 |
| email | Chuỗi rỗng, biên 0 ký tự | Không hợp lệ | LG-G1-06 |
| email | Thiếu field | Không hợp lệ | LG-G1-07 |
| email | `null` | Không hợp lệ | LG-G1-08 |
| email | Kiểu số | Không hợp lệ | LG-G1-09 |
| email | Khác chữ hoa/thường khi đăng ký | Chưa xác định; giả định không phân biệt | LG-G1-10 |
| email | Có khoảng trắng đầu | Chưa xác định; giả định trim | LG-G1-11 |
| email | Có khoảng trắng cuối | Chưa xác định; giả định trim | LG-G1-12 |
| email | Rất dài, 4096 ký tự | Chưa xác định; giả định từ chối | LG-G1-13 |
| password | Đúng | Hợp lệ | LG-G1-14 |
| password | Sai một ký tự | Không hợp lệ | LG-G1-15 |
| password | Sai hoa/thường | Không hợp lệ | LG-G1-16 |
| password | Rỗng, biên 0 ký tự | Không hợp lệ | LG-G1-17 |
| password | Thiếu field | Không hợp lệ | LG-G1-18 |
| password | `null` | Không hợp lệ | LG-G1-19 |
| password | Kiểu số | Không hợp lệ | LG-G1-20 |
| password | Rất dài, 4096 ký tự | Không khớp; giả định từ chối | LG-G1-21 |
| Body tổng thể | `{}` | Không hợp lệ; ngoại lệ toàn body | LG-G1-22 |
| Body tổng thể | JSON sai cú pháp | Không hợp lệ; ngoại lệ toàn body | LG-G1-23 |
| Body tổng thể | Content-Type không phải JSON | Chưa xác định; ngoại lệ toàn body | LG-G1-24 |
| Body tổng thể | Field thừa | Chưa xác định; giả định bỏ qua | LG-G1-25 |

### Quy ước setup độc lập

Mỗi dòng tự thực hiện setup mới, không dùng kết quả test khác: tạo `id` là chính ID của dòng viết thường (ví dụ `lg-g1-01`), `nonce` là UUID v4 mới từ Postman `pm.variables.replaceIn('{{$guid}}')`; đặt `email` = `lg-` + `id` + `-` + `nonce` + `@test.com`, `password` = `Test1234!`. Lưu vào biến Postman cùng tên. Gửi `POST /api/register`, `Content-Type: application/json`, body `{"name":"LG User","email":"{{email}}","password":"Test1234!"}`; yêu cầu đăng ký thành công HTTP 200 trước login, nếu không thì setup thất bại, không kết luận test login. Email cho LG-G1-02 là `absent-` + `email`: duy nhất theo nonce và chưa được đăng ký trong setup; giả định namespace này chưa tồn tại. Mỗi case chỉ gửi một login, không dùng tài khoản seed.

Trước login, tạo biến Postman: `upperEmail` = `email.toUpperCase()`; `spaceLead` = `' ' + email`; `spaceTail` = `email + ' '`; `missingAt` = `email.replace('@', '')`; `missingDomain` = phần trước `@` của email + `@`; `insideSpace` = `'x ' + email`; `longEmail` = `'a'.repeat(4087) + '@test.com'` (4096 ký tự); `longPassword` = `'a'.repeat(4096)`. Dùng `pm.variables.set` để lưu; các biến chuỗi chỉ chứa ký tự an toàn trong JSON, trừ khoảng trắng được giữ nguyên. Tất cả login dùng `POST /api/login`, không Authorization; trừ LG-G1-24 dùng `Content-Type: application/json`. Body được gửi nguyên văn như cột Request sau thay biến Postman; LG-G1-23 dùng raw text không sửa cú pháp.

Nguồn: **R** = `eshop-sut/README.md`; **A** = `eshop-sut/api_specification.md`. Ký hiệu trong bảng: **S** = HTTP 200, body có `token` là chuỗi JWT và có `user` (A:32, R:43); **E** = không cấp JWT, body có thông báo lỗi phù hợp không tiết lộ nguyên nhân; **GIẢ ĐỊNH** status mặc định 400 và nội dung lỗi ở E cho các input sai/malformed vì spec không quy định status hoặc schema lỗi; status trong từng dòng được ưu tiên nếu khác (LG-G1-24 là 415). Không bắt buộc tên field/thông điệp cụ thể. Những case giả định normalization, field thừa hoặc độ dài ghi rõ riêng dưới đây. Không khẳng định backend kiểm tra HTML5 email: R:44 chỉ quy định UI.

### Test case EP/BVA

|ID|Kỹ thuật|Requirement|Mục đích|Precondition / setup|Request|Expected status|Expected body / kiểm tra|Nguồn expected|
|---|---|---|---|---|---|---|---|---|
|LG-G1-01|EP|FR-02|Email tồn tại|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":"Test1234!"}`|200|S|A:24–32; R:40,43|
|LG-G1-02|EP|FR-02|Email chưa tồn tại|Setup độc lập; tạo `absentEmail = 'absent-' + email`|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{absentEmail}}","password":"Test1234!"}`|400 giả định|E|R:40–42; GIẢ ĐỊNH status/body E và email chưa tồn tại|
|LG-G1-03|EP|FR-02|Email thiếu @|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{missingAt}}","password":"Test1234!"}`|400 giả định|E|R:40–44; GIẢ ĐỊNH backend từ chối, status/body E|
|LG-G1-04|EP|FR-02|Email thiếu domain|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{missingDomain}}","password":"Test1234!"}`|400 giả định|E|R:40–44; GIẢ ĐỊNH backend từ chối, status/body E|
|LG-G1-05|EP|FR-02|Email có khoảng trắng trong|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{insideSpace}}","password":"Test1234!"}`|400 giả định|E|R:40–44; GIẢ ĐỊNH backend từ chối, status/body E|
|LG-G1-06|BVA|FR-02|Email rỗng|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"","password":"Test1234!"}`|400 giả định|E|R:40; GIẢ ĐỊNH từ chối, status/body E|
|LG-G1-07|EP|FR-02|Thiếu email|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"password":"Test1234!"}`|400 giả định|E|R:40; GIẢ ĐỊNH bắt buộc tại API, status/body E|
|LG-G1-08|EP|FR-02|Email null|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":null,"password":"Test1234!"}`|400 giả định|E|A:25–31; GIẢ ĐỊNH từ chối null, status/body E|
|LG-G1-09|EP|FR-02|Email số|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":12345,"password":"Test1234!"}`|400 giả định|E|A:25–31; GIẢ ĐỊNH từ chối số, status/body E|
|LG-G1-10|EP|FR-02|Email đổi chữ hoa/thường|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{upperEmail}}","password":"Test1234!"}`|200 giả định|S|A:32; GIẢ ĐỊNH email không phân biệt hoa/thường|
|LG-G1-11|EP|FR-02|Email có khoảng trắng đầu|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{spaceLead}}","password":"Test1234!"}`|200 giả định|S|A:32; GIẢ ĐỊNH trim khoảng trắng đầu|
|LG-G1-12|EP|FR-02|Email có khoảng trắng cuối|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{spaceTail}}","password":"Test1234!"}`|200 giả định|S|A:32; GIẢ ĐỊNH trim khoảng trắng cuối|
|LG-G1-13|BVA|FR-02|Email rất dài|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{longEmail}}","password":"Test1234!"}`|400 giả định|E|A:25–31; GIẢ ĐỊNH 4096 vượt giới hạn, từ chối và status/body E; spec không nêu ngưỡng|
|LG-G1-14|EP|FR-02|Password đúng|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":"Test1234!"}`|200|S|A:24–32; R:40,43|
|LG-G1-15|EP|FR-02|Password sai một ký tự|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":"Test1235!"}`|400 giả định|E|R:40–42; GIẢ ĐỊNH status/body E|
|LG-G1-16|EP|FR-02|Password sai chữ hoa/thường|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":"test1234!"}`|400 giả định|E|R:40–42; GIẢ ĐỊNH phân biệt hoa/thường và status/body E|
|LG-G1-17|BVA|FR-02|Password rỗng|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":""}`|400 giả định|E|R:40; GIẢ ĐỊNH từ chối, status/body E|
|LG-G1-18|EP|FR-02|Thiếu password|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}"}`|400 giả định|E|R:40; GIẢ ĐỊNH bắt buộc tại API, status/body E|
|LG-G1-19|EP|FR-02|Password null|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":null}`|400 giả định|E|A:25–31; GIẢ ĐỊNH từ chối null, status/body E|
|LG-G1-20|EP|FR-02|Password số|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":12345}`|400 giả định|E|A:25–31; GIẢ ĐỊNH từ chối số, status/body E|
|LG-G1-21|BVA|FR-02|Password rất dài|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":"{{longPassword}}"}`|400 giả định|E|R:40–42; GIẢ ĐỊNH 4096 vượt giới hạn hoặc không khớp và status/body E; spec không nêu ngưỡng|
|LG-G1-22|EP|FR-02|Body rỗng|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{}`|400 giả định|E|A:25–31; GIẢ ĐỊNH từ chối body thiếu cả hai field, status/body E|
|LG-G1-23|EP|FR-02|JSON sai cú pháp|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; Raw `{"email":"{{email}}","password":"Test1234!"` (thiếu `}`)|400 giả định|E|A:25–31; GIẢ ĐỊNH parser từ chối và status/body E|
|LG-G1-24|EP|FR-02|Media type khác JSON|Setup độc lập|`POST /api/login`; `Content-Type: text/plain`; no Authorization; raw `{"email":"{{email}}","password":"Test1234!"}`|415 giả định|E|A:25; GIẢ ĐỊNH từ chối media type bằng 415 và body E|
|LG-G1-25|EP|FR-02|Field thừa|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; no Authorization; `{"email":"{{email}}","password":"Test1234!","extra":"unused"}`|200 giả định|S|A:25–32; GIẢ ĐỊNH bỏ qua field thừa|

**Ghi chú của AI:**
- R:44 mô tả validation UI, không định nghĩa validation API; các kết quả từ chối format là giả định cần audit.
- Status/schema lỗi, chuẩn hóa email, media type và field thừa chưa được đặc tả; các lựa chọn ở bảng là giả định, không phải quan sát.
- 4096 chỉ là giá trị stress được chọn, không phải biên tối đa đã biết; password login không có chính sách độ dài riêng trong spec.
- FR-01 yêu cầu xác nhận mật khẩu nhưng API đăng ký không định nghĩa field xác nhận; setup dùng đúng body ví dụ A:12–21.
