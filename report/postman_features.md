# Postman features đã dùng – 23120190

Công cụ: Postman Desktop (PostmanRuntime/7.49.1) + Newman CLI + `newman-reporter-htmlextra`.
Số liệu đếm trực tiếp từ file collection trong `collections/`.

| # | Tính năng | Dùng ở đâu | Bằng chứng |
|---|---|---|---|
| 1 | **Workspace** | Workspace cá nhân chứa 3 collection API + collection Mock | `evidence/postman/01_workspace.png` |
| 2 | **Collections + folder lồng nhau** | 3 collection, tổng 300 folder / 2133 request, chia theo kỹ thuật G1 (partition), G2 (state), G3 (security), G4 (schema), G6, EX (human extend) | `collections/*.json`, `evidence/postman/01_workspace.png` |
| 3 | **Environment** | `EShop local` (`baseUrl`, `studentId`, tài khoản seed); `EShop mock` (`mockUrl`) | `environments/*.json`, `evidence/postman/02_environment.png` |
| 4 | **Variables** (environment, collection, local) | `pm.collectionVariables` lưu token/id giữa các request (API1 431, API2 692, API3 2025 lần gọi); `pm.variables` cho biến cục bộ | collection JSON |
| 5 | **Pre-request script cấp collection** | Gắn header `X-Student-Id` cho mọi request + `console.log` | `evidence/xstudentid_console.png` |
| 6 | **Test scripts (`pm.test`, Chai)** | Assertion status, body, header cho từng case | Newman report `results/newman/*.html` |
| 7 | **JSON Schema validation** (`pm.response.to.have.jsonSchema`) | API1 7, API2 52, API3 13 chỗ | collection JSON |
| 8 | **Điều khiển luồng `pm.execution.setNextRequest`** | API2 4, API3 10 chỗ (bỏ qua bước khi setup lỗi) | collection JSON |
| 9 | **Postman Console** | Xem request/response thật, header X-Student-Id; chụp bằng chứng 16 bug | `evidence/issues/BUG-*.png` |
| 10 | **Collection Runner** | Chạy từng folder khi tái hiện bug | `evidence/issues/BUG-*.png` |
| 11 | **Data-driven run (Runner + file CSV)** | Folder `DATA – LG-G1` đọc `data/lg_g1_partition.csv` (20 dòng) qua `pm.iterationData` | `evidence/postman/03_data_runner.png`, `results/newman/23120190_API1_Login-data_*.html` |
| 12 | **Saved examples** | Collection `23120190_Mock` có 4 example lấy từ response thật của SUT | `collections/23120190_Mock.postman_collection.json` |
| 13 | **Mock server** | Mock dựng từ `23120190_Mock`; chọn example bằng header `x-mock-response-name` | `evidence/postman/04_mock_server.png` |
| 14 | **Monitor** | Monitor chạy `23120190_Mock` trên cloud với env `EShop mock` (monitor không gọi được `localhost` nên dùng mock) | `evidence/postman/05_monitor.png` |
| 15 | **Newman CLI + htmlextra reporter** | `scripts/run_newman.sh`, xuất HTML + JSON | `results/newman/` |
| 16 | **CI/CD (Newman trong GitHub Actions)** | Xem báo cáo CI/CD | `report/cicd_report.md` |

## Ghi chú
- Mock server và monitor chỉ dùng để minh họa tính năng; kết quả kiểm thử SUT lấy từ Newman chạy `localhost`.
- Monitor lần chạy đầu (23:53) fail 7/7 vì `mockUrl` chỉ lưu giá trị local, cloud không thấy; sau khi share giá trị lên cloud, lần chạy 23:54 pass 7/7 (HEALTHY).
- Example trong collection Mock là response thật ghi lại từ SUT ngày 2026-11-25, không phải dữ liệu bịa.
