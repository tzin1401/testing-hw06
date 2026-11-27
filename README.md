# HW06 – API Testing (EShop)

Sinh viên **23120190** · SUT: [ttbhanh/eshop-sut](https://github.com/ttbhanh/eshop-sut) commit `85af3ba` · Base URL `http://localhost:3000`

## Chạy local

```bash
git clone https://github.com/ttbhanh/eshop-sut   # một lần
scripts/reset_sut.sh                              # khởi động/reset backend (DB seed lại, cart RAM bị xóa)
./scripts/run_newman.sh                            # sinh viên tự chạy: reset và chạy cả 3 API, sinh HTML/JSON
./scripts/run_newman.sh API1_Login                 # tùy chọn: chỉ chạy API1_Login, API2_CancelOrder hoặc API3_ProductCRUD
```

Báo cáo kết quả nằm trong `results/newman/`. Assertion lỗi không làm dừng các API còn lại. Script in tổng kết và trả exit 1 nếu có API fail.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `collections/` | Postman collection (.json) |
| `environments/` | Postman environment |
| `data/` | File dữ liệu cho data-driven run |
| `report/` | Báo cáo chính [`MAIN_REPORT.md`](report/MAIN_REPORT.md) (+ PDF), AI log, AI audit, bug report, CI/CD, Excel |
| `agent_skill/`, `.claude/skills/` | Sơ đồ tự vẽ, pseudocode, Agent Skill; video demo: https://youtu.be/FAk1krlB-ng |
| `skill_runs/` | Kết quả chạy Agent Skill (API 1) |
| `results/newman/` | Newman HTML report |
| `evidence/` | Ảnh chụp (console X-Student-Id, Issues, Postman, CI) |
| `.github/workflows/` | Pipeline CI chạy Newman |
| `scripts/` | Script tiện ích |

## Tự đánh giá

| No. | Criteria | Grade | Self-Assessed |
|---|---|---:|---:|
| 1 | API 1 – full pipeline | 30 | 30 |
| 2 | API 2 – full pipeline | 30 | 30 |
| 3 | API 3 – full pipeline | 30 | 30 |
| 4 | Agent Skill (AI test generator) | 10 | 10 |
| | **Total** | **100** | **100** |

## Test summary

Nguồn: sheet Summary trong [`report/23120190_HW06_TestCases.xlsx`](report/23120190_HW06_TestCases.xlsx), Newman chạy trên localhost ngày 2026-11-25. Not run là các case bị gắn nhãn INVALID khi audit.

| API | TC AI sinh | TC thêm | Tổng | Not run | Executed | Passed | Failed | Assertion (fail) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| API 1 – `POST /api/login` | 66 | 5 | 71 | 3 | 68 | 6 | 62 | 473 (152) |
| API 2 – `PUT /api/orders/:id/cancel` | 59 | 5 | 64 | 9 | 55 | 27 | 28 | 1232 (48) |
| API 3 – Product CRUD | 127 | 6 | 133 | 8 | 125 | 22 | 103 | 1270 (311) |
| **Tổng (3 API)** | **252** | **16** | **268** | **20** | **248** | **55** | **193** | **2975 (511)** |

- Bug: **16** (GitHub Issues [#1–#16](https://github.com/tzin1401/testing-hw06/issues)), trong đó 2 bug AI bỏ sót và chỉ case Human Extend tìm ra (BUG-06, BUG-11). Chi tiết ở [`report/bug_report.md`](report/bug_report.md).
- Agent Skill chạy trên API 1: 50 case, chạy 47, 33 PASS, 12 BUG_CANDIDATE ([`skill_runs/API1_Login/run_log.md`](skill_runs/API1_Login/run_log.md)).
