# B0 – Triage ứng viên bug

Nguồn: `report/execute/API1_login_results.md`, `API2_cancel_results.md`, `API3_product_results.md` và testcase tương ứng. `R:` chỉ dòng trong `eshop-sut/README.md`, `A:` chỉ dòng trong `eshop-sut/api_specification.md`; `server.js` và `database.js` thuộc `eshop-sut/backend/`. Đây là đề xuất của AI, không phải kết luận hay bug report đã được sinh viên xác nhận. Không chạy lại SUT. LSP không được cấu hình; đối chiếu trực tiếp mã và dòng. Nhóm nguồn dùng đúng thứ tự đánh số trong ba báo cáo Execute, không phải mã testcase. Một case có thể xuất hiện ở nhiều dòng khi các assertion phản ánh các nguyên nhân khác nhau; mỗi **nhóm nguồn** chỉ được phân loại một lần.

## a) Đề xuất là bug

Severity/Priority trong bảng đều là **đề xuất của AI**, không phải quyết định cuối. Cột xác nhận cố ý để trống. ID là ID dự kiến, chưa tạo issue.

| Nhóm nguồn | ID đề xuất | Tiêu đề | Case ID bị ảnh hưởng trong kết quả | Phát hiện bởi | Spec vi phạm | Nguyên nhân gốc – bằng chứng mã | Severity / Priority đề xuất của AI | Sinh viên xác nhận |
|---|---|---|---|---|---|---|---|---|
| LG-04, LG-05 | BUG-LG-01 | Đếm sai và khóa sai thời lượng | LG-G2-01, 04, 05, 06, 08, LG-EX-02; LG-G2-07, 11, LG-G3-09, LG-G6-03 (LG-G6-01 chỉ lệch status giả định) | Cả hai | R:41–42 | `server.js:54–57`: mỗi lần sai cộng **2**, ngưỡng 3 dẫn đến khóa sau hai lần; thời hạn cố định **180000 ms** thay vì 30 giây. Các phép chờ 31 giây quan sát 403; không cần giả định việc thử lại gia hạn khóa. | major / P1 |  |
| LG-07 | BUG-LG-02 | Login trả mật khẩu trong user | LG-G4-01, 02, 03, 07 | AI-generated | A:24–32; bảo mật hiển nhiên: không tiết lộ mật khẩu | `server.js:35,46,51–52`: SELECT toàn bộ user và trả nguyên object, gồm password; `database.js:50–55` có cột password. | critical / P1 |  |
| LG-10, CN-08 | BUG-LG-03 | Secret JWT cố định trong source cho phép giả mạo token | LG-EX-05; CN-EX-05 | Human Extend | R:43, 177–179, 279–280; A:59, 112 | `server.js:9,51,100–107`: cùng secret hardcode được dùng ký và xác minh; hai case tự ký được chấp nhận. Một nguyên nhân xuyên API login/user và cancel, chỉ một issue; không công bố secret/token. | critical / P0 |  |
| CN-01 | BUG-CN-01 | Chấp nhận scheme Basic như Bearer | CN-G1-13 | AI-generated | R:43; A:112 | `server.js:100–107`: tách lấy phần thứ hai của Authorization nhưng không kiểm scheme; token hợp lệ sau `Basic` được dùng hủy đơn. Không dựa vào mã 401 giả định. | major / P1 |  |
| CN-02 | BUG-CN-02 | User hủy được đơn đang shipping | CN-G2-03 | AI-generated | R:158–162, 236 | `server.js:321–335`: chỉ từ chối delivered/canceled, bỏ lọt shipping; oracle quan sát canceled. | major / P1 |  |
| CN-03 | BUG-CN-03 | Chuyển đơn canceled sang delivered | CN-G2-10 | AI-generated | R:158–162, 218–221 | `server.js:550–551` cho phép rõ canceled → delivered; oracle quan sát delivered. | major / P1 |  |
| PR-01, PR-02 | BUG-PR-01 | Thiếu kiểm tra ràng buộc sản phẩm khi tạo và sửa | POST: PR-G1-01, 02, 07, 09, 11, 12, 13, 18, 19, 21, 23, 24, 25, 26, 44; PR-G4-04; PR-EX-04. PUT: PR-G4-05; PR-G6-01, 02, 05, 06, 07, 09, 11, 12, 13, 14, 15 (09 và 15 từ lượt isolated) | Cả hai | R:191–198; A:87–99 | `server.js:167–186` ghi trực tiếp input không validate; `database.js:63–71` không có ràng buộc tương ứng. Kết quả cho thấy thiếu/rỗng/null/tên quá dài, giá thiếu/null/không dương/không phải số và category thiếu/không tồn tại được lưu. Thiếu trường PUT chỉ được đưa vào khi thực tế bị ghi null, không dựa vào giả định bắt buộc full PUT. | major / P1 |  |
| PR-03 | BUG-PR-02 | Mutation sản phẩm bỏ qua JWT và role admin | PR-G3-01–12; PR-G6-16–21, 30, 31 (isolated), 32 | AI-generated | R:174–179, 279–280; A:87–90 | `server.js:167–196`: POST/PUT/DELETE không gắn `authenticateToken` cũng không kiểm role; các mutation thành công và snapshot đổi. Các case G3-07–09 còn kiểm profile ở lỗi riêng bên dưới. | critical / P0 |  |
| PR-04 | BUG-PR-03 | User tự sửa role qua profile | PR-G3-07, 08, 09 | AI-generated | R:64–67, 283; A:64–73 | `server.js:118–129` nhận `role` từ client và đưa vào UPDATE; profile sau thao tác trả role admin. Đây là lỗi profile, khác thiếu middleware product. | critical / P1 |  |
| PR-07 | BUG-PR-04 | GET chi tiết sản phẩm gây mất kết nối với giá null | PR-G6-09, 15, 31 (ba lượt isolated) | AI-generated | R:83–85; A:84–85; tính sẵn sàng/bảo mật hiển nhiên | Trong ba lượt, PUT thành công, GET detail socket hang up. `server.js:159–163` gọi `row.price.toString()` cho ID chẵn mà không kiểm null; PUT thiếu/null price ghi null tại `server.js:179–183`. Đây là nguyên nhân mã phù hợp với evidence và độc lập với thiếu validation; kết quả không tự chứng minh toàn bộ tiến trình đã dừng. | critical / P1 |  |

**Giới hạn nhóm PR-01/02:** PR-G1-03 (chỉ whitespace), G1-10 (name số), G1-17/20 (ép kiểu giá), PR-G2-16 (partial PUT), PR-G6-03/08/33/34/35 (kiểu/ép kiểu) và PR-EX-03 (`1e309`/hữu hạn) cần sinh viên quyết định cách diễn giải, không tính là case vi phạm đã xác lập ở dòng trên. G6-33–35 là **PUT**, không phải POST. PR-G6-04 là tên 255 hợp lệ, fail detail/schema không chứng minh validation; không tính vào bug validation. Status 400 và schema error đều là giả định; spec không ấn định chúng. FR-15 yêu cầu giá là số dương, nhưng hình thức JSON và ép kiểu cần quyết định riêng. Thiếu field trong PUT có thể hiểu là partial update hoặc full replacement; dù theo cách nào kết quả cuối không được làm mất trường bắt buộc. Các phần mơ hồ này nằm trong ghi chú nhóm đã phân loại, không tạo bản sao nhóm trong bảng b.

## b) Cần sinh viên quyết định

Hai cách hiểu được nêu để review, không mặc định cách nào là kết luận. Status chênh lệch đơn thuần không đủ tạo bug.

| Nhóm nguồn | Case / bằng chứng | Hai cách hiểu và mã liên quan |
|---|---|---|
| LG-01 | LG-G1-10, 11, 12: 401 với email viết hoa/khoảng trắng | Email nên case-insensitive/trim để thuận tiện **hoặc** phải khớp chính xác input; R:40, A:24–32 không nêu normalization. `server.js:33–38` so sánh trực tiếp. |
| LG-02 | LG-G1-23: JSON sai cú pháp, HTML SyntaxError, oracle parse JSON fail | API nên trả JSON lỗi thống nhất **hoặc** parser được phép trả HTML 400; A:25–32 không quy định schema lỗi. `server.js:12` dùng body parser; không suy diễn lộ token. |
| LG-03 | LG-G1-24: media type không phải JSON, 500 HTML TypeError | Nên từ chối content type và trả lỗi có kiểm soát **hoặc** 415/JSON là oracle giả định chưa được spec bảo đảm; A:25–32. `server.js:12,32–33` parse JSON rồi destructure body; không khẳng định 415 là bắt buộc. |
| LG-06 | LG-EX-01: ba request thiếu password rồi login đúng bị khóa | Thiếu field không phải lần đăng nhập sai **hoặc** thông tin không hợp lệ cũng được tính sai; R:40–42 không phân biệt. `server.js:33–35,46,53–57` đưa password thiếu vào nhánh sai. Không gán lỗi policy giả định; lỗi +2 đã ghi riêng ở LG-04/05. |
| LG-08 | LG-G6-03: email không tồn tại trả thông báo khác với tài khoản đang khóa | Đồng nhất mọi response để tránh dò email **hoặc** thông báo khóa phù hợp và lỗi sai thông tin đã thỏa R:42; `server.js:35–43`. Không khẳng định khai thác từ riêng observation. |
| LG-09 | LG-EX-03: token không có `exp` | JWT nên hết hạn **hoặc** thời hạn không bắt buộc theo R:43/A:32; `server.js:51` ký không truyền expiresIn. Không suy ra một thời hạn cụ thể. |
| CN-04 | CN-G3-06: token của user đã xóa vẫn hủy đơn | Xóa user nên thu hồi mọi token **hoặc** JWT còn hiệu lực đến khi hết hạn và spec không quy định thu hồi; R:43, 279; A:112. `server.js:100–108,321–335,504–506` verify chữ ký, không kiểm tồn tại user. |
| CN-05 | CN-G3-11: admin không hủy đơn người khác qua user cancel | User/Admin được hủy theo sơ đồ FR-10 **hoặc** endpoint user chỉ thao tác đơn thuộc chính token và admin dùng endpoint trạng thái riêng; R:145–155, 218–221; A:145–147, 179–182. `server.js:321–326` lọc owner; status 200 giả định. |
| CN-06 | CN-EX-01, 03, 04: ID `+O`, `O.0`, `0O` khớp ID và hủy | Chỉ chấp nhận biểu diễn số nguyên chuẩn **hoặc** các biểu diễn số tương đương hợp lệ; A:145–147 không định dạng ID. `server.js:323–324` truyền tham số vào SQLite; chưa suy diễn thêm cách ép kiểu nội bộ. |
| CN-07 | CN-EX-02: token cũ vẫn hủy sau reset | Reset mật khẩu nên thu hồi token **hoặc** không có quy định thu hồi trong R:46–60/A:44–53; `server.js:87–95,100–108` không có cơ chế thu hồi. Oracle GET cũng dùng token cũ, nên nếu token bị vô hiệu thì GET lỗi không tự chứng minh trạng thái đơn. |
| PR-05 | GET detail/list price/schema: xem các failure nhóm 5 trong API3 results | JSON price phải là number và schema cố định **hoặc** spec chỉ yêu cầu hiển thị giá, không quy định wire type/schema; R:75–76, 83–85; A:80–85. `server.js:159–163` cố ý đổi price ID chẵn thành string; các sai schema khác không mặc nhiên cùng nguyên nhân. |
| PR-06 | ID vắng/định dạng: các failure nhóm 6 API3 results, gồm PR-EX-01, 02, 05, 06 | ID không tồn tại phải trả 404 và ID phải canonical **hoặc** status/shape và biểu diễn tương đương không được spec quy định; A:84–90. `server.js:159–165,179–195`: GET thiếu trả `{}`, PUT/DELETE không kiểm `changes`; SQLite so khớp ID. Không coi 404/400 giả định là bug. |

## c) Không phải bug – setup/oracle, không phải nhóm ứng viên bổ sung

| Nhóm nguồn | Case / lý do |
|---|---|
| — | CN-G3-04 INCOMPLETE: assertion setup yêu cầu `exp` có thể chờ nhưng undefined; không có request tấn công sau thời gian chờ. Không có bằng chứng token hết hạn được chấp nhận. Đây là failure setup/oracle độc lập ngoài 25 nhóm, không phải nhóm thứ 26. |

## Đối soát

- Bảng a: LG-04, LG-05, LG-07, LG-10; CN-01, CN-02, CN-03, CN-08; PR-01, PR-02, PR-03, PR-04, PR-07 = **13 nhóm**, gộp thành **10 dòng nguyên nhân gốc/bug đề xuất**.
- Bảng b: LG-01, LG-02, LG-03, LG-06, LG-08, LG-09; CN-04, CN-05, CN-06, CN-07; PR-05, PR-06 = **12 nhóm**.
- Bảng c: **0 nhóm ứng viên**, một failure setup độc lập. Tổng **13 + 12 + 0 = 25** nhóm, mỗi nhóm đúng một bảng.
- **AI bỏ sót: 1 dòng nguyên nhân gốc Human Extend-only**: BUG-LG-03 (LG-EX-05 và CN-EX-05). BUG-LG-01 và BUG-PR-01 có cả AI-generated và Human Extend nên không tính là Human Extend-only. Token sai được chấp nhận ở product là thiếu middleware product, không phải bằng chứng AI-generated cho secret hardcode.
- Các mã status 400/401/403/404/415/423 khi nguồn đánh dấu giả định không tự cấu thành bug. Các nhãn severity/priority chỉ là đề xuất; toàn bộ ô sinh viên xác nhận để trống.
