# API 2 – PUT /api/orders/:id/cancel – Test case do AI sinh

## G1 – Domain partition + boundary

### Lớp tương đương và biên

| Tham số | Lớp / giá trị đại diện | Phân loại để audit | Test |
|---|---|---|---|
| `:id` | ID đơn pending của chính user | Hợp lệ | CN-G1-01 |
| `:id` | ID số nguyên dương không tồn tại | Không tồn tại | CN-G1-02 |
| `:id` | `0` | Biên dưới giả định không hợp lệ | CN-G1-03 |
| `:id` | `-1` | Âm, giả định không hợp lệ | CN-G1-04 |
| `:id` | `2147483648` | Lớn hơn giới hạn số nguyên có dấu 32 bit, chưa quy định giới hạn | CN-G1-05 |
| `:id` | `9999999999` | Số rất lớn, chưa quy định giới hạn | CN-G1-06 |
| `:id` | `1.5` | Thập phân, giả định không hợp lệ | CN-G1-07 |
| `:id` | `abc` | Chữ, giả định không hợp lệ | CN-G1-08 |
| `:id` | `%40` (ký tự `@`) | Ký tự đặc biệt, giả định không hợp lệ | CN-G1-09 |
| `:id` | `%20` (một dấu cách) | Khoảng trắng, giả định không hợp lệ | CN-G1-10 |
| Authorization | Bearer JWT user hợp lệ | Hợp lệ | CN-G1-01 |
| Authorization | Không gửi header | Không hợp lệ | CN-G1-11 |
| Authorization | `Bearer ` không có token | Không hợp lệ | CN-G1-12 |
| Authorization | Scheme `Basic` với JWT hợp lệ | Không hợp lệ | CN-G1-13 |
| Authorization | Bearer JWT bị đổi chữ ký | Không hợp lệ | CN-G1-14 |
| Authorization | `Bearer not-a-jwt` | Không hợp lệ | CN-G1-15 |
| Body | Không có body | Hợp lệ theo endpoint | CN-G1-01 |
| Body | `{"status":"delivered"}` thừa | GIẢ ĐỊNH bỏ qua field thừa | CN-G1-16 |

**Setup độc lập S:** Với mỗi case tạo UUID mới, email `cn_<ID>_<UUID>@test.com` (thay dấu `-` trong ID bằng `_`), dùng password `Test1234!`. Gửi `POST /api/register`, `Content-Type: application/json`, body `{"name":"CN User","email":"<email>","password":"Test1234!"}`; gửi `POST /api/login` cùng content type, body `{"email":"<email>","password":"Test1234!"}`, lưu JWT response thành `T`. Gửi `GET /api/products/1` không body; lấy tên và giá sản phẩm thực tế `N`, `P`. Gửi `POST /api/cart`, `Authorization: Bearer <T>`, `Content-Type: application/json`, body `{"id":1,"name":"<N>","price":<P>,"quantity":1}`. Gửi `POST /api/checkout` cùng headers, body `{"total_amount":<P>,"shipping_address":"123 Le Loi, TP.HCM"}`; lấy ID đơn mới `O` từ response. GIẢ ĐỊNH response checkout cho phép xác định ID và đơn mới là pending; xác nhận bằng `GET /api/orders/<O>` với `Authorization: Bearer <T>`, không body, trước request. Spec chưa định nghĩa schema GET nên đối chiếu trạng thái theo dữ liệu trả về, không giả định tên field. Nếu setup thất bại hoặc không xác định được ID/trạng thái thì đánh dấu không thực thi, không dùng đơn khác.

**Kiểm tra K:** Sau request dùng `GET /api/orders/<O>`, `Authorization: Bearer <T>`, không body, kiểm tra trạng thái đơn theo tiêu chí mỗi dòng; schema GET chưa quy định. Với các ID không tồn tại, trước request đăng nhập admin bằng `POST /api/login`, `Content-Type: application/json`, body `{"email":"admin@eshop.com","password":"Admin123!"}`; dùng JWT admin gửi `GET /api/admin/orders`, `Authorization: Bearer <admin token>`, không body và xác nhận giá trị ID đích không có trong toàn bộ danh sách. Với CN-G1-02 chọn số nguyên dương `A` không có trong danh sách; nếu danh sách không cho phép xác minh toàn bộ thì không thực thi case. CN-G1-05/06 cũng chỉ thực thi khi xác minh ID tương ứng vắng mặt. GIẢ ĐỊNH danh sách admin đủ để xác minh ID, schema không được đặc tả.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| CN-G1-01 | EP | FR-10 | Hủy đơn pending của mình | S | `PUT /api/orders/<O>/cancel`; `Authorization: Bearer <T>`; không body | 200 | K: đơn `canceled`; body success không ràng buộc schema | README FR-10 dòng 150–155; API spec 145–147; GIẢ ĐỊNH 200 vì không nêu status |
| CN-G1-02 | EP | FR-10 | ID dương không tồn tại | S, xác minh `A` vắng mặt theo K | `PUT /api/orders/<A>/cancel`; `Authorization: Bearer <T>`; không body | 404 | Body biểu thị lỗi, không ràng buộc tên field; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH 404 và lỗi vì không quy định ID vắng mặt |
| CN-G1-03 | BVA | FR-10 | ID bằng 0 | S | `PUT /api/orders/0/cancel`; `Authorization: Bearer <T>`; không body | 400 | Body biểu thị lỗi; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH ID dương, 400 và lỗi vì chưa quy định miền ID |
| CN-G1-04 | BVA | FR-10 | ID âm | S | `PUT /api/orders/-1/cancel`; `Authorization: Bearer <T>`; không body | 400 | Body biểu thị lỗi; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH ID dương, 400 và lỗi vì chưa quy định miền ID |
| CN-G1-05 | BVA | FR-10 | ID vượt 32 bit | S, xác minh `2147483648` vắng mặt theo K | `PUT /api/orders/2147483648/cancel`; `Authorization: Bearer <T>`; không body | 404 | Body biểu thị lỗi; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH ID lớn được tra cứu và trả 404 khi vắng mặt, không quy định giới hạn |
| CN-G1-06 | BVA | FR-10 | ID rất lớn | S, xác minh `9999999999` vắng mặt theo K | `PUT /api/orders/9999999999/cancel`; `Authorization: Bearer <T>`; không body | 404 | Body biểu thị lỗi; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH ID lớn được tra cứu và trả 404 khi vắng mặt, không quy định giới hạn |
| CN-G1-07 | EP | FR-10 | ID thập phân | S | `PUT /api/orders/1.5/cancel`; `Authorization: Bearer <T>`; không body | 400 | Body biểu thị lỗi; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH ID nguyên và 400 vì chưa quy định kiểu |
| CN-G1-08 | EP | FR-10 | ID chữ | S | `PUT /api/orders/abc/cancel`; `Authorization: Bearer <T>`; không body | 400 | Body biểu thị lỗi; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH ID nguyên và 400 vì chưa quy định kiểu |
| CN-G1-09 | EP | FR-10 | ID ký tự đặc biệt | S | `PUT /api/orders/%40/cancel`; `Authorization: Bearer <T>`; không body | 400 | Body biểu thị lỗi; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH ID nguyên và 400 vì chưa quy định kiểu |
| CN-G1-10 | EP | FR-10 | ID khoảng trắng | S | `PUT /api/orders/%20/cancel`; `Authorization: Bearer <T>`; không body | 400 | Body biểu thị lỗi; K: O vẫn `pending` | API spec 145–147; GIẢ ĐỊNH ID nguyên và 400 vì chưa quy định kiểu |
| CN-G1-11 | EP | SEC-02 | Thiếu Authorization | S | `PUT /api/orders/<O>/cancel`; không Authorization; không body | 401 | Body biểu thị lỗi xác thực; K: O vẫn `pending` | README SEC-02 dòng 279; API spec 112; GIẢ ĐỊNH 401 và body lỗi vì chưa quy định |
| CN-G1-12 | EP | SEC-02 | Bearer không token | S | `PUT /api/orders/<O>/cancel`; `Authorization: Bearer `; không body | 401 | Body biểu thị lỗi xác thực; K: O vẫn `pending` | README SEC-02 dòng 279; API spec 112; GIẢ ĐỊNH 401 và body lỗi vì chưa quy định |
| CN-G1-13 | EP | SEC-02 | Sai scheme | S | `PUT /api/orders/<O>/cancel`; `Authorization: Basic <T>`; không body | 401 | Body biểu thị lỗi xác thực; K: O vẫn `pending` | README SEC-02 dòng 279; API spec 112; GIẢ ĐỊNH 401 và body lỗi vì chưa quy định |
| CN-G1-14 | EP | SEC-02 | JWT sai chữ ký | S; tạo `Tbad` từ T bằng cách đổi ký tự base64url đầu của phần chữ ký thành `A`, nếu đã là `A` thì đổi thành `B`, giữ nguyên hai phần còn lại | `PUT /api/orders/<O>/cancel`; `Authorization: Bearer <Tbad>`; không body | 401 | Body biểu thị lỗi xác thực; K: O vẫn `pending` | README SEC-02 dòng 279; API spec 112; GIẢ ĐỊNH 401 và body lỗi vì chưa quy định |
| CN-G1-15 | EP | SEC-02 | Token rác | S | `PUT /api/orders/<O>/cancel`; `Authorization: Bearer not-a-jwt`; không body | 401 | Body biểu thị lỗi xác thực; K: O vẫn `pending` | README SEC-02 dòng 279; API spec 112; GIẢ ĐỊNH 401 và body lỗi vì chưa quy định |
| CN-G1-16 | EP | FR-10 | Body thừa không đổi kết quả | S | `PUT /api/orders/<O>/cancel`; `Authorization: Bearer <T>`, `Content-Type: application/json`; body `{"status":"delivered"}` | 200 | K: O là `canceled`, không phải `delivered`; body success không ràng buộc schema | README FR-10 dòng 150–155; API spec 145–147; GIẢ ĐỊNH bỏ qua body thừa và 200 vì spec không định nghĩa |

**Ghi chú của AI:** Spec không định nghĩa miền/kiểu ID, mã HTTP hoặc schema lỗi; các giá trị dự kiến tương ứng là giả định cần audit.
Checkout không nêu trạng thái ban đầu hay schema trả ID; GET không nêu schema trạng thái, nên setup và đối chiếu phụ thuộc dữ liệu API thực tế.
Không có quy định xử lý body thừa; việc bỏ qua nó là giả định. Các phép kiểm tra sau request không chứng minh được toàn bộ dữ liệu hệ thống không đổi.

## G2 – State transition (FR-10)

**Setup S:** Mỗi case và mỗi phép thử cạnh trong case dùng UUID mới; đăng ký `cn_<ID>_<UUID>@test.com` (thay `-` trong ID bằng `_`) bằng `POST /api/register`, `Content-Type: application/json`, body `{"name":"CN User","email":"<email>","password":"Test1234!"}`. Đăng nhập bằng `POST /api/login`, cùng content type, body `{"email":"<email>","password":"Test1234!"}`, lưu JWT `T`. Đăng nhập admin bằng cùng endpoint và content type, body `{"email":"admin@eshop.com","password":"Admin123!"}`, lưu JWT `A`. Gửi `GET /api/products/1`, không body; lấy tên `N`, giá `P`. Gửi `POST /api/cart`, `Authorization: Bearer <T>`, `Content-Type: application/json`, body `{"id":1,"name":"<N>","price":<P>,"quantity":1}`; gửi `POST /api/checkout` cùng headers, body `{"total_amount":<P>,"shipping_address":"123 Le Loi, TP.HCM"}`; lấy ID đơn mới `O`. GIẢ ĐỊNH checkout tạo pending và response cho phép lấy ID; schema chưa được quy định. Dùng K(pending) xác nhận trước khi tiếp tục; nếu không đạt thì dừng phép thử.

**Quy ước request:** `U` = `PUT /api/orders/<O>/cancel`, `Authorization: Bearer <T>`, không body. `A(s)` = `PUT /api/admin/orders/<O>/status`, `Authorization: Bearer <A>`, `Content-Type: application/json`, body `{"status":"<s>"}`. `K(s)` = `GET /api/orders/<O>`, `Authorization: Bearer <T>`, không body; kiểm tra status HTTP 200 và trạng thái đơn bằng `s`. `D(s)` dựng nguồn từ pending bằng `A(confirmed)`, tiếp `A(shipping)`, tiếp `A(delivered)` theo thứ tự đến s; với canceled dùng U từ pending, với pending không gửi gì. Sau từng bước dựng phải K trạng thái tương ứng, nếu không đạt thì dừng. Các phép thử ma trận trong cùng case lặp lại S riêng cho mỗi đích, không dùng lại đơn.

**Ma trận 5×5:** `H` hợp lệ; `X` không hợp lệ; `A` là Admin qua endpoint status, `U` là User qua endpoint cancel. Mỗi ô trỏ trực tiếp case kiểm tra; mỗi ô ghi nguồn README FR-10. `GĐ` đánh dấu cách diễn giải chưa chắc chắn. Ngoài các cạnh vẽ trong sơ đồ, kỳ vọng từ chối dựa trên dòng 162; self-transition là GĐ vì spec không nêu rõ. Quyền Admin hủy shipping mơ hồ: kỳ vọng từ chối chỉ là GĐ từ sơ đồ.

| Nguồn \ Đích | pending | confirmed | shipping | delivered | canceled |
|---|---|---|---|---|---|
| pending | X GĐ A CN-G2-06, dòng 145–155,162 | H A CN-G2-06, dòng 145–148 | X A CN-G2-06, dòng 145–155,162 | X A CN-G2-06, dòng 145–155,162 | H A CN-G2-06 và U CN-G2-01, dòng 150–155 |
| confirmed | X A CN-G2-07, dòng 145–155,162 | X GĐ A CN-G2-07, dòng 145–155,162 | H A CN-G2-07, dòng 145–148 | X A CN-G2-07, dòng 145–155,162 | H A CN-G2-07 và U CN-G2-02, dòng 150–155 |
| shipping | X A CN-G2-08, dòng 145–155,162 | X A CN-G2-08, dòng 145–155,162 | X GĐ A CN-G2-08, dòng 145–155,162 | H A CN-G2-08, dòng 145–148 | X GĐ A CN-G2-08, X U CN-G2-03, dòng 145–155,161–162 |
| delivered | X A CN-G2-09, dòng 160–162 | X A CN-G2-09, dòng 160–162 | X A CN-G2-09, dòng 160–162 | X GĐ A CN-G2-09, dòng 160–162 | X A CN-G2-09 và U CN-G2-04, dòng 160–162 |
| canceled | X A CN-G2-10, dòng 160–162 | X A CN-G2-10, dòng 160–162 | X A CN-G2-10, dòng 160–162 | X A CN-G2-10, dòng 160–162 | X GĐ A CN-G2-10 và U CN-G2-05, dòng 160–162 |

**Expected chung:** GIẢ ĐỊNH thành công HTTP 200, lỗi HTTP 400, GET HTTP 200 và GET cho phép xác định trạng thái vì spec không định nghĩa status/schema. Body lỗi phải chứa thông báo phù hợp, không áp đặt field hay chuỗi; body thành công không áp đặt schema. K được thực hiện sau từng request trong chuỗi. `A[đích]` trong các case ma trận nghĩa là thực hiện từng `A(s)` với `s` thuộc danh sách đích, mỗi đích dựng S và D độc lập như trên.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| CN-G2-01 | ST | FR-10 | User hủy pending | S; D(pending) | U | 200 | K(canceled) | README 150–155; GIẢ ĐỊNH status/schema |
| CN-G2-02 | ST | FR-10 | User hủy confirmed | S; D(confirmed) | U | 200 | K(canceled) | README 150–155; GIẢ ĐỊNH status/schema |
| CN-G2-03 | ST | FR-10 | User không hủy shipping | S; D(shipping) | U | 400 | Body lỗi; K(shipping) | README 161–162; GIẢ ĐỊNH status/schema |
| CN-G2-04 | ST | FR-10 | User không hủy delivered | S; D(delivered) | U | 400 | Body lỗi; K(delivered) | README 160–162; GIẢ ĐỊNH status/schema |
| CN-G2-05 | ST | FR-10 | Hủy hai lần liên tiếp | S; D(pending) | U; K(canceled); U | 200; 400 | Lần hai có body lỗi; K(canceled) | README 150–155,160–162; GIẢ ĐỊNH tự chuyển bị từ chối, status/schema |
| CN-G2-06 | ST | FR-10 | Các cạnh từ pending | S; D(pending) riêng cho từng đích | A[pending, confirmed, shipping, delivered, canceled] | 400, 200, 400, 400, 200 tương ứng | Lỗi có thông báo; K lần lượt pending, confirmed, pending, pending, canceled | README 145–155,162; GIẢ ĐỊNH self-transition, status/schema |
| CN-G2-07 | ST | FR-10 | Các cạnh từ confirmed | S; D(confirmed) riêng cho từng đích | A[pending, confirmed, shipping, delivered, canceled] | 400, 400, 200, 400, 200 tương ứng | Lỗi có thông báo; K lần lượt confirmed, confirmed, shipping, confirmed, canceled | README 145–155,162; GIẢ ĐỊNH self-transition, status/schema |
| CN-G2-08 | ST | FR-10 | Các cạnh từ shipping | S; D(shipping) riêng cho từng đích | A[pending, confirmed, shipping, delivered, canceled] | 400, 400, 400, 200, 400 tương ứng | Lỗi có thông báo; K lần lượt shipping, shipping, shipping, delivered, shipping | README 145–155,161–162; GIẢ ĐỊNH self-transition, Admin không hủy shipping, status/schema |
| CN-G2-09 | ST | FR-10 | Các cạnh từ delivered | S; D(delivered) riêng cho từng đích | A[pending, confirmed, shipping, delivered, canceled] | 400 cho từng đích | Mỗi body lỗi; mỗi K(delivered) | README 160–162; GIẢ ĐỊNH self-transition, status/schema |
| CN-G2-10 | ST | FR-10 | Các cạnh từ canceled, gồm Admin thử confirmed, shipping, delivered | S; D(canceled) riêng cho từng đích | A[pending, confirmed, shipping, delivered, canceled] | 400 cho từng đích | Mỗi body lỗi; mỗi K(canceled) | README 160–162; GIẢ ĐỊNH self-transition, status/schema |
| CN-G2-11 | ST | FR-10 | Chuỗi pending → confirmed → hủy | S; D(pending) | A(confirmed); K(confirmed); U | 200; 200 | K(canceled) | README 145–155; GIẢ ĐỊNH status/schema |
| CN-G2-12 | ST | FR-10 | Chuỗi confirmed → shipping → User hủy | S; D(confirmed) | A(shipping); K(shipping); U | 200; 400 | Lần hủy có body lỗi; K(shipping) | README 145–148,161–162; GIẢ ĐỊNH status/schema |
| CN-G2-13 | ST | FR-10 | Hủy không đổi đơn khác | S; tạo đơn O2 khác O bằng cách lặp POST cart và checkout như S với cùng T, N, P; GET `/api/orders/<O2>` Bearer T xác nhận pending | U; `GET /api/orders/<O2>`, `Authorization: Bearer <T>`, không body | 200; 200 | K(canceled); O2 vẫn pending | API spec 143,145–147; GIẢ ĐỊNH chỉ đơn đích đổi, trạng thái ban đầu và status/schema |

**Ghi chú của AI:** Self-transition và tính idempotent chưa được định nghĩa; kỳ vọng từ chối là giả định cần audit.
Quyền Admin hủy shipping mơ hồ: sơ đồ không có cạnh nhưng dòng 161 không nêu rõ loại thao tác Admin.
Mã HTTP, schema lỗi, schema GET/checkout và trạng thái ban đầu checkout chưa được đặc tả; các giả định được đánh dấu ở trên.

## G3 – Security

**Áp dụng thế nào:**
- IDOR / FR-11: B thử hủy đơn A ở `pending` và `confirmed`, rồi A đọc lại đơn; ownership khi hủy là giả định bảo mật, FR-11 chỉ nói quyền xem.
- SEC-02: thử thiếu JWT, JWT hết hạn, sai chữ ký và JWT của user bị xóa; xác minh đơn không đổi.
- Token giả mạo: tự ký JWT mang id A với secret đoán, kiểm tra không được xác thực.
- SEC-05: đưa từng payload SQL vào path, đối chiếu hai đơn riêng sau mỗi lần và kiểm tra không lộ lỗi CSDL.
- Admin dùng endpoint User: thử token admin với đơn của A; quyền sử dụng endpoint này chưa được đặc tả rõ.
- Dò ID: so sánh phản hồi với hai ID liên tiếp thuộc A và ID không tồn tại đã xác minh; không phân biệt là giả định chống rò rỉ.

**Setup độc lập S3:** Mỗi case sinh UUID mới; tạo hai user A, B bằng `POST /api/register`, `Content-Type: application/json`, body lần lượt `{"name":"CN A","email":"cn_<ID>_<UUID>_a@test.com","password":"Test1234!"}` và `{"name":"CN B","email":"cn_<ID>_<UUID>_b@test.com","password":"Test1234!"}` (thay `-` trong ID bằng `_`); lưu `id` A từ response đăng ký. Đăng nhập từng user bằng `POST /api/login`, `Content-Type: application/json`, body `{"email":"<email tương ứng>","password":"Test1234!"}`, lưu JWT `TA`, `TB`; đăng nhập admin bằng cùng endpoint/header, body `{"email":"admin@eshop.com","password":"Admin123!"}`, lưu `TM`. `GET /api/products/1`, không body, lấy tên `N` và giá `P`; hai lần lần lượt gửi `POST /api/cart`, `Authorization: Bearer <TA>`, `Content-Type: application/json`, body `{"id":1,"name":"<N>","price":<P>,"quantity":1}`, rồi `POST /api/checkout` cùng headers, body `{"total_amount":<P>,"shipping_address":"123 Le Loi, TP.HCM"}`; lưu hai ID đơn mới `O1`, `O2`. Dùng `GET /api/orders/<O1>` và `GET /api/orders/<O2>`, `Authorization: Bearer <TA>`, không body, xác nhận cả hai `pending`; nếu không dựng được thì dừng case. GIẢ ĐỊNH checkout ban đầu pending và có thể xác định ID/trạng thái từ response; spec chưa định nghĩa schema.

**Kiểm tra K:** Sau mỗi request tấn công, `GET /api/orders/<O1>` và `GET /api/orders/<O2>`, `Authorization: Bearer <TA>`, không body; kỳ vọng HTTP 200, trạng thái lần lượt như trước tấn công. Với case user A bị xóa, thay hai GET bằng `GET /api/admin/orders`, `Authorization: Bearer <TM>`, không body, đối chiếu hai ID và trạng thái trước/sau; GIẢ ĐỊNH danh sách admin đủ để đối chiếu. Nếu không truy xuất được thì không thể kết luận trạng thái. Status GET, schema lỗi và status từ chối dưới đây đều là GIẢ ĐỊNH vì spec không quy định; body lỗi cần biểu thị từ chối, không ràng buộc tên field.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| CN-G3-01 | SEC | FR-10, FR-11 | B hủy đơn A pending | S3 | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TB>`; không body | 403 | Body biểu thị từ chối; K: cả hai pending | README FR-11 166, FR-10 150–155; GIẢ ĐỊNH quyền sở hữu khi hủy và 403 |
| CN-G3-02 | SEC | FR-10, FR-11 | B hủy đơn A confirmed | S3; `PUT /api/admin/orders/<O1>/status`, `Authorization: Bearer <TM>`, `Content-Type: application/json`, body `{"status":"confirmed"}`; GET O1 với TA xác nhận confirmed | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TB>`; không body | 403 | Body biểu thị từ chối; K: O1 confirmed, O2 pending | README FR-11 166, FR-10 145–155; GIẢ ĐỊNH quyền sở hữu khi hủy và 403 |
| CN-G3-03 | SEC | SEC-02 | Không token | S3 | `PUT /api/orders/<O1>/cancel`; không Authorization; không body | 401 | Body biểu thị lỗi xác thực; K: cả hai pending | README SEC-02 279; API spec 112; GIẢ ĐỊNH 401 |
| CN-G3-04 | SEC | SEC-02 | Token hết hạn | S3; giải mã payload TA không cần xác thực, lấy `exp` nếu có; đợi qua mốc Unix `exp` rồi dùng TA cũ; nếu không có `exp` hoặc không thể chờ thì không thực thi; đăng nhập lại A sau khi hết hạn lấy `TA` mới chỉ cho K | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <JWT A cũ đã hết hạn>`; không body | 401 | Body biểu thị lỗi xác thực; K: cả hai pending | README SEC-02 279; GIẢ ĐỊNH token có `exp`, hết hạn bị từ chối và 401; spec không nêu lifetime |
| CN-G3-05 | SEC | SEC-02 | JWT sai chữ ký | S3; đổi ký tự base64url đầu phần chữ ký TA thành `A`, nếu đã là `A` thì đổi `B`, giữ hai phần còn lại, được `Tbad` | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <Tbad>`; không body | 401 | Body biểu thị lỗi xác thực; K: cả hai pending | README SEC-02 279; GIẢ ĐỊNH 401 |
| CN-G3-06 | SEC | SEC-02 | Token user đã bị xóa | S3; `GET /api/admin/orders`, Bearer TM, lưu snapshot O1/O2; `DELETE /api/admin/users/<id A>`, `Authorization: Bearer <TM>`, không body; `GET /api/admin/users`, Bearer TM, xác nhận A vắng mặt; `GET /api/admin/orders`, Bearer TM, xác nhận hai đơn vẫn pending trước tấn công, nếu không thì dừng | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TA>`; không body | 401 | Body biểu thị lỗi xác thực; K dùng danh sách admin: cả hai pending | README SEC-02 279, FR-19 226–227; GIẢ ĐỊNH xóa user vô hiệu token, đơn còn tồn tại và 401 |
| CN-G3-07 | SEC | SEC-02 | JWT tự ký bằng secret đoán | S3; tạo JWT HS256 header `{"alg":"HS256","typ":"JWT"}`, payload `{"id":<id A>,"role":"user"}`, ký HMAC-SHA256 bằng UTF-8 `secret`, mã hóa base64url không padding; gọi `Tforge` | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <Tforge>`; không body | 401 | Body biểu thị lỗi xác thực; K: cả hai pending | README SEC-02 279; GIẢ ĐỊNH secret đoán không phải secret hợp lệ, claim id/role và 401; thuật toán thực tế không được spec nêu |
| CN-G3-08 | SEC | SEC-05 | SQL OR ở path | S3 | `PUT /api/orders/1%20OR%201%3D1/cancel`; `Authorization: Bearer <TA>`; không body | 400 | Body biểu thị lỗi, không chứa chi tiết SQL, SQLite, stack trace; K: cả hai pending | README SEC-05 282; GIẢ ĐỊNH malformed ID bị từ chối 400 và không lộ lỗi CSDL; black-box không chứng minh parameterized query |
| CN-G3-09 | SEC | SEC-05 | SQL DROP ở path | S3 | `PUT /api/orders/1%3BDROP%20TABLE%20orders/cancel`; `Authorization: Bearer <TA>`; không body | 400 | Body biểu thị lỗi, không chứa chi tiết SQL, SQLite, stack trace; K: cả hai pending và đọc được | README SEC-05 282; GIẢ ĐỊNH malformed ID bị từ chối 400 và không lộ lỗi CSDL |
| CN-G3-10 | SEC | SEC-05 | SQL comment ở path | S3 | `PUT /api/orders/1%27%20--/cancel`; `Authorization: Bearer <TA>`; không body | 400 | Body biểu thị lỗi, không chứa chi tiết SQL, SQLite, stack trace; K: cả hai pending | README SEC-05 282; GIẢ ĐỊNH malformed ID bị từ chối 400 và không lộ lỗi CSDL |
| CN-G3-11 | SEC | FR-10, FR-11 | Admin dùng endpoint User hủy đơn A | S3 | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TM>`; không body | 200 | K: O1 canceled, O2 pending; body thành công không ép schema | README FR-10 150–155; GIẢ ĐỊNH Admin được dùng chính endpoint User cho đơn người khác và 200; spec không nêu endpoint cho actor |
| CN-G3-12 | SEC | FR-11, SEC-02 | Dò ID liên tiếp và ID vắng mặt | S3; xác nhận O1 và O2 là hai số nguyên liên tiếp, nếu không thì dừng; `GET /api/admin/orders`, Bearer TM, không body, xác minh toàn bộ danh sách và chọn số nguyên dương `X` vắng mặt; nếu không xác minh được thì dừng | Lần lượt `PUT /api/orders/<O1>/cancel`, `PUT /api/orders/<O2>/cancel`, `PUT /api/orders/<X>/cancel`; mỗi request `Authorization: Bearer <TB>`, không body; K ngay sau từng request | 404 cho cả ba | Mỗi body biểu thị từ chối và giống nhau về nội dung sau khi loại giá trị ID được phản chiếu; K: cả hai pending sau mỗi request | README FR-11 166, SEC-02 279; GIẢ ĐỊNH ownership khi hủy, 404 thống nhất và body không phân biệt để tránh lộ tồn tại |

**Ghi chú của AI:** FR-11 chỉ quy định xem đơn; ownership khi hủy, quyền Admin tại endpoint User và chính sách chống dò ID là giả định cần audit.
Spec không nêu status, schema lỗi/GET, thời hạn JWT, hành vi xóa user hoặc khả năng giữ đơn sau xóa; các setup phụ thuộc điều kiện kiểm chứng được.
Kiểm tra hai đơn chỉ chứng minh hai đơn đó không đổi; API black-box không tự chứng minh mọi truy vấn đều parameterized.

## G4 – Schema validation

Ba schema draft-07 dưới đây là ứng viên để audit, không phải contract JSON được spec định nghĩa. Cho phép field bổ sung; `properties` không tự yêu cầu field phải hiện diện.

**Schema S-success — response hủy thành công:** `message` là quan sát, spec không nói (báo cáo 01 mục 4.4); kiểu object và kiểu string nếu có `message` là GIẢ ĐỊNH, không bắt buộc field này.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "message": { "type": "string" }
  }
}
```

**Schema S-error — response lỗi:** GIẢ ĐỊNH object có `error` kiểu string vì spec chỉ yêu cầu thông báo phù hợp, không quy định cấu trúc lỗi.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "error": { "type": "string" }
  },
  "required": ["error"]
}
```

**Schema S-order — object đơn từ GET:** các tên field và kiểu đều là GIẢ ĐỊNH, không quan sát GET; enum dựa trên README FR-10 dòng 143–155. Không field nào bắt buộc trong schema vì spec không định nghĩa schema GET. Các case dưới đây kiểm tra riêng `status` hiện diện và bằng giá trị yêu cầu.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "user_id": { "type": "integer" },
    "total_amount": { "type": "number" },
    "status": { "type": "string", "enum": ["pending", "confirmed", "shipping", "delivered", "canceled"] },
    "shipping_address": { "type": "string" },
    "created_at": { "type": "string" }
  }
}
```

**Setup S4 độc lập:** Mỗi case tạo UUID mới, email `cn_<ID>_<UUID>@test.com` (thay dấu `-` trong ID bằng `_`); `POST /api/register`, `Content-Type: application/json`, body `{"name":"CN User","email":"<email>","password":"Test1234!"}`; `POST /api/login` cùng content type, body `{"email":"<email>","password":"Test1234!"}`, lưu `token` là `T`. `GET /api/products/1`, không Authorization, không body, lấy tên `N`, giá `P`; `POST /api/cart`, `Authorization: Bearer <T>`, `Content-Type: application/json`, body `{"id":1,"name":"<N>","price":<P>,"quantity":1}`; `POST /api/checkout` cùng headers, body `{"total_amount":<P>,"shipping_address":"123 Le Loi, TP.HCM"}`, lấy `orderId` là `O`. `GET /api/orders/<O>`, `Authorization: Bearer <T>`, không body, xác nhận `status` là `pending`, nếu không thì dừng. GIẢ ĐỊNH tên field lấy từ response và trạng thái ban đầu; GET chưa có schema đặc tả.

**Quy ước:** `U` là `PUT /api/orders/<O>/cancel`, `Authorization: Bearer <T>`, không body. `K` là `GET /api/orders/<O>`, `Authorization: Bearer <T>`, không body. Đo thời gian từ lúc gửi đến lúc nhận toàn bộ response, không tính setup; `< 2000 ms` là GIẢ ĐỊNH tiêu chí hiệu năng, spec không quy định. Content-Type JSON nghĩa là media type `application/json`, cho phép tham số charset. Các status HTTP và Content-Type là GIẢ ĐỊNH vì spec không quy định.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| CN-G4-01 | SCH | FR-10 | Status, JSON và schema response hủy pending | S4 | U | 200 | Content-Type JSON; body parse JSON và khớp S-success; K: HTTP 200, body `status` bằng `canceled` | API spec 145–147; README 150–155; GIẢ ĐỊNH status, JSON và schema response |
| CN-G4-02 | SCH | FR-10, FR-11 | Schema GET sau hủy và spelling trạng thái | S4; U, giả định HTTP 200 | K | 200 | Content-Type JSON; body parse JSON khớp S-order, có `status` đúng `canceled` | API spec 143,147; README 143–155,167; GIẢ ĐỊNH status, JSON và schema GET |
| CN-G4-03 | SCH | FR-10 | Schema lỗi chuyển đổi sau hủy | S4; U, giả định HTTP 200; K xác nhận `canceled` | U | 400 | Content-Type JSON; body parse JSON khớp S-error với `error` là string; K: HTTP 200, `status` vẫn `canceled` | README 160–162; GIẢ ĐỊNH từ chối tự chuyển, 400, JSON và schema lỗi |
| CN-G4-04 | SCH | SEC-02 | Schema lỗi 4xx khi thiếu token | S4 | `PUT /api/orders/<O>/cancel`; không Authorization; không body | 401 | Content-Type JSON; body parse JSON khớp S-error với `error` là string; K: HTTP 200, `status` vẫn `pending` | README SEC-02 279; API spec 112; GIẢ ĐỊNH 401, JSON và schema lỗi |
| CN-G4-05 | SCH | FR-10 | Thời gian hủy thành công | S4 | U | 200 | Response nhận đầy đủ trong < 2000 ms; Content-Type JSON, body khớp S-success; K: HTTP 200, `status` bằng `canceled` | API spec 145–147; GIẢ ĐỊNH 200, JSON, schema và ngưỡng thời gian vì spec không nêu |
| CN-G4-06 | SCH | FR-10, FR-11 | Thời gian GET sau hủy | S4; U, giả định HTTP 200 | K | 200 | Response nhận đầy đủ trong < 2000 ms; Content-Type JSON, body khớp S-order, `status` bằng `canceled` | API spec 143,147; README 167; GIẢ ĐỊNH 200, JSON, schema và ngưỡng thời gian vì spec không nêu |

**Ghi chú của AI:** Response hủy từng quan sát có `message`, nhưng spec không bắt buộc field đó; S-success chỉ kiểm tra kiểu nếu có.
Schema lỗi, kiểu/tên field GET, mã HTTP, JSON và thời gian phản hồi là giả định cần audit, không phải response đã quan sát.
GET chi tiết chưa được quan sát trong báo cáo bước 0; enum là yêu cầu nghiệp vụ, còn tên field `status` trong JSON là giả định.

## G5 – Tổng hợp độ phủ (reviewer)

Báo cáo rà soát của AI về độ phủ G1–G4 (47 ID). Không sửa và không thêm test vào G1–G4, không gán nhãn VALID/INVALID/INCOMPLETE, không gửi request tới SUT. Nguồn đối chiếu: README FR-10 (dòng 141–162), FR-11 (164–167), FR-20 (233–236), SEC-02 (279), SEC-05 (282), API spec 4.6 (145–147), `report/01_spec_analysis.md` mục 2 và 3.4.

Quy ước ma trận: `∅N` là ô trống vì không áp dụng, có nêu lý do. `∅?` là ô trống ưu tiên thấp, có nêu ID gần nhất. `∅!` là ô trống quan trọng, mã H1–H9 trỏ tới mục 5.5. Mọi ô đều có ID trực tiếp hoặc một trong ba ký hiệu kèm lý do.

### 5.1 Bảng đếm

**Quy tắc trừ trùng:** một nhóm trùng thật là các ID có cùng trạng thái đơn ban đầu, cùng request, cùng status kỳ vọng và cùng phép kiểm tra sau request, chỉ khác nhãn kỹ thuật hoặc cách viết setup. Đếm theo nhóm (hợp các ID), mỗi nhóm giữ 1 ID là ID nhỏ nhất, trừ các ID còn lại. Gần trùng (cùng request nhưng khác oracle) không bị trừ, xem 5.2.

| Kỹ thuật | Tổng ID trước khi trừ | ID bị trừ (trùng thật) | Còn lại |
|---|---|---|---|
| EP | 12 (CN-G1-01, 02, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16) | 0 | 12 |
| BVA | 4 (CN-G1-03, 04, 05, 06) | 0 | 4 |
| ST | 13 (CN-G2-01 đến CN-G2-13) | 3 (CN-G2-01, CN-G2-11, CN-G2-12) | 10 |
| SEC | 12 (CN-G3-01 đến CN-G3-12) | 2 (CN-G3-03, CN-G3-05) | 10 |
| SCH | 6 (CN-G4-01 đến CN-G4-06) | 0 | 6 |
| **Tổng** | **47** | **5 (5 nhóm trùng, mỗi nhóm 2 ID)** | **42** |

| Mục | G1 | G2 | G3 | G4 | Tổng |
|---|---|---|---|---|---|
| ID trước khi trừ | 16 | 13 | 12 | 6 | 47 |
| ID sau khi trừ trùng | 16 | 10 | 10 | 6 | 42 |

- Nếu giữ bản G3 thay vì bản G1 cho hai nhóm bảo mật (D2, D3) thì EP còn 10 và SEC còn 12, tổng vẫn là 42.
- Số phép thử thực tế lớn hơn số ID: CN-G2-06 đến CN-G2-10 mỗi ID gồm 5 phép thử (25 phép thử), CN-G3-12 gồm 3 request. Bảng đếm tính theo ID.
- **Kết luận số lượng: ĐỦ ≥ 35** (42 ID sau khi trừ trùng thật). Tham khảo thêm, không phải quy tắc đếm: nếu gộp cả các cặp gần trùng ở 5.2 thì còn khoảng 32, thấp hơn 35. Danh sách lỗ hổng 5.5 là nguồn bổ sung nếu audit quyết định gộp.

### 5.2 Danh sách trùng

**Trùng thật (đã trừ ở 5.1, không xóa khỏi file):**

| Nhóm | ID | Lý do | Giữ / trừ |
|---|---|---|---|
| D1 | CN-G1-01, CN-G2-01 | Cùng đơn pending của chủ đơn, cùng `PUT /api/orders/<O>/cancel` với Bearer T không body, cùng 200, cùng kiểm tra đơn `canceled`. Chỉ khác nhãn EP và ST | Giữ CN-G1-01, trừ CN-G2-01 |
| D2 | CN-G1-11, CN-G3-03 | Cùng request không Authorization trên đơn pending, cùng 401, cùng kiểm tra đơn vẫn pending. CN-G3-03 chỉ kiểm tra thêm đơn thứ hai | Giữ CN-G1-11, trừ CN-G3-03 |
| D3 | CN-G1-14, CN-G3-05 | Cùng cách tạo JWT sai chữ ký (đổi ký tự base64url đầu của chữ ký), cùng request, cùng 401, cùng kiểm tra pending | Giữ CN-G1-14, trừ CN-G3-05 |
| D4 | CN-G2-02, CN-G2-11 | Cùng đơn confirmed dựng bằng pending rồi Admin confirmed, cùng User hủy, cùng 200, cùng K canceled. CN-G2-11 chỉ viết rõ chuỗi dựng | Giữ CN-G2-02, trừ CN-G2-11 |
| D5 | CN-G2-03, CN-G2-12 | Cùng chuỗi pending, confirmed, shipping, rồi User hủy, cùng 400, cùng K shipping. CN-G2-12 chỉ viết rõ chuỗi dựng | Giữ CN-G2-03, trừ CN-G2-12 |

**Gần trùng (không trừ, khác oracle hoặc khác biến thể đầu vào):**

| Nhóm | ID | Điểm giống | Điểm khác làm cho không bị trừ |
|---|---|---|---|
| N1 | CN-G1-03, CN-G1-04 | Cùng lớp số nguyên không dương, cùng 400 | 0 là biên, -1 là phía âm |
| N2 | CN-G1-05, CN-G1-06 | Cùng ID lớn vắng mặt, cùng 404 | CN-G1-05 sát giới hạn 32 bit |
| N3 | CN-G1-07, 08, 09, 10 | Cùng lớp ID không phải số nguyên, cùng 400 | Khác ký tự (thập phân, chữ, `@`, dấu cách) |
| N4 | CN-G4-01, CN-G4-05 (và nhóm D1) | Cùng request hủy đơn pending | G4-01 kiểm tra schema, G4-05 thêm ngưỡng thời gian |
| N5 | CN-G4-02, CN-G4-06 | Cùng GET sau hủy | G4-06 thêm ngưỡng thời gian |
| N6 | CN-G2-05, CN-G4-03 | Cùng hủy hai lần liên tiếp, lần hai 400 | G4-03 kiểm tra schema lỗi |
| N7 | CN-G4-04 (và nhóm D2) | Cùng request không Authorization | G4-04 kiểm tra schema lỗi |
| N8 | CN-G1-02, CN-G3-12 (request thứ ba) | Cùng ID vắng mặt, cùng 404 | Khác token (T và TB), G3-12 kiểm tra không phân biệt phản hồi |
| N9 | CN-G1-15, CN-G3-05, CN-G3-07 | Cùng lớp JWT không hợp lệ, cùng 401 | Khác cách tạo token (rác, sửa chữ ký, tự ký) |

Số khoảng 32 ở 5.1 là kết quả nếu gộp N1 (-1), N2 (-1), N3 (-3), N4 (-2), N5 (-1), N6 (-1), N7 (-1) vào 42. N8 và N9 không tính.

### 5.3 Ma trận độ phủ

#### 5.3a Các ô bảng 5×5 FR-10 liên quan tới User hủy (cột đích `canceled`)

Endpoint hủy chỉ tạo cạnh tới `canceled`, nên 5 ô cột `canceled` là các ô liên quan. Hai mươi ô còn lại chỉ do Admin qua `PUT /api/admin/orders/:id/status`, nằm ngoài phạm vi User hủy (CN-G2-06 đến CN-G2-10 dựng và kiểm tra chúng). Ô Admin hủy trong cùng cột được đưa vào cột ST.

| Ô (nguồn → canceled) | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|
| pending → canceled (R:151) | CN-G1-01, CN-G1-16 | ∅N: trạng thái là enum rời rạc, biên của `:id` nằm ở 5.3c | CN-G2-01 (trùng CN-G1-01), CN-G2-06 (Admin), CN-G2-13 | CN-G3-01, CN-G3-11 | CN-G4-01, CN-G4-02, CN-G4-05, CN-G4-06 |
| confirmed → canceled (R:151) | ∅?: lớp hợp lệ này chỉ có ở ST, gần nhất CN-G2-02 | ∅N: như trên | CN-G2-02, CN-G2-07 (Admin), CN-G2-11 (trùng CN-G2-02) | CN-G3-02 | ∅?: schema hủy chỉ thử trên pending, gần nhất CN-G4-01 |
| shipping → canceled (User bị cấm, R:161) | ∅?: gần nhất CN-G2-03 | ∅N: như trên | CN-G2-03, CN-G2-08 (Admin, GIẢ ĐỊNH), CN-G2-12 (trùng CN-G2-03) | ∅! H6, H7, H8: gần nhất CN-G3-11, chỉ thử trên pending | ∅! H5: gần nhất CN-G4-03, chỉ thử trên canceled |
| delivered → canceled (R:160) | ∅?: gần nhất CN-G2-04 | ∅N: như trên | CN-G2-04, CN-G2-09 | ∅! H6: gần nhất CN-G3-11, chỉ thử trên pending | ∅?: cùng đường lỗi với H5, gần nhất CN-G4-03 |
| canceled → canceled (R:160) | ∅?: gần nhất CN-G2-05 | ∅N: như trên | CN-G2-05, CN-G2-10 | ∅?: gần nhất CN-G3-01, thử trên pending | CN-G4-03 |

#### 5.3b Theo yêu cầu (FR và SEC)

| Yêu cầu | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|
| FR-10 R:150–155 hủy hợp lệ pending hoặc confirmed | CN-G1-01, CN-G1-16 | ∅N: không có giá trị số | CN-G2-01, CN-G2-02, CN-G2-06, CN-G2-07, CN-G2-11, CN-G2-13 | CN-G3-11 | CN-G4-01, CN-G4-05 |
| FR-10 R:160 trạng thái kết thúc | ∅N: kiểm tra bằng ST | ∅N | CN-G2-04, CN-G2-05, CN-G2-09, CN-G2-10 | ∅! H6 | CN-G4-03 |
| FR-10 R:161 shipping chỉ Admin thao tác | ∅N: kiểm tra bằng ST | ∅N | CN-G2-03, CN-G2-08, CN-G2-12 | ∅! H6, H8 | ∅! H5 |
| FR-10 R:162 chuyển đổi không hợp lệ phải có thông báo | ∅N: kiểm tra bằng ST | ∅N | CN-G2-03, CN-G2-04, CN-G2-05, CN-G2-06, CN-G2-07, CN-G2-08, CN-G2-09, CN-G2-10, CN-G2-12 | ∅N: không phải yêu cầu bảo mật | CN-G4-03 (chỉ canceled, shipping là H5) |
| FR-11 R:166 chỉ xem đơn của mình (ownership khi hủy là GIẢ ĐỊNH) | CN-G1-01 (lớp chủ đơn) | ∅N | ∅! H7: chưa thử người khác trên đơn shipping, delivered, canceled; gần nhất CN-G3-01, CN-G3-02 | CN-G3-01, CN-G3-02, CN-G3-12 | ∅?: H9, gần nhất CN-G4-03, CN-G4-04 |
| FR-11 R:167 và API spec 143: GET đối chiếu trạng thái | ∅N: GET chỉ là công cụ kiểm tra | ∅N | K trong CN-G2-01 đến CN-G2-13 | ∅N | CN-G4-02, CN-G4-06 |
| FR-20 R:236 chỉ hủy khi pending hoặc confirmed | CN-G1-01 | ∅N | CN-G2-01, CN-G2-02, CN-G2-03, CN-G2-04, CN-G2-05 | ∅N: yêu cầu giao diện Mobile, API qua FR-10 | ∅N: không có schema riêng |
| API spec A:147 "chưa giao" (rộng hơn R:161, mơ hồ) | ∅N | ∅N | CN-G2-03, CN-G2-04 | ∅N | ∅N |
| SEC-01 mật khẩu không plaintext | ∅N: cancel không nhận hay trả mật khẩu, hệ thống lưu trữ không kiểm được qua API này | ∅N | ∅N | ∅N | ∅N: CN-G4-01 cho phép field thừa nên không phát hiện lộ dữ liệu, spec không yêu cầu |
| SEC-02 API bảo mật cần JWT hợp lệ | CN-G1-11, CN-G1-12, CN-G1-13, CN-G1-14, CN-G1-15 | ∅N: biên hết hạn nằm ở ST | CN-G3-04 (hết hạn), CN-G3-06 (user bị xóa) | CN-G3-03, CN-G3-04, CN-G3-05, CN-G3-06, CN-G3-07; ∅! H1, H2 | CN-G4-04 |
| SEC-03 API Admin kiểm tra role | ∅N: cancel không phải API Admin | ∅N | ∅N | CN-G3-11 (Admin dùng endpoint User); ∅! H8: API Admin dùng để dựng trạng thái bị User gọi | ∅N |
| SEC-04 escape khi hiển thị UI | ∅N: response cancel là JSON, escape ở UI không kiểm được bằng API | ∅N | ∅N | ∅N: gần nhất CN-G3-12 (so sánh body sau khi bỏ ID phản chiếu) | ∅N |
| SEC-05 parameterized query | CN-G1-07, CN-G1-08, CN-G1-09, CN-G1-10 (ID lạ, không phải payload SQL) | ∅N | ∅N | CN-G3-08, CN-G3-09, CN-G3-10 | ∅N: kiểm tra không lộ SQL đã nằm trong G3 |
| SEC-06 không đổi `role` qua hồ sơ | ∅N: thuộc API hồ sơ, không có trong cancel | ∅N | ∅N | ∅N: leo thang role rồi gọi cancel là tổ hợp, gần nhất CN-G3-11 | ∅N |
| SEC-07 OTP đặt lại mật khẩu | ∅N: không có OTP trong cancel | ∅N | ∅N | ∅N | ∅N |
| FR-12 API Admin cần JWT và role admin | ∅N: cancel không phải API Admin | ∅N | ∅N | CN-G3-11; ∅! H8 | ∅N |

#### 5.3c Theo tham số

| Tham số | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|
| `:id` (path) | CN-G1-01, CN-G1-02, CN-G1-07, CN-G1-08, CN-G1-09, CN-G1-10; ∅! H3 | CN-G1-03, CN-G1-04, CN-G1-05, CN-G1-06; ∅! H4 | ∅N: trạng thái đơn mà ID trỏ tới nằm ở 5.3a | CN-G3-08, CN-G3-09, CN-G3-10, CN-G3-12; ∅! H3 | ∅?: H9, gần nhất CN-G4-03, CN-G4-04 |
| Authorization (header) | CN-G1-01, CN-G1-11, CN-G1-12, CN-G1-13, CN-G1-14, CN-G1-15 | ∅N: biên thời gian hết hạn thuộc CN-G3-04 | CN-G3-04, CN-G3-06 | CN-G3-03, CN-G3-04, CN-G3-05, CN-G3-06, CN-G3-07; ∅! H1, H2 | CN-G4-04 |
| Body | CN-G1-01 (không body), CN-G1-16 (body thừa) | ∅N: spec không mô tả body | ∅N | CN-G1-16 (gán `status` từ client, nhãn EP); ∅?: gửi body thừa trên đơn shipping, gần nhất CN-G1-16 | ∅N: không có contract body |
| Response (đầu ra) | ∅N | CN-G4-05, CN-G4-06 (ngưỡng thời gian, GIẢ ĐỊNH) | ∅N | ∅N | CN-G4-01 đến CN-G4-06 |

### 5.4 Kiểm tra định dạng

| Tiêu chí | Kết quả (đối chiếu bằng đọc, không chạy script) |
|---|---|
| Đủ 9 cột | Cả 47 hàng có 9 ô, tiêu đề giống mẫu. Lệch nhẹ: G1 chứa thêm bảng phân hoạch phụ, G2 chứa thêm ma trận 5×5, trong khi mẫu bước nói một bảng test |
| Precondition dựng được trạng thái | Đạt có điều kiện: S, S3, S4, D(s) đều định nghĩa trong cùng bước và Admin chỉ đi cạnh hợp lệ. Phụ thuộc chưa có trong spec nhưng đã ghi GIẢ ĐỊNH: ID đơn lấy từ response checkout và trạng thái ban đầu pending. `id` user lấy từ response đăng ký có trong API spec dòng 19. Rủi ro thực thi: CN-G3-04 phụ thuộc JWT có `exp` và phải chờ tới hạn, spec không nêu thời hạn nên có thể không bao giờ thực thi được và không có test thay thế; CN-G1-02, 05, 06 và CN-G3-12 chỉ chạy khi `GET /api/admin/orders` cho phép xác minh vắng mặt |
| Expected cụ thể | Status cụ thể ở 47/47. Body: 34/47 chỉ ghi "body biểu thị lỗi" hoặc tương đương (CN-G1-02 đến 15, CN-G2-03 đến 10 và 12, CN-G3-01 đến 10 và 12), 7/47 body thành công không ràng buộc (CN-G1-01, 16, CN-G2-01, 02, 11, 13, CN-G3-11), chỉ 6/47 (G4) có kiểm tra body cụ thể. Vế "biểu thị lỗi" chưa chuyển thành assertion Newman được nếu không tham chiếu S-error |
| Có Nguồn expected | 47/47 có cột nguồn và đều ghi GIẢ ĐỊNH cho phần spec không nêu. Số dòng đối chiếu với README và API spec hiện tại là khớp: README 160–162, 166, 167, 227, 279, 282; API spec 112, 143, 145–147 |
| Mâu thuẫn nội bộ | CN-G3-01 (B hủy đơn của A) kỳ vọng 403, CN-G3-12 (cùng sự kiện, B hủy O1 của A) kỳ vọng 404. Hai kỳ vọng cùng GIẢ ĐỊNH nhưng không thể cùng đạt, cần sinh viên chọn một quy ước khi audit |
| Ký hiệu và setup | Ký hiệu `A` dùng cho nhiều nghĩa: ID vắng mặt (G1), token Admin và hành động `A(s)` (G2), user A (G3). Setup coi mọi bước thành công là 200 (spec không nêu), nên setup có thể hỏng nếu SUT trả 201 hoặc 204 |
| Quyết định đã ghi trong G1–G4 cần audit | CN-G1-03 và CN-G1-04 kỳ vọng 400 còn CN-G1-05 và CN-G1-06 kỳ vọng 404. Cả hai đều là GIẢ ĐỊNH, nhưng 0 và -1 cũng có thể là số nguyên hợp lệ chưa tồn tại (404) |

### 5.5 Danh sách lỗ hổng (đầu vào cho G6)

Mỗi gợi ý chỉ là một dòng mô tả test cần sinh, chưa phải test case. Mọi status kỳ vọng nếu spec không nêu phải là GIẢ ĐỊNH khi G6 viết.

| Mã | Yêu cầu hoặc ô | Vì sao quan trọng | Gợi ý 1 test | Ưu tiên |
|---|---|---|---|---|
| H1 | SEC-02 và `:id`: chưa có test không token trên ID vắng mặt | CN-G1-11 và CN-G3-03 chỉ dùng ID tồn tại, CN-G3-12 chỉ dùng token. Không phân biệt được SUT kiểm tra xác thực trước hay tra cứu đơn trước, nên 404 có thể lộ ID tồn tại cho người chưa đăng nhập | `PUT /api/orders/<X>/cancel` không Authorization, `<X>` được xác minh vắng mặt như CN-G1-02; kỳ vọng 401 (GIẢ ĐỊNH, cùng CN-G1-11); K đơn O vẫn pending | Cao |
| H2 | SEC-02: JWT `alg: none` | Phân tích spec 3.4 nêu tự ký token và alg none. G3-05 và G3-07 chỉ thử chữ ký sai và secret đoán, chưa có token không chữ ký | `PUT /api/orders/<O1>/cancel` với `Bearer <header base64url của {"alg":"none","typ":"JWT"}>.<payload base64url của {"id":<id A>,"role":"user"}>.` (chữ ký rỗng); kỳ vọng 401 (GIẢ ĐỊNH claim giống CN-G3-07); K hai đơn vẫn pending | Cao |
| H3 | `:id` và SEC-05: chuẩn hóa ID lỏng trên đơn thật | CN-G1-07 đến 10 dùng ID không liên quan tới `<O>` nên kiểm tra "O vẫn pending" không phát hiện được SUT cắt chuỗi số rồi hủy đúng hoặc sai đơn. Đây là lỗi thực tế của parse lỏng | `PUT /api/orders/<O>abc/cancel` với Bearer T; kỳ vọng 400 (GIẢ ĐỊNH, cùng CN-G1-08); K đơn O vẫn pending | Cao |
| H4 | BVA `:id` phía trên | CN-G1-05 chỉ thử 2147483648 (ngay trên giới hạn 32 bit), thiếu giá trị biên hợp lệ lớn nhất kề nó nên cặp biên không đầy đủ | `PUT /api/orders/2147483647/cancel` với Bearer T, ID vắng mặt đã xác minh theo K của G1; kỳ vọng 404 (GIẢ ĐỊNH, cùng CN-G1-05); K đơn O vẫn pending | Thấp |
| H5 | FR-10 R:161–162, SCH: thông báo lỗi khi User hủy đơn shipping | Đây là luật cốt lõi nhất của endpoint. Schema S-error chỉ được kiểm tra trên canceled→canceled (CN-G4-03) và 401 (CN-G4-04), còn CN-G2-03 chỉ kiểm "body lỗi" | Setup D(shipping) như CN-G2-03, `PUT /api/orders/<O>/cancel` với Bearer T; kỳ vọng 400 (GIẢ ĐỊNH), Content-Type JSON, body khớp S-error; K đơn vẫn shipping | Trung bình |
| H6 | FR-10 R:160–161, SEC: Admin dùng endpoint User trên đơn delivered hoặc shipping | CN-G3-11 chỉ thử Admin hủy đơn pending. R:160 cấm chuyển khỏi delivered với mọi actor và R:161 mơ hồ về Admin hủy shipping; chưa có test nào kiểm tra cạnh bị cấm qua endpoint User bằng token Admin | Setup đơn delivered (D(delivered)), `PUT /api/orders/<O>/cancel` với Bearer TM (Admin); kỳ vọng 400 (GIẢ ĐỊNH status), K đơn vẫn delivered. Biến thể shipping để audit sau, kỳ vọng là GIẢ ĐỊNH vì R:161 không nói rõ | Trung bình |
| H7 | FR-11 R:166: người khác thử hủy đơn kết thúc hoặc shipping | CN-G3-01 và CN-G3-02 chỉ thử pending và confirmed. Chưa rõ thứ tự kiểm tra quyền sở hữu và kiểm tra trạng thái nên có thể lộ trạng thái đơn của người khác qua mã lỗi | Setup đơn của A ở shipping, `PUT /api/orders/<O>/cancel` với Bearer TB; kỳ vọng từ chối (status cùng quy ước được chọn cho CN-G3-01 và CN-G3-12, GIẢ ĐỊNH); K đơn vẫn shipping | Trung bình |
| H8 | SEC-03 và FR-12 (gián tiếp): User gọi API Admin để vượt R:161 | User không được tự hủy shipping, nhưng nếu API Admin đổi trạng thái không kiểm tra role thì User có thể hủy qua đó. CN-G3-11 chỉ đi chiều Admin dùng endpoint User | Setup đơn shipping của user, `PUT /api/admin/orders/<O>/status` với Bearer T (user thường), body `{"status":"canceled"}`; kỳ vọng 403 (GIẢ ĐỊNH, FR-12 chỉ nói yêu cầu role admin); K đơn vẫn shipping | Trung bình (có thể thuộc API khác) |
| H9 | SCH và `:id`: schema lỗi cho 404 và 403 | G4 chỉ kiểm schema lỗi cho 400 (canceled) và 401; CN-G1-02 và CN-G3-01 chỉ kiểm "biểu thị lỗi" | `PUT /api/orders/<X>/cancel` với Bearer T, `<X>` vắng mặt; kỳ vọng 404 (GIẢ ĐỊNH), Content-Type JSON, body khớp S-error; K đơn O vẫn pending | Thấp |

**Không đề xuất:** kiểm tra race (hai lần hủy đồng thời, hoặc Admin giao hàng khi User hủy) vì spec không cho kết quả tất định; hủy khi có coupon hoặc hoàn kho vì spec FR-10 không nêu tác dụng phụ.

### 5.6 Kết luận

- **Số lượng: ĐỦ ≥ 35** (42 ID sau khi trừ 5 nhóm trùng thật, phân bố EP 12, BVA 4, ST 10, SEC 10, SCH 6).
- **Cần G6: CÓ.** Chín lỗ hổng H1–H9 ở 5.5, trong đó H1, H2, H3 ưu tiên cao. Ngoài ra audit cần quyết định mâu thuẫn CN-G3-01 (403) và CN-G3-12 (404), và vế "body biểu thị lỗi" chưa kiểm tra được bằng Newman.

**Ghi chú của AI:** Ranh giới trùng thật và gần trùng là đánh giá của AI, sinh viên có thể chọn quy tắc khác ở bước Audit và số 42 sẽ thay đổi theo.
Ma trận dùng quan hệ ID trực tiếp; một số ô `∅N` là phán đoán về phạm vi (ví dụ SEC-06 thuộc API hồ sơ), không phải yêu cầu đã được spec khẳng định.
Mọi status trong gợi ý H1–H9 là GIẢ ĐỊNH và cần audit; spec không định nghĩa mã HTTP, schema lỗi hay thứ tự kiểm tra xác thực, quyền sở hữu và trạng thái.

## G6 – Bổ sung theo G5

**Quy ước GIẢ ĐỊNH hợp nhất cho toàn API 2 khi chuyển sang Execute:** Mọi response lỗi được mô tả là “biểu thị lỗi” hoặc tương đương trong G1–G5 và G6 phải có media type `application/json` (cho phép tham số charset), body JSON object với `error` là string không rỗng, không chứa JWT. Response cancel thành công là JSON object có `message` là string không rỗng và trạng thái đích `canceled`; đây là giả định dựa trên quan sát ở báo cáo bước 0, không phải yêu cầu spec. Mã giả định: body/path/state không hợp lệ 400, xác thực 401, thiếu role Admin 403, đơn vắng mặt 404; đơn thuộc người khác trả 404 đối với User không phải Admin. Với User, ưu tiên xác thực → ownership → trạng thái là GIẢ ĐỊNH để thống nhất oracle, không phải spec fact. GIẢ ĐỊNH Admin bỏ qua ownership và có thể dùng endpoint User cancel cho đơn người khác ở pending/confirmed như CN-G3-11; trạng thái vẫn phải được kiểm tra, shipping/delivered/canceled bị từ chối 400. Quyền Admin dùng endpoint này và bỏ qua ownership không được spec quy định. Riêng nghĩa expected của CN-G3-01 và CN-G3-02 chuyển từ 403 thành 404; ba 404 của CN-G3-12 giữ nguyên. Những nội dung G1–G5 không bị sửa.

**Setup độc lập S6:** Mỗi dòng sinh UUID mới và thay `-` trong ID case bằng `_`; đăng ký A và B riêng bằng `POST /api/register`, `Content-Type: application/json`, không Authorization, body lần lượt `{"name":"CN A","email":"cn_<ID>_<UUID>_a@test.com","password":"Test1234!"}` và `{"name":"CN B","email":"cn_<ID>_<UUID>_b@test.com","password":"Test1234!"}`. Đăng nhập từng user bằng `POST /api/login`, `Content-Type: application/json`, không Authorization, body `{"email":"<email tương ứng>","password":"Test1234!"}`, lưu JWT `TA`, `TB`; đăng nhập Admin cùng endpoint và header, body `{"email":"admin@eshop.com","password":"Admin123!"}`, lưu `TM`. `GET /api/products/1`, không Authorization, không body, lấy tên `N` và giá `P`; hai lần, mỗi lần `POST /api/cart`, `Authorization: Bearer <TA>`, `Content-Type: application/json`, body `{"id":1,"name":"<N>","price":<P>,"quantity":1}`, tiếp theo `POST /api/checkout` cùng headers, body `{"total_amount":<P>,"shipping_address":"123 Le Loi, TP.HCM"}`; lưu `orderId` lần lượt `O1`, `O2`, xác nhận khác nhau. Giá trị `P` là giá thực tế cho một sản phẩm; backend phải tự tính tổng theo FR-08. Dùng `GET /api/orders/<O1>` và `GET /api/orders/<O2>`, `Authorization: Bearer <TA>`, không body, xác nhận cả hai `pending`; nếu không đạt dừng case. GIẢ ĐỊNH checkout trả `orderId`, GET trả `status`, đơn mới pending và các bước setup có thể thực hiện; schema chưa quy định.

**D(s):** Với O1, đi lần lượt các cạnh cần thiết qua `PUT /api/admin/orders/<O1>/status`, `Authorization: Bearer <TM>`, `Content-Type: application/json`, body `{"status":"confirmed"}`, rồi `{"status":"shipping"}`, rồi `{"status":"delivered"}`; dừng tại s và GET O1 bằng TA sau mỗi cạnh xác nhận trạng thái. Với `canceled`, thay chuỗi bằng `PUT /api/orders/<O1>/cancel`, `Authorization: Bearer <TA>`, không body, rồi GET xác nhận `canceled`. `D(pending)` không gửi gì. Nếu setup không đạt, dừng case. O2 luôn pending. **K(s):** sau request thử, `GET /api/orders/<O1>` và `GET /api/orders/<O2>`, `Authorization: Bearer <TA>`, không body; giả định HTTP 200, xác nhận `status` lần lượt là s và `pending`. **V(x):** `GET /api/admin/orders`, `Authorization: Bearer <TM>`, không body; xác nhận x không có trong toàn bộ danh sách, nếu không thể xác minh toàn bộ thì dừng. `X` là một số nguyên dương được chọn sau khi nhận danh sách và V(X) thành công.

**E:** response phải có media type JSON như quy ước; parse thành object với `error` string không rỗng, không chứa JWT ở bất kỳ field nào. Mọi request thử dưới đây không body trừ H8. Status, schema lỗi, định dạng `status` khi GET và xác minh toàn bộ danh sách đều là GIẢ ĐỊNH vì spec không quy định. JWT `none` được tạo bằng base64url UTF-8 không padding: `base64url({"alg":"none","typ":"JWT"}) + "." + base64url(payload TA đã giải mã) + "."`; giữ nguyên đầy đủ payload TA của chính A, chữ ký rỗng, không ký lại.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| CN-G6-01 | SEC | SEC-02 | H1: thiếu token với ID vắng đã xác minh | S6; V(X) | `PUT /api/orders/<X>/cancel`; không Authorization; không body | 401 | E; K(pending) | README SEC-02 dòng 279; API spec 112,145–147; GIẢ ĐỊNH auth-first và 401 |
| CN-G6-02 | SEC | SEC-02 | H2: JWT alg none chữ ký rỗng | S6; tạo token `none` theo quy ước | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <token none>`; không body | 401 | E; K(pending) | README SEC-02 dòng 279; GIẢ ĐỊNH 401 và JWT không chữ ký không hợp lệ |
| CN-G6-03 | SEC | FR-10, SEC-05 | H3: ID thật nối chữ không được parse thành ID thật | S6; D(pending) | `PUT /api/orders/<O1>abc/cancel`; `Authorization: Bearer <TA>`; không body | 400 | E; K(pending) | API spec 145–147; README SEC-05 dòng 282; GIẢ ĐỊNH ID nguyên và 400 |
| CN-G6-04 | BVA | FR-10 | H4: mốc số nguyên có dấu 32 bit lớn nhất vắng mặt | S6; V(2147483647) | `PUT /api/orders/2147483647/cancel`; `Authorization: Bearer <TA>`; không body | 404 | E; K(pending) | API spec 145–147; GIẢ ĐỊNH tra cứu ID vắng trả 404; 2147483647 chỉ là mốc 32 bit, không phải trần spec |
| CN-G6-05 | SCH | FR-10 | H5: schema lỗi User hủy shipping | S6; D(shipping) | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TA>`; không body | 400 | E, gồm Content-Type JSON và schema lỗi; K(shipping) | README FR-10 dòng 161–162; GIẢ ĐỊNH 400 và schema lỗi |
| CN-G6-06 | SEC | FR-10 | H6: Admin dùng endpoint User với delivered | S6; D(delivered) | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TM>`; không body | 400 | E; K(delivered) | README FR-10 dòng 158–162; GIẢ ĐỊNH 400 và thứ tự kiểm tra |
| CN-G6-07 | SEC | FR-10 | H6: Admin dùng endpoint User với shipping | S6; D(shipping) | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TM>`; không body | 400 | E; K(shipping) | README FR-10 dòng 145–162; GIẢ ĐỊNH từ chối Admin hủy shipping vì sơ đồ không có cạnh và prose không rõ, 400 |
| CN-G6-08 | SEC | FR-10, FR-11 | H7: B hủy đơn A shipping | S6; D(shipping) | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TB>`; không body | 404 | E; K(shipping) | README FR-10 dòng 161, FR-11 dòng 166; GIẢ ĐỊNH ownership khi hủy, ownership trước state và 404 |
| CN-G6-09 | SEC | FR-10, FR-11 | H7: B hủy đơn A delivered | S6; D(delivered) | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TB>`; không body | 404 | E; K(delivered) | README FR-10 dòng 160, FR-11 dòng 166; GIẢ ĐỊNH ownership khi hủy, ownership trước state và 404 |
| CN-G6-10 | SEC | FR-10, FR-11 | H7: B hủy đơn A canceled | S6; D(canceled) | `PUT /api/orders/<O1>/cancel`; `Authorization: Bearer <TB>`; không body | 404 | E; K(canceled) | README FR-10 dòng 160, FR-11 dòng 166; GIẢ ĐỊNH ownership khi hủy, ownership trước state và 404 |
| CN-G6-11 | SEC | FR-10, FR-12, SEC-03 | H8: User gọi API Admin đổi đơn shipping | S6; D(shipping) | `PUT /api/admin/orders/<O1>/status`; `Authorization: Bearer <TA>`, `Content-Type: application/json`; body `{"status":"canceled"}` | 403 | E, gồm Content-Type JSON và schema lỗi; K(shipping) | README FR-12 dòng 174–179, SEC-03 dòng 280; API spec 173,179–182; GIẢ ĐỊNH 403 và schema lỗi |
| CN-G6-12 | SCH | FR-10 | H9: owner token, đơn vắng và schema lỗi 404 | S6; V(X) | `PUT /api/orders/<X>/cancel`; `Authorization: Bearer <TA>`; không body | 404 | E, gồm Content-Type JSON và schema lỗi; K(pending) | API spec 112,145–147; GIẢ ĐỊNH 404 và schema lỗi |

**Ghi chú của AI:** G6 ánh xạ H1→01, H2→02, H3→03, H4→04, H5→05, H6→06–07, H7→08–10, H8→11, H9→12; schema 403 được kiểm ở 11. G5 đếm 42 ID sau trừ trùng, thêm 12 biến thể với input, actor, trạng thái hoặc oracle riêng thành 54 theo cách đếm G5, vượt 35.
Mã HTTP, JSON, schema và thứ tự xác thực/ownership/state đều là giả định; FR-11 chỉ quy định quyền xem, không quy định trực tiếp quyền hủy. Admin hủy shipping còn mơ hồ giữa sơ đồ và prose.
CN-G3-04 hết hạn và CN-G3-06 user bị xóa vẫn có điều kiện như G3, không giả làm luôn thực thi được; không gọi SUT trong bước này.

## G5 – Tổng hợp độ phủ (reviewer)

**Bản rà lại sau G6, là kết luận hiện hành của API 2.** Mục `## G5` đứng trước G6 (42 ID) và toàn bộ G1–G4, G6 được giữ nguyên để trace. Mục này chỉ báo cáo: không sửa hay thêm test, không gán nhãn VALID/INVALID/INCOMPLETE, không gửi request tới SUT, không chạy script kiểm thử (đếm bằng đọc bảng; số cột đã đối chiếu bằng tìm kiếm văn bản trên chính file này). Nguồn đối chiếu: README FR-10 (141–162), FR-11 (164–167), FR-12 (172–179), FR-20 (233–236), SEC-01 đến SEC-07 (277–284), API spec 4.5–4.6 (139–147) và 6.2 (179–182), `report/01_spec_analysis.md` mục 2.

Ký hiệu ma trận: `∅N` ô trống vì không áp dụng, có lý do. `∅?` ô trống ưu tiên thấp, có ID gần nhất. `∅!` ô trống quan trọng (sau G6 không còn ô nào). `(đk)` là case có điều kiện thực thi mà spec không bảo đảm, xem 5.6B. Hàng cũ ghi 403 hoặc "biểu thị lỗi" được đọc theo quy ước hợp nhất của G6 (5.4).

### 5.1 Bảng đếm

**Quy tắc trừ trùng (hiện hành):** một nhóm trùng thật là các ID có cùng trạng thái đơn ban đầu, cùng request (cùng actor, cùng loại ID), cùng status kỳ vọng và cùng phép kiểm tra sau request. Sau G6, mọi cụm "biểu thị lỗi" ở G1–G5 được hiểu là predicate E của G6 (JSON, `error` là string không rỗng, không chứa JWT), nên hàng cũ có oracle yếu và hàng G4 hoặc G6 có oracle E hoặc S-error được coi là cùng oracle. Khác nhãn kỹ thuật, khác cách viết setup, hoặc thêm đơn thứ hai trong K chỉ là setup và assertion dùng chung, không làm hai case khác nhau. Case có thêm assertion độc lập (ngưỡng thời gian, schema thành công, schema GET) hoặc khác actor, ID, trạng thái là gần trùng và không bị trừ. Đếm theo nhóm (hợp các ID, không trừ theo từng cặp), mỗi nhóm giữ ID nhỏ nhất.

| Kỹ thuật | ID trước khi trừ | ID bị trừ (trùng thật) | Còn lại |
|---|---|---|---|
| EP | 12 (CN-G1-01, 02, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16) | 0 | 12 |
| BVA | 5 (CN-G1-03, 04, 05, 06, CN-G6-04) | 0 | 5 |
| ST | 13 (CN-G2-01 đến CN-G2-13) | 3 (CN-G2-01, CN-G2-11, CN-G2-12) | 10 |
| SEC | 21 (CN-G3-01 đến 12; CN-G6-01, 02, 03, 06, 07, 08, 09, 10, 11) | 2 (CN-G3-03, CN-G3-05) | 19 |
| SCH | 8 (CN-G4-01 đến 06; CN-G6-05, CN-G6-12) | 4 (CN-G4-03, CN-G4-04, CN-G6-05, CN-G6-12) | 4 |
| **Tổng** | **59** | **9 (7 nhóm trùng thật)** | **50** |

| Khối | G1 | G2 | G3 | G4 | G6 | Tổng |
|---|---|---|---|---|---|---|
| ID trước khi trừ | 16 | 13 | 12 | 6 | 12 | 59 |
| ID sau khi trừ trùng | 16 | 10 | 10 | 4 | 10 | 50 |

- **Số khác theo quy tắc khác (chỉ để đối chiếu):** theo quy tắc cũ của G5 trước G6 (oracle theo chữ của từng hàng, 5 nhóm D1 đến D5 cũ) là 54, khớp ghi chú cuối G6. Nếu gộp luôn các nhóm gần trùng N1 đến N5 ở 5.2 thì còn 41. Các nhóm N6 đến N10 không gộp vì khác request, actor hoặc trạng thái.
- Số phép thử thực tế lớn hơn số ID: CN-G2-06 đến CN-G2-10 mỗi ID gồm 5 phép thử (25 phép thử), CN-G3-12 gồm 3 request, CN-G2-05 gồm 2 lần hủy. Bảng đếm tính theo ID.
- SCH chỉ còn 4 ID vì 4 hàng schema lỗi bị gộp vào hàng giữ lại, không phải vì mất kiểm tra schema. Các hàng bị trừ không bị xóa. Nếu sinh viên không áp dụng E cho hàng cũ khi Execute thì chính CN-G4-03, CN-G4-04, CN-G6-05, CN-G6-12 là hàng duy nhất viết rõ assertion schema lỗi, nên không nên bỏ chúng khỏi collection.
- **Kết luận số lượng: ĐỦ ≥ 35** (50 ID sau trừ trùng thật; thấp nhất theo mọi cách đếm ở trên là 41, vẫn ≥ 35).

### 5.2 Danh sách trùng

**Trùng thật (đã trừ ở 5.1, không xóa khỏi file):**

| Nhóm | ID | Lý do | Giữ / trừ |
|---|---|---|---|
| D1 | CN-G1-01, CN-G2-01 | Cùng đơn pending của chủ đơn, cùng `PUT /api/orders/<O>/cancel` Bearer T không body, cùng 200, cùng kiểm tra đơn `canceled`. Chỉ khác nhãn EP và ST | Giữ CN-G1-01, trừ CN-G2-01 |
| D2 | CN-G1-11, CN-G3-03, CN-G4-04 | Cùng request không Authorization trên đơn pending, cùng 401, cùng K pending. CN-G3-03 chỉ thêm đơn thứ hai trong K. Oracle S-error của CN-G4-04 (JSON, `error` string) nằm trong E | Giữ CN-G1-11, trừ CN-G3-03 và CN-G4-04 |
| D3 | CN-G1-14, CN-G3-05 | Cùng cách tạo JWT sai chữ ký (đổi ký tự base64url đầu của chữ ký), cùng request, 401, K pending | Giữ CN-G1-14, trừ CN-G3-05 |
| D4 | CN-G2-02, CN-G2-11 | Cùng đơn confirmed dựng bằng Admin, cùng User hủy, 200, K canceled. CN-G2-11 chỉ viết rõ chuỗi dựng | Giữ CN-G2-02, trừ CN-G2-11 |
| D5 | CN-G2-03, CN-G2-12, CN-G6-05 | Cùng đơn shipping, cùng chủ đơn hủy bằng endpoint User, 400, K shipping. CN-G2-12 chỉ viết rõ chuỗi dựng; CN-G6-05 viết rõ E và S-error, đã là oracle của hàng cũ sau G6 | Giữ CN-G2-03, trừ CN-G2-12 và CN-G6-05 |
| D6 | CN-G1-02, CN-G6-12 | Cùng chủ đơn (token user có đơn) hủy ID dương đã xác minh vắng, 404, K pending, cùng E. CN-G6-12 chỉ khác nhãn SCH và có thêm đơn thứ hai trong K | Giữ CN-G1-02, trừ CN-G6-12 |
| D7 | CN-G2-05, CN-G4-03 | Cùng chuỗi hủy pending rồi hủy lại, 200 rồi 400, K canceled. S-error của CN-G4-03 nằm trong E | Giữ CN-G2-05, trừ CN-G4-03 |

**Gần trùng (không trừ):**

| Nhóm | ID | Điểm giống | Điểm khác làm cho không bị trừ |
|---|---|---|---|
| N1 | CN-G1-03, CN-G1-04 | Cùng lớp ID không dương, 400 | 0 là biên, -1 là phía âm |
| N2 | CN-G1-05, CN-G1-06, CN-G6-04 | Cùng lớp ID lớn vắng mặt, 404 | Ba giá trị biên khác nhau: 2147483648, 9999999999, 2147483647 |
| N3 | CN-G1-07, 08, 09, 10 | Cùng lớp ID không phải số nguyên, 400 | Khác ký tự (thập phân, chữ, `@`, dấu cách) |
| N4 | CN-G1-01 (nhóm D1), CN-G4-01, CN-G4-05 | Cùng request hủy đơn pending, 200; ô cũ CN-G1-01 không ràng buộc body, nhưng hiện áp predicate success của G6 (JSON object, `message` string không rỗng) | CN-G4-01 thêm kiểm tra header Content-Type JSON và S-success; CN-G4-05 thêm ngưỡng thời gian |
| N5 | CN-G4-02, CN-G4-06 | Cùng GET sau hủy | CN-G4-06 thêm ngưỡng thời gian |
| N6 | CN-G3-12 với CN-G3-01, CN-G1-02, CN-G6-12 | Request 1 của CN-G3-12 giống CN-G3-01 (B hủy đơn pending của A, 404 theo G6); request 3 cùng lớp ID vắng với CN-G1-02 | CN-G3-12 là case hợp 3 request cộng oracle "body giống nhau sau khi bỏ ID phản chiếu"; request 3 dùng token TB, không phải token chủ đơn |
| N7 | CN-G1-14 (nhóm D3), CN-G1-15, CN-G3-07, CN-G6-02 | Cùng lớp JWT không hợp lệ, 401 | Cách tạo khác nhau: sửa chữ ký, chuỗi rác, tự ký HS256 bằng secret đoán, `alg: none` |
| N8 | CN-G2-03 (nhóm D5), CN-G6-07, CN-G6-08, CN-G6-11 | Cùng đơn shipping, đều bị từ chối | Khác actor hoặc endpoint: chủ đơn, Admin ở endpoint User, B ở endpoint User, User ở endpoint Admin; status 400, 400, 404, 403 |
| N9 | CN-G2-04, CN-G6-06, CN-G6-09 | Cùng đơn delivered, đều bị từ chối | Khác actor: chủ đơn, Admin, B; status 400, 400, 404 |
| N10 | CN-G3-11, CN-G6-06, CN-G6-07 | Admin dùng endpoint User trên đơn của A | Khác trạng thái đơn: pending cho 200, delivered và shipping cho 400 |

**G6 không trùng với hàng cũ:** CN-G6-01 với CN-G1-11 (ID vắng mặt, không phải đơn tồn tại); CN-G6-03 với CN-G1-08 (hậu tố chữ gắn vào ID đơn thật `<O1>abc`, không phải chuỗi chữ thuần); CN-G6-04 với CN-G1-05 (giá trị 2147483647 khác 2147483648); CN-G6-08 đến CN-G6-10 với CN-G3-01, CN-G3-02 (khác trạng thái đơn); CN-G6-11 với CN-G2-08 (khác actor và endpoint).

### 5.3 Ma trận độ phủ

#### 5.3a Các ô bảng 5×5 FR-10 liên quan tới User hủy (cột đích `canceled`)

Endpoint hủy chỉ tạo cạnh tới `canceled`, nên 5 ô cột `canceled` là các ô liên quan. Hai mươi ô còn lại chỉ do Admin qua `PUT /api/admin/orders/:id/status` và nằm ngoài phạm vi User hủy (CN-G2-06 đến CN-G2-10 dựng và kiểm tra chúng). Cạnh Admin hủy trong cùng cột được đưa vào cột ST, cạnh Admin hoặc người khác đi qua endpoint User được đưa vào cột SEC.

| Ô (nguồn → canceled) | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|
| pending → canceled (R:151) | CN-G1-01, CN-G1-16 | ∅N: ô là enum trạng thái rời rạc, biên số của `:id` ở 5.3c | CN-G2-01 (trùng D1), CN-G2-06 (Admin qua status), CN-G2-13 | CN-G3-01 (404 theo G6), CN-G3-03 đến CN-G3-10 (tấn công trên đơn pending, K pending), CN-G3-11 (Admin), CN-G3-12, CN-G6-02, CN-G6-03 | CN-G4-01, CN-G4-02, CN-G4-04, CN-G4-05, CN-G4-06 |
| confirmed → canceled (R:151) | ∅?: lớp hợp lệ chỉ có ở ST, gần nhất CN-G2-02 | ∅N: như trên | CN-G2-02, CN-G2-07 (Admin), CN-G2-11 (trùng D4) | CN-G3-02 (404 theo G6) | ∅?: schema thành công chỉ thử trên pending, gần nhất CN-G4-01; schema lỗi theo E |
| shipping → canceled (User bị cấm, R:161) | ∅?: lớp này kiểm bằng ST và SCH, gần nhất CN-G2-03, CN-G6-05 | ∅N: như trên | CN-G2-03, CN-G2-08 (Admin, GIẢ ĐỊNH), CN-G2-12 (trùng D5) | CN-G6-07 (Admin qua endpoint User, GIẢ ĐỊNH), CN-G6-08 (B), CN-G6-11 (User gọi API Admin, 403) | CN-G6-05 (nhóm D5), CN-G6-11 (schema 403) |
| delivered → canceled (R:160) | ∅?: gần nhất CN-G2-04 | ∅N: như trên | CN-G2-04, CN-G2-09 | CN-G6-06 (Admin), CN-G6-09 (B) | ∅?: cùng đường lỗi với CN-G6-05 và E của CN-G2-04, gần nhất CN-G4-03 |
| canceled → canceled (R:160) | ∅?: gần nhất CN-G2-05 | ∅N: như trên | CN-G2-05, CN-G2-10 | CN-G6-10 (B); ∅?: Admin qua endpoint User trên đơn canceled, gần nhất CN-G6-06 | CN-G4-03 (trùng D7) |

#### 5.3b Theo yêu cầu (FR và SEC)

| Yêu cầu | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|
| FR-10 R:150–155 hủy hợp lệ pending hoặc confirmed | CN-G1-01, CN-G1-16 | ∅N: không có giá trị số trong quy tắc | CN-G2-01, CN-G2-02, CN-G2-06, CN-G2-07, CN-G2-11, CN-G2-13 | CN-G3-11 (Admin, GIẢ ĐỊNH) | CN-G4-01, CN-G4-05 |
| FR-10 R:160 trạng thái kết thúc | ∅N: kiểm tra bằng ST | ∅N | CN-G2-04, CN-G2-05, CN-G2-09, CN-G2-10 | CN-G6-06, CN-G6-09, CN-G6-10 | CN-G4-03 |
| FR-10 R:161 shipping chỉ Admin thao tác | ∅N: kiểm tra bằng ST | ∅N | CN-G2-03, CN-G2-08, CN-G2-12 | CN-G6-07, CN-G6-08, CN-G6-11 | CN-G6-05 |
| FR-10 R:162 chuyển đổi không hợp lệ phải có thông báo lỗi | ∅N: kiểm tra bằng ST | ∅N | CN-G2-03 đến CN-G2-10, CN-G2-12 | ∅N: không phải yêu cầu bảo mật | CN-G4-03, CN-G6-05, CN-G6-11 và E của mọi hàng lỗi |
| FR-11 R:166 chỉ xem đơn của mình (ownership khi hủy là GIẢ ĐỊNH) | CN-G1-01 (lớp chủ đơn) | ∅N | ∅N: quyền sở hữu không phải cạnh trạng thái; tổ hợp người khác và trạng thái nằm ở cột SEC | CN-G3-01, CN-G3-02, CN-G3-12, CN-G6-08, CN-G6-09, CN-G6-10 | CN-G6-08 (E, schema lỗi 404 của B) |
| FR-11 R:167 và API spec 143: GET đối chiếu trạng thái | ∅N: GET chỉ là công cụ kiểm tra | ∅N | K trong CN-G2-01 đến CN-G2-13 và G6 | ∅N | CN-G4-02, CN-G4-06 |
| FR-12 R:174–179 API Admin cần JWT và role admin | ∅N: cancel không phải API Admin | ∅N | ∅N: CN-G2-06 đến CN-G2-10 dùng token Admin hợp lệ làm setup, không kiểm role | CN-G6-11 (User gọi API Admin); CN-G3-11 (gián tiếp: Admin dùng endpoint User) | CN-G6-11 (schema 403) |
| FR-20 R:236 chỉ hủy khi pending hoặc confirmed | CN-G1-01 | ∅N | CN-G2-01, CN-G2-02, CN-G2-03, CN-G2-04, CN-G2-05 | ∅N: yêu cầu giao diện Mobile, API đã kiểm qua FR-10 | ∅N: không có schema riêng |
| API spec A:147 "chưa giao" (rộng hơn R:161, mơ hồ) | ∅N | ∅N | CN-G2-03, CN-G2-04 | CN-G6-07 (Admin trên shipping, GIẢ ĐỊNH) | ∅N |
| SEC-01 mật khẩu không plaintext | ∅N: cancel không nhận hay trả mật khẩu; cách lưu mật khẩu không quan sát được qua API này | ∅N | ∅N | ∅N: E của G6 chỉ kiểm không lộ JWT, không kiểm mật khẩu | ∅N |
| SEC-02 API bảo mật cần JWT hợp lệ | CN-G1-11, CN-G1-12, CN-G1-13, CN-G1-14, CN-G1-15 | ∅N: biên thời gian hết hạn thuộc CN-G3-04 (đk) | CN-G3-04 (hết hạn, đk), CN-G3-06 (user bị xóa, đk) | CN-G3-03, CN-G3-04 (đk), CN-G3-05, CN-G3-06 (đk), CN-G3-07, CN-G6-01, CN-G6-02 | CN-G4-04, E của CN-G6-01 và CN-G6-02 |
| SEC-03 API Admin kiểm tra role | ∅N: cancel không phải API Admin, spec không yêu cầu role admin cho cancel | ∅N | ∅N: setup Admin dùng token đúng role | CN-G6-11, CN-G3-11 | CN-G6-11 |
| SEC-04 escape khi hiển thị UI | ∅N: response cancel là JSON, việc escape ở giao diện không kiểm được bằng API này | ∅N | ∅N | ∅N: gián tiếp, CN-G3-12 chỉ so sánh body sau khi bỏ ID phản chiếu | ∅N |
| SEC-05 parameterized query | CN-G1-07, CN-G1-08, CN-G1-09, CN-G1-10 (ID lạ, không phải payload SQL) | ∅N: spec không có giá trị biên cho tấn công SQL | ∅N | CN-G3-08, CN-G3-09, CN-G3-10, CN-G6-03 | ∅N: không có schema riêng; E áp dụng cho CN-G3-08 đến 10 và CN-G6-03 |
| SEC-06 không đổi `role` qua hồ sơ | ∅N: thuộc API hồ sơ, không có trong cancel | ∅N | ∅N | ∅N: gián tiếp, CN-G3-07 giả mạo claim `role` trong token là tấn công token, không phải API hồ sơ | ∅N |
| SEC-07 OTP đặt lại mật khẩu | ∅N: không có OTP trong cancel | ∅N | ∅N | ∅N | ∅N |

#### 5.3c Theo tham số

| Tham số | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|
| `:id` (path) | CN-G1-01, CN-G1-02, CN-G1-07, CN-G1-08, CN-G1-09, CN-G1-10 | CN-G1-03, CN-G1-04, CN-G1-05, CN-G1-06, CN-G6-04 | ∅N: trạng thái đơn mà ID trỏ tới nằm ở 5.3a | CN-G3-08, CN-G3-09, CN-G3-10, CN-G3-12, CN-G6-01, CN-G6-03 | CN-G6-12 (nhóm D6, schema 404), CN-G6-05 |
| Authorization (header, gồm role của token) | CN-G1-01, CN-G1-11, CN-G1-12, CN-G1-13, CN-G1-14, CN-G1-15 | ∅N: biên thời gian hết hạn thuộc CN-G3-04 (đk) | CN-G3-04 (đk), CN-G3-06 (đk) | CN-G3-03, CN-G3-04 (đk), CN-G3-05, CN-G3-06 (đk), CN-G3-07, CN-G6-01, CN-G6-02; theo role: CN-G3-11, CN-G6-06, CN-G6-07, CN-G6-11 | CN-G4-04, CN-G6-11 |
| Body | CN-G1-01 (không body), CN-G1-16 (body thừa) | ∅N: spec không mô tả body | ∅N | CN-G1-16 (gán `status` từ client, nhãn EP); ∅?: body thừa trên đơn shipping, gần nhất CN-G1-16 | ∅N: không có contract body |
| Response (đầu ra) | ∅N | CN-G4-05, CN-G4-06 (ngưỡng thời gian, GIẢ ĐỊNH) | ∅N | CN-G3-08, CN-G3-09, CN-G3-10 (không lộ SQL); E của G6 (không lộ JWT) | CN-G4-01 đến CN-G4-06, CN-G6-05, CN-G6-11, CN-G6-12 |

### 5.4 Ánh xạ H1–H9 và các phát hiện cũ sang G6

| Mã cũ | Case mới | Ô hoặc hàng đóng | Ghi chú còn lại |
|---|---|---|---|
| H1 không token trên ID vắng | CN-G6-01 | SEC-02 × `:id`; Authorization SEC | Phụ thuộc V(X) xác minh vắng mặt (5.6B) |
| H2 JWT `alg: none` | CN-G6-02 | SEC-02 SEC; Authorization SEC | Token tạo từ payload TA, không cần secret |
| H3 chuẩn hóa ID lỏng trên đơn thật | CN-G6-03 | `:id` SEC; SEC-05 SEC | Không còn ∅ ở `:id` |
| H4 biên số trên | CN-G6-04 | `:id` BVA | Cặp với CN-G1-05 (2147483648) |
| H5 schema lỗi User hủy shipping | CN-G6-05 | shipping → canceled SCH; R:161 SCH | Thuộc nhóm D5 nên không tăng số đếm |
| H6 Admin trên endpoint User, delivered và shipping | CN-G6-06, CN-G6-07 | delivered và shipping → canceled SEC; R:160, R:161 SEC | CN-G6-07 là GIẢ ĐỊNH, không suy luận quyền Admin hủy shipping |
| H7 B hủy đơn shipping, delivered, canceled | CN-G6-08, CN-G6-09, CN-G6-10 | FR-11 R:166 SEC; ba ô → canceled SEC | Thứ tự xác thực, ownership, trạng thái là GIẢ ĐỊNH |
| H8 User gọi API Admin để vượt R:161 | CN-G6-11 | SEC-03 SEC; FR-12 SEC; shipping → canceled SEC | Có thể thuộc API khác, vẫn có trong API 2 |
| H9 schema lỗi 404 và 403 | CN-G6-12 (404), CN-G6-11 (403) | `:id` SCH | CN-G6-12 thuộc nhóm D6 |
| Mâu thuẫn 403 và 404 (5.4 cũ) | Quy ước G6; CN-G3-12, CN-G6-08 đến 10 | FR-11 R:166 SEC | Hiệu lực: User không phải chủ đơn nhận 404. Hàng CN-G3-01 và CN-G3-02 còn ghi 403, đã bị thay thế bởi 404 và giữ nguyên để trace; CN-G3-12 (ba 404) đúng, không cần đổi |
| Oracle lỗi yếu "biểu thị lỗi" (5.4 cũ) | Predicate E của G6 | 34 hàng cũ (CN-G1-02 đến 15, CN-G2-03 đến 10, CN-G2-12, CN-G3-01 đến 10, CN-G3-12) | E áp dụng cho các hàng này khi Execute: JSON, `error` string không rỗng, không chứa JWT; 12 hàng G6 và S-error của G4 đã viết rõ |

Các điểm cũ không đổi và vẫn thuộc việc audit của sinh viên, không phải lỗ hổng: CN-G1-03 và CN-G1-04 kỳ vọng 400 còn CN-G1-05, CN-G1-06, CN-G6-04 kỳ vọng 404 (0 và -1 có thể cũng là ID hợp lệ chưa tồn tại); ký hiệu `A` trong G1 chỉ ID vắng còn G2 và G3 dùng cho Admin hoặc user A; setup coi mọi bước thành công là 200.

### 5.5 Kiểm tra định dạng (59 hàng)

| Tiêu chí | Kết quả (đối chiếu bằng đọc và tìm kiếm văn bản, không chạy script, không gửi request) |
|---|---|
| Đủ 9 cột | 59/59 hàng bắt đầu bằng `CN-Gx-yy` có đúng 9 ô (tìm các hàng không có đúng 9 ô trả về 0 hàng); tiêu đề giống mẫu. Lệch nhẹ so với "một bảng": G1 có thêm bảng phân hoạch phụ, G2 có thêm ma trận 5×5 |
| ID duy nhất | 16 + 13 + 12 + 6 + 12 = 59 ID, không trùng |
| Precondition dựng được trạng thái | Đạt có điều kiện. S, S3, S4, S6, D(s), V(x), K(s) đều được định nghĩa trong cùng bước, Admin chỉ đi cạnh hợp lệ pending → confirmed → shipping → delivered hoặc hủy. Phụ thuộc không có trong spec đã ghi GIẢ ĐỊNH: `orderId` trong response checkout, GET trả `status`, đơn mới là pending. Điều kiện không bảo đảm được thực thi: xem 5.6B |
| Expected cụ thể | Status cụ thể ở 59/59 (CN-G2-06 đến 10 liệt kê status theo từng đích). Body: 34 hàng lỗi cũ nay đọc theo E; 12 hàng G6 dẫn E; 6 hàng G4 có schema rõ. Bảy hàng success cũ (CN-G1-01, 16, CN-G2-01, 02, 11, 13, CN-G3-11) nay áp predicate success của G6: JSON object, `message` string không rỗng, đơn đích `canceled`. Các quy ước hợp nhất nằm trong phần chữ G6, không được chép lại vào từng ô cũ |
| Có Nguồn expected | 59/59 có cột nguồn, phần spec không nêu đều ghi GIẢ ĐỊNH. Số dòng đối chiếu với README và API spec: README 158–162, 166, 167, 236, 279, 280, 282; API spec 112, 143, 145–147, 179–182 là khớp với nội dung được trích |
| Request đủ để chuyển thành request | Đạt: method, path, header, body tường minh hoặc là macro (U, A(s), K, S, S3, S4, S6, D(s), V(x), E) có định nghĩa đầy đủ trong cùng bước. Chưa kiểm được bằng cách chạy; chỉ đọc |
| Hàng cũ lệch quy ước G6 | CN-G3-01 và CN-G3-02 ghi 403, hiệu lực 404 theo G6. Nếu sinh viên chuyển thẳng ô cũ sang Postman thì sẽ assert 403 và mâu thuẫn với CN-G3-12 và CN-G6-08 đến 10; đây là rủi ro khi chuyển đổi, đã được ghi ở 5.4 |

### 5.6 Lỗ hổng còn lại và điều kiện thực thi

**A. Lỗ hổng độ phủ.** Không còn ô `∅!` và không còn lỗ hổng thật cần G7: H1 đến H9 đều đã có case (5.4). Các ô `∅?` dưới đây vẫn trống ở ma trận 5.3, ưu tiên thấp, đều đã có hàng gần nhất; liệt kê để sinh viên quyết định, không đề xuất bắt buộc.

| Mã | Yêu cầu hoặc ô | Vì sao có thể quan trọng | Gợi ý 1 test (nếu sinh viên muốn) |
|---|---|---|---|
| L1 | canceled → canceled, SEC, Admin qua endpoint User | R:160 cấm chuyển từ canceled với mọi actor; CN-G6-06 chỉ thử Admin trên delivered | `PUT /api/orders/<O1>/cancel` với Bearer TM trên D(canceled); kỳ vọng 400 (GIẢ ĐỊNH), E, K(canceled) |
| L2 | Body thừa trên đơn shipping, cột SEC | CN-G1-16 chỉ thử gán `status` trên đơn pending | `PUT /api/orders/<O1>/cancel` với Bearer TA, body `{"status":"canceled"}` trên D(shipping); kỳ vọng 400 (GIẢ ĐỊNH), E, K(shipping) |
| L3 | confirmed → canceled, SCH thành công | S-success chỉ kiểm trên pending (CN-G4-01) | Như CN-G4-01 nhưng setup đơn confirmed; kỳ vọng 200, khớp S-success, K(canceled) |

**B. Điều kiện thực thi do spec không nêu (không phải thiếu case, và không được coi là đã chạy được).**

| Case | Điều kiện spec không bảo đảm | Hệ quả khi Execute |
|---|---|---|
| CN-G3-04 | JWT có claim `exp` và thời hạn đủ ngắn để chờ; spec không nêu | Case tồn tại nhưng có thể không thực thi được; không có case thay thế, nên phải ghi là chưa chạy được thay vì pass |
| CN-G3-06 | README FR-19 R:227 chỉ nói Admin xóa user; không nêu hiệu lực token và số phận đơn sau khi xóa | Setup chỉ dừng nếu A chưa được xóa hoặc hai đơn không còn để đối chiếu. Sau khi xác nhận setup, token cũ vẫn hủy được đơn là thất bại của test, không phải lý do bỏ qua; kỳ vọng 401 vẫn là GIẢ ĐỊNH |
| V(x) trong CN-G1-02, 05, 06, CN-G3-12, CN-G6-01, CN-G6-04, CN-G6-12 | `GET /api/admin/orders` liệt kê toàn bộ đơn: API spec 6.2 dòng 179 ghi "Toàn hệ thống" và README R:220 ghi Admin xem toàn bộ đơn, nhưng phân trang hoặc giới hạn không được nêu | Các case dừng nếu không xác minh được ID vắng mặt trong toàn bộ danh sách |
| CN-G3-11, CN-G6-06, CN-G6-07 | README R:151 chỉ nói "User/Admin hủy"; không nói Admin dùng endpoint User hay bỏ qua ownership | Kỳ vọng 200 và 400 là GIẢ ĐỊNH; riêng shipping do Admin ở CN-G6-07 và CN-G2-08 không suy luận quyền hủy |
| CN-G6-01 | Thứ tự xác thực trước tra cứu đơn | Kỳ vọng 401 trên ID vắng là GIẢ ĐỊNH |

### 5.7 Kết luận hiện hành

- **Số lượng: ĐỦ ≥ 35.** 59 ID tổng, 50 ID sau khi trừ 7 nhóm trùng thật: EP 12, BVA 5, ST 10, SEC 19, SCH 4 (G1 16, G2 10, G3 10, G4 4, G6 10).
- **Lỗ hổng thật còn lại: không.** Ba ô `∅?` L1 đến L3 là tùy chọn. Năm điều kiện thực thi ở 5.6B cần sinh viên xử lý khi Execute và không được báo là pass nếu không chạy được.

**Ghi chú của AI:** Ranh giới trùng thật và gần trùng là đánh giá của AI. Sinh viên có thể dùng quy tắc khác ở bước Audit; số 50 đổi theo (54 theo quy tắc cũ, 41 nếu gộp cả gần trùng).
Việc nhập E vào hàng cũ là diễn giải của quy ước G6, không phải sửa ô cũ; Execute phải áp dụng E và quy ước 404 cho CN-G3-01, CN-G3-02 một cách tường minh.
Các mã HTTP, schema lỗi, thứ tự xác thực/ownership, trạng thái ban đầu sau checkout và việc Admin dùng endpoint User là GIẢ ĐỊNH, không phải response đã quan sát. Năm trạng thái và các ràng buộc chuyển trạng thái FR-10 có nguồn đặc tả, không phải tất cả đều là giả định. Một số ô `∅N` là phán đoán về phạm vi (ví dụ SEC-06 thuộc API hồ sơ).
