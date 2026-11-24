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
