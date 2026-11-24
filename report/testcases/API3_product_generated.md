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
