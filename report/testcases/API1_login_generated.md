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

## G2 – State transition

**Mô hình:** `0`, `1`, `2` là số lần sai liên tiếp khi chưa khóa; `K` là đang khóa. Các trạng thái là mô hình black-box, không đòi response lộ counter. `W` là login sai, `C` là login đúng, `T` là chờ hết 30 giây; T không phải HTTP request. `E` là HTTP 400 **GIẢ ĐỊNH**, không có JWT, body có thông báo lỗi phù hợp; `L` là HTTP 423 **GIẢ ĐỊNH**, không có JWT, body có thông báo lỗi phù hợp không tiết lộ chi tiết nguyên nhân; `S` là HTTP 200, body có `token` JWT và `user`. R:41–43; A:24–32. HTTP status và hình dạng lỗi không được đặc tả. GIẢ ĐỊNH W/C khi K không kéo dài khóa; reset counter khi C thành công hoặc hết khóa là suy luận, không được nêu tường minh.

| Trạng thái | W: sai | C: đúng | T: hết 30 giây |
|---|---|---|---|
| 0 | 1, E — LG-G2-01 | 0, S — LG-G2-04 | 0, không response; sự kiện không áp dụng, giả định không đổi — LG-G2-08 |
| 1 | 2, E — LG-G2-02 | 0, S — LG-G2-05 | 1, không response; không áp dụng, giả định không đổi — LG-G2-09 |
| 2 | K, L — LG-G2-03 | 0, S — LG-G2-06 | 2, không response; không áp dụng, giả định không đổi — LG-G2-10 |
| K | K, L; không hợp lệ trong khóa, giả định không gia hạn — LG-G2-07 | K, L; không hợp lệ trong khóa, giả định không gia hạn — LG-G2-07 | 0, không response; giả định reset — LG-G2-11 |

**Setup độc lập cho từng case:** tạo `nonce` bằng `pm.variables.replaceIn('{{$guid}}')`; `email` = ID dòng viết thường + `-` + nonce + `@test.com`. `POST /api/register`, `Content-Type: application/json`, không Authorization, body `{"name":"LG User","email":"{{email}}","password":"Test1234!"}`; yêu cầu HTTP 200 trước khi tiếp tục. Với LG-G2-12 cũng tạo `emailB` = ID dòng viết thường + `-b-` + UUID v4 mới + `@test.com` và đăng ký cùng body thay email bằng `{{emailB}}`. Không dùng tài khoản hay kết quả từ case khác.

**Request/macro trong bước này:** `W` = `POST /api/login`, `Content-Type: application/json`, không Authorization, body `{"email":"{{email}}","password":"Wrong123!"}`; `C` = cùng method/path/header, body `{"email":"{{email}}","password":"Test1234!"}`; `CB` = như C nhưng email `{{emailB}}`. Gửi từng request tuần tự, xác nhận từng response theo chuỗi ở cột kiểm tra trước khi tiếp tục; chờ bằng Postman `setTimeout` hoặc runner. `t0` là thời điểm nhận response W thứ ba gây khóa; ~29 giây và ~31 giây tính từ `t0`, không cộng dồn các khoảng chờ. Không giả định field counter trong response.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
|LG-G2-01|ST|FR-02|0 → 1; kiểm tra không nhảy counter|Setup độc lập; không login trước|W; W; C|400, 400 giả định; 200|E, E, S; hai lần sai không khóa, chứng minh lần đầu không tăng quá 1|R:41–43; A:32; GIẢ ĐỊNH E và reset sau thành công|
|LG-G2-02|ST|FR-02|1 → 2; biên hai lần chưa khóa|Setup độc lập; W → E|W; C|400 giả định; 200|E rồi S, lần sai thứ hai chưa khóa|R:41–43; A:32; GIẢ ĐỊNH E|
|LG-G2-03|ST|FR-02|2 → K; sai lần ba khóa|Setup độc lập; W → E; W → E|W; C ngay sau đó|423 giả định; 423 giả định|L, L; lần thứ ba khóa và từ chối đúng ngay lập tức|R:41–43; GIẢ ĐỊNH status và nội dung lỗi L|
|LG-G2-04|ST|FR-02|0 → 0 khi đúng|Setup độc lập|C; W; W; C|200; 400, 400 giả định; 200|S, E, E, S; thành công không tạo số lần sai|R:41–43; A:32; GIẢ ĐỊNH E|
|LG-G2-05|ST|FR-02|1 → 0 khi đúng|Setup độc lập; W → E|C; W; W; C|200; 400, 400 giả định; 200|S, E, E, S; thành công xóa chuỗi sai cũ|R:41–43; A:32; GIẢ ĐỊNH reset và E|
|LG-G2-06|ST|FR-02|2 → 0; chuỗi 1-switch sai hai → đúng → sai hai|Setup độc lập; W → E; W → E|C; W; W; C|200; 400, 400 giả định; 200|S, E, E, S; không khóa sau chuỗi mới gồm hai sai|R:41–43; A:32; GIẢ ĐỊNH reset và E|
|LG-G2-07|ST|FR-02|Trong khóa cả sai và đúng đều bị từ chối, không kéo dài khóa|Setup độc lập; W → E; W → E; W → L, ghi `t0`|W ngay; C ngay; chờ tới `t0` + 31 giây; C|423, 423 giả định; 200|L, L, S; lỗi khóa không nêu password sai, email tồn tại, counter hay nguyên nhân chi tiết|R:42–43; A:32; GIẢ ĐỊNH status L và request trong khóa không gia hạn|
|LG-G2-08|ST|FR-02|T không áp dụng tại 0, không gây thay đổi|Setup độc lập; đợi 31 giây không gửi login|W; W; C|400, 400 giả định; 200|E, E, S; vẫn chưa khóa sau hai sai|R:41–43; A:32; GIẢ ĐỊNH T khi chưa khóa không đổi và E|
|LG-G2-09|ST|FR-02|T không áp dụng tại 1, không tự xóa counter|Setup độc lập; W → E; đợi 31 giây|W; W; C|400, 423, 423 giả định|E, L, L; lần sai tổng thứ ba khóa|R:41–42; GIẢ ĐỊNH counter không tự hết hạn khi chưa khóa, status/body E và L|
|LG-G2-10|ST|FR-02|T không áp dụng tại 2, không tự xóa counter|Setup độc lập; W → E; W → E; đợi 31 giây|W; C|423, 423 giả định|L, L; lần sai tổng thứ ba khóa|R:41–42; GIẢ ĐỊNH counter không tự hết hạn khi chưa khóa, status/body E và L|
|LG-G2-11|ST|FR-02|Biên thời gian ~29 và ~31 giây; K → 0|Setup độc lập; W → E; W → E; W → L, ghi `t0`; chờ tới `t0` + 29 giây|C; chờ tới `t0` + 31 giây; C; W; W; C|423 giả định; 200; 400, 400 giả định; 200|L ở ~29 giây, S ở ~31 giây; E, E, S chứng minh chuỗi sau hết khóa bắt đầu lại|R:41–43; A:32; GIẢ ĐỊNH thời điểm khóa gần response thứ ba, reset counter, không gia hạn khi thử, status/body|
|LG-G2-12|ST|FR-02|Khóa A không ảnh hưởng B|Setup độc lập tạo A và B; W → E; W → E; W → L cho A|CB; C ngay sau đó cho A|200; 423 giả định|B nhận S; A vẫn nhận L, không JWT|R:42–43; A:32; GIẢ ĐỊNH khóa theo từng tài khoản và status/body L|

**Ghi chú của AI:**
- Các phép chờ khi chưa khóa và reset counter sau thành công/hết khóa là giả định cần audit; FR-02 không nêu vòng đời counter chi tiết.
- Sai trong lúc khóa có tăng counter hoặc kéo dài thời hạn không được đặc tả; các test chọn giả định không gia hạn, không coi là quan sát.
- HTTP 400/423, cấu trúc thông báo và mốc `t0` là giả định; timing mạng có thể ảnh hưởng phép đo gần biên 29/31 giây.
- Bằng chứng counter dùng hành vi khóa, không khẳng định quan sát trực tiếp giá trị nội bộ; đăng ký dùng body API mẫu dù FR-01 còn yêu cầu xác nhận mật khẩu.
