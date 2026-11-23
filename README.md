# HW06 – API Testing (EShop)

Sinh viên **23120190** · SUT: [ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut) commit `85af3ba` · Base URL `http://localhost:3000`

## Chạy local

```bash
git clone https://github.com/ttbhanh/eshop-sut   # một lần
scripts/reset_sut.sh                              # khởi động/reset backend (DB seed lại, cart RAM bị xóa)
newman run collections/<file>.json -e environments/local.postman_environment.json -r cli,htmlextra --reporter-htmlextra-export results/newman/report.html
```

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
