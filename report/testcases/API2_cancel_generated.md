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
