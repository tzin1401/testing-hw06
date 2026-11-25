# API 1 – Kết quả Execute Login

## Nguồn và phạm vi

- Kết quả chính: `results/newman/23120190_API1_Login_20261125.json` (4.519.804 byte, SHA-256 `1af844f2e10e4e93a7783572f399a0c4c1c0bac26c006e6b91443fe3aecad966`); HTML tương ứng `results/newman/23120190_API1_Login_20261125.html` (4.945.289 byte, SHA-256 `9b39b352addc30db955916b5d5c01dde491391e7f2dabe3116384cd075a5ee1e`).
- Kỳ vọng và nhãn: `report/testcases/API1_login_generated.md`; đối chiếu phạm vi: `report/execute/API1_login_mapping.md`. Theo G6, LG-G4-04 dùng 400 và LG-G4-05 dùng 423, đều GIẢ ĐỊNH; LG-G1-24 giữ 415 giả định. Ký hiệu S = JWT và user; E/L = lỗi không token, thông báo phù hợp, theo quy ước nguồn; W = sai, C = đúng, ME = `/api/users/me`. Nhiều kỳ vọng core cũng dựa trên giả định, không mặc nhiên là yêu cầu đặc tả.
- JSON chứa 229 execution, tất cả request có host `localhost` (229/229), không chứng minh host của những lần chạy khác. Các body dưới đây lấy từ `response.stream` của chính execution chứa assertion, không phải response ghép theo tên request. Token, password, hash và secret được ẩn. Số execution là vị trí 1-based trong `run.executions`, để phân biệt request lặp cùng ID.
- Phạm vi mapping 68 case (61 VALID, 2 INCOMPLETE, 5 EX) / 71 ID nguồn; 3 INVALID bỏ qua: LG-G1-14, LG-G2-02, LG-G3-06. 229 request và 473 assertion khớp mapping, không gồm `_smoke` và DATA. Có 62 ID với ít nhất một assertion fail; đây không phải số case fail độc lập với precondition.

## Tổng hợp JSON chính

| Chỉ số | Tổng | Pass / không lỗi | Fail |
|---|---:|---:|---:|
| Iteration | 1 | 1 | 0 |
| Request | 229 | 229 | 0 |
| Assertion | 473 | 321 | 152 |
| Test script | 229 | 229 | 0 |
| Pre-request script | 334 | 334 | 0 |

Thời gian `completed - started` = **257.312 ms** (4 phút 17,312 giây). `run.failures` có 152 mục; 152 assertion lỗi trong các execution, gồm 109 status GIẢ ĐỊNH, 12 status tường minh và 31 core. Không có lỗi request, test script hay pre-request script theo `run.stats`; các assertion ở request mang tên setup vẫn được liệt kê theo nội dung thực tế, không suy diễn đăng ký thất bại. Những case có precondition không đạt không đủ căn cứ quy lỗi tiếp theo cho SUT; không có assertion setup đăng ký thất bại trong run này.

## DATA – báo cáo riêng, không cộng vào JSON chính

`results/newman/23120190_API1_Login-data_20261125.html` (882.231 byte; SHA-256 `3f71825e0cff48bc5504739f83fa7cc905a6931ef16afbc4c7099dc7819d15d7`) hiển thị folder DATA – LG-G1: 20 iteration, 40 request (0 request lỗi), 76 assertion, 22 failed test, 0 skipped, thời gian 1.078 ms. Suy ra 54 assertion không fail từ tổng trừ 22; đây là số hiển thị HTML, không phải thống kê từ JSON DATA: runner không xuất JSON cho DATA. Không cộng hai lượt chạy thành một kết quả hay suy diễn body/failure DATA từ JSON chính.

## Nhóm cần sinh viên xem xét — 10 nhóm ứng viên, không phải kết luận bug

1. **Chuẩn hóa email**, LG-G1-10/11/12: core JWT/user và status giả định đều fail với 401; viết hoa/trim là giả định của test, chưa xác lập vi phạm hợp đồng.
2. **JSON sai cú pháp**, LG-G1-23: body HTML có SyntaxError, hai assertion core parse JSON thất bại; không đủ từ đó kết luận có token hay lộ thông tin nhạy cảm, cần review oracle/đặc tả lỗi.
3. **Media type**, LG-G1-24: HTTP 500 và trang HTML có TypeError; status 415 là giả định, hai core thất bại vì không parse được JSON. Có dấu hiệu xử lý lỗi chưa phù hợp, nguyên nhân gốc chưa xác minh.
4. **Bộ đếm/khóa sớm**, LG-G2-01/04/05/06/08 và LG-EX-02: sau hai lần sai, login đúng nhận 403; EX-02 đọc `login_attempts:2` sau một lần sai. Có thể cùng liên quan bộ đếm nhưng chưa chứng minh chung nguyên nhân; reset sau login đúng cũng là giả định trong test.
5. **Hết hạn khóa**, LG-G2-07/11, LG-G3-09, LG-G6-03: login đúng sau mốc 31 giây vẫn 403; LG-G6-01 cũng quan sát 403 sau chờ nhưng chỉ có status giả định fail. Thời điểm đo và việc thử trong lúc khóa có thể ảnh hưởng; chưa xác minh nguyên nhân hoặc chính sách gia hạn.
6. **Thiếu password gây khóa**, LG-EX-01: login đúng sau ba request thiếu password nhận 403; ME sau đó fail theo chuỗi. Nguồn ghi giả định lỗi thiếu field không tính là lần sai; cần sinh viên xác nhận.
7. **Trả trường password**, LG-G4-01/02/03/07: schema không cho `user.password`, và kiểm đệ quy fail; body thật có key password đã ẩn. Suy luận không lộ dữ liệu nhạy cảm là giả định bảo mật của testcase, không chứng minh cách lưu.
8. **Phân biệt email**, LG-G6-03: lần 3–4 email vắng trả 401/`Invalid email or password`, email đã đăng ký trả 403/thông báo khóa. So sánh đồng nhất là diễn giải bảo mật có giả định, không chứng minh khai thác.
9. **Thời hạn JWT**, LG-EX-03: assertion payload thất bại vì kỳ vọng số không có; nguồn kỳ vọng `exp` nguyên > `iat`, nhưng spec không quy định thời hạn. Body chứa token đã ẩn; không khẳng định nội dung payload chưa quan sát.
10. **Token tự ký**, LG-EX-05: request ME với token dựng theo testcase nhận 200 và dữ liệu user thay vì từ chối. Kỳ vọng từ chối dựa trên giả định secret không được lộ trong source; cần review và không công bố secret/token trong báo cáo.

Những status GIẢ ĐỊNH không kèm core/status tường minh chỉ phản ánh khác biệt oracle, không tạo ứng viên riêng: 400 thường nhận 401; 423 thường nhận 403; xem từng bước trong bảng. Status giả định tại case có core fail cũng không được đếm thành nhóm mới. Fail ME sau login thất bại có thể là hệ quả thiếu token, không tách thành bug riêng. Không gán severity hoặc tạo bug report.

## Đối chiếu toàn bộ 152 assertion thất bại

Mỗi dòng ứng với một assertion thất bại; cột kỳ vọng lấy từ testcase và G6 (nếu là status, ghi giá trị tương ứng với đúng bước trong tên assertion). Trích body rút gọn, dấu `[ĐÃ ẨN]` thay giá trị nhạy cảm, không thể dùng để suy ra giá trị gốc. Với HTML, chỉ trích đầu response thực tế. Các request setup W là bước thử trạng thái theo testcase, không tự động là lỗi setup đăng ký.

| Execution | ID | Assertion / bước | Loại | Kỳ vọng nguồn | Status thực tế — body thật đã ẩn |
|---:|---|---|---|---|---|
| 4 | LG-G1-02 | [LG-G1-02] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 6 | LG-G1-03 | [LG-G1-03] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 8 | LG-G1-04 | [LG-G1-04] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 10 | LG-G1-05 | [LG-G1-05] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 12 | LG-G1-06 | [LG-G1-06] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 14 | LG-G1-07 | [LG-G1-07] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 16 | LG-G1-08 | [LG-G1-08] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 18 | LG-G1-09 | [LG-G1-09] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 20 | LG-G1-10 | [LG-G1-10] status 200 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 200 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 20 | LG-G1-10 | [LG-G1-10] core: JWT và user – login | core | S | 401 — `{"error":"Invalid email or password"}` |
| 22 | LG-G1-11 | [LG-G1-11] status 200 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 200 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 22 | LG-G1-11 | [LG-G1-11] core: JWT và user – login | core | S | 401 — `{"error":"Invalid email or password"}` |
| 24 | LG-G1-12 | [LG-G1-12] status 200 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 200 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 24 | LG-G1-12 | [LG-G1-12] core: JWT và user – login | core | S | 401 — `{"error":"Invalid email or password"}` |
| 26 | LG-G1-13 | [LG-G1-13] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 28 | LG-G1-15 | [LG-G1-15] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 30 | LG-G1-16 | [LG-G1-16] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 32 | LG-G1-17 | [LG-G1-17] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 34 | LG-G1-18 | [LG-G1-18] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 36 | LG-G1-19 | [LG-G1-19] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 38 | LG-G1-20 | [LG-G1-20] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 40 | LG-G1-21 | [LG-G1-21] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 42 | LG-G1-22 | [LG-G1-22] status 400 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 44 | LG-G1-23 | [LG-G1-23] core: lỗi không cấp token – login | core | E | 400 — `<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf-8"> <title>Error</title> </head> <body> <pre>SyntaxError: Expected &#39;,&#39; or &#39;}&#39; after property value in JSON at position 91 (line 1 column 92)<br> &nbsp; &nbsp;at JSON.parse (&l` |
| 44 | LG-G1-23 | [LG-G1-23] core: lỗi không lộ nguyên nhân | core | E | 400 — `<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf-8"> <title>Error</title> </head> <body> <pre>SyntaxError: Expected &#39;,&#39; or &#39;}&#39; after property value in JSON at position 91 (line 1 column 92)<br> &nbsp; &nbsp;at JSON.parse (&l` |
| 46 | LG-G1-24 | [LG-G1-24] status 415 (GIẢ ĐỊNH) – login | status GIẢ ĐỊNH | 415 GIẢ ĐỊNH | 500 — `<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf-8"> <title>Error</title> </head> <body> <pre>TypeError: Cannot destructure property &#39;email&#39; of &#39;req.body&#39; as it is undefined.<br> &nbsp; &nbsp;at /home/zinn/zinn/testing/hw06/` |
| 46 | LG-G1-24 | [LG-G1-24] core: lỗi không cấp token – login | core | E | 500 — `<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf-8"> <title>Error</title> </head> <body> <pre>TypeError: Cannot destructure property &#39;email&#39; of &#39;req.body&#39; as it is undefined.<br> &nbsp; &nbsp;at /home/zinn/zinn/testing/hw06/` |
| 46 | LG-G1-24 | [LG-G1-24] core: lỗi không lộ nguyên nhân | core | E | 500 — `<!DOCTYPE html> <html lang="en"> <head> <meta charset="utf-8"> <title>Error</title> </head> <body> <pre>TypeError: Cannot destructure property &#39;email&#39; of &#39;req.body&#39; as it is undefined.<br> &nbsp; &nbsp;at /home/zinn/zinn/testing/hw06/` |
| 50 | LG-G2-01 | [LG-G2-01] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 51 | LG-G2-01 | [LG-G2-01] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 52 | LG-G2-01 | [LG-G2-01] status 200 – bước 3 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 52 | LG-G2-01 | [LG-G2-01] core: JWT và user – bước 3 C | core | E, E, S; hai lần sai không khóa, chứng minh lần đầu không tăng quá 1 | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 54 | LG-G2-03 | [LG-G2-03] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 55 | LG-G2-03 | [LG-G2-03] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 56 | LG-G2-03 | [LG-G2-03] status 423 (GIẢ ĐỊNH) – bước 3 W | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 57 | LG-G2-03 | [LG-G2-03] status 423 (GIẢ ĐỊNH) – bước 4 C | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 60 | LG-G2-04 | [LG-G2-04] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 61 | LG-G2-04 | [LG-G2-04] status 400 (GIẢ ĐỊNH) – bước 3 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 62 | LG-G2-04 | [LG-G2-04] status 200 – bước 4 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 62 | LG-G2-04 | [LG-G2-04] core: JWT và user – bước 4 C | core | S, E, E, S; thành công không tạo số lần sai | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 64 | LG-G2-05 | [LG-G2-05] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 66 | LG-G2-05 | [LG-G2-05] status 400 (GIẢ ĐỊNH) – bước 3 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 67 | LG-G2-05 | [LG-G2-05] status 400 (GIẢ ĐỊNH) – bước 4 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 68 | LG-G2-05 | [LG-G2-05] status 200 – bước 5 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 68 | LG-G2-05 | [LG-G2-05] core: JWT và user – bước 5 C | core | S, E, E, S; thành công xóa chuỗi sai cũ | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 70 | LG-G2-06 | [LG-G2-06] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 71 | LG-G2-06 | [LG-G2-06] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 72 | LG-G2-06 | [LG-G2-06] status 200 – bước 3 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 72 | LG-G2-06 | [LG-G2-06] core: JWT và user – bước 3 C | core | S, E, E, S; không khóa sau chuỗi mới gồm hai sai | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 73 | LG-G2-06 | [LG-G2-06] status 400 (GIẢ ĐỊNH) – bước 4 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 74 | LG-G2-06 | [LG-G2-06] status 400 (GIẢ ĐỊNH) – bước 5 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 75 | LG-G2-06 | [LG-G2-06] status 200 – bước 6 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 75 | LG-G2-06 | [LG-G2-06] core: JWT và user – bước 6 C | core | S, E, E, S; không khóa sau chuỗi mới gồm hai sai | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 77 | LG-G2-07 | [LG-G2-07] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 78 | LG-G2-07 | [LG-G2-07] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 79 | LG-G2-07 | [LG-G2-07] status 423 (GIẢ ĐỊNH) – bước 3 W | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 80 | LG-G2-07 | [LG-G2-07] status 423 (GIẢ ĐỊNH) – bước 4 W | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 81 | LG-G2-07 | [LG-G2-07] status 423 (GIẢ ĐỊNH) – bước 5 C | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 82 | LG-G2-07 | [LG-G2-07] status 200 – bước 6 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 82 | LG-G2-07 | [LG-G2-07] core: JWT và user – bước 6 C | core | L, L, S; lỗi khóa không nêu password sai, email tồn tại, counter hay nguyên nhân chi tiết | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 84 | LG-G2-08 | [LG-G2-08] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 85 | LG-G2-08 | [LG-G2-08] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 86 | LG-G2-08 | [LG-G2-08] status 200 – bước 3 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 86 | LG-G2-08 | [LG-G2-08] core: JWT và user – bước 3 C | core | E, E, S; vẫn chưa khóa sau hai sai | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 88 | LG-G2-09 | [LG-G2-09] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 89 | LG-G2-09 | [LG-G2-09] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 90 | LG-G2-09 | [LG-G2-09] status 423 (GIẢ ĐỊNH) – bước 3 W | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 91 | LG-G2-09 | [LG-G2-09] status 423 (GIẢ ĐỊNH) – bước 4 C | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 93 | LG-G2-10 | [LG-G2-10] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 94 | LG-G2-10 | [LG-G2-10] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 95 | LG-G2-10 | [LG-G2-10] status 423 (GIẢ ĐỊNH) – bước 3 W | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 96 | LG-G2-10 | [LG-G2-10] status 423 (GIẢ ĐỊNH) – bước 4 C | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 98 | LG-G2-11 | [LG-G2-11] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 99 | LG-G2-11 | [LG-G2-11] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 100 | LG-G2-11 | [LG-G2-11] status 423 (GIẢ ĐỊNH) – bước 3 W | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 101 | LG-G2-11 | [LG-G2-11] status 423 (GIẢ ĐỊNH) – bước 4 C | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 102 | LG-G2-11 | [LG-G2-11] status 200 – bước 5 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 102 | LG-G2-11 | [LG-G2-11] core: JWT và user – bước 5 C | core | L ở ~29 giây, S ở ~31 giây; E, E, S chứng minh chuỗi sau hết khóa bắt đầu lại | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 103 | LG-G2-11 | [LG-G2-11] status 400 (GIẢ ĐỊNH) – bước 6 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 104 | LG-G2-11 | [LG-G2-11] status 400 (GIẢ ĐỊNH) – bước 7 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 105 | LG-G2-11 | [LG-G2-11] status 200 – bước 8 C | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 105 | LG-G2-11 | [LG-G2-11] core: JWT và user – bước 8 C | core | L ở ~29 giây, S ở ~31 giây; E, E, S chứng minh chuỗi sau hết khóa bắt đầu lại | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 108 | LG-G2-12 | [LG-G2-12] status 400 (GIẢ ĐỊNH) – bước 1 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 109 | LG-G2-12 | [LG-G2-12] status 400 (GIẢ ĐỊNH) – bước 2 W | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 110 | LG-G2-12 | [LG-G2-12] status 423 (GIẢ ĐỊNH) – bước 3 W | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 112 | LG-G2-12 | [LG-G2-12] status 423 (GIẢ ĐỊNH) – bước 5 C | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 114 | LG-G3-01 | [LG-G3-01] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 117 | LG-G3-02 | [LG-G3-02] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 120 | LG-G3-03 | [LG-G3-03] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 123 | LG-G3-04 | [LG-G3-04] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 126 | LG-G3-05 | [LG-G3-05] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 129 | LG-G3-07 | [LG-G3-07] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 130 | LG-G3-07 | [LG-G3-07] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 135 | LG-G3-09 | [LG-G3-09] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 136 | LG-G3-09 | [LG-G3-09] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 137 | LG-G3-09 | [LG-G3-09] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 138 | LG-G3-09 | [LG-G3-09] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 139 | LG-G3-09 | [LG-G3-09] status 200 | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 139 | LG-G3-09 | [LG-G3-09] core: JWT và user đúng tài khoản | core | Hai E; lần ba và C trong khóa không JWT, có thông báo phù hợp không lộ nguyên nhân; C sau chờ trả JWT và đúng `user.id` | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 141 | LG-G3-10 | [LG-G3-10] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 144 | LG-G3-11 | [LG-G3-11] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 147 | LG-G3-12 | [LG-G3-12] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 150 | LG-G3-13 | [LG-G3-13] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 153 | LG-G3-14 | [LG-G3-14] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 156 | LG-G3-15 | [LG-G3-15] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 159 | LG-G3-16 | [LG-G3-16] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 162 | LG-G3-17 | [LG-G3-17] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 165 | LG-G4-01 | [LG-G4-01] core: schema JSON | core | Content-Type media type `application/json`; parse JSON và khớp schema 200; `token` là string không rỗng, có `user` | 200 — `{"message":"Login successful","token":"[ĐÃ ẨN]","user":{"id":55,"password":"[ĐÃ ẨN]","login_attempts":0}}` |
| 167 | LG-G4-02 | [LG-G4-02] core: schema JSON | core | Schema 200 khớp; `user.id` tồn tại và là integer, `user.name` và `user.email` tồn tại và là string; `user.role` tồn tại và thuộc `user`, `admin`; `token` là string không rỗng | 200 — `{"message":"Login successful","token":"[ĐÃ ẨN]","user":{"id":56,"password":"[ĐÃ ẨN]","login_attempts":0}}` |
| 169 | LG-G4-03 | [LG-G4-03] core: schema JSON | core | Schema 200 khớp; duyệt đệ quy object/array, không key chứa `password`, `passwd`, `hash` hoặc `reset_token` không phân biệt hoa thường; không giá trị bằng `Test1234!` | 200 — `{"message":"Login successful","token":"[ĐÃ ẨN]","user":{"id":57,"password":"[ĐÃ ẨN]","login_attempts":0}}` |
| 169 | LG-G4-03 | [LG-G4-03] core: không lộ password hoặc hash đệ quy | core | Schema 200 khớp; duyệt đệ quy object/array, không key chứa `password`, `passwd`, `hash` hoặc `reset_token` không phân biệt hoa thường; không giá trị bằng `Test1234!` | 200 — `{"message":"Login successful","token":"[ĐÃ ẨN]","user":{"id":57,"password":"[ĐÃ ẨN]","login_attempts":0}}` |
| 171 | LG-G4-04 | [LG-G4-04] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 173 | LG-G4-05 | [LG-G4-05] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 174 | LG-G4-05 | [LG-G4-05] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 175 | LG-G4-05 | [LG-G4-05] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 176 | LG-G4-05 | [LG-G4-05] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 178 | LG-G4-06 | [LG-G4-06] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 180 | LG-G4-07 | [LG-G4-07] core: schema JSON | core | Schema 200 khớp; `pm.response.responseTime < 2000` ms | 200 — `{"message":"Login successful","token":"[ĐÃ ẨN]","user":{"id":61,"password":"[ĐÃ ẨN]","login_attempts":0}}` |
| 182 | LG-G6-01 | [LG-G6-01] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 183 | LG-G6-01 | [LG-G6-01] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 184 | LG-G6-01 | [LG-G6-01] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 185 | LG-G6-01 | [LG-G6-01] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 186 | LG-G6-01 | [LG-G6-01] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 187 | LG-G6-01 | [LG-G6-01] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 188 | LG-G6-01 | [LG-G6-01] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 193 | LG-G6-03 | [LG-G6-03] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 194 | LG-G6-03 | [LG-G6-03] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 195 | LG-G6-03 | [LG-G6-03] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 196 | LG-G6-03 | [LG-G6-03] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 197 | LG-G6-03 | [LG-G6-03] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 198 | LG-G6-03 | [LG-G6-03] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 199 | LG-G6-03 | [LG-G6-03] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 199 | LG-G6-03 | [LG-G6-03] core: status và lỗi giống tài khoản đã đăng ký | core | Mỗi lỗi có `error` không rỗng, không token; so sánh từng cặp tương ứng: status và chuỗi `error` giống hệt, kể cả lần 3 và 4; C và ME xác nhận tài khoản riêng vẫn đúng danh tính | 401 — `{"error":"Invalid email or password"}` |
| 200 | LG-G6-03 | [LG-G6-03] status 423 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 423 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 200 | LG-G6-03 | [LG-G6-03] core: status và lỗi giống tài khoản đã đăng ký | core | Mỗi lỗi có `error` không rỗng, không token; so sánh từng cặp tương ứng: status và chuỗi `error` giống hệt, kể cả lần 3 và 4; C và ME xác nhận tài khoản riêng vẫn đúng danh tính | 401 — `{"error":"Invalid email or password"}` |
| 201 | LG-G6-03 | [LG-G6-03] status 200 | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 201 | LG-G6-03 | [LG-G6-03] core: token và user | core | Mỗi lỗi có `error` không rỗng, không token; so sánh từng cặp tương ứng: status và chuỗi `error` giống hệt, kể cả lần 3 và 4; C và ME xác nhận tài khoản riêng vẫn đúng danh tính | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 202 | LG-G6-03 | [LG-G6-03] status 200 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 200 GIẢ ĐỊNH | 403 — `{"error":"Forbidden"}` |
| 202 | LG-G6-03 | [LG-G6-03] core: đúng danh tính | core | Mỗi lỗi có `error` không rỗng, không token; so sánh từng cặp tương ứng: status và chuỗi `error` giống hệt, kể cả lần 3 và 4; C và ME xác nhận tài khoản riêng vẫn đúng danh tính | 403 — `{"error":"Forbidden"}` |
| 210 | LG-EX-01 | [LG-EX-01] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 211 | LG-EX-01 | [LG-EX-01] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 212 | LG-EX-01 | [LG-EX-01] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 213 | LG-EX-01 | [LG-EX-01] status 200 | status tường minh | 200  | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 213 | LG-EX-01 | [LG-EX-01] core: token và user | core | Ba response đầu: JSON `error` không rỗng, không `token`; response cuối 200 có `token` và `ME` với token đó trả 200 đúng `email` | 403 — `{"error":"Tài khoản đã bị khóa. Vui lòng thử lại sau."}` |
| 214 | LG-EX-01 | [LG-EX-01] status 200 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 200 GIẢ ĐỊNH | 403 — `{"error":"Forbidden"}` |
| 214 | LG-EX-01 | [LG-EX-01] core: đúng email | core | Ba response đầu: JSON `error` không rỗng, không `token`; response cuối 200 có `token` và `ME` với token đó trả 200 đúng `email` | 403 — `{"error":"Forbidden"}` |
| 217 | LG-EX-02 | [LG-EX-02] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 218 | LG-EX-02 | [LG-EX-02] core: login_attempts bằng 1 | core | JSON có `login_attempts` bằng 1, không phải 0 hoặc 2 | 200 — `{"id":68,"password":"[ĐÃ ẨN]","login_attempts":2}` |
| 221 | LG-EX-03 | [LG-EX-03] core: JWT payload | core | Payload có `exp` là số nguyên và `exp` > `iat`; ngoài ra có `id`, `role` | 200 — `{"message":"Login successful","token":"[ĐÃ ẨN]","user":{"id":69,"password":"[ĐÃ ẨN]","login_attempts":0}}` |
| 225 | LG-EX-04 | [LG-EX-04] status 400 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 400 GIẢ ĐỊNH | 401 — `{"error":"Invalid email or password"}` |
| 229 | LG-EX-05 | [LG-EX-05] status 401 (GIẢ ĐỊNH) | status GIẢ ĐỊNH | 401 GIẢ ĐỊNH | 200 — `{"id":71,"password":"[ĐÃ ẨN]","login_attempts":0}` |
| 229 | LG-EX-05 | [LG-EX-05] core: không trả dữ liệu nạn nhân | core | JSON `error` không rỗng; không trả dữ liệu của B | 200 — `{"id":71,"password":"[ĐÃ ẨN]","login_attempts":0}` |
