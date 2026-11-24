# API 3 – Product CRUD – Test case do AI sinh

## G1 – Domain partition + boundary

### Bảng phân hoạch và biên

| Tham số | Lớp / giá trị biên và test trực tiếp |
|---|---|
| name | Thiếu 01; rỗng 02; chỉ khoảng trắng 03; 1 ký tự 04; 254 ký tự 05; 255 ký tự 06; 256 ký tự 07; tiếng Việt có dấu 08; null 09; số 10. 03, 09, 10 là phân loại giả định. |
| price | Thiếu 11; 0 12; -1 13; 0.01 14; 1 15; 1e15 16; chuỗi số 17; chuỗi chữ 18; null 19; boolean 20. Phân loại 16–20 cần audit. |
| category_id | Thiếu 21; id có sẵn 22; 99999 không tồn tại 23; 0 24; âm 25; chuỗi 26. Với 24–26, tính không hợp lệ là giả định nếu không có trong danh sách. |
| description | Thiếu 27; rỗng 28; rất dài 29: các kết quả đều giả định do chưa có validation. |
| imageUrl | Thiếu 30; rỗng 31; rất dài 32; không phải URL 33: các kết quả đều giả định do chưa có validation. |
| PUT :id | Tồn tại 34; không tồn tại 35; 0 36; âm 37; abc 38. Tính không hợp lệ của 36–38 và status là giả định. |
| DELETE :id | Tồn tại 39; không tồn tại 40; 0 41; âm 42; abc 43. Tính không hợp lệ của 41–43 và status là giả định. |
| Body | `{}` 44; JSON sai cú pháp 45; field thừa `id` 46. Các kết quả/status cụ thể là giả định. |

Trong bảng, số là hậu tố đầy đủ của `PR-G1-xx`. Quy ước thực thi **riêng cho từng dòng**: sinh UUID mới `U`, đặt `K` là ID case nối `-` với `U`; login `POST /api/login`, `Content-Type: application/json`, body `{"email":"admin@eshop.com","password":"Admin123!"}` lấy JWT `T`; `GET /api/categories` lấy `C` là id một danh mục hiện có. Nếu danh sách rỗng thì setup thất bại, không chạy test. Mọi request chính mang `Authorization: Bearer {{T}}`; request có body mang thêm `Content-Type: application/json`; DELETE không body. `B` là JSON `{"name":"{{K}}","price":100000,"description":"Mô tả","imageUrl":"https://example.com/product.png","category_id":{{C}}}`; trước khi gửi thay các placeholder bằng giá trị thực và `C` là JSON number. `B[field]=value` nghĩa là bản sao B với đúng field thay bằng giá trị JSON đã cho; `B-field` là bản sao B xóa đúng field. Chuỗi `a×N` là đúng N ký tự ASCII `a`, tạo trước khi serialize JSON; `tên N` là đúng N ký tự bằng `K` nối thêm `a` đủ N ký tự (nếu `K` dài hơn N thì setup thất bại), trừ trường hợp 1 ký tự dùng `a`. Tên 1/254/255 không cần chứa K: dữ liệu riêng được xác định bởi sản phẩm riêng và UUID setup, không dựa uniqueness tên.

Setup `P`: POST `/api/products` với B và admin token; tìm đúng sản phẩm có name `K` qua `GET /api/products`, lấy id `P` từ kết quả; nếu không xác định duy nhất thì setup thất bại. Lưu snapshot danh sách trước request; không sửa/xóa sản phẩm seed. Setup `A(x)`: `GET /api/products` và xác nhận không có product id `x`; nếu tồn tại thì setup thất bại; với `99999` bắt buộc xác nhận riêng cho category qua `GET /api/categories`. Với 0, -1, abc cũng xác nhận không có product/category id tương ứng qua danh sách trước khi dùng. Sau PUT thành công GET `/api/products/{{P}}`, đối chiếu các field gửi và snapshot các sản phẩm khác; sau DELETE thành công GET list xác nhận P không còn. Sau mọi request dự kiến lỗi, GET list so với snapshot để xác nhận không có thay đổi; status lỗi không quy định body cụ thể nên giả định body JSON có `error` là chuỗi không rỗng. GET list/detail schema, cách trích id, status mutations và kiểm tra persistence đều là giả định cần audit; các bước setup chỉ chạy khi thành công.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| PR-G1-01 | EP | FR-15 | Thiếu name | Quy ước chung, snapshot list | POST /api/products; Bearer T; JSON `B-name` | 400 | JSON `error` không rỗng; list không đổi | README:195; GIẢ ĐỊNH status/error |
| PR-G1-02 | EP | FR-15 | Name rỗng | Chung, snapshot | POST /api/products; Bearer T; JSON `B[name]=""` | 400 | error không rỗng; list không đổi | README:195; GIẢ ĐỊNH rỗng bị từ chối và status/error |
| PR-G1-03 | EP | FR-15 | Name khoảng trắng | Chung, snapshot | POST /api/products; Bearer T; JSON `B[name]="   "` | 400 | error không rỗng; list không đổi | README:195; GIẢ ĐỊNH trim, status/error |
| PR-G1-04 | BVA | FR-15 | Name 1 ký tự | Chung | POST /api/products; Bearer T; JSON `B[name]="a"` | 200 | GET list có sản phẩm name `a`, price 100000, category C | README:193–195; GIẢ ĐỊNH status, lưu và schema |
| PR-G1-05 | BVA | FR-15 | Name 254 ký tự | Chung | POST /api/products; Bearer T; JSON `B[name]=tên 254` | 200 | GET list có đúng name đã gửi | README:193–195; GIẢ ĐỊNH status, lưu và schema |
| PR-G1-06 | BVA | FR-15 | Name 255 ký tự | Chung | POST /api/products; Bearer T; JSON `B[name]=tên 255` | 200 | GET list có đúng name đã gửi | README:193–195; GIẢ ĐỊNH status, lưu và schema |
| PR-G1-07 | BVA | FR-15 | Name 256 ký tự | Chung, snapshot | POST /api/products; Bearer T; JSON `B[name]=tên 256` | 400 | error không rỗng; list không đổi | README:195; GIẢ ĐỊNH status/error |
| PR-G1-08 | EP | FR-15 | Name tiếng Việt | Chung | POST /api/products; Bearer T; JSON `B[name]="Sản phẩm {{K}}"` | 200 | GET list có đúng name gửi | README:193–195; GIẢ ĐỊNH Unicode, status, lưu/schema |
| PR-G1-09 | EP | FR-15 | Name null | Chung, snapshot | POST /api/products; Bearer T; JSON `B[name]=null` | 400 | error không rỗng; list không đổi | README:195; GIẢ ĐỊNH null không thỏa bắt buộc, status/error |
| PR-G1-10 | EP | FR-15 | Name số | Chung, snapshot | POST /api/products; Bearer T; JSON `B[name]=123` | 400 | error không rỗng; list không đổi | API spec:94; GIẢ ĐỊNH yêu cầu string, status/error |
| PR-G1-11 | EP | FR-15 | Thiếu price | Chung, snapshot | POST /api/products; Bearer T; JSON `B-price` | 400 | error không rỗng; list không đổi | README:196; GIẢ ĐỊNH status/error |
| PR-G1-12 | BVA | FR-15 | Price bằng 0 | Chung, snapshot | POST /api/products; Bearer T; JSON `B[price]=0` | 400 | error không rỗng; list không đổi | README:196; GIẢ ĐỊNH status/error |
| PR-G1-13 | BVA | FR-15 | Price âm | Chung, snapshot | POST /api/products; Bearer T; JSON `B[price]=-1` | 400 | error không rỗng; list không đổi | README:196; GIẢ ĐỊNH status/error |
| PR-G1-14 | BVA | FR-15 | Price 0.01 | Chung | POST /api/products; Bearer T; JSON `B[price]=0.01` | 200 | GET list có name K và price 0.01 | README:193,196; GIẢ ĐỊNH status và độ chính xác lưu |
| PR-G1-15 | BVA | FR-15 | Price 1 | Chung | POST /api/products; Bearer T; JSON `B[price]=1` | 200 | GET list có name K và price 1 | README:193,196; GIẢ ĐỊNH status/lưu |
| PR-G1-16 | EP | FR-15 | Price rất lớn | Chung | POST /api/products; Bearer T; JSON `B[price]=1e15` | 200 | GET list có name K và price 1000000000000000 | README:196; GIẢ ĐỊNH không có trần, status/lưu |
| PR-G1-17 | EP | FR-15 | Price chuỗi số | Chung, snapshot | POST /api/products; Bearer T; JSON `B[price]="100000"` | 400 | error không rỗng; list không đổi | README:196; GIẢ ĐỊNH không ép kiểu, status/error |
| PR-G1-18 | EP | FR-15 | Price chuỗi chữ | Chung, snapshot | POST /api/products; Bearer T; JSON `B[price]="abc"` | 400 | error không rỗng; list không đổi | README:196; GIẢ ĐỊNH status/error |
| PR-G1-19 | EP | FR-15 | Price null | Chung, snapshot | POST /api/products; Bearer T; JSON `B[price]=null` | 400 | error không rỗng; list không đổi | README:196; GIẢ ĐỊNH status/error |
| PR-G1-20 | EP | FR-15 | Price boolean | Chung, snapshot | POST /api/products; Bearer T; JSON `B[price]=true` | 400 | error không rỗng; list không đổi | README:196; GIẢ ĐỊNH không ép kiểu, status/error |
| PR-G1-21 | EP | FR-15 | Thiếu category_id | Chung, snapshot | POST /api/products; Bearer T; JSON `B-category_id` | 400 | error không rỗng; list không đổi | README:197; GIẢ ĐỊNH status/error |
| PR-G1-22 | EP | FR-15 | Category tồn tại | Chung | POST /api/products; Bearer T; JSON `B` | 200 | GET list có name K và category_id C | README:193,197; GIẢ ĐỊNH status/lưu/schema |
| PR-G1-23 | EP | FR-15 | Category không tồn tại | Chung; xác nhận 99999 không có trong categories; snapshot | POST /api/products; Bearer T; JSON `B[category_id]=99999` | 400 | error không rỗng; list không đổi | README:197; GIẢ ĐỊNH status/error |
| PR-G1-24 | BVA | FR-15 | Category 0 | Chung; xác nhận 0 không có trong categories; snapshot | POST /api/products; Bearer T; JSON `B[category_id]=0` | 400 | error không rỗng; list không đổi | README:197; GIẢ ĐỊNH status/error |
| PR-G1-25 | BVA | FR-15 | Category âm | Chung; xác nhận -1 không có trong categories; snapshot | POST /api/products; Bearer T; JSON `B[category_id]=-1` | 400 | error không rỗng; list không đổi | README:197; GIẢ ĐỊNH status/error |
| PR-G1-26 | EP | FR-15 | Category chuỗi | Chung; snapshot | POST /api/products; Bearer T; JSON `B[category_id]="abc"` | 400 | error không rỗng; list không đổi | README:197; GIẢ ĐỊNH string abc không phải id hợp lệ, status/error |
| PR-G1-27 | EP | FR-15 | Thiếu description | Chung | POST /api/products; Bearer T; JSON `B-description` | 200 | GET list có name K | API spec:91–99; GIẢ ĐỊNH description tùy chọn, status/lưu |
| PR-G1-28 | EP | FR-15 | Description rỗng | Chung | POST /api/products; Bearer T; JSON `B[description]=""` | 200 | GET list có name K và description rỗng | API spec:96; GIẢ ĐỊNH cho rỗng, status/lưu |
| PR-G1-29 | EP | FR-15 | Description rất dài | Chung | POST /api/products; Bearer T; JSON `B[description]=a×10000` | 200 | GET list có name K và description đúng 10000 ký tự a | API spec:96; GIẢ ĐỊNH không giới hạn, status/lưu |
| PR-G1-30 | EP | FR-15 | Thiếu imageUrl | Chung | POST /api/products; Bearer T; JSON `B-imageUrl` | 200 | GET list có name K | API spec:97; GIẢ ĐỊNH tùy chọn, status/lưu |
| PR-G1-31 | EP | FR-15 | Image rỗng | Chung | POST /api/products; Bearer T; JSON `B[imageUrl]=""` | 200 | GET list có name K và imageUrl rỗng | API spec:97,194; GIẢ ĐỊNH status/lưu |
| PR-G1-32 | EP | FR-15 | Image rất dài | Chung | POST /api/products; Bearer T; JSON `B[imageUrl]=a×10000` | 200 | GET list có name K và imageUrl đúng 10000 ký tự a | API spec:97; GIẢ ĐỊNH không giới hạn/URL, status/lưu |
| PR-G1-33 | EP | FR-15 | Image không phải URL | Chung | POST /api/products; Bearer T; JSON `B[imageUrl]="not-a-url"` | 200 | GET list có name K và imageUrl `not-a-url` | API spec:97; GIẢ ĐỊNH không validate URL, status/lưu |
| PR-G1-34 | EP | FR-15 | PUT id tồn tại | Chung; P | PUT /api/products/{{P}}; Bearer T; JSON `B[price]=1` | 200 | GET P có price 1, các field B còn lại đúng; sản phẩm khác không đổi | README:193,198; GIẢ ĐỊNH status/schema |
| PR-G1-35 | EP | FR-15 | PUT id không tồn tại | Chung; A(99999); snapshot | PUT /api/products/99999; Bearer T; JSON `B` | 404 | error không rỗng; list không đổi | API spec:89; GIẢ ĐỊNH không upsert, status/error |
| PR-G1-36 | BVA | FR-15 | PUT id 0 | Chung; A(0); snapshot | PUT /api/products/0; Bearer T; JSON `B` | 404 | error không rỗng; list không đổi | API spec:89; GIẢ ĐỊNH không upsert, status/error |
| PR-G1-37 | BVA | FR-15 | PUT id âm | Chung; A(-1); snapshot | PUT /api/products/-1; Bearer T; JSON `B` | 404 | error không rỗng; list không đổi | API spec:89; GIẢ ĐỊNH không upsert, status/error |
| PR-G1-38 | EP | FR-15 | PUT id chữ | Chung; A(abc); snapshot | PUT /api/products/abc; Bearer T; JSON `B` | 400 | error không rỗng; list không đổi | API spec:89; GIẢ ĐỊNH id số, status/error |
| PR-G1-39 | EP | FR-15 | DELETE id tồn tại | Chung; P | DELETE /api/products/{{P}}; Bearer T; không body | 200 | GET list không còn P; các sản phẩm khác không đổi | README:193; GIẢ ĐỊNH status, list phản ánh xóa |
| PR-G1-40 | EP | FR-15 | DELETE id không tồn tại | Chung; A(99999); snapshot | DELETE /api/products/99999; Bearer T; không body | 404 | error không rỗng; list không đổi | API spec:90; GIẢ ĐỊNH status/error |
| PR-G1-41 | BVA | FR-15 | DELETE id 0 | Chung; A(0); snapshot | DELETE /api/products/0; Bearer T; không body | 404 | error không rỗng; list không đổi | API spec:90; GIẢ ĐỊNH status/error |
| PR-G1-42 | BVA | FR-15 | DELETE id âm | Chung; A(-1); snapshot | DELETE /api/products/-1; Bearer T; không body | 404 | error không rỗng; list không đổi | API spec:90; GIẢ ĐỊNH status/error |
| PR-G1-43 | EP | FR-15 | DELETE id chữ | Chung; A(abc); snapshot | DELETE /api/products/abc; Bearer T; không body | 400 | error không rỗng; list không đổi | API spec:90; GIẢ ĐỊNH id số, status/error |
| PR-G1-44 | EP | FR-15 | Body rỗng | Chung, snapshot | POST /api/products; Bearer T; JSON `{}` | 400 | error không rỗng; list không đổi | README:195–197; GIẢ ĐỊNH status/error; kiểm thử tổng thể cố ý thiếu nhiều field |
| PR-G1-45 | EP | FR-15 | JSON sai cú pháp | Chung, snapshot | POST /api/products; Bearer T; raw JSON `{"name":` | 400 | error không rỗng; list không đổi | API spec:91; GIẢ ĐỊNH parser và status/error |
| PR-G1-46 | EP | FR-15 | Field id thừa | Chung; A(99999); snapshot | POST /api/products; Bearer T; JSON `B` thêm `"id":99999` | 200 | GET list có name K với id khác 99999; các sản phẩm cũ không đổi | API spec:91–99; GIẢ ĐỊNH bỏ qua id client, status/lưu |

**Ghi chú của AI:** FR-15 không quy định whitespace, kiểu name/category, optional fields, coercion, giới hạn độ dài phụ hoặc status và JSON lỗi; các diễn giải đều cần audit.
Không có schema GET hoặc mô tả cách trích id sản phẩm; setup và đối chiếu trường GET là giả định, không phải response đã quan sát.
PUT full/partial và hành vi id vắng mặt chưa rõ; các case chọn full body và giả định không upsert. Chưa gọi SUT.

## G2 – State transition (vòng đời sản phẩm)

Mô hình này là diễn giải CRUD, không phải state machine được đặc tả. Bảng trạng thái sau biểu diễn từng cặp trạng thái của **id mục tiêu** và sự kiện; `P mới` là id do POST cấp, không phải POST tới `/api/products/:id`. Mỗi ô dẫn trực tiếp case kiểm thử:

| Trạng thái | POST | GET /api/products/:id | PUT | DELETE |
|---|---|---|---|---|
| Chưa tồn tại | `P mới` tồn tại, 200 (PR-G2-01) | Chưa tồn tại, 404 (PR-G2-02) | Chưa tồn tại, 404 (PR-G2-03) | Chưa tồn tại, 404 (PR-G2-04) |
| Đang tồn tại | Id mục tiêu vẫn tồn tại và có `P mới` riêng, 200 (PR-G2-05) | Vẫn tồn tại, 200 (PR-G2-06) | Vẫn tồn tại, dữ liệu mới, 200 (PR-G2-07) | Đã xóa, 200 (PR-G2-08) |
| Đã xóa | Id đã xóa vẫn không hoạt động và có `P mới` riêng, 200 (PR-G2-09) | Vẫn đã xóa, 404 (PR-G2-10) | Vẫn đã xóa, 404 (PR-G2-11) | Lần hai: vẫn đã xóa, 404 (PR-G2-12) |

Tất cả status của product GET/POST/PUT/DELETE, JSON lỗi, việc không upsert, không tái sử dụng id đã xóa và POST tạo id mới là **GIẢ ĐỊNH** vì spec không quy định; GET sau xóa không còn sản phẩm hoạt động là diễn giải CRUD. Các thao tác POST ở ba hàng đều là tạo trên collection, không thao tác trực tiếp lên id mục tiêu. Các case 01–04 chọn một id vắng mặt trước POST; case 01 không giả định POST phải cấp đúng id đó.

Quy ước thực thi **độc lập cho từng case**: sinh UUID mới `U`, đặt `K` là ID case nối `-` với `U`; POST `/api/login`, header `Content-Type: application/json`, body `{"email":"admin@eshop.com","password":"Admin123!"}` và lấy `token` làm `T` (API spec:23–32). GET `/api/categories`, không body, chọn id danh mục hiện có làm số `C`; nếu không có danh mục thì setup thất bại. Mọi request product bên dưới dùng `Authorization: Bearer {{T}}`; request JSON thêm `Content-Type: application/json`, GET/DELETE không body. Thay placeholder trước khi gửi. `B` là `{"name":"{{K}}","price":100000,"description":"Mô tả ban đầu","imageUrl":"https://example.com/initial.png","category_id":{{C}}}`; `B2` là `{"name":"{{K}}-updated","price":150000,"description":"Mô tả mới","imageUrl":"https://example.com/updated.png","category_id":{{C}}}`; `Bnew` là `{"name":"{{K}}-new","price":120000,"description":"Sản phẩm mới","imageUrl":"https://example.com/new.png","category_id":{{C}}}`. Các trường trong response GET và cách lấy id từ danh sách là **GIẢ ĐỊNH**, không phải schema được spec đảm bảo.

Setup `P`: POST `/api/products` body `B`, GET `/api/products`, tìm duy nhất sản phẩm name `K` và lưu id `P`; nếu không tìm thấy duy nhất hoặc `P` thuộc 1..5 thì setup thất bại. Setup `D`: thực hiện `P`, DELETE `/api/products/{{P}}`, rồi GET `/api/products/{{P}}` xác nhận 404 và GET `/api/products` xác nhận không có id `P`; nếu không thì setup thất bại. Setup `A`: GET `/api/products`, chọn số nguyên dương `A` lớn hơn mọi id trong danh sách và lớn hơn 5, GET `/api/products/{{A}}` xác nhận 404; nếu không thì setup thất bại. Mỗi case lưu snapshot `S` từ GET `/api/products` ngay trước request chính; đối chiếu bằng id và toàn bộ field được trả về, bỏ qua thứ tự danh sách. Với chuỗi nhiều request, lưu snapshot tại thời điểm được chỉ định. Giả định không có actor khác thay đổi dữ liệu trong khi chạy.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| PR-G2-01 | ST | FR-15 | POST khi id mục tiêu chưa tồn tại | Chung; A; S | POST /api/products; Bearer T; JSON B | 200 | GET list có đúng một sản phẩm mới name K với price 100000, category_id C; mọi id trong S không đổi; không đòi id mới bằng A | README:193–197; API spec:80–98; GIẢ ĐỊNH status, shape list và cấp id |
| PR-G2-02 | ST | FR-15 | GET id chưa tồn tại | Chung; A; S | GET /api/products/{{A}}; Bearer T; không body | 404 | JSON error không rỗng; GET list bằng S | API spec:84–85; GIẢ ĐỊNH status, error và không thay đổi |
| PR-G2-03 | ST | FR-15 | PUT id chưa tồn tại không tạo mới | Chung; A; S | PUT /api/products/{{A}}; Bearer T; JSON B2 | 404 | JSON error không rỗng; GET list bằng S, không có id A | API spec:89; GIẢ ĐỊNH không upsert, status và error |
| PR-G2-04 | ST | FR-15 | DELETE id chưa tồn tại | Chung; A; S | DELETE /api/products/{{A}}; Bearer T; không body | 404 | JSON error không rỗng; GET list bằng S | API spec:90; GIẢ ĐỊNH status và error |
| PR-G2-05 | ST | FR-15 | POST khi sản phẩm mục tiêu đang tồn tại | Chung; P; S | POST /api/products; Bearer T; JSON Bnew | 200 | GET list có P với B không đổi và đúng một sản phẩm mới name K-new, id khác P; các id trong S không đổi | README:193; API spec:80–98; GIẢ ĐỊNH status, id và GET shape |
| PR-G2-06 | ST | FR-15 | GET sản phẩm đang tồn tại | Chung; P; S | GET /api/products/{{P}}; Bearer T; không body | 200 | Body có id P, name K, price 100000, description và imageUrl như B, category_id C; GET list bằng S | README:193; API spec:84–85; GIẢ ĐỊNH status và GET shape |
| PR-G2-07 | ST | FR-15 | PUT sản phẩm tồn tại | Chung; P; S | PUT /api/products/{{P}}; Bearer T; JSON B2 | 200 | GET P có name K-updated, price 150000, description, imageUrl và category_id như B2; các id khác P trong GET list bằng S | README:193,198; API spec:89,91–99; GIẢ ĐỊNH status và GET shape |
| PR-G2-08 | ST | FR-15 | DELETE sản phẩm tồn tại | Chung; P; S | DELETE /api/products/{{P}}; Bearer T; không body | 200 | GET P 404, GET list không có P và các id khác P bằng S | README:193; API spec:80–90; GIẢ ĐỊNH status, không còn hoạt động và GET shape |
| PR-G2-09 | ST | FR-15 | POST sau khi xóa sản phẩm khác | Chung; D; S | POST /api/products; Bearer T; JSON Bnew | 200 | GET P 404; GET list có đúng một sản phẩm name K-new với id khác P; mọi id trong S không đổi | README:193; API spec:80–90; GIẢ ĐỊNH status, không tái dùng id và GET shape |
| PR-G2-10 | ST | FR-15 | GET sản phẩm đã xóa | Chung; D; S | GET /api/products/{{P}}; Bearer T; không body | 404 | JSON error không rỗng; GET list bằng S, không có P | README:193; API spec:84–85,90; GIẢ ĐỊNH status, error và không còn hoạt động |
| PR-G2-11 | ST | FR-15 | PUT sản phẩm đã xóa | Chung; D; S | PUT /api/products/{{P}}; Bearer T; JSON B2 | 404 | JSON error không rỗng; GET P 404, GET list bằng S và không có P | API spec:89–90; GIẢ ĐỊNH không khôi phục/upsert, status và error |
| PR-G2-12 | ST | FR-15 | DELETE hai lần | Chung; D đã DELETE một lần; S | DELETE /api/products/{{P}}; Bearer T; không body | 404 | JSON error không rỗng; GET P 404, GET list bằng S và không có P | API spec:90; GIẢ ĐỊNH xóa lần hai lỗi, status và error |
| PR-G2-13 | ST | FR-15 | Vòng đời đầy đủ | Chung; GET list lưu S trước POST | POST /api/products JSON B → GET /api/products/{{P}} → PUT /api/products/{{P}} JSON B2 → GET /api/products/{{P}} → DELETE /api/products/{{P}} → GET /api/products/{{P}} → GET /api/products; tất cả Bearer T; GET/DELETE không body; sau POST lấy P duy nhất theo K từ GET list, dừng nếu P thuộc 1..5 | 200 → 200 → 200 → 200 → 200 → 404 → 200 | GET đầu có id P và mọi field B; GET sau PUT có id P và mọi field B2; GET sau DELETE có JSON error không rỗng; list cuối không có P và bằng S | README:193,198; API spec:80–99; GIẢ ĐỊNH status, error, GET shape và không còn hoạt động |
| PR-G2-14 | ST | FR-15 | Chỉ sản phẩm đích thay đổi | Chung; P; tạo thêm Q bằng POST Bnew, lấy id duy nhất theo K-new từ GET list, dừng nếu Q thuộc 1..5 hoặc Q=P; GET list lưu S | PUT /api/products/{{P}}; Bearer T; JSON B2 | 200 | GET P có mọi field B2; GET list so sánh theo id, toàn bộ sản phẩm khác P gồm Q và seed 1..5 giữ nguyên như S, không thêm/mất id | README:198; API spec:81,89,91–99; GIẢ ĐỊNH status và GET shape |
| PR-G2-15 | ST | FR-15 | Hai sản phẩm trùng tên | Chung; P; S | POST /api/products; Bearer T; JSON B | 200 | GET list có đúng hai id khác nhau cùng name K và các field B; P và các id trong S không đổi | README:193–197; API spec:88,91–99; GIẢ ĐỊNH tên không cần duy nhất, status và GET shape |
| PR-G2-16 | ST | FR-15 | PUT một phần giữ field không gửi | Chung; P; S | PUT /api/products/{{P}}; Bearer T; JSON `{"price":150000}` | 200 | GET P có price 150000; name, description, imageUrl, category_id giữ như B, không bị xóa trắng; mọi id khác P bằng S | README:193–198; API spec:89,91–99; GIẢ ĐỊNH partial PUT được chấp nhận, giữ field không gửi, status và GET shape |

**Ghi chú của AI:** Spec không định nghĩa uniqueness tên, partial PUT, id tái sử dụng, upsert hoặc xóa lần hai; các kết quả tương ứng là giả định cần audit.
Status và schema response sản phẩm/lỗi đều không được quy định; các điều kiện GET/error trong bảng là giả định, không phải response đã quan sát.
Không có request nào được gửi tới SUT trong bước này.

## G3 – Security

- FR-12 + SEC-02: cả POST, PUT, DELETE phải từ chối request thiếu JWT và không thay đổi dữ liệu.
- FR-12 + SEC-03: cả ba method phải từ chối JWT của user thường; SEC-06 kiểm tra thử sửa role qua profile rồi đăng nhập lại trước mỗi method.
- Token giả mạo: cả ba method phải từ chối JWT có claim admin nhưng chữ ký tự tạo hoặc không có chữ ký.
- SEC-05: POST/PUT thử injection ở name và description; PUT/DELETE thử injection trong path id; so sánh số lượng và toàn bộ sản phẩm sau request.
- SEC-04: POST/PUT thử stored XSS ở name; DELETE không có body name theo API spec nên không áp dụng payload body; API không chứng minh UI escape.
- Mass assignment: POST/PUT gửi id của sản phẩm khác và field lạ; DELETE không có body contract nên không áp dụng phép gán field.

Quy ước riêng G3, thực hiện độc lập cho **mỗi dòng**: tạo UUID mới `U`, `K` là ID case nối `-` với `U`. Login `POST /api/login`, `Content-Type: application/json`, body `{"email":"admin@eshop.com","password":"Admin123!"}`, lấy `token` làm `T`; login tương tự bằng `{"email":"test@eshop.com","password":"Test1234!"}` lấy `V`. `GET /api/categories` chọn id danh mục hiện có làm số `C`; nếu rỗng dừng setup. JSON `B` = `{"name":"{{K}}","price":100000,"description":"Mô tả {{K}}","imageUrl":"https://example.com/product.png","category_id":{{C}}}`; `B2` = `{"name":"{{K}}-updated","price":150000,"description":"Mô tả mới {{K}}","imageUrl":"https://example.com/new.png","category_id":{{C}}}`. Các phép `B[field]=value`, `B2[field]=value` là thay field trong bản sao JSON; `+field` là thêm field. Thay placeholder bằng giá trị thực trước khi gửi; C, P, Q là số JSON khi xuất hiện trong body. Mọi body JSON dùng `Content-Type: application/json`; GET/DELETE không body.

Setup `P,Q`: dùng `Authorization: Bearer {{T}}` POST `/api/products` với B, sau đó POST cùng B nhưng `name="{{K}}-other"`; GET `/api/products` tìm chính xác hai sản phẩm theo tên để lấy id `P,Q`; dừng nếu không duy nhất, bằng nhau, thuộc 1..5, hoặc không xác nhận được cả hai. Mỗi dòng đều dựng P,Q, rồi GET `/api/products` lưu snapshot `S` gồm toàn bộ sản phẩm, số lượng `N`; giả định không có actor khác sửa dữ liệu trong lúc test. Sau request chính GET `/api/products` và GET `/api/products/{{P}}`, `/api/products/{{Q}}` với Bearer T, đối chiếu theo id và toàn bộ field trả về, bỏ qua thứ tự. `S không đổi` nghĩa là số lượng N và mọi id cùng toàn bộ field bằng S, gồm P,Q và seed. Trường hợp thành công có thay đổi đích thì kiểm tra riêng trong bảng, các sản phẩm khác phải giữ nguyên. Shape list/detail, tên field GET và status product đều là giả định, không phải response quan sát.

Setup `E`: đăng ký user riêng qua POST `/api/register`, JSON `{"name":"{{K}}","email":"pr_{{U}}@test.com","password":"Test1234!"}`; login bằng email đó cùng password lấy `W`; PUT `/api/users/me`, Bearer W, JSON `{"role":"admin"}`; bất kể response, login lại cùng credentials lấy `W2`, GET `/api/users/me` với Bearer W2 xác nhận role không phải admin (field role là giả định); nếu role đã thành admin vẫn tiếp tục request chính để phát hiện leo quyền và ghi nhận thất bại SEC-06. Đăng ký dùng body theo API spec; field xác nhận mật khẩu ở README không có tên API được đặc tả.

Setup `F`: tạo JWT HS256 bằng cách base64url không padding UTF-8 của header `{"alg":"HS256","typ":"JWT"}` và payload `{"id":1,"role":"admin"}`, nối bằng dấu chấm rồi ký HMAC-SHA256 với secret thử `wrong-secret-{{U}}`, base64url không padding chữ ký; token là ba phần nối dấu chấm. Đây là token giả, không giả định secret hay thuật toán thật; test chỉ có ý nghĩa nếu secret thử không trùng secret thật. `H` là chuỗi token đó. `I` là URL-encoded `1%20OR%201%3D1`, tương ứng path id `1 OR 1=1`; nó không nhắm trực tiếp id seed hợp lệ.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| PR-G3-01 | SEC | FR-12, SEC-02 | Thiếu token tạo | Chung; P,Q; S | POST /api/products; không Authorization; JSON B2 | 401 | JSON object có `error` không rỗng; S không đổi, không có name K-updated | README:177–179,279; GIẢ ĐỊNH status/error và GET |
| PR-G3-02 | SEC | FR-12, SEC-02 | Thiếu token sửa | Chung; P,Q; S | PUT /api/products/{{P}}; không Authorization; JSON B2 | 401 | JSON object có `error` không rỗng; S không đổi | README:177–179,279; GIẢ ĐỊNH status/error và GET |
| PR-G3-03 | SEC | FR-12, SEC-02 | Thiếu token xóa | Chung; P,Q; S | DELETE /api/products/{{P}}; không Authorization; không body | 401 | JSON object có `error` không rỗng; S không đổi | README:177–179,279; GIẢ ĐỊNH status/error và GET |
| PR-G3-04 | SEC | FR-12, SEC-03 | User thường tạo | Chung; P,Q; S | POST /api/products; Authorization: Bearer {{V}}; JSON B2 | 403 | JSON `error` không rỗng; S không đổi, không có name K-updated | README:177–179,280; GIẢ ĐỊNH status/error và GET |
| PR-G3-05 | SEC | FR-12, SEC-03 | User thường sửa | Chung; P,Q; S | PUT /api/products/{{P}}; Authorization: Bearer {{V}}; JSON B2 | 403 | JSON `error` không rỗng; S không đổi | README:177–179,280; GIẢ ĐỊNH status/error và GET |
| PR-G3-06 | SEC | FR-12, SEC-03 | User thường xóa | Chung; P,Q; S | DELETE /api/products/{{P}}; Authorization: Bearer {{V}}; không body | 403 | JSON `error` không rỗng; S không đổi | README:177–179,280; GIẢ ĐỊNH status/error và GET |
| PR-G3-07 | SEC | FR-04, FR-12, SEC-03, SEC-06 | Tự nâng role rồi tạo | Chung; P,Q; E; S sau E | POST /api/products; Authorization: Bearer {{W2}}; JSON B2 | 403 | Profile sau E không có role admin; JSON `error` không rỗng; S không đổi | README:67,177–179,280,283; GIẢ ĐỊNH status/error và field role |
| PR-G3-08 | SEC | FR-04, FR-12, SEC-03, SEC-06 | Tự nâng role rồi sửa | Chung; P,Q; E; S sau E | PUT /api/products/{{P}}; Authorization: Bearer {{W2}}; JSON B2 | 403 | Profile sau E không có role admin; JSON `error` không rỗng; S không đổi | README:67,177–179,280,283; GIẢ ĐỊNH status/error và field role |
| PR-G3-09 | SEC | FR-04, FR-12, SEC-03, SEC-06 | Tự nâng role rồi xóa | Chung; P,Q; E; S sau E | DELETE /api/products/{{P}}; Authorization: Bearer {{W2}}; không body | 403 | Profile sau E không có role admin; JSON `error` không rỗng; S không đổi | README:67,177–179,280,283; GIẢ ĐỊNH status/error và field role |
| PR-G3-10 | SEC | FR-12, SEC-02, SEC-03 | JWT tự ký tạo | Chung; P,Q; F; S | POST /api/products; Authorization: Bearer {{H}}; JSON B2 | 401 | JSON `error` không rỗng; S không đổi | README:177–179,279–280; GIẢ ĐỊNH chữ ký sai, status/error |
| PR-G3-11 | SEC | FR-12, SEC-02, SEC-03 | JWT tự ký sửa | Chung; P,Q; F; S | PUT /api/products/{{P}}; Authorization: Bearer {{H}}; JSON B2 | 401 | JSON `error` không rỗng; S không đổi | README:177–179,279–280; GIẢ ĐỊNH chữ ký sai, status/error |
| PR-G3-12 | SEC | FR-12, SEC-02, SEC-03 | JWT tự ký xóa | Chung; P,Q; F; S | DELETE /api/products/{{P}}; Authorization: Bearer {{H}}; không body | 401 | JSON `error` không rỗng; S không đổi | README:177–179,279–280; GIẢ ĐỊNH chữ ký sai, status/error |
| PR-G3-13 | SEC | FR-15, SEC-05 | SQL injection name khi tạo | Chung; P,Q; S | POST /api/products; Authorization: Bearer {{T}}; JSON `B2[name]="{{K}}' OR 1=1 --"` | 200 | GET list có đúng một product mới với name literal đã gửi, N+1; mọi id trong S giữ nguyên | README:193–195,282; GIẢ ĐỊNH chấp nhận literal, status và GET |
| PR-G3-14 | SEC | FR-15, SEC-05 | SQL injection description khi tạo | Chung; P,Q; S | POST /api/products; Authorization: Bearer {{T}}; JSON `B2[description]="' OR 1=1 --"` | 200 | GET list có đúng một product mới name K-updated và description literal đã gửi, N+1; mọi id trong S giữ nguyên | README:193,282; API spec:96; GIẢ ĐỊNH chấp nhận literal, status và GET |
| PR-G3-15 | SEC | FR-15, SEC-05 | SQL injection name khi sửa | Chung; P,Q; S | PUT /api/products/{{P}}; Authorization: Bearer {{T}}; JSON `B2[name]="{{K}}' OR 1=1 --"` | 200 | GET P có name literal đã gửi; list N, mọi id khác P giữ nguyên như S | README:193,195,198,282; GIẢ ĐỊNH chấp nhận literal, status và GET |
| PR-G3-16 | SEC | FR-15, SEC-05 | SQL injection description khi sửa | Chung; P,Q; S | PUT /api/products/{{P}}; Authorization: Bearer {{T}}; JSON `B2[description]="' OR 1=1 --"` | 200 | GET P có description literal đã gửi; list N, mọi id khác P giữ nguyên như S | README:193,198,282; API spec:96; GIẢ ĐỊNH chấp nhận literal, status và GET |
| PR-G3-17 | SEC | FR-15, SEC-05 | SQL injection path sửa | Chung; P,Q; S | PUT /api/products/{{I}}; Authorization: Bearer {{T}}; JSON B2 | 400 | JSON `error` không rỗng; S không đổi, N không đổi | README:198,282; API spec:89; GIẢ ĐỊNH malformed id bị từ chối, status/error |
| PR-G3-18 | SEC | FR-15, SEC-05 | SQL injection path xóa | Chung; P,Q; S | DELETE /api/products/{{I}}; Authorization: Bearer {{T}}; không body | 400 | JSON `error` không rỗng; S không đổi, N không đổi | README:193,282; API spec:90; GIẢ ĐỊNH malformed id bị từ chối, status/error |
| PR-G3-19 | SEC | FR-15, SEC-04 | Stored XSS name khi tạo | Chung; P,Q; S | POST /api/products; Authorization: Bearer {{T}}; JSON `B2[name]="<script>alert(1)</script>"` | 200 | GET list có đúng một product mới với name literal đã gửi, N+1; mọi id trong S không đổi; không kết luận UI an toàn | README:195,281; GIẢ ĐỊNH API cho lưu nguyên văn, status và GET; spec chỉ yêu cầu UI escape |
| PR-G3-20 | SEC | FR-15, SEC-04 | Stored XSS name khi sửa | Chung; P,Q; S | PUT /api/products/{{P}}; Authorization: Bearer {{T}}; JSON `B2[name]="<img src=x onerror=alert(1)>"` | 200 | GET P có name literal đã gửi; list N, mọi id khác P không đổi; không kết luận UI an toàn | README:195,198,281; GIẢ ĐỊNH API cho lưu nguyên văn, status và GET; spec chỉ yêu cầu UI escape |
| PR-G3-21 | SEC | FR-15 | Mass assignment id và field lạ khi tạo | Chung; P,Q; S | POST /api/products; Authorization: Bearer {{T}}; JSON `B2` thêm `"id":{{Q}},"unexpected":"overwrite"` | 200 | GET list có một product mới name K-updated với id khác Q, N+1; mọi id S gồm Q không đổi; product mới không có field unexpected | README:193,198; API spec:87–99; GIẢ ĐỊNH server bỏ qua field thừa, cấp id mới, status và GET |
| PR-G3-22 | SEC | FR-15 | Mass assignment id và field lạ khi sửa | Chung; P,Q; S | PUT /api/products/{{P}}; Authorization: Bearer {{T}}; JSON `B2` thêm `"id":{{Q}},"unexpected":"overwrite"` | 200 | GET P giữ id P và có name K-updated; Q và mọi id khác P giữ nguyên; N không đổi; P không có field unexpected | README:193,198; API spec:89–99; GIẢ ĐỊNH server bỏ qua field thừa, status và GET |

**Ghi chú của AI:** Status và schema lỗi, GET shape, xử lý field thừa, HTML và malformed id đều không được quy định cụ thể; lựa chọn trong bảng là giả định để audit.
SEC-04 yêu cầu escape khi hiển thị UI, không bắt buộc API từ chối HTML; kiểm thử API không chứng minh việc render an toàn.
SEC-05 yêu cầu parameterized query; các phép thử black-box chỉ kiểm tra hậu quả của payload, không chứng minh cơ chế nội bộ.

## G4 – Schema validation

Bốn schema JSON Schema draft-07 dưới đây là mô hình kiểm thử, không phải hợp đồng response được spec bảo đảm. Spec không quy định field response bắt buộc; do đó các field đều tùy chọn trong schema, còn các case yêu cầu hiện diện được ghi rõ là **GIẢ ĐỊNH**. Mục 4.5 của phân tích chỉ quan sát POST có `message` string và `id` integer, PUT/DELETE có `message` string; không coi các quan sát này là yêu cầu. GET product chưa được quan sát.

**S1 — POST thành công:** `message`, `id` là field đã quan sát, nhưng spec không nói.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "message": {"type": "string"},
    "id": {"type": "integer"}
  }
}
```

**S2 — PUT và DELETE thành công:** `message` đã quan sát, nhưng spec không nói; dùng chung vì hai response quan sát có cùng cấu trúc.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "message": {"type": "string"}
  }
}
```

**S3 — lỗi:** shape `{error: string}` là GIẢ ĐỊNH, chưa được quan sát hoặc đặc tả; case lỗi yêu cầu `error` hiện diện riêng.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "error": {"type": "string"}
  }
}
```

**S4 — object sản phẩm:** toàn bộ field và kiểu response là GIẢ ĐỊNH; API spec 3.3 chỉ đưa ví dụ body input, không định nghĩa response GET. Ràng buộc price dương dựa trên FR-15.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "price": {"type": "number", "exclusiveMinimum": 0},
    "description": {"type": "string"},
    "imageUrl": {"type": "string"},
    "category_id": {"type": "integer"}
  }
}
```

Quy ước G4 độc lập **mỗi dòng**: sinh UUID mới `U`, `K` là ID case nối `-` với `U`. POST `/api/login` không Authorization, header `Content-Type: application/json`, body `{"email":"admin@eshop.com","password":"Admin123!"}`, lấy `token` làm `T`; GET `/api/categories` không body, chọn id danh mục hiện có làm số `C`, nếu không chọn được thì dừng setup. Với mọi request product dùng `Authorization: Bearer {{T}}`; POST/PUT thêm `Content-Type: application/json`, GET/DELETE không body. `B` = `{"name":"{{K}}","price":12345,"description":"Mô tả {{K}}","imageUrl":"https://example.com/initial.png","category_id":{{C}}}`; `B2` = `{"name":"{{K}}-updated","price":23456,"description":"Mô tả mới {{K}}","imageUrl":"https://example.com/updated.png","category_id":{{C}}}`. Thay placeholder bằng giá trị thực, C là JSON number.

Setup `P`: POST `/api/products` với B, sau đó GET `/api/products` tìm duy nhất sản phẩm name K, lấy integer id `P`; dừng nếu không xác định duy nhất hoặc P thuộc 1..5. Setup lấy id theo list và hình dạng list là giả định. Mỗi request chính và GET xác minh trong bảng phải có `Content-Type` response `application/json` (cho phép tham số charset), hoàn tất trong **< 2000 ms** tính riêng từng request, và đúng status trong bảng; các điều kiện này đều là GIẢ ĐỊNH do spec không quy định. Nếu setup thất bại, ghi thất bại setup, không dùng dữ liệu case khác.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| PR-G4-01 | SCH | FR-15 | Schema tạo và round-trip price | Quy ước G4; chưa tạo P | POST /api/products; Bearer T; JSON B; GET /api/products lấy P duy nhất theo K, dừng nếu P thuộc 1..5; GET /api/products/{{P}}; Bearer T; không body | 200 → 200 → 200 | POST khớp S1 và có message string, id integer bằng P; GET detail khớp S4, có id P, name K, price kiểu number bằng 12345, description/imageUrl/category_id đúng B | README:193–197; API spec:81,85,88,91–99; GIẢ ĐỊNH status, content-type, timing, response schema, list/GET shape và id |
| PR-G4-02 | SCH | FR-15 | Schema sửa và kiểm tra giá trị mới | Quy ước G4; P | PUT /api/products/{{P}}; Bearer T; JSON B2; GET /api/products/{{P}}; Bearer T; không body | 200 → 200 | PUT khớp S2, có message string; GET khớp S4, có id P, name K-updated, price number bằng 23456, description/imageUrl/category_id đúng B2 | README:193,196,198; API spec:85,89,91–99; GIẢ ĐỊNH status, content-type, timing, response schema và GET shape |
| PR-G4-03 | SCH | FR-15 | Schema xóa | Quy ước G4; P | DELETE /api/products/{{P}}; Bearer T; không body; GET /api/products/{{P}}; Bearer T; không body | 200 → 404 | DELETE khớp S2 và có message string; GET khớp S3 và có error string không rỗng | README:193; API spec:85,90; GIẢ ĐỊNH status, content-type, timing, schema lỗi/success và GET sau xóa |
| PR-G4-04 | SCH | FR-15 | Lỗi tạo thiếu name | Quy ước G4; GET /api/products lưu snapshot S theo id và toàn bộ field | POST /api/products; Bearer T; JSON `{"price":12345,"description":"Mô tả {{K}}","imageUrl":"https://example.com/initial.png","category_id":{{C}}}`; GET /api/products; Bearer T; không body | 400 → 200 | POST khớp S3, có error string không rỗng; list sau bằng S bỏ qua thứ tự | README:195; API spec:81,88,91–99; GIẢ ĐỊNH status, content-type, timing, error schema và GET list shape |
| PR-G4-05 | SCH | FR-15 | Lỗi sửa price không dương | Quy ước G4; P; GET /api/products lưu snapshot S | PUT /api/products/{{P}}; Bearer T; JSON `{"name":"{{K}}","price":0,"description":"Mô tả {{K}}","imageUrl":"https://example.com/initial.png","category_id":{{C}}}`; GET /api/products; Bearer T; không body | 400 → 200 | PUT khớp S3, có error string không rỗng; list sau bằng S bỏ qua thứ tự | README:196,198; API spec:81,89,91–99; GIẢ ĐỊNH status, content-type, timing, error schema và GET list shape |
| PR-G4-06 | SCH | FR-15 | Lỗi xóa id không tồn tại | Quy ước G4; GET /api/products chọn integer A lớn hơn 5 và mọi id trong list; GET /api/products/{{A}} xác nhận 404; lưu list làm S | DELETE /api/products/{{A}}; Bearer T; không body; GET /api/products; Bearer T; không body | 404 → 200 | DELETE khớp S3, có error string không rỗng; list sau bằng S bỏ qua thứ tự | API spec:81,85,90; GIẢ ĐỊNH status, content-type, timing, error schema và hành vi id vắng mặt |
| PR-G4-07 | SCH | FR-15 | Kiểu price trên product id chẵn và lẻ | Quy ước G4; lần lượt POST tối đa 10 sản phẩm bằng B, thay name thành `{{K}}-1` đến `{{K}}-10`, thay price tương ứng 10001 đến 10010; sau mỗi POST GET /api/products tìm id duy nhất theo name, dừng khi có một id chẵn E và một id lẻ O đều >5, lưu price đã gửi là PE, PO; không đủ hai parity thì setup thất bại | GET /api/products/{{E}}; Bearer T; không body; GET /api/products/{{O}}; Bearer T; không body | 200 → 200 | Mỗi body khớp S4 và có id đúng E hoặc O, price là number chứ không phải string và bằng PE hoặc PO tương ứng | README:193,196; API spec:81,85,88,91–99; GIẢ ĐỊNH id integer, phân bổ parity, status, content-type, timing và GET shape |
| PR-G4-08 | SCH | FR-15 | Kiểm tra GET object đầy đủ | Quy ước G4; P | GET /api/products/{{P}}; Bearer T; không body | 200 | Body khớp S4 và có đủ id, name, price, description, imageUrl, category_id; id P và mọi giá trị còn lại đúng B, price number bằng 12345 | README:193,196; API spec:85,91–99; GIẢ ĐỊNH status, content-type, timing và mọi field/kiểu GET |

**Ghi chú của AI:** Spec không quy định response schema/status, `Content-Type` hay ngưỡng 2000 ms; các kiểm tra tương ứng là giả định để audit, không phải kết quả SUT.
`message`/`id` chỉ được quan sát ở response POST trước đó; `message` PUT/DELETE cũng chỉ là quan sát. GET product và lỗi chưa được quan sát.
Parity id không được spec bảo đảm; case 07 dừng setup sau 10 sản phẩm nếu không tạo được cả hai loại, không sửa hay xóa seed.

## G5 – Tổng hợp độ phủ (reviewer)

Phạm vi: chỉ đọc `API3_product_generated.md` (G1–G4), `report/01_spec_analysis.md`, `eshop-sut/README.md` (FR-12, FR-15, SEC-01..07) và `api_specification.md`; không gửi request, không xóa hay sửa case của bước trước, không gán nhãn audit. ID viết tắt bỏ tiền tố `PR-` (ví dụ `G3-04` là `PR-G3-04`). Trong ma trận (5.3) mỗi ô liệt kê **mọi** ID liên quan, tính trước khi trừ trùng. Ký hiệu: `TRỐNG ⚠` là ô trống quan trọng; `TRỐNG (thấp)` là ô trống ưu tiên thấp; `N/A` là không áp dụng kèm lý do. Mức ưu tiên là đề xuất của AI.

### 5.1 Bảng đếm

Tổng thô 92 case (G1 46, G2 16, G3 22, G4 8). Trừ 7 case thuộc nhóm trùng thật (mục 5.2a) còn **85** case độc lập.

| Kỹ thuật | Thô | Trừ trùng | Sau trừ trùng | Ghi chú |
|---|---|---|---|---|
| EP | 32 | 4 (G1-22, G1-35, G1-39, G1-40) | 28 | G1: 32 case EP |
| BVA | 14 | 0 | 14 | G1-04..07, 12..15, 24, 25, 36, 37, 41, 42 |
| ST | 16 | 3 (G2-01, G2-07, G2-09) | 13 | toàn bộ G2 |
| SEC | 22 | 0 | 22 | toàn bộ G3 |
| SCH | 8 | 0 | 8 | toàn bộ G4 |
| **Tổng** | **92** | **7** | **85** | |

Đếm theo method đang được kiểm thử (method chính của request kiểm tra; G2-13 là chuỗi POST, GET, PUT, GET, DELETE, GET nên tính riêng; setup không tính):

| Method | G1 | G2 | G3 | G4 | Thô | Trừ trùng | Sau trừ trùng |
|---|---|---|---|---|---|---|---|
| POST /api/products | 36 | 4 | 8 | 2 | 50 | 3 (G1-22, G2-01, G2-09) | 47 |
| PUT /api/products/:id | 5 | 5 | 9 | 2 | 21 | 2 (G1-35, G2-07) | 19 |
| DELETE /api/products/:id | 5 | 3 | 5 | 2 | 15 | 2 (G1-39, G1-40) | 13 |
| GET (chi tiết, không phải mutation) | 0 | 3 | 0 | 2 | 5 | 0 | 5 |
| Chuỗi nhiều method (G2-13) | 0 | 1 | 0 | 0 | 1 | 0 | 1 |
| **Tổng** | 46 | 16 | 22 | 8 | **92** | **7** | **85** |

### 5.2 Test trùng và gần trùng (không xóa)

**5.2a Nhóm trùng thật.** Tiêu chí: cùng method, cùng lớp input, cùng lớp trạng thái đích, cùng status mong đợi, và phần kiểm tra nghiệp vụ giống nhau hoặc là tập con của nhau. Lớp kiểm tra bổ sung về schema, header hay thời gian không coi là trùng. Mỗi nhóm đếm một lần (hợp của nhóm), chỉ trừ số thành viên thừa so với đại diện giữ lại.

| Nhóm | ID trong nhóm | Lý do trùng | Đại diện giữ khi đếm | Số trừ |
|---|---|---|---|---|
| D1 | G1-22, G2-01, G2-05, G2-09 | Cùng `POST /api/products` với body hợp lệ, cùng 200, cùng kiểm tra "có đúng một sản phẩm mới, các sản phẩm khác không đổi". POST là tạo trên collection nên trạng thái của sản phẩm P hay id A trong precondition không phải input của request; G2-05 và G2-09 chỉ thêm khẳng định về P không đổi hoặc vẫn đã xóa | G2-05 | 3 |
| D2 | G2-07, G2-14 | Cùng `PUT` sản phẩm đang tồn tại với `B2` đầy đủ, cùng 200, cùng kiểm tra "P đổi, mọi id khác bằng S". G2-14 chỉ thêm sản phẩm Q vào tập các sản phẩm khác | G2-14 | 1 |
| D3 | G1-35, G2-03 | Cùng `PUT` id số chưa từng tồn tại, cùng body đầy đủ, cùng 404, cùng "error không rỗng, list không đổi" | G2-03 | 1 |
| D4 | G1-40, G2-04 | Cùng `DELETE` id số chưa từng tồn tại, cùng 404, cùng "error không rỗng, list không đổi" | G2-04 | 1 |
| D5 | G1-39, G2-08 | Cùng `DELETE` sản phẩm đang tồn tại, cùng 200, cùng "P không còn trong list, id khác không đổi"; G2-08 chỉ thêm GET P trả 404 | G2-08 | 1 |

Tổng trừ: 3 + 1 + 1 + 1 + 1 = **7**.

**5.2b Gần trùng (không trừ, giữ vì khác mục đích hoặc khác ô ma trận).**

| Cặp / nhóm | Giống | Khác | Vì sao không tính là trùng |
|---|---|---|---|
| G1-01 và G4-04 | POST thiếu name, 400, list không đổi | G4-04 thêm schema S3, Content-Type, thời gian | Có khẳng định SCH riêng |
| G1-40, G2-04 và G4-06 | DELETE id vắng, 404 | G4-06 thêm S3, Content-Type, thời gian | Có khẳng định SCH riêng |
| G1-39, G2-08 và G4-03 | DELETE sản phẩm tồn tại | G4-03 thêm schema S2/S3 | Có khẳng định SCH riêng |
| G2-07, G2-14 và G4-02 | PUT tồn tại với body đầy đủ | G4-02 thêm schema S2/S4, kiểu number của price | Có khẳng định SCH riêng |
| G1-22, G2-05 và G4-01 | POST hợp lệ, round-trip GET | G4-01 thêm S1, S4, id trả về bằng P | Có khẳng định SCH riêng |
| G2-06 và G4-08 | GET sản phẩm tồn tại, so mọi field với B | G4-08 thêm S4, Content-Type, thời gian; G2-06 thêm list bằng S | Mỗi bên có khẳng định riêng |
| G1-34 và G2-07, G2-14 | PUT tồn tại, các sản phẩm khác không đổi | G1-34 chỉ đổi price thành 1 (giá trị hợp lệ sát biên dưới) | Input khác nhau |
| G2-02/G2-10, G2-03/G2-11, G2-04/G2-12 | Cùng kết quả quan sát 404 và list không đổi | Chưa từng tồn tại so với đã xóa | Spec không phân biệt; hai ô trạng thái ST khác nhau |
| G1-38 và G3-17; G1-43 và G3-18 | PUT/DELETE với id không phải số, cùng 400 | G3 dùng payload `1 OR 1=1` cho SEC-05 | Khác mục đích (EP so với SEC-05) |
| G1-46 và G3-21 | POST kèm field `id` thừa | G1-46 dùng id vắng; G3-21 dùng id của Q đang tồn tại cùng field lạ | Kịch bản ghi đè khác nhau |
| G2-13 | Chuỗi gồm G2-01, 06, 07, 08, 10 | Kiểm thử chuỗi liên tục | Composite, không phải bản sao |
| G1-44 | Body rỗng bao gồm G1-01, 11, 21 | Thiếu đồng thời nhiều field | Composite |
| G2-15 | POST hợp lệ như D1 | Hai sản phẩm trùng tên | Khẳng định riêng về tên không duy nhất |

Nếu loại thêm toàn bộ các case phụ của 5.2b (tối đa 16 ID: G1-34, G1-44, G2-10, G2-11, G2-12, G2-13, G2-15, G3-17, G3-18, G3-21, G4-01, G4-02, G4-03, G4-04, G4-06, G4-08) thì còn ít nhất 69 case, vẫn vượt 35.

### 5.3 Ma trận độ phủ

Hàng ràng buộc FR-15 tách theo POST và PUT vì README:195–198 áp dụng cho cả "Thêm" và "Sửa" nhưng bộ case phân bố không đều.

| Hàng | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|
| FR-15 name, POST (R:195) | G1-01, 02, 03, 08, 09, 10, 44 | G1-04, 05, 06, 07 (1, 254, 255, 256 ký tự) | G2-01, 05, 09, 15 | G3-13 (SQL), G3-19 (XSS) | G4-04 (lỗi thiếu name), G4-01 |
| FR-15 name, PUT | Lớp hợp lệ: G1-34. Lớp không hợp lệ (thiếu, rỗng, không phải chuỗi): **TRỐNG ⚠** | **TRỐNG ⚠** (không có PUT name 255/256) | G2-07, 11, 14, 16 | G3-15 (SQL), G3-20 (XSS) | G4-02 |
| FR-15 price, POST (R:196) | G1-11, 16, 17, 18, 19, 20 | G1-12, 13, 14, 15 (0, âm, 0.01, 1) | G2-01, 05, 09, 13 (giá hợp lệ trong vòng đời) | TRỐNG (thấp): chưa có payload injection qua price (G1-18 chỉ là chuỗi chữ thường) | G4-01, 07, 08 (kiểu number) |
| FR-15 price, PUT | Lớp hợp lệ: G1-34. Lớp không hợp lệ (âm, chuỗi, null): **TRỐNG ⚠** | G4-05 (price 0, mang nhãn SCH); âm và 0.01 trên PUT: **TRỐNG ⚠** | G2-07, 14, 16 | TRỐNG (thấp) | G4-02, 05 |
| FR-15 category, POST (R:197) | G1-21, 22, 23, 26, 44 | G1-24, 25 (0, âm) | G2-01, 05, 09, 13 | TRỐNG (thấp): G1-26 chỉ là chuỗi chữ, chưa có payload SQL trong category_id | G4-01, 08 (category_id đúng giá trị) |
| FR-15 category, PUT | Lớp hợp lệ: G1-34. Lớp không hợp lệ (id vắng, thiếu): **TRỐNG ⚠** | **TRỐNG ⚠** (0, âm trên PUT) | G2-07, 13 | TRỐNG (thấp) | G4-02 |
| FR-15 chỉ sửa 1 sản phẩm (R:198) | G1-34 | N/A: quan hệ "một so với phần còn lại" không có giá trị biên số trong spec | G2-07, 14 (trực tiếp), G2-16 | G3-15, 16, 20, 22 (PUT độc hại, Q và sản phẩm khác giữ nguyên), G3-17 (path injection, S không đổi) | TRỐNG (thấp): G4-02 chỉ kiểm tra schema sản phẩm đích |
| Body chung và mass assignment (A:91–99) | G1-44, 45, 46 | N/A: không có biên số trên cấu trúc body | G2-15 (trùng tên) | G3-21 (POST), G3-22 (PUT) | G4-04 |
| FR-12 và SEC-02: JWT hợp lệ | G3-01, 02, 03 (thiếu token) | N/A: spec không nêu hạn token hay ngưỡng thời gian | N/A: spec không định nghĩa trạng thái token | G3-01, 02, 03, 10, 11, 12 (thiếu và HS256 ký sai); token không chữ ký (alg none) và token sai định dạng: **TRỐNG ⚠** | Một phần: G3-01.. kiểm tra `error` không rỗng; chưa kiểm tra S3 hay Content-Type cho 401 và 403 (TRỐNG, thấp) |
| FR-12 và SEC-03: role admin | G3-04, 05, 06 (user thường) | N/A: role không có giá trị biên | G3-07, 08, 09 (chuỗi nâng role rồi gọi) | G3-04..12 | TRỐNG (thấp) như hàng trên |
| SEC-04: escape khi hiển thị | G1-08 (Unicode), G1-33 (imageUrl không phải URL) gần nhưng không phải payload | N/A: không có biên | N/A: không có trạng thái | G3-19 (POST name), G3-20 (PUT name). XSS qua description và imageUrl: **TRỐNG ⚠ (trung bình)**. DELETE: N/A vì spec_analysis 3.4 ghi không có body contract. Việc UI escape: N/A cho collection API | N/A |
| SEC-05: parameterized query | G1-26, G1-38, G1-43 (kiểu id không phải số, không phải payload SQL) | G1-36, 37, 41, 42 (id biên số, không phải payload SQL) | N/A: không có trạng thái | G3-13, 14 (POST), G3-15, 16, 17 (PUT), G3-18 (DELETE) | N/A |
| SEC-06: không đổi role qua profile | N/A: chuỗi tấn công, không có lớp input riêng | N/A | G3-07, 08, 09 (chuỗi PUT /api/users/me rồi login lại rồi gọi product) | G3-07 (POST), G3-08 (PUT), G3-09 (DELETE) | N/A |
| SEC-01 | N/A: product API không xử lý password (R:278); chỉ là setup login | N/A | N/A | N/A | N/A |
| SEC-07 | N/A: product API không có OTP (R:284) | N/A | N/A | N/A | N/A |
| Method POST | G1-01, 02, 03, 08, 09, 10, 11, 16..23, 26..33, 44, 45, 46 | G1-04..07, 12..15, 24, 25 | G2-01, 05, 09, 15 | G3-01, 04, 07, 10, 13, 14, 19, 21 | G4-01, 04 |
| Method PUT | G1-34, 35, 38 (chỉ lớp id; lớp body không hợp lệ: **TRỐNG ⚠**) | G1-36, 37 (id biên) | G2-03, 07, 11, 14, 16 | G3-02, 05, 08, 11, 15, 16, 17, 20, 22 | G4-02, 05 |
| Method DELETE | G1-39, 40, 43 | G1-41, 42 | G2-04, 08, 12 | G3-03, 06, 09, 12, 18 | G4-03, 06 |

Ghi chú ma trận: các method GET (G2-02, 06, 10; G4-07, 08) chỉ có vai trò quan sát "Xem" của R:193 và không có hàng riêng. G2-13 (vòng đời đầy đủ) được tính vào hàng liên quan ở cột ST.

### 5.4 Kiểm tra định dạng

| Tiêu chí | Kết quả |
|---|---|
| Đủ 9 cột, đúng thứ tự tiêu đề | 92/92 dòng case có 9 ô; không có ký tự gạch đứng thừa làm lệch cột |
| ID không trùng, đúng mẫu `PR-G<n>-<2 chữ số>` | 92 ID duy nhất: G1 01–46, G2 01–16, G3 01–22, G4 01–08 |
| Request ghi rõ method và path | 92/92; body JSON dùng macro `B`, `B2`, `Bnew`, `B[field]=value` được định nghĩa trong cùng mục |
| Expected status cụ thể | 92/92 có mã cụ thể (G2-13 và các case G4 nhiều bước có chuỗi status theo từng bước) |
| Expected body cụ thể | 92/92 có điều kiện body hoặc điều kiện trạng thái dữ liệu; 49 dòng nêu `error` không rỗng |
| Có Nguồn expected | 92/92 trích README hoặc API spec kèm số dòng; 92/92 có "GIẢ ĐỊNH" (không case nào có status do spec quy định, vì spec không nêu status) |
| Không có nhãn audit | Không tìm thấy nhãn audit trong G1–G4 |

Điểm yếu về khả năng thực thi (ghi nhận, chưa sửa):
- **PR-G1-04**: name là `a` nên không chứa `K`; kiểm tra "GET list có sản phẩm name a" không phân biệt được sản phẩm của lần chạy này với sản phẩm khác tên `a` (ví dụ lần chạy trước chưa reset). Không có kiểm tra N+1 bằng snapshot.
- **G3, mục Token giả mạo**: đoạn mô tả nói "chữ ký tự tạo hoặc không có chữ ký" nhưng setup `F` chỉ tạo token HS256 ký bằng secret thử; không có token `alg` `none` hay token sai định dạng.
- **PR-G2-16**: PUT chỉ gửi `{"price":150000}` và mong 200, trong khi README:195–197 ghi name, price, category là bắt buộc và PR-G1-01 cùng nhóm kỳ vọng POST thiếu name trả 400. Quan hệ giữa hai giả định chưa được thống nhất.
- **PR-G2-13**: danh sách status có 7 phần tử, nhưng bước "lấy P theo K từ GET list" nằm ngoài chuỗi status; thực thi được nhưng người chuyển sang Postman phải tự thêm request.
- Mọi kiểm tra `GET /api/products` (list) dựa trên shape list không được spec đặc tả; các case đã nêu điều này là GIẢ ĐỊNH.

### 5.5 Kết luận

Tổng thô 92, trừ trùng 7, còn **85 case** ≥ 35 → **ĐỦ ≥ 35**. Phân bố: POST 47, PUT 19, DELETE 13, GET 5, chuỗi 1; EP 28, BVA 14, ST 13, SEC 22, SCH 8. Số lượng đủ, nhưng phân bố lệch: hàng PUT có 6 ô ma trận trống quan trọng về validation (H1..H3 dưới đây) và SEC-02 còn thiếu loại token không chữ ký. Đề xuất chuyển lỗ hổng cho bước G6.

### 5.6 Danh sách lỗ hổng cho G6

Mức ưu tiên là đề xuất của AI; mỗi test gợi ý dùng data riêng theo quy ước của mục liên quan, không đụng sản phẩm seed 1..5.

| Mã | Yêu cầu | Vì sao quan trọng | Gợi ý 1 test | Ưu tiên |
|---|---|---|---|---|
| H1 | FR-15 name khi Sửa (R:195; A:91–94, body Thêm/Sửa dùng chung) | Chỉ POST được kiểm tra name; PUT là đường khác có thể bỏ sót validation; 255 là ràng buộc số duy nhất của name | PUT `/api/products/{{P}}`, Bearer T, JSON `B2[name]=` chuỗi 256 ký tự bắt đầu bằng K → 400, error không rỗng, GET P giữ name cũ, list bằng S (GIẢ ĐỊNH status) | Cao |
| H2 | FR-15 price khi Sửa (R:196) | Chỉ G4-05 thử price 0 và có nhãn SCH; thiếu giá trị âm, chuỗi, 0.01 ở PUT | PUT `/api/products/{{P}}`, Bearer T, JSON `B2[price]=-1` → 400, error không rỗng, GET P giữ price cũ, list bằng S (GIẢ ĐỊNH status) | Cao |
| H3 | FR-15 category khi Sửa (R:197) | Không có PUT với category_id vắng hoặc không hợp lệ; PUT có thể gán danh mục sai và làm hỏng dữ liệu | PUT `/api/products/{{P}}`, Bearer T, JSON `B2[category_id]=99999` sau khi GET `/api/categories` xác nhận 99999 vắng → 400, GET P giữ category cũ, list bằng S (GIẢ ĐỊNH status) | Cao |
| H4 | SEC-02 và SEC-03 (R:279–280): token không chữ ký | Đoạn mô tả G3 hứa kiểm tra token "không có chữ ký" nhưng không có case; `alg` `none` là tấn công JWT phổ biến vào API Admin | Tạo token header `{"alg":"none","typ":"JWT"}` payload `{"id":1,"role":"admin"}` chữ ký rỗng (hai dấu chấm), POST `/api/products`, Bearer token đó, JSON `B2` → 401, error không rỗng, list bằng S (GIẢ ĐỊNH status) | Cao |
| H5 | SEC-02: token sai định dạng | Chỉ có thiếu token và HS256 ký sai; chuỗi không phải JWT (3 phần) chưa thử | PUT `/api/products/{{P}}`, `Authorization: Bearer not.a.jwt`, JSON `B2` → 401, list bằng S (GIẢ ĐỊNH status) | Trung bình |
| H6 | SEC-04 và SEC-05 qua description và imageUrl (R:281–282) | G3 chỉ thử name và description cho SQL; XSS chỉ ở name; imageUrl có thể chứa `javascript:` và được render thành ảnh hoặc liên kết | POST `/api/products`, Bearer T, JSON `B[imageUrl]="javascript:alert(1)"` và `B[description]="<img src=x onerror=alert(1)>"` → 200 (GIẢ ĐỊNH), GET list có đúng một sản phẩm mới với hai giá trị literal, N+1, mọi id trong S không đổi; ghi chú không chứng minh UI an toàn | Trung bình |
| H7 | FR-15 name khi POST: executability của G1-04 | Kết quả có thể khớp sản phẩm khác tên `a`, nên test có thể đạt nhầm hoặc không chạy ổn định | Sửa kiểm tra của G1-04: lưu snapshot S trước POST, sau POST so N+1 và đúng một sản phẩm mới có name `a`, price 100000, category C | Trung bình |
| H8 | FR-15 bắt buộc khi Sửa (R:195–197) so với G2-16 | G2-16 chấp nhận PUT một phần trong khi POST thiếu field bị từ chối; hai giả định cần thống nhất để expected không mâu thuẫn | PUT `/api/products/{{P}}`, Bearer T, JSON `B2-name` → 400 nếu coi name bắt buộc khi Sửa (GIẢ ĐỊNH, đối lập G2-16), GET P giữ nguyên; sinh viên chọn giữ một trong hai ở bước audit | Trung bình |
| H9 | FR-15 "Xem" (R:193; A:80–85): schema list | Mọi kiểm tra dữ liệu dựa trên `GET /api/products` nhưng không có schema cho list; G4-08 chỉ kiểm tra detail | GET `/api/products`, Bearer T → 200, body là mảng và mỗi phần tử khớp S4, chứa các id 1..5 (GIẢ ĐỊNH shape) | Thấp |
| H10 | SEC-02: thứ tự kiểm tra auth và validation | Request không token với body sai nên trả 401, không phải 400, để không lộ quy tắc validation cho người chưa xác thực | POST `/api/products`, không Authorization, JSON `{}` → 401, list bằng S (GIẢ ĐỊNH status và thứ tự) | Thấp |

**Ghi chú của AI:** Ma trận chỉ ghi ID có hiệu lực kiểm tra trực tiếp; các ô `N/A` đều nêu lý do và không tính là lỗ hổng.
Việc xác định nhóm trùng thật phụ thuộc tiêu chí ở 5.2a; sinh viên có thể coi G2-05 và G2-09 là khác nhau nếu muốn giữ đủ ô ST, khi đó tổng sau trừ trùng là 87.
Mọi status trong bộ case đều là GIẢ ĐỊNH nên độ phủ ở đây là độ phủ tình huống, chưa phải xác nhận hành vi SUT. Chưa gửi request nào tới SUT.

## G6 – Bổ sung theo G5

Ma trận lỗ hổng → case mới: H1 → PR-G6-01–06, 33–34; H2 → PR-G6-07–10, 35; H3 → PR-G6-11–14; H4 → PR-G6-16–18; H5 → PR-G6-19–21, 32; H6 → PR-G6-22–27; H7 → PR-G6-28; H8 → PR-G6-01, 11, 15; H9 → PR-G6-29; H10 → PR-G6-30–31.

**Quy tắc toàn bộ API 3 khi chuyển sang Execute:** chọn diễn giải full PUT yêu cầu đủ `name`, `price`, `category_id`: thiếu bất kỳ trường nào trả 400 và không đổi dữ liệu. Theo giả định hiện hành này, expected 200 của PR-G2-16 được thay bằng **400 và dữ liệu không đổi**; giữ nguyên mục cũ chỉ để truy vết nguồn gốc. Spec không giải quyết full/partial nên đây là GIẢ ĐỊNH, không phải sự thật đặc tả, cần audit. PR-G6-15 chỉ thiếu price, không lặp request thiếu cả name và category của PR-G2-16.

Quy ước độc lập **mỗi dòng**: tạo UUID mới `U`, `K` = ID case + `-` + `U`; POST `/api/login`, `Content-Type: application/json`, body `{"email":"admin@eshop.com","password":"Admin123!"}` lấy `token` làm `T`. GET `/api/categories` không body chọn id có sẵn làm số `C`; dừng setup nếu không có. `B` = `{"name":"{{K}}","price":100000,"description":"Mô tả {{K}}","imageUrl":"https://example.com/initial.png","category_id":{{C}}}`; `V` = `{"name":"{{K}}-updated","price":150000,"description":"Mô tả mới {{K}}","imageUrl":"https://example.com/new.png","category_id":{{C}}}`. `V[field]=value` thay đúng field trong bản sao V, `V-field` bỏ đúng field đó; các field khác giữ nguyên. `a×255`, `a×256` là chuỗi gồm chính xác 255 hoặc 256 ký tự ASCII `a`, không phải chuỗi ký hiệu nhân. Thay placeholder bằng giá trị thực, C là JSON number. Mọi request POST/PUT JSON thêm `Content-Type: application/json`; GET/DELETE không body. Các request setup và GET xác minh dùng `Authorization: Bearer {{T}}`, trừ GET categories và login.

Setup `P`: POST `/api/products` với Bearer T và JSON B; GET `/api/products` tìm duy nhất name K lấy id P, dừng nếu không duy nhất hoặc P thuộc 1..5. Trước request chính GET list và GET `/api/products/{{P}}` lưu snapshot `S` và detail `D`; so sánh theo id và toàn bộ field, bỏ qua thứ tự list, giả định không có actor khác thay dữ liệu. Sau **mọi** request chính, GET list và GET detail P với Bearer T. `Không đổi` nghĩa là list bằng S, detail bằng D, số lượng/id không đổi. Với PUT thành công: detail P đúng tất cả field V đã biến đổi, id P không đổi, list có cùng tập id và mọi sản phẩm khác P bằng S. Với POST thành công: list có đúng một id mới ngoài S, mọi id S không đổi; GET detail id mới đúng toàn bộ field body đã gửi. GET shape, status xác minh 200, identity và các predicate response đều là GIẢ ĐỊNH do spec chưa quy định; mọi setup thất bại thì dừng, không lấy dữ liệu case khác. Không sửa/xóa seed.

Token `N`: base64url không padding UTF-8 header `{"alg":"none","typ":"JWT"}` + `.` + base64url không padding UTF-8 payload `{"id":1,"role":"admin"}` + `.` (chữ ký rỗng). Claim id/role là GIẢ ĐỊNH, không dựa vào thuật toán hay secret thật. Token `M` là literal `not.a.jwt`; `M2` là literal `not-a-jwt`. Tất cả token tấn công truyền nguyên văn sau `Bearer `. Ở các case lỗi, giả định JSON object có `error` string không rỗng; status và shape lỗi không được spec nêu.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| PR-G6-01 | EP | FR-15 | H1, H8: thiếu name PUT | Quy ước G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V-name` | 400 | error không rỗng; Không đổi | README:195,198; API spec:89–99; GIẢ ĐỊNH full PUT, status/error |
| PR-G6-02 | EP | FR-15 | H1: name rỗng PUT | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[name]=""` | 400 | error không rỗng; Không đổi | README:195,198; GIẢ ĐỊNH rỗng bị từ chối, status/error |
| PR-G6-03 | EP | FR-15 | H1: name sai kiểu số | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[name]=123` | 400 | error không rỗng; Không đổi | README:195,198; API spec:94; GIẢ ĐỊNH string bắt buộc, status/error |
| PR-G6-04 | BVA | FR-15 | H1: name 255 ký tự | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[name]=a×255` | 200 | Detail P đúng V đã đổi name; list chỉ P đổi | README:195,198; GIẢ ĐỊNH status và GET |
| PR-G6-05 | BVA | FR-15 | H1: name 256 ký tự | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[name]=a×256` | 400 | error không rỗng; Không đổi | README:195,198; GIẢ ĐỊNH status/error |
| PR-G6-06 | EP | FR-15 | H1: name null | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[name]=null` | 400 | error không rỗng; Không đổi | README:195,198; GIẢ ĐỊNH null không hợp lệ, status/error |
| PR-G6-07 | BVA | FR-15 | H2: price âm | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[price]=-1` | 400 | error không rỗng; Không đổi | README:196,198; GIẢ ĐỊNH status/error |
| PR-G6-08 | EP | FR-15 | H2: price chuỗi | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[price]="150000"` | 400 | error không rỗng; Không đổi | README:196,198; GIẢ ĐỊNH không ép kiểu, status/error |
| PR-G6-09 | EP | FR-15 | H2: price null | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[price]=null` | 400 | error không rỗng; Không đổi | README:196,198; GIẢ ĐỊNH status/error |
| PR-G6-10 | BVA | FR-15 | H2: price dương 0.01 | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[price]=0.01` | 200 | Detail P đúng V với price number 0.01; list chỉ P đổi | README:196,198; GIẢ ĐỊNH status và độ chính xác lưu |
| PR-G6-11 | EP | FR-15 | H3, H8: thiếu category | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V-category_id` | 400 | error không rỗng; Không đổi | README:197–198; GIẢ ĐỊNH full PUT, status/error |
| PR-G6-12 | EP | FR-15 | H3: category 99999 không tồn tại | G6; P; GET /api/categories xác nhận không có id 99999, nếu có thì dừng; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[category_id]=99999` | 400 | error không rỗng; Không đổi | README:197–198; API spec:103; GIẢ ĐỊNH status/error |
| PR-G6-13 | BVA | FR-15 | H3: category 0 | G6; P; GET /api/categories xác nhận không có id 0, nếu có thì dừng; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[category_id]=0` | 400 | error không rỗng; Không đổi | README:197–198; GIẢ ĐỊNH status/error |
| PR-G6-14 | BVA | FR-15 | H3: category âm | G6; P; GET /api/categories xác nhận không có id -1, nếu có thì dừng; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[category_id]=-1` | 400 | error không rỗng; Không đổi | README:197–198; GIẢ ĐỊNH status/error |
| PR-G6-15 | EP | FR-15 | H8: thiếu riêng price | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V-price` | 400 | error không rỗng; Không đổi | README:196,198; GIẢ ĐỊNH full PUT, status/error |
| PR-G6-16 | SEC | FR-12, SEC-02, SEC-03 | H4: alg none tạo | G6; P; S,D; tạo N | POST /api/products; Authorization: Bearer {{N}}; JSON V | 401 | error không rỗng; Không đổi; không có sản phẩm mới name K-updated | README:177–179,279–280; GIẢ ĐỊNH status/error |
| PR-G6-17 | SEC | FR-12, SEC-02, SEC-03 | H4: alg none sửa | G6; P; S,D; tạo N | PUT /api/products/{{P}}; Authorization: Bearer {{N}}; JSON V | 401 | error không rỗng; Không đổi | README:177–179,279–280; GIẢ ĐỊNH status/error |
| PR-G6-18 | SEC | FR-12, SEC-02, SEC-03 | H4: alg none xóa | G6; P; S,D; tạo N | DELETE /api/products/{{P}}; Authorization: Bearer {{N}}; không body | 401 | error không rỗng; Không đổi | README:177–179,279–280; GIẢ ĐỊNH status/error |
| PR-G6-19 | SEC | FR-12, SEC-02 | H5: JWT sai cấu trúc tạo | G6; P; S,D | POST /api/products; Authorization: Bearer {{M}}; JSON V | 401 | error không rỗng; Không đổi | README:177–179,279; GIẢ ĐỊNH status/error |
| PR-G6-20 | SEC | FR-12, SEC-02 | H5: JWT sai cấu trúc sửa | G6; P; S,D | PUT /api/products/{{P}}; Authorization: Bearer {{M}}; JSON V | 401 | error không rỗng; Không đổi | README:177–179,279; GIẢ ĐỊNH status/error |
| PR-G6-21 | SEC | FR-12, SEC-02 | H5: JWT sai cấu trúc xóa | G6; P; S,D | DELETE /api/products/{{P}}; Authorization: Bearer {{M}}; không body | 401 | error không rỗng; Không đổi | README:177–179,279; GIẢ ĐỊNH status/error |
| PR-G6-22 | SEC | FR-15, SEC-04 | H6: XSS description POST | G6; P; S,D | POST /api/products; Bearer T; JSON `V[description]="<script>alert(1)</script>"` | 200 | Đúng một id mới có body literal, S và P không đổi; không kết luận UI | README:193,281; API spec:96; GIẢ ĐỊNH lưu literal, status/GET |
| PR-G6-23 | SEC | FR-15, SEC-04 | H6: XSS description PUT | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[description]="<script>alert(1)</script>"` | 200 | P đúng V gồm literal; list chỉ P đổi; không kết luận UI | README:198,281; API spec:96; GIẢ ĐỊNH lưu literal, status/GET |
| PR-G6-24 | SEC | FR-15, SEC-04 | H6: XSS imageUrl POST | G6; P; S,D | POST /api/products; Bearer T; JSON `V[imageUrl]="javascript:alert(1)"` | 200 | Đúng một id mới có body literal, S và P không đổi; không kết luận UI | README:193,281; API spec:97; GIẢ ĐỊNH lưu literal, status/GET |
| PR-G6-25 | SEC | FR-15, SEC-04 | H6: XSS imageUrl PUT | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[imageUrl]="javascript:alert(1)"` | 200 | P đúng V gồm literal; list chỉ P đổi; không kết luận UI | README:198,281; API spec:97; GIẢ ĐỊNH lưu literal, status/GET |
| PR-G6-26 | SEC | FR-15, SEC-05 | H6: SQL imageUrl POST | G6; P; S,D | POST /api/products; Bearer T; JSON `V[imageUrl]="' OR 1=1 --"` | 200 | Đúng một id mới có body literal, S và P không đổi | README:193,282; API spec:97; GIẢ ĐỊNH lưu literal, status/GET |
| PR-G6-27 | SEC | FR-15, SEC-05 | H6: SQL imageUrl PUT | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[imageUrl]="' OR 1=1 --"` | 200 | P đúng V gồm literal; list chỉ P đổi | README:198,282; API spec:97; GIẢ ĐỊNH lưu literal, status/GET |
| PR-G6-28 | BVA | FR-15 | H7: name một ký tự, xác nhận identity | G6; P; S,D; S là list trước POST | POST /api/products; Bearer T; JSON `V[name]="a"` | 200 | Tập id sau trừ id S có đúng một id mới; GET id mới có name `a` và mọi field còn lại đúng V; mọi id S gồm P không đổi, không dùng name để nhận diện | README:193–197; GIẢ ĐỊNH status, identity và GET |
| PR-G6-29 | SCH | FR-05, FR-15 | H9: schema list sản phẩm | G6; P; S,D | GET /api/products; Bearer T; không body | 200 | Body là JSON array; mọi phần tử khớp S4 G4; chứa đúng một object id P với đủ field và giá trị B; list bằng S, detail P bằng D | API spec:81,91–99; README:75,193; GIẢ ĐỊNH array, kiểu/field response, status và GET; không giả định seed là contract |
| PR-G6-30 | SEC | FR-12, FR-15, SEC-02 | H10: auth-first POST body rỗng | G6; P; S,D | POST /api/products; không Authorization; JSON `{}` | 401 | error không rỗng; Không đổi | README:177–179,195–197,279; GIẢ ĐỊNH auth trước validation, status/error |
| PR-G6-31 | SEC | FR-12, FR-15, SEC-02 | H10: auth-first PUT body rỗng | G6; P; S,D | PUT /api/products/{{P}}; không Authorization; JSON `{}` | 401 | error không rỗng; Không đổi | README:177–179,195–198,279; GIẢ ĐỊNH auth trước validation, status/error |
| PR-G6-32 | SEC | FR-12, SEC-02 | H5: JWT thiếu dấu phân cách | G6; P; S,D | POST /api/products; Authorization: Bearer {{M2}}; JSON V | 401 | error không rỗng; Không đổi | README:177–179,279; GIẢ ĐỊNH status/error |
| PR-G6-33 | EP | FR-15 | H1: name kiểu array | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[name]=["abc"]` | 400 | error không rỗng; Không đổi | README:195,198; API spec:94; GIẢ ĐỊNH string bắt buộc, status/error |
| PR-G6-34 | EP | FR-15 | H1: name kiểu boolean | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[name]=true` | 400 | error không rỗng; Không đổi | README:195,198; API spec:94; GIẢ ĐỊNH string bắt buộc, status/error |
| PR-G6-35 | EP | FR-15 | H2: price kiểu boolean | G6; P; S,D | PUT /api/products/{{P}}; Bearer T; JSON `V[price]=true` | 400 | error không rỗng; Không đổi | README:196,198; GIẢ ĐỊNH boolean không ép thành số, status/error |

**Ghi chú của AI:** Full PUT, thứ tự auth/validation, status, error schema, response GET và chấp nhận literal là giả định cần audit, không phải hành vi quan sát.
S4 chỉ kiểm kiểu các field có mặt; case 29 yêu cầu riêng đủ field cho sản phẩm tự tạo, không áp đặt seed hoặc field bắt buộc cho mọi item.
SEC-04 là yêu cầu escape ở UI; kiểm tra API không chứng minh UI an toàn. SEC-05 black-box không chứng minh cơ chế parameterized query.

## G5 – Tổng hợp độ phủ (reviewer)

Mục này là kết luận **hiện hành** sau khi đọc cả G1–G4 và G6; số liệu của mục G5 trước (85 case) được thay bằng số liệu bên dưới, mục cũ giữ nguyên để truy vết. Chỉ đọc file này, `report/01_spec_analysis.md`, `eshop-sut/README.md` (FR-05, FR-12, FR-15, SEC-01..07) và `eshop-sut/api_specification.md`; không gửi request tới SUT, không sửa hay xóa case nào, không gán nhãn audit. ID viết tắt bỏ tiền tố `PR-` (ví dụ `G6-28` là `PR-G6-28`). Quy tắc hiện hành cho cả file: **full PUT** của G6 (thiếu `name`, `price` hoặc `category_id` thì 400 và dữ liệu không đổi) là GIẢ ĐỊNH, không phải sự thật đặc tả; vì vậy G2-16 được đếm với expected hiện hành **400 và không đổi**, dòng 200 cũ của G2-16 chỉ để truy vết. Mọi status, JSON lỗi và hình dạng GET đều là GIẢ ĐỊNH vì spec không quy định.

### 5.A Bảng đếm

Tổng thô **127** case (G1 46, G2 16, G3 22, G4 8, G6 35). Có 6 nhóm trùng thật (mục 5.B1), hợp các nhóm có 8 thành viên thừa, còn **119** case độc lập. Sau trừ trùng theo mục: G1 41, G2 13, G3 22, G4 8, G6 35. So với G5 cũ: 85 + 35 case G6 − 1 nhóm trùng mới (D6) = 119.

| Kỹ thuật | G1 | G2 | G3 | G4 | G6 | Thô | Trừ trùng | Sau trừ trùng |
|---|---|---|---|---|---|---|---|---|
| EP | 32 | 0 | 0 | 0 | 12 | 44 | 4 (G1-22, G1-35, G1-39, G1-40) | 40 |
| BVA | 14 | 0 | 0 | 0 | 7 | 21 | 1 (G1-04) | 20 |
| ST | 0 | 16 | 0 | 0 | 0 | 16 | 3 (G2-01, G2-07, G2-09) | 13 |
| SEC | 0 | 0 | 22 | 0 | 15 | 37 | 0 | 37 |
| SCH | 0 | 0 | 0 | 8 | 1 | 9 | 0 | 9 |
| **Tổng** | 46 | 16 | 22 | 8 | 35 | **127** | **8** | **119** |

Đếm theo method của request chính được kiểm thử (request đầu tiên của case; GET xác minh sau request chính không tính; G2-13 là chuỗi POST, GET, PUT, GET, DELETE, GET nên tính riêng):

| Method | G1 | G2 | G3 | G4 | G6 | Thô | Trừ trùng | Sau trừ trùng |
|---|---|---|---|---|---|---|---|---|
| POST /api/products | 36 | 4 | 8 | 2 | 8 | 58 | 4 (G1-04, G1-22, G2-01, G2-09) | 54 |
| PUT /api/products/:id | 5 | 5 | 9 | 2 | 24 | 45 | 2 (G1-35, G2-07) | 43 |
| DELETE /api/products/:id | 5 | 3 | 5 | 2 | 2 | 17 | 2 (G1-39, G1-40) | 15 |
| GET (quan sát, không phải mutation) | 0 | 3 | 0 | 2 | 1 | 6 | 0 | 6 |
| Chuỗi nhiều method (G2-13) | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 |
| **Tổng** | 46 | 16 | 22 | 8 | 35 | **127** | **8** | **119** |

Số liệu thô G1–G4 khớp mục G5 cũ (92); G6 đếm từ file: 35 dòng, EP 12, BVA 7, SEC 15, SCH 1; POST 8, PUT 24, DELETE 2, GET 1.

### 5.B Test trùng và gần trùng (không xóa)

**5.B1 Nhóm trùng thật.** Tiêu chí: cùng method, cùng lớp input, cùng lớp trạng thái đích, cùng status, phần kiểm tra nghiệp vụ giống nhau hoặc là tập con của nhau. Thêm kiểm tra schema, header hay thời gian là khẳng định khác nên không phải trùng. Mỗi nhóm đếm một lần theo hợp của nhóm: chỉ trừ số thành viên thừa so với đại diện.

| Nhóm | ID trong nhóm | Lý do trùng | Đại diện giữ | Số trừ |
|---|---|---|---|---|
| D1 | G1-22, G2-01, G2-05, G2-09 | Cùng `POST /api/products` với body hợp lệ, cùng 200, cùng kiểm tra "đúng một sản phẩm mới, các sản phẩm khác không đổi"; POST là tạo trên collection nên trạng thái của P hay id A trong precondition không phải input của request | G2-05 | 3 |
| D2 | G2-07, G2-14 | Cùng PUT sản phẩm đang tồn tại với body đầy đủ, cùng 200, cùng "P đổi, mọi id khác bằng S"; G2-14 chỉ thêm sản phẩm Q | G2-14 | 1 |
| D3 | G1-35, G2-03 | Cùng PUT id số chưa từng tồn tại, body đầy đủ, 404, "error không rỗng, list không đổi" | G2-03 | 1 |
| D4 | G1-40, G2-04 | Cùng DELETE id số chưa từng tồn tại, 404, "error không rỗng, list không đổi" | G2-04 | 1 |
| D5 | G1-39, G2-08 | Cùng DELETE sản phẩm đang tồn tại, 200, "P không còn trong list, id khác không đổi"; G2-08 chỉ thêm GET P trả 404 | G2-08 | 1 |
| D6 (mới) | G1-04, G6-28 | Cùng POST, cùng lớp name 1 ký tự `a`, cùng 200; kiểm tra của G1-04 ("có sản phẩm name `a` và các field còn lại đúng") là tập con của G6-28, vốn thêm snapshot delta (đúng một id mới ngoài S, nhận diện theo id chứ không theo name). Giá trị price và description khác nhau không tạo lớp input khác. G6-28 thay thế G1-04 trong tính đếm; G1-04 chỉ giữ để truy vết, pass của G1-04 không được dùng làm bằng chứng do có thể khớp nhầm sản phẩm tên `a` khác | G6-28 | 1 |

Tổng trừ: 3 + 1 + 1 + 1 + 1 + 1 = **8**.

**5.B2 Gần trùng (không trừ).**

| Nhóm | Giống | Khác | Vì sao giữ |
|---|---|---|---|
| G1-01, G1-40, G2-04, G4-06, G1-39, G2-08, G4-03, G2-07, G2-14, G4-02, G1-22, G2-05, G4-01, G2-06, G4-08 | Cùng request với case chức năng ở nhóm D | G4 thêm schema S1 đến S4, Content-Type, thời gian; G2-06 thêm list bằng S | Có khẳng định SCH hoặc ST riêng |
| G1-34 với G2-07, G2-14 | PUT tồn tại, id khác không đổi | G1-34 chỉ đổi price thành 1 | Input khác |
| G2-02/G2-10, G2-03/G2-11, G2-04/G2-12 | Cùng 404, list không đổi | Chưa từng tồn tại so với đã xóa | Hai ô ST khác nhau |
| G1-38/G3-17, G1-43/G3-18 | PUT hoặc DELETE id không phải số, 400 | G3 dùng payload `1 OR 1=1` | Khác mục đích EP và SEC-05 |
| G1-46 với G3-21 | POST kèm `id` thừa | G3-21 dùng id của Q đang tồn tại cùng field lạ | Kịch bản ghi đè khác |
| G2-13, G1-44, G2-15 | Bao gồm hoặc gần các case khác | Chuỗi liên tục; thiếu đồng thời nhiều field; tên trùng | Composite hoặc khẳng định riêng |
| G2-16 với G6-01, G6-11, G6-15 | PUT thiếu field bắt buộc, 400 theo full PUT, không đổi | G2-16 chỉ gửi price (thiếu 4 field); mỗi case G6 thiếu đúng một field | Composite so với từng lớp thiếu, giống G1-44 |
| G6-03, G6-33, G6-34 (name số, array, boolean) và G6-08, G6-09, G6-35 (price chuỗi, null, boolean) | Cùng PUT, cùng field, cùng 400, cùng "không đổi" | Kiểu JSON khác nhau | Theo quy ước G1-09, G1-10, G1-17..20; mỗi kiểu có thể đi nhánh kiểm tra khác |
| G6-12, G6-13, G6-14 với G1-23, G1-24, G1-25 | Category 99999, 0, -1, 400 | PUT so với POST | Khác method |
| G6-04, G6-05, G6-07, G6-10 với G1-06, G1-07, G1-13, G1-14 | Cùng giá trị biên name hoặc price | PUT so với POST | Khác method |
| G6-16/G3-10, G6-17/G3-11, G6-18/G3-12 | Token admin giả bị từ chối, 401 | alg none (không chữ ký) so với HS256 sai secret | Khác lớp token |
| G6-19 với G6-32 | POST với chuỗi không phải JWT, 401 | `not.a.jwt` có 3 đoạn, `not-a-jwt` không có dấu chấm | Khác lớp cấu trúc |
| G6-30, G6-31 với G3-01, G3-02 | Không token, 401 | G6 gửi body `{}` để kiểm tra auth trước validation | Khác mục đích |
| G6-22..27 với G3-13..20 | Cùng loại payload SQL hoặc XSS | Field description, imageUrl so với name | Khác field |
| G6-29 với G2-06, G4-08 | GET dữ liệu sản phẩm | List mảng so với detail | Khác endpoint |

Cận dưới bảo thủ: loại thêm toàn bộ thành viên phụ của 5.B2 (G1-34, G1-44, G2-10, G2-11, G2-12, G2-13, G2-15, G2-16, G3-17, G3-18, G3-21, G4-01, G4-02, G4-03, G4-04, G4-06, G4-08, G6-09, G6-13, G6-14, G6-32, G6-33, G6-34, G6-35: 24 ID, không có ID nào đã bị trừ ở D1..D6) thì còn ít nhất **95**, vẫn vượt 35. Nếu sinh viên coi G2-01 và G2-09 là ô ST độc lập (D1 chỉ trừ G1-22) thì tổng là 121.

### 5.C Ma trận độ phủ

Mỗi ô liệt kê mọi ID có hiệu lực kiểm tra trực tiếp, tính trước khi trừ trùng. Cột là nhãn kỹ thuật của chính case, ngoại lệ ghi rõ. `TRỐNG (thấp)` là ô trống ưu tiên thấp, giải thích ở 5.F; `N/A` kèm lý do. Không còn ô `TRỐNG` quan trọng.

| Hàng | EP | BVA | ST | SEC | SCH |
|---|---|---|---|---|---|
| FR-15 name, POST (R:195) | G1-01, 02, 03, 08, 09, 10, 44 | G1-04, 05, 06, 07 (1, 254, 255, 256 ký tự), G6-28 (1 ký tự có snapshot delta) | G2-01, 05, 09, 15 | G3-13 (SQL), G3-19 (XSS) | G4-01, G4-04 (thiếu name) |
| FR-15 name, PUT | Lớp hợp lệ G1-34; lớp không hợp lệ G6-01 (thiếu), 02 (rỗng), 03 (số), 06 (null), 33 (array), 34 (boolean) | G6-04 (255), G6-05 (256) | G2-07, 14, 13; G2-16 (full PUT, thiếu name trong số các field thiếu: 400) | G3-15 (SQL), G3-20 (XSS) | G4-02 |
| FR-15 price, POST (R:196) | G1-11, 16, 17, 18, 19, 20 | G1-12, 13, 14, 15 (0, âm, 0.01, 1) | G2-01, 05, 09, 13 | TRỐNG (thấp) | G4-01, 07, 08 (price kiểu number) |
| FR-15 price, PUT | Lớp hợp lệ G1-34; lớp không hợp lệ G6-08 (chuỗi), 09 (null), 35 (boolean), 15 (thiếu) | G6-07 (-1), G6-10 (0.01), G4-05 (0, nhãn SCH) | G2-07, 14, 13; G2-16 | TRỐNG (thấp) | G4-02, G4-05 |
| FR-15 category, POST (R:197) | G1-21, 22, 23, 26, 44 | G1-24, 25 (0, -1) | G2-01, 05, 09, 13 | TRỐNG (thấp) | G4-01, G4-08 |
| FR-15 category, PUT | Lớp hợp lệ G1-34; lớp không hợp lệ G6-11 (thiếu), G6-12 (99999 vắng) | G6-13 (0), G6-14 (-1) | G2-07, 14, 13; G2-16 | TRỐNG (thấp) | G4-02 |
| FR-15 chỉ sửa 1 sản phẩm (R:198) | G1-34 | N/A: quan hệ "một so với phần còn lại" không có biên số trong spec | G2-07, 14, 13; G2-16 (PUT bị từ chối không đổi gì); G1-34 | PUT thành công, list khác không đổi: G3-15, 16, 20, 22, G6-23, 25, 27. PUT bị từ chối, không đổi: G3-02, 05, 08, 11, 17, G6-17, 20, 31 | G4-02 (sản phẩm đích); list bằng S kiểm bằng G6-29 (GET, không có PUT) |
| Body chung và mass assignment (A:91–99) | G1-44, 45, 46 | N/A: không có biên số trên cấu trúc body | G2-15 (tên trùng); G2-16 (full PUT) | G3-21 (POST), G3-22 (PUT) | G4-04, G4-05 |
| FR-12 và SEC-02: JWT hợp lệ (R:177–179, 279) | Lớp token (nhãn kỹ thuật các case này là SEC): thiếu G3-01..03; HS256 sai secret G3-10..12; alg none G6-16..18; sai cấu trúc G6-19..21, 32 | N/A: spec không nêu hạn hay độ dài token | N/A: spec không định nghĩa trạng thái token | POST: G3-01, 10, G6-16, 19, 30, 32. PUT: G3-02, 11, G6-17, 20, 31. DELETE: G3-03, 12, G6-18, 21 (auth-first không áp dụng: DELETE không có body) | TRỐNG (thấp) |
| FR-12 và SEC-03: role admin (R:280) | G3-04, 05, 06 (user thường) | N/A: role không có biên | G3-07, 08, 09 (nâng role rồi gọi) | G3-04..09; token admin giả cũng bị chặn ở G3-10..12, G6-16..18 | TRỐNG (thấp) |
| SEC-04: escape khi hiển thị (R:281) | Lớp input chứa HTML hoặc JS theo field (nhãn SEC): name G3-19, 20; description G6-22, 23; imageUrl G6-24, 25 | N/A: không có biên | N/A: spec không có trạng thái cho escape | POST: G3-19, G6-22, 24. PUT: G3-20, G6-23, 25. DELETE: N/A, không có body, chỉ gián tiếp qua UI (spec_analysis 3.4) | N/A: escape xảy ra ở UI, API không có schema escape; không chứng minh UI an toàn |
| SEC-05: parameterized query (R:282) | G1-38, G1-43 (id không phải số); G3-17, G3-18 (payload ở path) | G1-36, 37, 41, 42 (id biên, không payload) | N/A: không có trạng thái | POST: G3-13, 14, G6-26. PUT: G3-15, 16, 17, G6-27. DELETE: G3-18 | N/A: black-box không chứng minh cơ chế |
| SEC-06: không đổi role qua profile (R:283) | N/A: chuỗi tấn công, không có lớp input riêng | N/A | G3-07, 08, 09 (PUT /api/users/me rồi đăng nhập lại rồi gọi product) | G3-07 (POST), G3-08 (PUT), G3-09 (DELETE) | N/A |
| SEC-01 (R:278) | N/A: product API không xử lý password, login chỉ là setup | N/A | N/A | N/A | N/A |
| SEC-07 (R:284) | N/A: product API không có OTP | N/A | N/A | N/A | N/A |
| Method POST | G1-01..03, 08..11, 16..23, 26..33, 44..46 | G1-04..07, 12..15, 24, 25, G6-28 | G2-01, 05, 09, 15 | G3-01, 04, 07, 10, 13, 14, 19, 21, G6-16, 19, 22, 24, 26, 30, 32 | G4-01, 04 |
| Method PUT | G1-34, 35, 38, G6-01, 02, 03, 06, 08, 09, 11, 12, 15, 33, 34, 35 | G1-36, 37, G6-04, 05, 07, 10, 13, 14 | G2-03, 07, 11, 14, 16 | G3-02, 05, 08, 11, 15, 16, 17, 20, 22, G6-17, 20, 23, 25, 27, 31 | G4-02, 05 |
| Method DELETE | G1-39, 40, 43 | G1-41, 42 | G2-04, 08, 12 | G3-03, 06, 09, 12, 18, G6-18, 21 | G4-03, 06 |
| GET quan sát (R:193 "Xem") | N/A: không phải mutation | N/A | G2-02, 06, 10, 13 | N/A | G4-07, 08, G6-29 (list, mỗi phần tử khớp S4) |

Hàng ST cho 12 ô trạng thái (3 trạng thái × 4 sự kiện) của G2 đều có case trực tiếp: POST G2-01, 05, 09; GET G2-02, 06, 10; PUT G2-03, 07, 11; DELETE G2-04, 08, 12.

### 5.D Kiểm tra định dạng

Kết quả đếm bằng grep/awk trên file (chỉ đọc), tính cho toàn bộ 127 dòng case.

| Tiêu chí | Kết quả |
|---|---|
| Đủ 9 cột | 127/127 dòng có đúng 9 ô, không ô trống, không dấu gạch đứng thừa (G1 46, G2 16, G3 22, G4 8, G6 35) |
| ID duy nhất, đúng mẫu `PR-G<n>-<2 chữ số>` | 127 ID duy nhất; G1 01–46, G2 01–16, G3 01–22, G4 01–08, G6 01–35 |
| Request ghi rõ method | 127/127 bắt đầu bằng POST, PUT, DELETE hoặc GET (G2-13 và case G4 nhiều bước liệt kê method từng bước); body dùng macro B, B2, Bnew, V, N, M, M2 được định nghĩa trong cùng mục của case |
| Expected status cụ thể | 127/127 có mã số cụ thể (chuỗi mã cho case nhiều bước) |
| Expected body cụ thể | 127/127 có predicate dữ liệu; 78 dòng nêu `error` không rỗng (regex trên cột Expected body) |
| Nguồn expected | 127/127 trích README hoặc API spec kèm số dòng; 127/127 có "GIẢ ĐỊNH" (spec không quy định status) |
| Nhãn audit | Không có nhãn audit nào trong file |

Khả năng thực thi, đánh giá trên văn bản:
- Điểm yếu đã nêu ở G5 cũ nay đã được xử lý bằng case hoặc quy tắc: G1-04 false-pass qua G6-28 (D6); token không chữ ký qua G6-16..18; xung đột G2-16 với G1-01 qua full PUT (G2-16 hiện hành 400, dòng 200 cũ chỉ truy vết, khi chuyển sang Postman phải dùng 400).
- Còn lại là lưu ý, không phải thiếu case: G2-13 cần thêm bước tra P theo K bằng GET list ngoài chuỗi status; G6-29 dùng S4 của G4 (không định nghĩa schema mới), và S4 không có `required` nên "khớp S4" cho phần tử seed chỉ kiểm kiểu field có mặt, còn sự hiện diện đủ field chỉ được khẳng định cho sản phẩm tự tạo P; đây là hệ quả của việc spec không bảo đảm field response, đã ghi giả định.
- Các token N, M, M2, snapshot S, detail D và setup P đều có định nghĩa đủ trong mục G6 để dựng request Postman; chưa gửi request nào.

### 5.E Ánh xạ H1..H10 sang G6

| Hạng mục | Case G6 | Ghi nhận |
|---|---|---|
| H1 name khi Sửa | G6-01 (thiếu), 02 (rỗng), 03 (số), 04 (255), 05 (256), 06 (null), 33 (array), 34 (boolean) | Gợi ý gốc PUT name 256 là G6-05 |
| H2 price khi Sửa | G6-07 (-1), 08 (chuỗi), 09 (null), 10 (0.01), 35 (boolean) | Giá trị 0 giữ ở G4-05 |
| H3 category khi Sửa | G6-11 (thiếu), 12 (99999 vắng), 13 (0), 14 (-1) | Setup xác nhận id vắng qua GET /api/categories |
| H4 token không chữ ký | G6-16 (POST), 17 (PUT), 18 (DELETE) | Đủ 3 method; token N có chữ ký rỗng, phân biệt với token sai chữ ký G3-10..12 |
| H5 token sai định dạng | G6-19 (POST), 20 (PUT), 21 (DELETE), 32 (POST, không dấu chấm) | `not.a.jwt` khác `not-a-jwt`: hai lớp cấu trúc khác nhau |
| H6 description và imageUrl | G6-22, 23 (XSS description POST, PUT), 24, 25 (`javascript:alert(1)` ở imageUrl POST, PUT), 26, 27 (SQL imageUrl POST, PUT) | Chỉ kiểm tra lưu và đọc lại literal, không chứng minh UI an toàn; gợi ý gốc dùng `<img onerror>`, G6 dùng `<script>` cho description, cùng lớp HTML/JS |
| H7 G1-04 executability | G6-28 | Snapshot delta thay nhận diện theo name; D6 |
| H8 full/partial PUT | Quy tắc full PUT của G6; G6-01, 11, 15; G2-16 hiện hành 400 | Giả định hiện hành cho cả file, cần audit; không còn mâu thuẫn với G1-01 |
| H9 schema list | G6-29 | Dùng S4 của G4 cho từng phần tử, không tạo schema riêng |
| H10 auth trước validation | G6-30 (POST), 31 (PUT) | DELETE không có body nên không có phép thử tương ứng |

Cả 35 case G6 đều được ánh xạ (01–06 H1, 07–10 H2, 11–14 H3, 15 H8, 16–18 H4, 19–21 H5, 22–27 H6, 28 H7, 29 H9, 30–31 H10, 32 H5, 33–34 H1, 35 H2). Không có case G6 nào mồ côi.

### 5.F Kết luận và lỗ hổng

Sau trừ trùng còn **119 case**, vượt ngưỡng 35 → **ĐỦ ≥ 35** (THIẾU 0 case). Phân bố: EP 40, BVA 20, ST 13, SEC 37, SCH 9; POST 54, PUT 43, DELETE 15, GET 6, chuỗi 1. Mỗi hàng ràng buộc FR-15 (name, price, category, chỉ sửa 1 sản phẩm) có case ở cả POST và PUT, ba method đều có EP, BVA hoặc SEC, SEC-02..06 đều có case cho từng method áp dụng, 12 ô ST đều có case.

**Lỗ hổng thật còn lại: không có.** Không cần vòng G6 tiếp theo.

Các điểm sau không tính là thiếu case vì là giới hạn của spec đã ghi giả định hoặc nằm ngoài phạm vi yêu cầu G1–G4; ghi để sinh viên cân nhắc ở bước Audit:

| Điểm | Vì sao không tính là lỗ hổng |
|---|---|
| Status, JSON lỗi, id cấp mới, hình dạng GET list và detail, Content-Type, 2000 ms | Spec không quy định; thêm case không giải quyết được, cần audit giả định |
| Token hết hạn hoặc bị thu hồi | Spec không nêu thời hạn token; không thể dựng token hợp lệ đã hết hạn nếu không biết secret |
| SQL injection qua price và category_id | G3 gốc chỉ yêu cầu name, description và path id (G6 đã thêm imageUrl); lớp "không phải số" và "không thuộc danh sách" đã có G1-17, 18, 26 và G6-08, 12, 13, 14, nên thêm payload là mở rộng phạm vi |
| Độ dài name tính theo ký tự đa byte | Các case BVA 255 và 256 dùng ký tự ASCII; spec nói "255 ký tự" nhưng không nêu mã hóa; chỉ là ý tưởng tùy chọn, không thuộc yêu cầu G1–G4 |
| Auth trước validation cho DELETE | DELETE không có body contract nên không có phép thử body sai |
| Schema S3 và Content-Type cho 401 và 403 | Shape lỗi là giả định; G3 và G6 đã kiểm `error` không rỗng cho mọi case từ chối |

**Ghi chú của AI:** Việc chọn nhóm trùng phụ thuộc tiêu chí ở 5.B1; D6 coi G6-28 thay thế G1-04, còn nếu giữ ô ST độc lập thì tổng là 121, kết luận ĐỦ không đổi.
Full PUT là giả định hiện hành, không phải đặc tả; nếu audit chọn PUT một phần thì G2-16, G6-01, 11, 15 và các case G6 PUT thiếu field phải đổi expected cùng lúc.
Mọi status, JSON lỗi, GET shape và việc chấp nhận literal HTML hoặc SQL đều là GIẢ ĐỊNH; độ phủ ở đây là độ phủ tình huống, chưa xác nhận hành vi SUT. Chưa gửi request nào.

## Audit – Nhãn VALID / INVALID / INCOMPLETE (Human review)

Phần này chỉ gắn nhãn, không sửa bảng test phía trên. Nhãn xét theo quy ước hiện hành của chính file (quy tắc hợp nhất ở G6).
- **VALID** – chạy được ngay theo dòng; expected rõ, có nguồn spec hoặc giả định đã ghi và không mâu thuẫn.
- **INCOMPLETE** – request đúng nhưng còn thiếu hoặc không chắc một phần để chạy/assert: status cũ đã có quy ước thay thế, setup có điều kiện spec không bảo đảm, hoặc oracle chưa kiểm được.
- **INVALID** – trùng ngữ nghĩa với case khác (không thêm độ phủ), hoặc case không kiểm được điều nó tuyên bố.

| ID | Nhãn | Lý do (1 dòng) |
|---|---|---|
| PR-G1-01 | VALID | Thiếu name → 400; snapshot list xác nhận không đổi. |
| PR-G1-02 | VALID | Name rỗng → 400; một field sai duy nhất. |
| PR-G1-03 | VALID | Name toàn khoảng trắng → 400; giả định trim đã ghi. |
| PR-G1-04 | INVALID | False-pass: nhận diện theo name 'a' có thể khớp sản phẩm khác; G6-28 thay thế. |
| PR-G1-05 | VALID | Name 254 ký tự → 200; sát biên dưới 255. |
| PR-G1-06 | VALID | Name 255 ký tự → 200; đúng biên trên của FR-15. |
| PR-G1-07 | VALID | Name 256 ký tự → 400; ngay trên biên. |
| PR-G1-08 | VALID | Name tiếng Việt có dấu → 200; kiểm Unicode. |
| PR-G1-09 | VALID | Name null → 400; giả định kiểu đã ghi. |
| PR-G1-10 | VALID | Name kiểu số → 400; API spec yêu cầu string. |
| PR-G1-11 | VALID | Thiếu price → 400; trường bắt buộc theo R:196. |
| PR-G1-12 | VALID | Price 0 → 400; biên dưới của > 0. |
| PR-G1-13 | VALID | Price -1 → 400; phía âm. |
| PR-G1-14 | VALID | Price 0.01 → 200; giá dương nhỏ nhất thực dụng. |
| PR-G1-15 | VALID | Price 1 → 200; giá dương nhỏ. |
| PR-G1-16 | VALID | Price 1e15 → 200; spec không nêu trần, giả định đã ghi. |
| PR-G1-17 | VALID | Price chuỗi số → 400; giả định không ép kiểu đã ghi. |
| PR-G1-18 | VALID | Price chuỗi chữ → 400; cùng lớp kiểu. |
| PR-G1-19 | VALID | Price null → 400. |
| PR-G1-20 | VALID | Price boolean → 400; giả định không ép kiểu. |
| PR-G1-21 | VALID | Thiếu category_id → 400; trường bắt buộc. |
| PR-G1-22 | INVALID | Trùng D1 với PR-G2-05: cùng POST body hợp lệ, cùng 200 và oracle. |
| PR-G1-23 | VALID | Category 99999 không tồn tại → 400; xác minh trước bằng categories. |
| PR-G1-24 | VALID | Category 0 → 400; biên dưới. |
| PR-G1-25 | VALID | Category -1 → 400; phía âm. |
| PR-G1-26 | VALID | Category chuỗi abc → 400; sai kiểu. |
| PR-G1-27 | VALID | Thiếu description → 200; field tùy chọn theo A:91–99. |
| PR-G1-28 | VALID | Description rỗng → 200; giả định cho rỗng đã ghi. |
| PR-G1-29 | VALID | Description 10.000 ký tự → 200; giả định không giới hạn. |
| PR-G1-30 | VALID | Thiếu imageUrl → 200; field tùy chọn. |
| PR-G1-31 | VALID | ImageUrl rỗng → 200; giả định đã ghi. |
| PR-G1-32 | VALID | ImageUrl 10.000 ký tự → 200; kiểm không giới hạn. |
| PR-G1-33 | VALID | ImageUrl không phải URL → 200; giả định không validate URL. |
| PR-G1-34 | VALID | PUT id tồn tại, chỉ đổi price → 200; các field khác giữ nguyên. |
| PR-G1-35 | INVALID | Trùng D3 với PR-G2-03: cùng PUT id vắng, cùng 404. |
| PR-G1-36 | VALID | PUT id 0 → 404; không upsert, giả định đã ghi. |
| PR-G1-37 | VALID | PUT id âm → 404; cùng lớp id vắng. |
| PR-G1-38 | VALID | PUT id abc → 400; id không phải số. |
| PR-G1-39 | INVALID | Trùng D5 với PR-G2-08: cùng DELETE sản phẩm tồn tại, cùng 200. |
| PR-G1-40 | INVALID | Trùng D4 với PR-G2-04: cùng DELETE id vắng, cùng 404. |
| PR-G1-41 | VALID | DELETE id 0 → 404. |
| PR-G1-42 | VALID | DELETE id âm → 404. |
| PR-G1-43 | VALID | DELETE id abc → 400; sai kiểu. |
| PR-G1-44 | VALID | Body {} → 400; thiếu đồng thời nhiều field. |
| PR-G1-45 | VALID | JSON sai cú pháp → 400; parser phải từ chối. |
| PR-G1-46 | VALID | Field id thừa → 200, id mới khác 99999; chống ghi đè. |
| PR-G2-01 | INVALID | Trùng D1 với PR-G2-05: cùng POST body hợp lệ, cùng 200. |
| PR-G2-02 | VALID | GET id chưa tồn tại → 404; trạng thái chưa tồn tại. |
| PR-G2-03 | VALID | PUT id chưa tồn tại không upsert → 404. |
| PR-G2-04 | VALID | DELETE id chưa tồn tại → 404. |
| PR-G2-05 | VALID | POST khi P đang tồn tại → 200; P không đổi, id mới riêng. |
| PR-G2-06 | VALID | GET P hiện tại → 200, đủ field B; K list bằng S. |
| PR-G2-07 | INVALID | Trùng D2 với PR-G2-14: cùng PUT B2 đầy đủ, cùng 200 và oracle. |
| PR-G2-08 | VALID | DELETE P → 200; GET 404, list không còn P. |
| PR-G2-09 | INVALID | Trùng D1 với PR-G2-05: cùng POST body, cùng 200, khác trạng thái setup. |
| PR-G2-10 | VALID | GET P đã xóa → 404; trạng thái đã xóa. |
| PR-G2-11 | VALID | PUT P đã xóa → 404; không khôi phục. |
| PR-G2-12 | VALID | DELETE hai lần → 404; idempotent ở mức lỗi. |
| PR-G2-13 | VALID | Vòng đời đầy đủ POST→GET→PUT→GET→DELETE→GET→list; status từng bước. |
| PR-G2-14 | VALID | Chỉ P đổi; Q và seed 1..5 giữ nguyên. |
| PR-G2-15 | VALID | Hai sản phẩm trùng tên → 200; giả định tên không unique. |
| PR-G2-16 | INCOMPLETE | PUT partial 200 trái quy ước full PUT hiện hành (400); phải sửa expected. |
| PR-G3-01 | VALID | Thiếu token POST → 401; S không đổi. |
| PR-G3-02 | VALID | Thiếu token PUT → 401. |
| PR-G3-03 | VALID | Thiếu token DELETE → 401. |
| PR-G3-04 | VALID | User thường POST → 403; role admin bắt buộc. |
| PR-G3-05 | VALID | User thường PUT → 403. |
| PR-G3-06 | VALID | User thường DELETE → 403. |
| PR-G3-07 | VALID | Nâng role qua profile rồi POST → 403; profile vẫn user. |
| PR-G3-08 | VALID | Nâng role rồi PUT → 403. |
| PR-G3-09 | VALID | Nâng role rồi DELETE → 403. |
| PR-G3-10 | VALID | JWT tự ký HS256 POST → 401. |
| PR-G3-11 | VALID | JWT tự ký HS256 PUT → 401. |
| PR-G3-12 | VALID | JWT tự ký HS256 DELETE → 401. |
| PR-G3-13 | VALID | SQLi name POST → 200 lưu literal, N+1; kiểm hậu quả. |
| PR-G3-14 | VALID | SQLi description POST → 200 lưu literal. |
| PR-G3-15 | VALID | SQLi name PUT → 200 lưu literal; id khác không đổi. |
| PR-G3-16 | VALID | SQLi description PUT → 200 lưu literal. |
| PR-G3-17 | VALID | SQLi path PUT → 400; S và N không đổi. |
| PR-G3-18 | VALID | SQLi path DELETE → 400. |
| PR-G3-19 | VALID | XSS name POST → 200 lưu literal; không kết luận UI. |
| PR-G3-20 | VALID | XSS name PUT → 200 lưu literal. |
| PR-G3-21 | VALID | Mass assignment id + field lạ POST; id mới khác Q. |
| PR-G3-22 | VALID | Mass assignment id + field lạ PUT; P giữ id. |
| PR-G4-01 | VALID | Schema POST + round-trip price; assertion cụ thể. |
| PR-G4-02 | VALID | Schema PUT + giá trị mới; kiểm price number. |
| PR-G4-03 | VALID | Schema DELETE + GET 404; S2 và S3 rõ. |
| PR-G4-04 | VALID | Schema lỗi thiếu name; list bằng snapshot. |
| PR-G4-05 | VALID | Schema lỗi price 0; cùng predicate S3. |
| PR-G4-06 | VALID | Schema lỗi DELETE id vắng → 404. |
| PR-G4-07 | INCOMPLETE | Phụ thuộc phân bổ id chẵn/lẻ trong 10 lần POST; có thể dừng setup. |
| PR-G4-08 | VALID | GET object đầy đủ; kiểm kiểu và giá trị từng field. |
| PR-G6-01 | VALID | Thiếu name PUT → 400; dữ liệu không đổi. |
| PR-G6-02 | VALID | Name rỗng PUT → 400. |
| PR-G6-03 | VALID | Name số PUT → 400; giả định string bắt buộc. |
| PR-G6-04 | VALID | Name 255 ký tự PUT → 200; đúng biên. |
| PR-G6-05 | VALID | Name 256 ký tự PUT → 400; ngay trên biên. |
| PR-G6-06 | VALID | Name null PUT → 400. |
| PR-G6-07 | VALID | Price -1 PUT → 400; biên âm. |
| PR-G6-08 | VALID | Price chuỗi PUT → 400. |
| PR-G6-09 | VALID | Price null PUT → 400. |
| PR-G6-10 | VALID | Price 0.01 PUT → 200; biên dương nhỏ. |
| PR-G6-11 | VALID | Thiếu category PUT → 400; full PUT. |
| PR-G6-12 | VALID | Category 99999 PUT → 400; xác minh vắng trước. |
| PR-G6-13 | VALID | Category 0 PUT → 400. |
| PR-G6-14 | VALID | Category -1 PUT → 400. |
| PR-G6-15 | VALID | Thiếu price PUT → 400. |
| PR-G6-16 | VALID | JWT alg none POST → 401; token N cụ thể. |
| PR-G6-17 | VALID | JWT alg none PUT → 401. |
| PR-G6-18 | VALID | JWT alg none DELETE → 401. |
| PR-G6-19 | VALID | JWT sai cấu trúc not.a.jwt POST → 401. |
| PR-G6-20 | VALID | JWT sai cấu trúc PUT → 401. |
| PR-G6-21 | VALID | JWT sai cấu trúc DELETE → 401. |
| PR-G6-22 | VALID | XSS description POST → 200 lưu literal; không kết luận UI. |
| PR-G6-23 | VALID | XSS description PUT → 200 lưu literal. |
| PR-G6-24 | VALID | javascript: ở imageUrl POST → 200 lưu literal. |
| PR-G6-25 | VALID | javascript: ở imageUrl PUT → 200 lưu literal. |
| PR-G6-26 | VALID | SQLi imageUrl POST → 200 lưu literal. |
| PR-G6-27 | VALID | SQLi imageUrl PUT → 200 lưu literal. |
| PR-G6-28 | VALID | Name 1 ký tự nhưng nhận diện bằng snapshot delta, không theo name. |
| PR-G6-29 | VALID | Schema list; kiểm phần tử và đúng một object P. |
| PR-G6-30 | VALID | Auth-first: POST body {} không token → 401. |
| PR-G6-31 | VALID | Auth-first: PUT body {} không token → 401. |
| PR-G6-32 | VALID | JWT không dấu chấm POST → 401; lớp cấu trúc khác. |
| PR-G6-33 | VALID | Name array PUT → 400; sai kiểu. |
| PR-G6-34 | VALID | Name boolean PUT → 400. |
| PR-G6-35 | VALID | Price boolean PUT → 400. |

**Tổng: 117 VALID – 2 INCOMPLETE – 8 INVALID / 127 case.**

## Extend – Human

Sinh sau khi Generate đã xong và được phép đọc `eshop-sut/backend/server.js`; mỗi case dưới đây chỉ dùng `POST/PUT/DELETE /api/products` (GET chỉ làm oracle) và nhắm một hành vi code khác spec mà bộ case AI chưa kiểm. Expected lấy từ spec; chỗ spec không nói ghi GIẢ ĐỊNH. Bảng giữ đúng 9 cột như bảng gốc.

Quy ước: dùng lại G3 — login `admin@eshop.com` / `Admin123!` lấy `T`; `GET /api/categories` lấy `C`; `GET /api/products` lưu snapshot `S` trước mỗi request; setup `P` bằng POST `B` rồi xác định `P` theo name `K` như G3.

| ID | Kỹ thuật | Requirement | Mục đích | Precondition / setup | Request | Expected status | Expected body / kiểm tra | Nguồn expected |
|---|---|---|---|---|---|---|---|---|
| PR-EX-01 | EP | FR-15, API spec:89 | ID có dấu `+` không được sửa sản phẩm | Setup P; snapshot S | `PUT /api/products/%2B{{P}}`; Bearer T; JSON `V` | 400 | JSON `error` không rỗng; GET `P` giữ nguyên B, list bằng S | FR-15; GIẢ ĐỊNH ID nguyên không dấu, như PR-G1-38 dùng `abc` |
| PR-EX-02 | EP | FR-15 | ID dạng `P.0` không được sửa sản phẩm | Setup P; snapshot S | `PUT /api/products/{{P}}.0`; Bearer T; JSON `V` | 400 | JSON `error` không rỗng; GET `P` giữ nguyên B, list bằng S | FR-15; GIẢ ĐỊNH ID nguyên, như PR-G1-38 dùng `abc` |
| PR-EX-03 | BVA | FR-15 | Price vượt giới hạn double phải bị từ chối | Snapshot S | `POST /api/products`; Bearer T; JSON `B[price]=1e309` | 400 | JSON `error` không rỗng; list bằng S | FR-15 "price là số dương"; GIẢ ĐỊNH 1e309 không phải số hữu hạn hợp lệ |
| PR-EX-04 | BVA | FR-15 | Price `-0` phải bị từ chối | Snapshot S | `POST /api/products`; Bearer T; JSON `B[price]=-0` | 400 | JSON `error` không rỗng; list bằng S | FR-15; GIẢ ĐỊNH `-0` không phải số dương vì bằng 0 |
| PR-EX-05 | EP | FR-15, API spec:89–90 | ID không nguyên không được xóa sản phẩm | S; xác nhận product id 2 tồn tại; chạy trên DB reset riêng và reset lại ngay sau case vì đây là seed | `DELETE /api/products/2.0`; Bearer T; không body | 400 | JSON `error` không rỗng; list vẫn có id 2 và bằng S | FR-15; GIẢ ĐỊNH ID nguyên, như PR-G1-43 dùng `abc` |
| PR-EX-06 | EP | FR-15, API spec:89–90 | ID có dấu `+` không được xóa sản phẩm | Setup P; snapshot S | `DELETE /api/products/%2B{{P}}`; Bearer T; không body | 400 | JSON `error` không rỗng; list vẫn có P, bằng S | FR-15; GIẢ ĐỊNH ID nguyên không dấu |

**Vì sao AI bỏ sót**
- **PR-EX-01:** AI chỉ thử `abc` cho path PUT; không biết SQLite tự ép `+P` thành số nguyên nên request vẫn sửa được P.
- **PR-EX-02:** AI chỉ thử id `0`, âm, `abc` và id vắng; không thử số thực khớp số nguyên.
- **PR-EX-03:** AI chỉ thử price `0`, âm, `null`, boolean, chuỗi; không thử tràn double `1e309` (JSON vẫn hợp lệ) nên không thấy dữ liệu bị `null`.
- **PR-EX-04:** AI chỉ thử biên `0`; không thử `-0`, giá trị bằng 0 nhưng khác dấu.
- **PR-EX-05:** AI chỉ kiểm `abc` cho path; PR-G4-07 chỉ kiểm kiểu price nên không thấy `2.0` xóa được seed.
- **PR-EX-06:** AI chỉ thử `abc`, `%40`, `%20`; không biết SQLite ép `+P` nên không thấy DELETE vẫn xóa P.
