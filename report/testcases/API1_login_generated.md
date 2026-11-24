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

## G3 – Security

- **SEC-05:** Áp dụng cho login bằng payload SQL ở cả email và password; kiểm tra không vượt xác thực, không lộ lỗi CSDL và tài khoản vẫn dùng được.
- **SEC-01:** Áp dụng bằng kiểm tra response login không lộ plaintext hay hash; đây là suy luận bảo mật, không chứng minh cách lưu password.
- **FR-02 chống dò email:** Áp dụng bằng so sánh status và thông điệp giữa email không tồn tại và password sai; sự đồng nhất là diễn giải bảo mật cần audit.
- **JWT:** Áp dụng bằng giải mã payload không cần secret và đối chiếu ID đăng ký, role user; tên claim và role mặc định là giả định.
- **FR-02 brute force:** Áp dụng bằng ba lần sai rồi thử mật khẩu đúng ngay trong thời gian khóa.
- **Input độc hại khác:** Áp dụng bằng chuỗi 10.000 ký tự, ký tự điều khiển và object/array ở hai trường xác thực.

**Setup chung độc lập:** Mỗi dòng lấy UUID v4 mới bằng `pm.variables.replaceIn('{{$guid}}')`, đặt `email` = ID dòng viết thường + `-` + UUID + `@test.com`, `password` = `Test1234!`; đăng ký bằng `POST /api/register`, `Content-Type: application/json`, không Authorization, body `{"name":"LG Security","email":"{{email}}","password":"Test1234!"}`. Cần HTTP 200 và lưu `id` từ response đăng ký; nếu setup thất bại, dừng case. Không dùng kết quả case khác.

**Quy ước request trong G3:** Mọi login là `POST /api/login`, `Content-Type: application/json`, không Authorization; `C` là body `{"email":"{{email}}","password":"Test1234!"}`, `W` là `{"email":"{{email}}","password":"Wrong123!"}`. Sau từng tấn công không gây khóa, gửi C: HTTP 200, body có JWT `token`, `user`; đối chiếu `user.id` với `id` đăng ký (tên field là **GIẢ ĐỊNH**) để kiểm tra dữ liệu tài khoản không bị thay đổi và không xác thực nhầm. Với case khóa, kiểm tra bằng C sau khi hết khóa như dòng tương ứng. Tạo `longEmail` = `'a'.repeat(9991) + '@test.com'`, `longPassword` = `'a'.repeat(10000)`; cả hai dài đúng 10.000 ký tự. **E**: HTTP 400 **GIẢ ĐỊNH**, body có thông báo lỗi không rỗng, không `token`, không chứa `SQLITE`, `SQL syntax`, stack trace hoặc câu SQL; status và schema lỗi chưa được spec quy định. Các phép so sánh text không phân biệt hoa/thường. Không khẳng định test black-box chứng minh truy vấn đã parameterize.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
|LG-G3-01|SEC|SEC-05, FR-02|SQL tautology tại email|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"' OR '1'='1","password":"Wrong123!"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:282,40–43; A:32; GIẢ ĐỊNH status/body E và `user.id`|
|LG-G3-02|SEC|SEC-05, FR-02|SQL comment tại email|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"admin@eshop.com'--","password":"Wrong123!"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:282,40–43; A:32; GIẢ ĐỊNH status/body E và `user.id`|
|LG-G3-03|SEC|SEC-05, FR-02|SQL UNION tại email|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"' UNION SELECT NULL--","password":"Wrong123!"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:282,40–43; A:32; GIẢ ĐỊNH status/body E và `user.id`|
|LG-G3-04|SEC|SEC-05, FR-02|SQL tautology tại password|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"{{email}}","password":"' OR '1'='1"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:282,40–43; A:32; GIẢ ĐỊNH status/body E và `user.id`|
|LG-G3-05|SEC|SEC-05, FR-02|SQL UNION tại password|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"{{email}}","password":"' UNION SELECT NULL--"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:282,40–43; A:32; GIẢ ĐỊNH status/body E và `user.id`|
|LG-G3-06|SEC|SEC-01, FR-02|Không lộ password trong response thành công|Setup chung|C|200|Có token và user; duyệt đệ quy toàn response JSON: không có key chứa `password`, `passwd` hoặc `hash`, không có giá trị bằng `Test1234!`; không có plaintext/hash mật khẩu|R:278,43; A:32; GIẢ ĐỊNH loại password/hash khỏi response là suy luận bảo mật, không chứng minh storage|
|LG-G3-07|SEC|FR-02|Chống dò email bằng so sánh lỗi|Setup chung; `absentEmail` = `absent-` + email, GIẢ ĐỊNH namespace UUID này chưa tồn tại|`POST /api/login`; JSON; không Authorization; `{"email":"{{absentEmail}}","password":"Wrong123!"}`; W; C|400, 400 giả định; 200|Hai lỗi E có cùng status và cùng thông điệp không rỗng, không JWT; C xác nhận tài khoản còn nguyên|R:42; A:32; GIẢ ĐỊNH cùng thông điệp áp dụng cả email chưa tồn tại, status/body E và `user.id`|
|LG-G3-08|SEC|FR-02|JWT đúng cấu trúc và danh tính user|Setup chung|C|200|`token` có đúng 3 phần ngăn bởi dấu chấm; base64url-decode và parse JSON phần giữa; payload `id` bằng `id` đăng ký, `role` bằng `user`; `user.id` bằng `id` đăng ký|R:43,176–179; A:21,32; GIẢ ĐỊNH tên claim `id`, `role`, kiểu so sánh ID và role mặc định user; decode không xác minh chữ ký|
|LG-G3-09|SEC|FR-02|Khóa chặn mật khẩu đúng sau brute force|Setup chung|W; W; W; C ngay; chờ 31 giây từ response W thứ ba; C|400, 400, 423, 423 giả định; 200|Hai E; lần ba và C trong khóa không JWT, có thông báo phù hợp không lộ nguyên nhân; C sau chờ trả JWT và đúng `user.id`|R:41–43; A:32; GIẢ ĐỊNH status lỗi, mốc đo và thử trong khóa không gia hạn khóa, `user.id`|
|LG-G3-10|SEC|FR-02|Email độc hại 10.000 ký tự|Setup chung; tạo `longEmail` theo quy ước|`POST /api/login`; JSON; không Authorization; `{"email":"{{longEmail}}","password":"Test1234!"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:40–43; A:25–32; GIẢ ĐỊNH từ chối input dài, status/body E và `user.id`|
|LG-G3-11|SEC|FR-02|Password độc hại 10.000 ký tự|Setup chung; tạo `longPassword` theo quy ước|`POST /api/login`; JSON; không Authorization; `{"email":"{{email}}","password":"{{longPassword}}"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:40–43; A:25–32; GIẢ ĐỊNH status/body E và `user.id`|
|LG-G3-12|SEC|FR-02|Ký tự điều khiển trong email|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"\u0000{{email}}\n","password":"Test1234!"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:40–43; A:25–32; GIẢ ĐỊNH không normalize chuỗi này thành email hợp lệ, status/body E và `user.id`|
|LG-G3-13|SEC|FR-02|Ký tự điều khiển trong password|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"{{email}}","password":"Test1234!\u0000\n"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:40–43; A:25–32; GIẢ ĐỊNH phân biệt password nguyên văn, status/body E và `user.id`|
|LG-G3-14|SEC|FR-02, SEC-05|Object kiểu toán tử thay email|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":{"$ne":null},"password":"Wrong123!"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:40–43,282; A:25–32; GIẢ ĐỊNH từ chối object, status/body E và `user.id`|
|LG-G3-15|SEC|FR-02, SEC-05|Object kiểu toán tử thay password|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"{{email}}","password":{"$ne":null}}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:40–43,282; A:25–32; GIẢ ĐỊNH từ chối object, status/body E và `user.id`|
|LG-G3-16|SEC|FR-02|Array thay email|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":["{{email}}"],"password":"Test1234!"}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:40–43; A:25–32; GIẢ ĐỊNH từ chối array, status/body E và `user.id`|
|LG-G3-17|SEC|FR-02|Array thay password|Setup chung|`POST /api/login`; JSON; không Authorization; `{"email":"{{email}}","password":["Test1234!"]}`; sau đó C|400 giả định; 200|E; C xác nhận tài khoản riêng còn nguyên|R:40–43; A:25–32; GIẢ ĐỊNH từ chối array, status/body E và `user.id`|

**Ghi chú của AI:**
- Status/schema lỗi, trường `user.id`, JWT claims và role mặc định không được spec định nghĩa; các lựa chọn là giả định cần audit.
- Không thể xác nhận mọi hash mật khẩu tùy ý hoặc phương pháp lưu qua API black-box; kiểm tra key nhạy cảm và plaintext chỉ phát hiện phần rò rỉ tương ứng.
- So sánh lỗi chống dò email và không lộ lỗi CSDL thô là diễn giải bảo mật; email vắng mặt dựa vào namespace UUID giả định.
- Kiểm tra sau tấn công xác nhận tài khoản riêng vẫn đăng nhập được, không chứng minh toàn bộ dữ liệu CSDL không đổi; lockout có sai số thời gian mạng.

## G4 – Schema validation

Schema 200 dưới đây chỉ bắt buộc `token` và `user` theo A:32. `message`, `user.id`, `user.name`, `user.email`, `user.role` là **quan sát, spec không nói** (phân tích 4.1–4.2); kiểu và enum được kiểm tra nếu xuất hiện là **GIẢ ĐỊNH**. `user` là object và token không rỗng là **GIẢ ĐỊNH** từ mô tả thông tin user/JWT. Cấm `password` tại root và trong user là suy luận bảo mật, không phải hợp đồng response tường minh của SEC-01. Các field khác không bị cấm bởi schema; kiểm tra nhạy cảm đệ quy ở bảng bổ sung phạm vi này.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["token", "user"],
  "not": {"required": ["password"]},
  "properties": {
    "message": {"type": "string"},
    "token": {"type": "string", "minLength": 1},
    "user": {
      "type": "object",
      "not": {"required": ["password"]},
      "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "role": {"type": "string", "enum": ["user", "admin"]}
      }
    }
  }
}
```

Schema lỗi dưới đây là **GIẢ ĐỊNH**: R:42 chỉ yêu cầu thông báo phù hợp không lộ nguyên nhân, không quy định object hay tên và kiểu `error`. Áp dụng cùng schema cho các status lỗi giả định 400, 401, 403.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["error"],
  "properties": {
    "error": {"type": "string", "minLength": 1}
  }
}
```

**Setup độc lập cho từng dòng:** tạo UUID v4 mới bằng `pm.variables.replaceIn('{{$guid}}')`, đặt `email` = ID dòng viết thường + `-` + UUID + `@test.com`. Gửi `POST /api/register`, `Content-Type: application/json`, không Authorization, body `{"name":"LG Schema","email":"{{email}}","password":"Test1234!"}`; yêu cầu HTTP 200 trước khi tiếp tục, nếu không thì setup thất bại. Không dùng dữ liệu case khác.

**Quy ước riêng G4:** `C` = `POST /api/login`, `Content-Type: application/json`, không Authorization, body `{"email":"{{email}}","password":"Test1234!"}`; `W` = cùng method/path/header với body `{"email":"{{email}}","password":"Wrong123!"}`; `M` = cùng method/path/header với body `{"email":"{{email}}"}`. Schema 200 và schema lỗi là hai khối JSON ngay trên; trong Postman dùng `pm.response.to.have.jsonSchema(schema)` tương ứng. Content-Type kiểm tra media type không phân biệt hoa thường, cho phép tham số charset. Thời gian dùng `pm.response.responseTime`.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
|LG-G4-01|SCH|FR-02|Status, media type và schema thành công|Setup độc lập|C|200|Content-Type media type `application/json`; parse JSON và khớp schema 200; `token` là string không rỗng, có `user`|A:25–32; GIẢ ĐỊNH response Content-Type, object user và các ràng buộc schema chưa nêu|
|LG-G4-02|SCH|FR-02|Kiểu từng field user|Setup độc lập|C|200|Schema 200 khớp; `user.id` tồn tại và là integer, `user.name` và `user.email` tồn tại và là string; `user.role` tồn tại và thuộc `user`, `admin`; `token` là string không rỗng|A:32; phân tích 4.1–4.2: field quan sát, spec không nói; GIẢ ĐỊNH các field bắt buộc và kiểu/enum|
|LG-G4-03|SCH|SEC-01, FR-02|Không lộ field nhạy cảm|Setup độc lập|C|200|Schema 200 khớp; duyệt đệ quy object/array, không key chứa `password`, `passwd`, `hash` hoặc `reset_token` không phân biệt hoa thường; không giá trị bằng `Test1234!`|R:278; A:32; GIẢ ĐỊNH không tiết lộ dữ liệu này là suy luận bảo mật; không chứng minh cách lưu|
|LG-G4-04|SCH|FR-02|Schema lỗi sai mật khẩu|Setup độc lập|W|401 giả định|Content-Type `application/json`; parse JSON khớp schema lỗi; `error` string không rỗng, không `token`|R:40–42; GIẢ ĐỊNH 401, JSON, schema lỗi và không cấp token|
|LG-G4-05|SCH|FR-02|Schema lỗi tài khoản khóa|Setup độc lập; gửi W ba lần liên tiếp ngay trước request, giả định lần ba bắt đầu khóa|C ngay trong 30 giây|403 giả định|Content-Type `application/json`; parse JSON khớp schema lỗi; `error` string không rỗng, không `token`, không tiết lộ nguyên nhân chi tiết|R:41–42; GIẢ ĐỊNH 403, JSON, schema lỗi và chặn login đúng trong khóa|
|LG-G4-06|SCH|FR-02|Schema lỗi thiếu password|Setup độc lập|M|400 giả định|Content-Type `application/json`; parse JSON khớp schema lỗi; `error` string không rỗng, không `token`|A:25–31; R:40; GIẢ ĐỊNH thiếu password bị từ chối với 400, JSON và schema lỗi|
|LG-G4-07|SCH|FR-02|Thời gian phản hồi login thành công|Setup độc lập|C|200|Schema 200 khớp; `pm.response.responseTime < 2000` ms|A:32; GIẢ ĐỊNH ngưỡng 2000 ms vì spec không nêu SLA|

**Ghi chú của AI:**
- Các status lỗi, Content-Type response, schema lỗi và ngưỡng thời gian là giả định cần audit; không phải kết quả thực thi.
- Các field user được quan sát không phải yêu cầu bắt buộc theo spec; riêng LG-G4-02 chủ động giả định chúng có mặt để kiểm tra kiểu.
- Quan sát tại phân tích 4.1–4.2 có `user.password`; schema loại field này theo suy luận bảo mật, không khẳng định SUT đã đáp ứng.

## G5 – Tổng hợp độ phủ (reviewer)

Phạm vi: chỉ đọc `API1_login_generated.md` (G1–G4), `report/01_spec_analysis.md`, `eshop-sut/README.md` (FR-02, SEC-01..07) và `eshop-sut/api_specification.md`; không gửi request, không sửa mục G1–G4, không gán nhãn VALID/INVALID/INCOMPLETE. Nguồn dòng theo quy ước cũ: **R** = README, **A** = api_specification.

### 1. Kiểm tra định dạng (đã đọc từng dòng test)

- 61 dòng `LG-Gx-nn`, mỗi dòng đúng 9 cột (đếm 11 trường gồm hai ô rỗng đầu/cuối của Markdown, không có dấu `|` lạc trong ô); không trùng ID: G1 = 25, G2 = 12, G3 = 17, G4 = 7.
- Mọi dòng đều có cột "Nguồn expected" (trích R/A, hoặc GIẢ ĐỊNH kèm lý do). Request dùng macro (`C`, `W`, `M`, `CB`, `S`, `E`, `L`, biến `{{email}}`…) đều được định nghĩa trong cùng mục; method, path, header và body đủ để chuyển thành request Postman. Status đều cụ thể (200/400/423/415/401/403), không có ô "trả lỗi" chung chung.
- **F1 – Mâu thuẫn giả định status giữa các mục** (không thể cùng đúng trên một SUT): (a) "email tồn tại + password sai" là 400 ở LG-G1-15, LG-G1-16, LG-G2-01…, LG-G3-07, nhưng là 401 ở LG-G4-04; (b) "login trong thời gian khóa" là 423 ở LG-G2-03, LG-G2-07, LG-G2-09…12, LG-G3-09, nhưng là 403 ở LG-G4-05. Đoạn dẫn G4 viết "áp dụng cùng schema cho 400, 401, 403" trong khi quy ước E/L ở G1–G3 cố định 400/423. Ít nhất một case trong mỗi cặp có expected status không thể đạt cùng lúc; cần thống nhất một giá trị giả định (hoặc ghi rõ tập chấp nhận) trước Execute.
- **F2 – Tên field lỗi không đồng nhất:** E ở G1–G3 chỉ yêu cầu "có thông báo lỗi" (G1 không yêu cầu không rỗng, không nêu tên field), còn schema lỗi G4 bắt buộc `error` kiểu string không rỗng. Cả hai đều là giả định; kiểm tra G1–G3 yếu hơn G4.
- **F3 – Biểu thức ký hiệu:** cột "Expected body" của G1/G2 dùng ký hiệu S/E/L thay cho predicate viết ra từng dòng; chấp nhận được vì ký hiệu được định nghĩa trong mục, nhưng script Postman phải cài S/E/L một lần cho từng mục.
- Không phát hiện dòng thiếu cột, thiếu nguồn hoặc thiếu request.

### 2. Danh sách trùng (không xóa)

Chỉ tính **nhóm trùng ngữ nghĩa thật**: cùng input/chuỗi request quan sát được, cùng điều kiện expected, một case là tập con hoàn toàn của case kia. Setup đăng ký chung, assertion thành công chung không tính. Các nhóm rời nhau, nên không có trừ chồng.

| Nhóm | Cặp ID | Lý do | ID loại khỏi tổng (đề xuất của AI, sinh viên quyết định) |
|---|---|---|---|
| D1 | LG-G1-01 và LG-G1-14 | Request, status, body và nguồn giống hệt nhau: login đúng email đã đăng ký với `Test1234!`, mong đợi S (HTTP 200); chỉ khác tên mục đích "Email tồn tại" so với "Password đúng". | LG-G1-14 |
| D2 | LG-G3-06 và LG-G4-03 | Cùng request C, cùng kiểm tra đệ quy không có key chứa `password`, `passwd`, `hash`, không có giá trị `Test1234!`, cùng nguồn R:278 + A:32; G4-03 là tập cha (thêm kiểm schema 200, `reset_token`). | LG-G3-06 |
| D3 | LG-G2-01 và LG-G2-02 | Chuỗi request quan sát hoàn toàn trùng: W, W, C với kết quả 400, 400, 200 (G2-02 chỉ chuyển lần W đầu vào Setup); kết luận kiểm tra cũng giống nhau (hai lần sai chưa khóa, đúng sau đó thành công). Khác nhau chỉ ở nhãn cạnh ST. | LG-G2-02 |

**Gần trùng, KHÔNG tính vào số trùng** (khác giá trị đầu vào hoặc khác assertion): LG-G1-13 ~ LG-G3-10 (email 4096 ký tự và 10.000 ký tự); LG-G1-21 ~ LG-G3-11 (password 4096 và 10.000); LG-G1-18 ~ LG-G4-06 (cùng request thiếu password và cùng 400, nhưng G4-06 thêm Content-Type và schema lỗi); LG-G1-01/14 ~ LG-G4-01 ~ LG-G4-02 ~ LG-G4-07 (cùng C → 200, assertion media type, kiểu field, thời gian khác nhau); LG-G2-03 ~ LG-G4-05 (cùng chuỗi W, W, W, C nhưng G4-05 kiểm schema và dùng status khác, xem F1); LG-G2-07 ~ LG-G3-09 (G2-07 có thêm W trong khóa, G3-09 có thêm đối chiếu `user.id`); LG-G1-15 ~ LG-G4-04 (cùng lớp "password sai", assertion khác, status xung đột theo F1).

### 3. Ma trận độ phủ

Cột = nhãn "Kỹ thuật" ghi trong từng test. `∅` = ô trống; `N/A` = không áp dụng, kèm lý do; ô trống quan trọng đánh dấu **[LỖ HỔNG Hn]** và xem mục 5. Dấu † = ID đã bị loại ở mục 2 (vẫn liệt kê để dò vết). Khi một biên được phủ bằng ST thay vì nhãn BVA, ô BVA ghi `∅ (nhãn)` kèm ID phủ ngữ nghĩa.

| # | Yêu cầu / tham số | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|---|
| M01 | Tham số `email` (R:40; A:25–31) | LG-G1-01, 02, 03, 04, 05, 07, 08, 09, 10, 11, 12 | LG-G1-06, 13 | LG-G2-12 (A khóa không ảnh hưởng B); mọi case G2 dùng email riêng | LG-G3-01, 02, 03, 07, 10, 12, 14, 16 | ∅ không quan trọng: không case SCH nào gửi email lỗi; schema lỗi dùng chung đã được LG-G4-04, 05, 06 kiểm bằng các input khác |
| M02 | Tham số `password` (R:40; A:25–31) | LG-G1-14†, 15, 16, 18, 19, 20 | LG-G1-17, 21 | LG-G2-01 (W sai), LG-G2-04 (C đúng) | LG-G3-04, 05, 11, 13, 15, 17 | LG-G4-04, 06 |
| M03 | Body tổng thể và header Content-Type (A:25) | LG-G1-22, 23, 24, 25 | N/A: không có biên số lượng/kích thước body trong spec | N/A: không có trạng thái | N/A: spec không có yêu cầu bảo mật riêng cho body | LG-G4-06 (thiếu field → schema lỗi) |
| M04 | Header Authorization (R:43 ghi header cho request có xác thực; login không yêu cầu) | ∅ **[LỖ HỔNG H4, P3]**: mọi login đều không gửi Authorization | N/A | N/A | ∅ (cùng H4) | N/A |
| M05 | FR-02 tăng bộ đếm đúng 1 sau mỗi lần sai (R:41) | LG-G1-15, 16 (một lần sai) | ∅ (nhãn): biên 1 và 2 phủ ngữ nghĩa bởi LG-G2-01, 02† | LG-G2-01, 02†, 03, 04, 05, 06, 08, 09, 10 | LG-G3-09 | N/A: bộ đếm không nằm trong response theo spec (không bắt buộc field counter) |
| M06 | FR-02 sai ≥ 3 lần liên tiếp thì khóa (R:42), kể cả "liên tiếp" | ∅ (nhãn): không có case EP riêng; phủ bởi ST | ∅ (nhãn): biên 2 chưa khóa, 3 khóa, 4 trong khóa phủ ngữ nghĩa bởi LG-G2-02†, 03, 07 | LG-G2-03, 05, 06 (sai–đúng–sai không cộng dồn), 07, 09, 10, 12 | LG-G3-09 | LG-G4-05 |
| M07 | FR-02 khóa 30 giây rồi mở (R:42) | ∅ (nhãn): phủ bởi ST | ∅ (nhãn): biên ~29 giây bị khóa, ~31 giây mở phủ bởi LG-G2-11 | LG-G2-07, 11 (mở khóa nhưng qua login đúng) **[LỖ HỔNG H1]** | LG-G3-09 | N/A: thời gian khóa không nằm trong response |
| M08 | FR-02 thông báo lỗi phù hợp, không lộ nguyên nhân (R:42) | LG-G1-02, 15, 16 (E) | N/A | LG-G2-03, 07 (L không nêu nguyên nhân) | LG-G3-07 (so sánh email lạ và password sai), LG-G3-09; khóa với email không tồn tại ∅ **[LỖ HỔNG H3]** | LG-G4-04, 05, 06 |
| M09 | FR-02 login đúng trả JWT (R:43; A:32) | LG-G1-01, 10, 11, 12, 14†, 25 | N/A: không có biên cho login đúng | LG-G2-04, 05, 06, 07, 11, 12 (S) | LG-G3-08 (cấu trúc, `id`, `role`) | LG-G4-01, 02, 07 |
| M10 | FR-02 token dùng làm Bearer ở request có xác thực (R:43; A:59, A:62) | ∅ **[LỖ HỔNG H2, P2]** | N/A | ∅ (cùng H2) | ∅ (cùng H2) | N/A |
| M11 | FR-02 email `type="email"` HTML5 (R:44) | LG-G1-03, 04, 05 (chỉ là giả định backend từ chối; UI-only theo R:44) | N/A | N/A | N/A | N/A |
| M12 | SEC-01 không lưu plaintext (R:278) | N/A: không kiểm được storage qua API | N/A | N/A | LG-G3-06† (suy luận: không lộ password/hash trong response) | LG-G4-03 |
| M13 | SEC-02 JWT hợp lệ cho API bảo mật (R:279) | ∅ **[LỖ HỔNG H2]** | N/A | N/A | LG-G3-08 (chỉ giải mã payload, không chứng minh token được API bảo mật chấp nhận) ; thiếu Bearer sai gửi vào login ∅ **[LỖ HỔNG H4]** | N/A |
| M14 | SEC-03 kiểm role admin (R:280): không trực tiếp (login không phải API Admin) | N/A | N/A | N/A | Gián tiếp: LG-G3-08 (role = user). Role từ client trong body login ∅ **[LỖ HỔNG H5, P3]** | N/A |
| M15 | SEC-04 escape khi hiển thị UI (R:281) | N/A: API trả JSON, escape là việc UI; không có contract trong spec cho login | N/A | N/A | N/A (không có case; không áp dụng ở mức API) | N/A |
| M16 | SEC-05 parameterized query (R:282) | N/A | N/A | N/A | LG-G3-01, 02, 03, 04, 05, 14, 15 (kiểm tài khoản còn dùng được sau tấn công) | N/A |
| M17 | SEC-06 không cho client đổi `role` (R:283): áp dụng cho profile, gián tiếp với login | N/A | N/A | N/A | Gián tiếp: LG-G3-08 (role JWT = user); xem H5 | N/A |
| M18 | SEC-07 OTP đặt lại mật khẩu (R:284): không áp dụng | N/A: login không có OTP | N/A | N/A | N/A | N/A |

### 4. Bảng đếm

Đếm theo nhãn "Kỹ thuật" của từng test, sau khi trừ D1, D2, D3 (mỗi nhóm trừ đúng một ID).

| Kỹ thuật | G1 | G2 | G3 | G4 | Tổng thô | ID loại (trùng) | Tổng sau trừ trùng |
|---|---|---|---|---|---|---|---|
| EP | 21 | 0 | 0 | 0 | 21 | LG-G1-14 | 20 |
| BVA | 4 | 0 | 0 | 0 | 4 | không | 4 |
| ST | 0 | 12 | 0 | 0 | 12 | LG-G2-02 | 11 |
| SEC | 0 | 0 | 17 | 0 | 17 | LG-G3-06 | 16 |
| SCH | 0 | 0 | 0 | 7 | 7 | không | 7 |
| **Tổng** | 25 | 12 | 17 | 7 | **61** | 3 | **58** |

**Kết luận: ĐỦ ≥ 35** (58 case sau khi trừ 3 nhóm trùng; 61 theo tổng thô; vượt ngưỡng 35 thêm 23). Không "THIẾU n case". Cả năm kỹ thuật EP, BVA, ST, SEC, SCH đều có case.

### 5. Danh sách lỗ hổng độ phủ (chuyển G6 nếu sinh viên đồng ý)

Các đề xuất dưới đây là đề xuất của AI; trạng thái kỳ vọng lấy từ spec hoặc đánh dấu GIẢ ĐỊNH, không dựa vào hành vi SUT.

| # | Yêu cầu | Vì sao quan trọng | Gợi ý đúng 1 test case (Request đủ chạy) | Ưu tiên |
|---|---|---|---|---|
| H1 | FR-02 R:42 hết 30 giây khóa; ma trận M07 | Cạnh "K + T → 0" ở bảng G2 chỉ được kiểm bằng LG-G2-11, nhưng case đó gọi C đúng (thành công, tự reset) ngay sau khi hết khóa nên không phân biệt "counter reset do hết khóa" với "counter reset do login đúng". Nếu SUT giữ counter = 3 sau khi hết khóa, sai ngay lần W đầu lại khóa lại, và bộ test hiện tại không phát hiện. | `LG-G6-01` (ST): Setup đăng ký `lg-g6-01-{{uuid}}@test.com` / `Test1234!` (HTTP 200); W, W, W → ghi `t0` (lần ba khóa, L); chờ `t0` + 31 giây không gửi request; rồi W → E (400 giả định), W → E, W → L (423 giả định); kiểm thêm C ngay sau cùng → L. Kỳ vọng: sau hết khóa chuỗi sai bắt đầu lại từ 0 (GIẢ ĐỊNH reset khi hết khóa, R:41–42 không nói rõ). | P2 |
| H2 | FR-02 R:43 + SEC-02 R:279; A:59, A:62 | Spec nói token "gửi kèm tất cả các yêu cầu có xác thực" và API bảo mật phải yêu cầu JWT hợp lệ; LG-G3-08 chỉ giải mã phần payload, không chứng minh chữ ký/hạn dùng đủ để API bảo mật chấp nhận. Không case nào dùng token vừa cấp. | `LG-G6-02` (SEC): Setup đăng ký user mới (HTTP 200, lưu `email`); `POST /api/login` body C → 200, lấy `token`; sau đó `GET /api/users/me`, header `Authorization: Bearer {{token}}`, không body. Kỳ vọng: HTTP 200 (GIẢ ĐỊNH, A:62 không nêu status) và thông tin đúng user vừa đăng ký (field email khớp `email`; tên field là GIẢ ĐỊNH). | P2 |
| H3 | FR-02 R:42 "không để lộ chi tiết nguyên nhân"; M08 | LG-G3-07 chỉ so sánh một lần sai. Nếu email tồn tại bị khóa ở lần 3 (423) nhưng email không tồn tại vẫn trả 400 mãi, kẻ tấn công phân biệt được email nào đã đăng ký. Đây là diễn giải bảo mật của R:42, cần audit. | `LG-G6-03` (SEC): Setup độc lập tạo `emailX` đã đăng ký và `absentX` = `absent-` + UUID chưa đăng ký. Gửi tuần tự 4 lần W (password `Wrong123!`) cho `emailX` rồi 4 lần cho `absentX` (không gửi C). Kỳ vọng: chuỗi (status, thông điệp) 4 lần của `absentX` bằng đúng chuỗi của `emailX`, cả hai không có JWT; không giả định số status tuyệt đối (GIẢ ĐỊNH so sánh tương đối). | P2 |
| H4 | R:43 và SEC-02: login không cần token trước (cùng M04) | Tham số header Authorization chưa có case nào; nếu middleware xác thực chặn nhầm login khi client gửi Bearer cũ hoặc sai (ví dụ token hết hạn còn lưu ở client sau logout), người dùng không đăng nhập lại được. | `LG-G6-04` (EP): Setup đăng ký user mới; `POST /api/login`, `Content-Type: application/json`, `Authorization: Bearer invalid.token.value`, body C. Kỳ vọng: HTTP 200 và S (GIẢ ĐỊNH: login không bị chặn bởi token đầu vào; R:43 chỉ nói login sinh token). | P3 |
| H5 | SEC-03 R:280 / SEC-06 R:283 (gián tiếp): role không do client quyết | SEC-06 nói cho API cập nhật hồ sơ, nhưng nếu login nhận trường `role` thừa và đưa vào JWT, user thường có JWT admin. LG-G1-25 chỉ gửi `extra` vô hại. | `LG-G6-05` (SEC): Setup đăng ký user mới; `POST /api/login`, JSON, không Authorization, body `{"email":"{{email}}","password":"Test1234!","role":"admin"}`. Kỳ vọng: nếu trả 200 thì `user.role` (nếu có) bằng `user` và payload JWT `role` bằng `user`; không được là `admin` (GIẢ ĐỊNH tên claim `role`; chấp nhận 400 nếu từ chối field thừa). | P3 |

**Ghi chú của AI (reviewer):**
- Ma trận và số đếm dựa trên nhãn "Kỹ thuật" của từng dòng; một số biên (số lần sai, 29/31 giây) được phủ bằng ST nên ô BVA ghi `∅ (nhãn)` kèm ID phủ ngữ nghĩa, không coi là lỗ hổng.
- Tổng 58 phụ thuộc quyết định của sinh viên về D1–D3; D3 (LG-G2-01 và LG-G2-02) là nhóm dễ gây tranh luận vì hai case gắn nhãn cạnh ST khác nhau dù chuỗi quan sát giống hệt.
- F1 (mâu thuẫn 400/401 và 423/403) ảnh hưởng trực tiếp khả năng thực thi đúng của LG-G4-04 và LG-G4-05, cần giải quyết ở Audit/G6 trước Execute; tôi không sửa các mục G1–G4.
- Không ghi nhãn VALID/INVALID/INCOMPLETE; mọi số liệu trong mục này là kết quả đọc và đếm tài liệu, không có lần chạy SUT.

## G6 – Bổ sung theo G5

**Quy tắc giả định hợp nhất cho toàn tài liệu khi chuyển sang Execute (F1/F2):** sai credentials hoặc input dùng HTTP **400**, đang khóa dùng HTTP **423**; response lỗi JSON có `error` là string không rỗng và không có `token`. Đây là **GIẢ ĐỊNH** chung về status/schema, không phải quy định spec hay kết quả quan sát. Status 401 của LG-G4-04 và 403 của LG-G4-05 là lựa chọn cũ, **không áp dụng khi chuyển sang Execute**: dùng lần lượt 400 và 423; giữ nguyên các mục cũ để truy vết. Các field/claim và vòng đời chưa nêu trong spec đều là GIẢ ĐỊNH như chỉ rõ bên dưới; các kỳ vọng cũ khác vẫn cần audit.

**Setup độc lập từng dòng:** tạo UUID v4 mới bằng `pm.variables.replaceIn('{{$guid}}')`; `email` = ID dòng viết thường + `-` + UUID + `@test.com`. Gửi `POST /api/register`, `Content-Type: application/json`, không Authorization, body `{"name":"LG G6","email":"{{email}}","password":"Test1234!"}`; yêu cầu HTTP 200 và lưu `id` đăng ký, nếu không thì dừng setup. Không dùng dữ liệu case khác. Với LG-G6-03, tạo `absentEmail` = `absent-` + ID dòng viết thường + `-` + UUID v4 mới + `@test.com`; không đăng ký email này, giả định UUID chưa tồn tại.

**Macro chỉ trong G6:** `W` = `POST /api/login`, `Content-Type: application/json`, không Authorization, body `{"email":"{{email}}","password":"Wrong123!"}`; `WA` = như W nhưng email `{{absentEmail}}`; `C` = cùng method/path/header, body `{"email":"{{email}}","password":"Test1234!"}`. Gửi tuần tự và kiểm từng response. `E` = 400, `L` = 423, đều theo schema lỗi giả định hợp nhất ở trên; `S` = 200, có `token` JWT và `user` theo A:32. `t0` là thời điểm nhận response W thứ ba; chờ tới `t0` + 31 giây bằng timer, không gửi login đúng trước khi hết khóa. `ME` = `GET /api/users/me`, header `Authorization: Bearer {{token}}`, không body; lấy `token` từ login thành công ngay trước ME. Body ME có `email` bằng `{{email}}` và `id` bằng `id` đăng ký là GIẢ ĐỊNH tên field/kiểu định danh; HTTP 200 của ME là GIẢ ĐỊNH vì A:62 không nêu status.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
|LG-G6-01|ST|FR-02|H1: phân biệt reset do hết khóa với reset do login thành công|Setup độc lập; không login trước|W; W; W, ghi `t0`; chờ đến `t0` + 31 giây; W; W; W; C ngay|400, 400, 423; 400, 400, 423, 423, tất cả giả định|E, E, L; sau chờ E, E, L, L; không login đúng trước ba lần sai sau chờ; không token ở mọi response|R:41–42; GIẢ ĐỊNH hết khóa reset counter, status/schema lỗi và mốc khóa gần response thứ ba|
|LG-G6-02|SEC|FR-02, SEC-02|H2: JWT mới được API bảo mật chấp nhận và đúng danh tính|Setup độc lập, lưu `id`|C; lưu `token`; ME|200; 200 giả định|S; ME trả JSON có `email` khớp email đăng ký và `id` khớp id đăng ký|R:43,279; A:21,32,59–62; GIẢ ĐỊNH status và field/kiểu ID của ME|
|LG-G6-03|SEC|FR-02|H3: chống dò email sau ba và bốn lần sai|Setup độc lập; tạo `absentEmail` chưa đăng ký theo quy ước|W; W; W ghi `t0`; W ngay; WA; WA; WA; WA ngay; chờ tới `t0` + 31 giây; C; lưu `token`; ME|400, 400, 423, 423; 400, 400, 423, 423 giả định; 200; 200 giả định|Mỗi lỗi có `error` không rỗng, không token; so sánh từng cặp tương ứng: status và chuỗi `error` giống hệt, kể cả lần 3 và 4; C và ME xác nhận tài khoản riêng vẫn đúng danh tính|R:41–43; A:32,59–62; GIẢ ĐỊNH lỗi email vắng mặt có cùng khóa/status/message, namespace UUID chưa tồn tại, không gia hạn khóa khi thử, schema lỗi và ME|
|LG-G6-04|EP|FR-02, SEC-02|H4: Bearer sai không chặn login với credentials đúng|Setup độc lập|`POST /api/login`; `Content-Type: application/json`; `Authorization: Bearer invalid.token.value`; `{"email":"{{email}}","password":"Test1234!"}`; lưu `token`; ME|200 giả định; 200 giả định|S; ME trả đúng email và id đăng ký, chứng minh token mới dùng được|R:43,279; A:32,59–62; GIẢ ĐỊNH bỏ qua Bearer đầu vào không hợp lệ khi login và status/field ME|
|LG-G6-05|SEC|FR-02, SEC-03, SEC-06|H5: role admin do client gửi không nâng quyền user|Setup độc lập; GIẢ ĐỊNH user mới có role `user`|`POST /api/login`; `Content-Type: application/json`; không Authorization; `{"email":"{{email}}","password":"Test1234!","role":"admin"}`; lưu `token`; ME|200 giả định; 200 giả định|S; base64url-decode phần payload JWT thành JSON, `role` bằng `user`, không phải `admin`; nếu `user.role` có mặt thì bằng `user`; ME trả đúng email và id đăng ký, nếu ME có `role` thì bằng `user`|R:43,280,283; A:32,59–62; GIẢ ĐỊNH login bỏ qua field thừa, role mặc định `user`, tên/giá trị claim `role`, field và status ME; SEC-06 áp dụng gián tiếp|

**Ghi chú của AI:**
- H1 giả định counter reset khi hết khóa; H3 diễn giải yêu cầu không lộ nguyên nhân thành so sánh lỗi và giả định tài khoản vắng mặt cũng có chính sách khóa tương đương.
- H4 chọn bỏ qua Bearer sai; H5 chọn thành công và bỏ qua `role` thừa, không khẳng định spec quy định các lựa chọn này. Decode JWT không tự xác minh chữ ký; ME kiểm tra token được API bảo mật chấp nhận.
- G5 tính 58 case sau trừ ba nhóm trùng; năm case G6 có chuỗi/assertion mới, nâng tổng lên **63**, vượt 35. Chưa thực thi SUT; các status/schema và field chưa đặc tả cần audit.
