# Run log – API1_Login (POST /api/login)

- Thời gian: 2026-11-26 17:33 (giờ máy, lấy bằng `date`)
- Generator: Claude Opus 5.5 (`claude-opus-5-5`), mỗi kỹ thuật một lượt sinh riêng: `gen/generate.py <G1|G2|G3|G4|G6|EX>` → `gen/<G>.json` → `merge`
- Auditor: subagent độc lập, Claude Sonnet (`sonnet`), context riêng, không đọc source SUT. Kết quả: `audit_r1.json`, `audit_r2.json`, `audit_r3.json`
- SUT: `http://localhost:3000`, reset bằng `scripts/reset_sut.sh` trước mỗi lần chạy

## Case theo nhóm và nhãn

| Nhóm | Tổng | VALID | INVALID |
|---|---:|---:|---:|
| G1 | 15 | 15 | 0 |
| G2 | 8 | 8 | 0 |
| G3 | 10 | 9 | 1 |
| G4 | 4 | 4 | 0 |
| G6 | 6 | 6 | 0 |
| EX | 7 | 5 | 2 |
| **Tổng** | **50** | **47** | **3** |

Không có INCOMPLETE ở trạng thái cuối.

## Audit và sinh lại

| Vòng | Case audit | VALID | INCOMPLETE | INVALID |
|---|---:|---:|---:|---:|
| 1 | 50 | 40 | 8 | 2 (EX-05 trùng G2-05, EX-07 trùng G4-01) |
| 2 (sinh lại lần 1) | 8 | 6 | 2 (G3-09, G4-03) | 0 |
| 3 (sinh lại lần 2) | 2 | 1 | 1 (G3-09) | 0 |

- Số lần sinh lại: **2**. G3-09 vẫn INCOMPLETE sau 2 vòng → **INVALID**, không đưa vào collection.

## Nhóm / mẫu bỏ qua

- G5 không có trong `techniques.md`. Mọi nhóm G1, G2, G3, G4, G6 đều áp dụng.
- Không áp dụng cho /api/login: P1 (secret hardcode, cần API có auth), P2 (không có path id), P5 (login không nhận header Authorization).
- G2 bỏ cạnh "hết khóa rồi sai 1 lần": spec không nói bộ đếm có reset khi hết khóa hay không.

## Thay đổi script trong lần chạy này

`build_collection.py` thêm: `wait_ms` (chờ trước request, cho case khóa 30 s), check `header`/`includes`, `max_ms`, path lọc mảng `[key=value]`, `equals: "{{var}}"` giữ kiểu biến. `cases_schema.md` cập nhật tương ứng .

## Kết quả Newman (thật)

- `newman/main.json` / `main.html`: 135 request, 226 assertion, 31 fail
- `newman/isolated-LG-EX-06.*`: case `crashes_sut`, chạy riêng sau reset

| PASS | SPEC_AMBIGUOUS | BUG_CANDIDATE | SETUP_ERROR | NOT_RUN |
|---:|---:|---:|---:|---:|
| 33 | 1 | 12 | 1 | 3 |

- SETUP_ERROR LG-G2-07: bước setup "đăng nhập đúng (reset)" sau 2 lần sai nhận 403 vì tài khoản đã bị khóa. Cùng gốc bug bộ đếm của LG-G2-02.
- NOT_RUN: 3 case INVALID (G3-09, EX-05, EX-07).
- 12 BUG_CANDIDATE quy về khoảng 7 nguyên nhân gốc (xem `triage.md`). Severity là đề xuất của AI.
