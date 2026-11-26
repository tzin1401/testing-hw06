---
name: api-test-generator
description: Sinh test API tự động từ đầu đến cuối (không human-in-the-loop) cho một endpoint của SUT EShop - phân tích spec, sinh case theo từng kỹ thuật (partition/BVA, state, security, schema, heuristic) và mẫu bug AI hay bỏ sót, tự audit bằng agent thứ hai, dựng Postman collection có X-Student-Id, chạy Newman thật trên localhost rồi phân loại kết quả thành PASS / SPEC_AMBIGUOUS / BUG_CANDIDATE. Dùng khi được yêu cầu "sinh test cho API ...", "chạy test generator", /api-test-generator <METHOD path>.
---

# API Test Generator (end-to-end, không human-in-the-loop)

Thiết kế: `agent_skill/pseudocode.md`. Skill này hiện thực đúng 8 bước trong đó.

**Đầu vào** (args): endpoint, ví dụ `POST /api/login`; tùy chọn `--api API1_Login --prefix LG`.
**Đầu ra**: thư mục `skill_runs/<api>/`. Không ghi đè `collections/`, `report/`, `results/newman/` của bài làm tay.

Chạy hết các bước, không dừng hỏi người. Chỗ spec mơ hồ thì ghi **GIẢ ĐỊNH**, không hỏi.

## Luật cứng

- Kết quả chỉ lấy từ Newman chạy thật trên `localhost` / `127.0.0.1`. Không bao giờ tự viết hay sửa file report, response hay kết quả.
- Mọi request mang `X-Student-Id` qua pre-request cấp collection. `build_collection.py` tự gắn.
- Generator và auditor phải là hai lượt độc lập. Auditor chạy bằng subagent (Agent tool) có context riêng; nếu được thì dùng model khác generator. Không để generator tự chấm case của chính nó.
- Severity của bug chỉ là "đề xuất của AI".

## Các bước

Đặt `S=.claude/skills/api-test-generator`, `OUT=skill_runs/<api>`.

1. **Phân tích spec.** Đọc `eshop-sut/api_specification.md` (A) và `eshop-sut/README.md` (R). Ghi `OUT/01_spec.md` gồm:
   - endpoint, auth, body, response mẫu;
   - FR/SEC liên quan, kèm số dòng;
   - state machine nếu có;
   - danh sách GIẢ ĐỊNH (status hoặc schema lỗi mà spec không nêu; mặc định 400).
2. **Sinh theo từng kỹ thuật.** Mỗi kỹ thuật trong `references/techniques.md` là một lượt sinh riêng: G1, G2, G3, G4, G6. Nhóm nào không áp dụng cho endpoint thì bỏ, nhưng phải ghi lý do. Ghi case theo định dạng `references/cases_schema.md` vào `OUT/cases.json`, mỗi case `"label": "PENDING"`.
3. **Mẫu bug bỏ sót.** Với mỗi mẫu trong `references/bug_patterns.md` liên quan tới endpoint, thêm 1 case nhóm `EX`.
4. **Audit tự động.** Giao cho subagent auditor checklist `references/audit_checklist.md` cùng `OUT/cases.json` và `OUT/01_spec.md`.
   - Auditor trả nhãn VALID / INVALID / INCOMPLETE kèm lý do cho từng case.
   - Ghi nhãn vào `label` và `label_reason`.
   - Còn INCOMPLETE thì sinh lại đúng các case đó rồi audit lại, tối đa 2 vòng; quá 2 vòng thì case vẫn INCOMPLETE thành INVALID.
5. **Dựng collection và kiểm tra tĩnh.**
   ```bash
   python3 $S/scripts/build_collection.py OUT/cases.json OUT/collection.json
   python3 $S/scripts/static_check.py OUT/collection.json OUT/cases.json
   ```
   `static_check` fail thì sửa `cases.json` rồi dựng lại. Nếu sau 2 lần vẫn fail thì dừng và ghi lỗi vào `OUT/run_log.md`.
6. **Chạy thật.**
   ```bash
   $S/scripts/run.sh OUT
   ```
   Script reset SUT, chạy riêng từng case có `crashes_sut: true`, sau đó chạy phần còn lại. Report HTML và JSON do Newman sinh ra.
7. **Phân loại.**
   ```bash
   python3 $S/scripts/triage.py OUT
   ```
   Kết quả ghi vào `OUT/triage.md`:
   - PASS
   - SPEC_AMBIGUOUS: chỉ lệch ở assertion GIẢ ĐỊNH
   - BUG_CANDIDATE: kèm request và response thật lấy từ Newman JSON

   Bug nào chỉ case EX bắt được thì đề xuất thêm mẫu mới vào `references/bug_patterns.md`, ghi ở cuối `triage.md`.
8. **Ghi log.** Viết `OUT/run_log.md` gồm:
   - thời gian (lấy bằng `date`);
   - model của generator và auditor;
   - số case theo nhóm và nhãn;
   - số lần sinh lại;
   - tổng PASS / SPEC_AMBIGUOUS / BUG_CANDIDATE.

## Kết thúc

Trả về một bảng ngắn: số case, số chạy, PASS / SPEC_AMBIGUOUS / BUG_CANDIDATE, và đường dẫn `OUT/`.
