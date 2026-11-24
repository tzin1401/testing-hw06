# HW06 – API Testing (EShop)

Sinh viên **23120190** · SUT: [ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut) commit `85af3ba` · Base URL `http://localhost:3000`

## Chạy local

```bash
git clone https://github.com/ttbhanh/eshop-sut   # một lần
scripts/reset_sut.sh                              # khởi động/reset backend (DB seed lại, cart RAM bị xóa)
./scripts/run_newman.sh                            # sinh viên tự chạy: reset và chạy cả 3 API, sinh HTML/JSON
./scripts/run_newman.sh API1_Login                 # tùy chọn: chỉ chạy API1_Login, API2_CancelOrder hoặc API3_ProductCRUD
```

Hạ tầng hiện ở X0: ba collection chỉ có `_smoke`, các folder test case còn rỗng; chưa dùng kết quả smoke làm kết quả Execute chính thức.
Để kiểm tra kỹ thuật không tạo report: reset SUT trước mỗi lần, rồi chạy `newman run collections/23120190_API1_Login.postman_collection.json -e environments/local.postman_environment.json --reporters cli --folder _smoke` (đổi tên collection tương ứng cho API 2/3).
Runner chính thức dành cho sinh viên: báo cáo nằm trong `results/newman/`, lỗi assertion không dừng các API còn lại; script in tổng kết và trả exit 1 nếu có API fail.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `collections/` | Postman collection (.json) |
| `environments/` | Postman environment |
| `data/` | File dữ liệu cho data-driven run |
| `report/` | Báo cáo Markdown/PDF, AI log, bug report |
| `results/newman/` | Newman HTML report |
| `evidence/` | Ảnh chụp (console X-Student-Id, Issues, CI) |
| `scripts/` | Script tiện ích |

## Tự đánh giá

| No. | Criteria | Grade | Self-Assessed |
|---|---|---:|---:|
| 1 | API 1 – full pipeline | 30 | |
| 2 | API 2 – full pipeline | 30 | |
| 3 | API 3 – full pipeline | 30 | |
| 4 | Agent Skill (AI test generator) | 10 | |
| | **Total** | **100** | |

## Test summary

| APIs | TC AI sinh | TC thêm | Executed | Passed | Failed | Bugs |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | | | | | | |
