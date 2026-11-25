# API 2 – Kết quả Execute: hủy đơn

## Nguồn và tổng hợp

- Nguồn kết quả chính: `results/newman/23120190_API2_CancelOrder_20261125.json` (10.988.550 byte; SHA-256 `0bb5cf4fe1fd3bcba8751f0723692c3208c89be158352986371921937577046c`), `run.stats`, `run.timings`, `run.failures`, `run.executions` và `response.stream`. HTML tương ứng: `results/newman/23120190_API2_CancelOrder_20261125.html` (16.959.722 byte; SHA-256 `34189b4bcf5adab450506cd415079cb0300c00fcf0bed902278be6e1dc4b9402`); HTML ghi 905 request, 1.232 assertion, 48 failed tests.
- Expected: `report/testcases/API2_cancel_generated.md` (gồm Audit, G6 và Extend); đối chiếu giới hạn triển khai tại `report/execute/API2_cancel_mapping.md`, F1–F7. Đây là lần chạy chính thức do sinh viên thực hiện, không phải số liệu chạy thử X4.
- Một iteration; **905 request**, 905 thành công ở tầng request, 0 lỗi request; **1.232 assertion**, **1.184 pass, 48 fail**; test scripts 905/905 và pre-request scripts 1.074/1.074 không lỗi. Thời gian tổng theo `completed - started`: **34.558 ms (34,558 giây)**. Đây không phải thời gian trung bình response.
- Cả 905 URL request trong JSON có host `localhost`, port `3000`, HTTP. Các failure dưới đây được nối với execution theo `cursor.position` và đối chiếu `httpRequestId`; số vị trí bắt đầu từ 0. Response là dữ liệu thực tế từ stream, rút gọn chỉ giữ trường liên quan; token, mật khẩu và bí mật không được chép.
- Đối soát: **48 hàng = 30 failure thuộc 8 nhóm ứng viên + 17 failure chỉ lệch status GIẢ ĐỊNH + 1 failure setup INCOMPLETE**. Không có failure request/script. Một nhóm có thể chứa nhiều assertion và nhiều ID; đây là nhóm để sinh viên điều tra, không phải kết luận nguyên nhân gốc hay bug report.

## Nhóm ứng viên cần điều tra (8 nhóm)

1. **CN-G1-13:** scheme Basic được xử lý như xác thực hợp lệ; cancel thành công và oracle thấy canceled. Kiểm tra cơ chế phân tích Authorization; nguyên nhân chưa xác minh.
2. **CN-G2-03:** user hủy được đơn shipping; oracle thấy canceled, trái kỳ vọng FR-10.
3. **CN-G2-10:** admin chuyển canceled → delivered, oracle thấy delivered, trái kỳ vọng trạng thái kết thúc.
4. **CN-G3-06:** token user đã xóa vẫn thực hiện hủy; giả định token phải mất hiệu lực và đơn phải tồn tại cần được sinh viên xác nhận; đối chiếu điều kiện dừng F3.
5. **CN-G3-11:** admin không hủy được đơn người khác qua endpoint user; quyền này và status 200 đều là GIẢ ĐỊNH, cần xác nhận hợp đồng trước khi kết luận.
6. **CN-EX-01, 03, 04:** ID dạng `+O`, `O.0`, `0O` đều khớp đơn và hủy thành công; quy tắc biểu diễn ID trong expected là GIẢ ĐỊNH. Có thể liên quan chuẩn hóa/ép kiểu ID, chưa xác minh nguyên nhân.
7. **CN-EX-02:** token cũ sau reset mật khẩu vẫn hủy; việc vô hiệu token cũ là GIẢ ĐỊNH. F6: oracle GET cũng dùng token cũ; nếu token bị vô hiệu, GET 401 sẽ khiến oracle pending fail vì lý do khác, do đó không tự chứng minh trạng thái đơn. Lần này GET thực tế 200 và thấy canceled.
8. **CN-EX-05:** token tự ký trong case được chấp nhận và hủy đơn; giả định secret không lộ và token tự ký vô hiệu cần đối chiếu bối cảnh cấu hình. Không chép token hoặc secret.

## Toàn bộ failure

Quy ước: `E` là JSON có `error` string không rỗng, không lộ JWT theo quy ước G6; những expected status ghi GĐ là GIẢ ĐỊNH. `PUT`/`GET` trong cột request là request thực sự mang assertion, không phải request lân cận. Body GET chỉ trích trường thực tế liên quan.

| # | ID | Assertion / loại | Cursor; request | Expected từ testcase / G6 | HTTP thực tế; body thực tế trích | 
|---:|---|---|---|---|---|
| 1 | CN-G1-03 | status 400 GĐ | 24; PUT `/orders/0/cancel` | 400 | 404 `{"error":"Order not found"}` |
| 2 | CN-G1-04 | status 400 GĐ | 32; PUT `/orders/-1/cancel` | 400 | 404 `{"error":"Order not found"}` |
| 3 | CN-G1-07 | status 400 GĐ | 60; PUT `/orders/1.5/cancel` | 400 | 404 `{"error":"Order not found"}` |
| 4 | CN-G1-08 | status 400 GĐ | 68; PUT `/orders/abc/cancel` | 400 | 404 `{"error":"Order not found"}` |
| 5 | CN-G1-09 | status 400 GĐ | 76; PUT `/orders/%40/cancel` | 400 | 404 `{"error":"Order not found"}` |
| 6 | CN-G1-10 | status 400 GĐ | 84; PUT `/orders/%20/cancel` | 400 | 404 `{"error":"Order not found"}` |
| 7 | CN-G1-13 | status 401 GĐ | 108; PUT cancel | 401 với Basic | 200 `{"message":"Order canceled successfully"}` |
| 8 | CN-G1-13 | core: E | 108; PUT cancel | lỗi xác thực, E | 200 `{"message":"Order canceled successfully"}` |
| 9 | CN-G1-13 | core: đơn pending | 109; GET đơn | đơn vẫn pending | 200 `{"id":13,"status":"canceled"}` |
| 10 | CN-G1-14 | status 401 GĐ | 117; PUT cancel, JWT sai chữ ký | 401 | 403 `{"error":"Forbidden"}` |
| 11 | CN-G1-15 | status 401 GĐ | 125; PUT cancel, token rác | 401 | 403 `{"error":"Forbidden"}` |
| 12 | CN-G2-03 | status 400 GĐ | 157; PUT cancel | 400 | 200 `{"message":"Order canceled successfully"}` |
| 13 | CN-G2-03 | core: E | 157; PUT cancel | lỗi khi user hủy shipping | 200 `{"message":"Order canceled successfully"}` |
| 14 | CN-G2-03 | core: đơn shipping | 158; GET đơn | đơn vẫn shipping | 200 `{"id":18,"status":"canceled"}` |
| 15 | CN-G2-10 | status 400 GĐ | 467; PUT admin status canceled → delivered | 400 | 200 `{"message":"Order status updated"}` |
| 16 | CN-G2-10 | core: E | 467; PUT admin status canceled → delivered | lỗi chuyển trạng thái | 200 `{"message":"Order status updated"}` |
| 17 | CN-G2-10 | core: đơn canceled | 468; GET đơn | đơn vẫn canceled | 200 `{"id":44,"status":"delivered"}` |
| 18 | CN-G3-04 | setup: claim exp có thể chờ | 537; GET setup kiểm exp | claim `exp` dạng số và có thể chờ để thực hiện phần hết hạn | 200 `{"id":52,"status":"pending"}`; assertion báo `exp` undefined, không phải thông tin nằm trong body GET |
| 19 | CN-G3-06 | status 401 GĐ | 554; PUT cancel bằng token user đã xóa | 401 | 200 `{"message":"Order canceled successfully"}` |
| 20 | CN-G3-06 | core: lỗi JSON không rỗng và không lộ JWT | 554; PUT cancel | lỗi xác thực, E | 200 `{"message":"Order canceled successfully"}` |
| 21 | CN-G3-06 | core: hai đơn vẫn pending | 555; GET admin orders | cả hai pending | 200 trích `[ {"id":55,"status":"pending"}, {"id":54,"status":"canceled"} ]` |
| 22 | CN-G3-07 | status 401 GĐ | 568; PUT cancel, JWT tự ký | 401 | 403 `{"error":"Forbidden"}` |
| 23 | CN-G3-08 | status 400 GĐ | 583; PUT SQL OR | 400 | 404 `{"error":"Order not found"}` |
| 24 | CN-G3-09 | status 400 GĐ | 598; PUT SQL DROP | 400 | 404 `{"error":"Order not found"}` |
| 25 | CN-G3-10 | status 400 GĐ | 613; PUT SQL comment | 400 | 404 `{"error":"Order not found"}` |
| 26 | CN-G3-11 | status 200 GĐ | 628; PUT cancel bằng admin | 200 | 404 `{"error":"Order not found"}` |
| 27 | CN-G3-11 | core: thành công | 628; PUT cancel bằng admin | thành công, message string theo G6 | 404 `{"error":"Order not found"}` |
| 28 | CN-G3-11 | core: đơn 1 canceled | 629; GET đơn 1 | canceled | 200 `{"id":64,"status":"pending"}` |
| 29 | CN-G6-02 | status 401 GĐ | 713; PUT cancel, alg none | 401 | 403 `{"error":"Forbidden"}` |
| 30 | CN-G6-03 | status 400 GĐ | 728; PUT cancel, ID `Oabc` | 400 | 404 `{"error":"Order not found"}` |
| 31 | CN-G6-06 | status 400 GĐ | 765; PUT cancel, admin trên delivered | 400 | 404 `{"error":"Order not found"}` |
| 32 | CN-G6-07 | status 400 GĐ | 784; PUT cancel, admin trên shipping | 400 | 404 `{"error":"Order not found"}` |
| 33 | CN-G6-11 | status 403 GĐ | 860; PUT admin status bằng user | 403 | 400 `{"error":"Invalid state transition from shipping to canceled"}` |
| 34 | CN-EX-01 | status 400 GĐ | 869; PUT cancel, ID `+O` | 400 | 200 `{"message":"Order canceled successfully"}` |
| 35 | CN-EX-01 | core: error không rỗng | 869; PUT cancel, ID `+O` | JSON error không rỗng | 200 `{"message":"Order canceled successfully"}` |
| 36 | CN-EX-01 | core: đơn 1 pending | 870; GET oracle đơn 1 | đơn pending | 200 `{"id":92,"status":"canceled"}` |
| 37 | CN-EX-02 | status 401 GĐ | 879; PUT cancel bằng token cũ | 401 | 200 `{"message":"Order canceled successfully"}` |
| 38 | CN-EX-02 | core: error không rỗng | 879; PUT cancel bằng token cũ | JSON error không rỗng | 200 `{"message":"Order canceled successfully"}` |
| 39 | CN-EX-02 | core: đơn 1 pending | 880; GET oracle đơn 1 bằng token cũ | đơn pending | 200 `{"id":93,"status":"canceled"}` |
| 40 | CN-EX-03 | status 400 GĐ | 887; PUT cancel, ID `O.0` | 400 | 200 `{"message":"Order canceled successfully"}` |
| 41 | CN-EX-03 | core: error không rỗng | 887; PUT cancel, ID `O.0` | JSON error không rỗng | 200 `{"message":"Order canceled successfully"}` |
| 42 | CN-EX-03 | core: đơn 1 pending | 888; GET oracle đơn 1 | đơn pending | 200 `{"id":94,"status":"canceled"}` |
| 43 | CN-EX-04 | status 400 GĐ | 895; PUT cancel, ID `0O` | 400 | 200 `{"message":"Order canceled successfully"}` |
| 44 | CN-EX-04 | core: error không rỗng | 895; PUT cancel, ID `0O` | JSON error không rỗng | 200 `{"message":"Order canceled successfully"}` |
| 45 | CN-EX-04 | core: đơn 1 pending | 896; GET oracle đơn 1 | đơn pending | 200 `{"id":95,"status":"canceled"}` |
| 46 | CN-EX-05 | status 401 GĐ | 903; PUT cancel, JWT tự ký | 401 | 200 `{"message":"Order canceled successfully"}` |
| 47 | CN-EX-05 | core: error không rỗng | 903; PUT cancel, JWT tự ký | JSON error không rỗng | 200 `{"message":"Order canceled successfully"}` |
| 48 | CN-EX-05 | core: đơn 1 pending | 904; GET oracle đơn 1 | đơn pending | 200 `{"id":96,"status":"canceled"}` |

Đường dẫn rút gọn `/orders/...` trong bảng có tiền tố `/api`. Những request chỉ ghi `PUT cancel` dùng đường dẫn và biến cụ thể được định danh bằng ID và cursor trong JSON.

## Status GIẢ ĐỊNH và giới hạn diễn giải

- **17 failure chỉ lệch status**, không có core failure cùng case: hàng 1–6, 10–11, 22–25, 29–33. Các mã 400/401/403/404 đều là kỳ vọng giả định; không tự coi lệch mã là bug. Riêng CN-G6-11, response cho thấy server xử lý chuyển trạng thái và trả lỗi 400; kết quả này chưa chứng minh phép kiểm role độc lập. Sinh viên cần quyết định oracle và điều tra thêm.
- **CN-G3-04 INCOMPLETE:** chỉ setup kiểm claim `exp` fail vì undefined; không có chờ, không có request tấn công token hết hạn và không có K. Không kết luận hành vi token hết hạn. Theo F2, ngay cả nếu có `exp`, collection hiện tại cũng không thực hiện nhánh chờ/tấn công.
- F1: một số GET oracle G6/EX có tên `setup: oracle`, nhưng assertion `core` là kiểm tra sau request; hàng 36, 39, 42, 45, 48 là oracle, không phải lỗi dựng dữ liệu. F3: CN-G3-06 có điều kiện dừng cứng; trong lần này request tấn công và GET oracle đều thực sự xuất hiện. F4: regex phát hiện JWT của G6/EX rộng, có thể dương tính giả với chuỗi ba phần; không suy ra có lộ token từ các failure trên. F5: assertion so body đầu tiên của CN-G3-12 chỉ lưu baseline, hai lần sau mới so sánh. F6 nêu tại nhóm 7. F7: tên folder G6/EX chung chung, nên đọc ID và testcase để hiểu mục đích.
- Theo mapping, 9 ID INVALID không được chuyển; CN-G3-01/02 dùng 404 GIẢ ĐỊNH theo G6 thay vì 403 ban đầu. Các giới hạn này không biến assertion pass thành bằng chứng ngoài phạm vi kiểm tra.
