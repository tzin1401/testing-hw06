# AI Audit Report – HW06 API Testing

Sinh viên: 23120190 · Repo: https://github.com/tzin1401/testing-hw06

## Tuyên bố

**I use AI tools for the following tasks:** phân tích spec, sinh test case theo từng kỹ thuật (domain partition, state transition, security, schema, heuristic), audit test case bằng một model độc lập, dựng Postman collection và chạy Newman, phân loại kết quả và soạn bug report, dựng Postman mock server, monitor và pipeline CI/CD, tạo file Excel test case, viết Agent Skill sinh test tự động, soạn nháp tài liệu.

Những thứ sau **không** do AI tạo hay sửa:
- Newman report: chỉ sinh từ lần chạy `newman` thật trên `localhost`.
- Ảnh chụp console `X-Student-Id`, ảnh GitHub Issues, ảnh Postman, ảnh CI: sinh viên tự chụp.
- Sơ đồ Agent Skill: sinh viên tự vẽ.
- Video demo: sinh viên tự quay (https://youtu.be/FAk1krlB-ng).

## Công cụ AI đã dùng

| Công cụ | Model | Vai trò |
|---|---|---|
| omp multi-agent – Manager | openai-codex/gpt-6.1-sol | Điều phối, giao bước, kiểm tra output, ghi log, commit |
| omp – task workers | openai-codex/gpt-6.1-terra | Sinh test case G1–G4, G6; dựng collection; chạy Newman; viết kết quả |
| omp – sonic / scout | openai-codex/gpt-6-luna | Gọi thử SUT, kiểm tra CLI, phân loại bug |
| omp – auditor / reviewer | anthropic/claude-sonnet-5-5 | Audit test case (bước G5, G5R2), review mapping và kết quả |
| Claude Code | claude-opus-5-5 | Soạn bộ prompt giao cho omp. Từ 2026-11-25: ảnh bug và GitHub Issues, Postman features, CI/CD, Excel, Agent Skill. Các phiên này không ghi từng entry, xem mục bên dưới |
| Claude Code – subagent auditor | Claude Sonnet | Auditor độc lập trong lần chạy Agent Skill trên API 1 |

**Cách ghi log:** theo quy tắc trong [`agent.md`](../agent.md) mục 1.
- Mỗi prompt có cụm "ghi vào log" thì agent tự append một entry gồm tên công cụ, ngày giờ (lấy từ lệnh `date`), prompt nguyên văn và tóm tắt output.
- Mục **Human review** do sinh viên tự điền.

## Danh sách tương tác (38 entry)

Prompt nguyên văn, AI output và Human review của từng entry nằm trong [AI_LOG.md](AI_LOG.md). Bản PDF kèm toàn văn log ở phụ lục.

Trong log, bước **G5 / G5R2** là bước audit: model Claude Sonnet độc lập gắn nhãn VALID / INVALID / INCOMPLETE, rồi audit lại sau khi sinh lại.

| # | Thời gian (giờ VN) | Bước | Công cụ AI |
|---:|---|---|---|
| 1 | 2026-11-24 01:49 | API 1, API 2, API 3 – Bước 0: Phân tích spec | omp Manager (openai-codex/gpt-6.1-sol), phối hợp scout phân tích spec và sonic thực thi happy path |
| 2 | 2026-11-24 14:41 | API 1 – Generate – LG-G1: Domain partition + boundary | task LoginG1 – OpenAI Codex (openai-codex/gpt-6.1-terra); Manager kiểm tra và ghi log (openai-codex/gpt-6.1-sol) |
| 3 | 2026-11-24 14:51 | LG-G2 – Generate | LGG2 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 4 | 2026-11-24 14:51 | CN-G1 – Generate | CNG1 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 5 | 2026-11-24 14:52 | PR-G1 – Generate | PRG1 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 6 | 2026-11-24 14:53 | LG-G3 – Generate | LGG3 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 7 | 2026-11-24 14:54 | PR-G2 – Generate | PRG2 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 8 | 2026-11-24 14:54 | LG-G4 – Generate | LGG4 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 9 | 2026-11-24 14:54 | CN-G2 – Generate | CNG2 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 10 | 2026-11-24 14:56 | PR-G3 – Generate | PRG3 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 11 | 2026-11-24 14:56 | CN-G3 – Generate | CNG3 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 12 | 2026-11-24 14:57 | CN-G4 – Generate | CNG4 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 13 | 2026-11-24 14:57 | PR-G4 – Generate | PRG4 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 14 | 2026-11-24 14:59 | LG-G5 – Generate | LGG5 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 15 | 2026-11-24 15:01 | LG-G6 – Generate | LGG6 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 16 | 2026-11-24 15:03 | PR-G5 – Generate | PRG5 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 17 | 2026-11-24 15:04 | CN-G5 – Generate | CNG5 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 18 | 2026-11-24 15:05 | LG-G5R2 – Generate | LGG5R2 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 19 | 2026-11-24 15:07 | PR-G6 – Generate | PRG6 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 20 | 2026-11-24 15:07 | CN-G6 – Generate | CNG6 (openai-codex/gpt-6.1-terra); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 21 | 2026-11-24 15:13 | PR-G5R2 – Generate | PRG5R2 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 22 | 2026-11-24 15:15 | CN-G5R2 – Generate | CNG5R2 (anthropic/claude-sonnet-5-5); Manager ghi log/commit (openai-codex/gpt-6.1-sol) |
| 23 | 2026-11-24 22:08 | Execute – X0: Hạ tầng dùng chung | task ExecuteX0 (openai-codex/gpt-6.1-terra); omp Manager (openai-codex/gpt-6.1-sol); sonic kiểm tra CLI (worker không cung cấp model id) |
| 24 | 2026-11-24 22:32 | CN-X1 – Execute | CN-X1 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 25 | 2026-11-24 22:32 | LG-X1 – Execute | LG-X1 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 26 | 2026-11-24 22:37 | PR-X1 – Execute | PR-X1 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 27 | 2026-11-24 22:42 | LG-X2 – Execute | LG-X2 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 28 | 2026-11-24 22:47 | PR-X2 – Execute | PR-X2 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 29 | 2026-11-24 22:50 | API 2 – Execute – CN-X2 | task CNX2 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 30 | 2026-11-24 22:57 | API 1 – Execute – LG-X3 | task LGX3 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 31 | 2026-11-24 23:03 | API 3 – Execute – PR-X3 | task PRX3 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 32 | 2026-11-24 23:05 | API 2 – Execute – CN-X3 | task CNX3 (openai-codex/gpt-6.1-terra); Manager ghi log (openai-codex/gpt-6.1-sol) |
| 33 | 2026-11-25 03:07 | API 1 – Execute – LG-X4 | Manager (openai-codex/gpt-6.1-sol) |
| 34 | 2026-11-25 03:07 | Execute – X-DATA | Manager (openai-codex/gpt-6.1-sol); sonic ExecuteProof (openai-codex/gpt-6-luna) |
| 35 | 2026-11-25 15:23 | API 2 – Execute – CN-X4 | Manager (openai-codex/gpt-6.1-sol) |
| 36 | 2026-11-25 15:33 | API 3 – Execute – PR-X4 | Manager (openai-codex/gpt-6.1-sol); task ProductIsolation (openai-codex/gpt-6.1-terra); sonic ProductRuntime/ProductProof (openai-codex/gpt-6-luna); reviewer ProductMappingReview (anthropic/claude-sonnet-5-5) |
| 37 | 2026-11-25 16:05 | API 1, API 2, API 3 – Execute – X5 | Manager (openai-codex/gpt-6.1-sol); task LoginResults/CancelResults/ProductResults (openai-codex/gpt-6.1-terra); sonic OfficialManifest (openai-codex/gpt-6-luna); reviewer ResultsReview (anthropic/claude-sonnet-5-5) |
| 38 | 2026-11-25 16:17 | API 1, API 2, API 3 – Bug report – B0 | Manager (openai-codex/gpt-6.1-sol); scout BugTriage (openai-codex/gpt-6-luna); task CorrectTriage (openai-codex/gpt-6.1-terra) |

## Các phiên Claude Code không ghi từng entry

Những bước dưới đây làm trực tiếp với Claude Code (claude-opus-5-5) sau entry #38. Prompt không có cụm "ghi vào log" nên không có entry riêng. Bằng chứng nằm trong commit và file kết quả tương ứng.

| Thời gian (giờ VN) | Bước | Bằng chứng |
|---|---|---|
| 2026-11-25 | Ảnh bug BUG-01…16, nhúng ảnh vào GitHub Issues #1–16 | [`bug_report.md`](bug_report.md), `evidence/issues/` (ảnh sinh viên tự chụp) |
| 2026-11-25 | Postman features: mock server, monitor | [`postman_features.md`](postman_features.md), `evidence/postman/` |
| 2026-11-26 | CI/CD GitHub Actions chạy Newman regression | [`cicd_report.md`](cicd_report.md), `.github/workflows/api-tests.yml`, `evidence/cicd/` |
| 2026-11-26 | File Excel test case kèm test summary | [`23120190_HW06_TestCases.xlsx`](23120190_HW06_TestCases.xlsx), `scripts/gen_testcases_xlsx.py` |
| 2026-11-26 | Agent Skill: pseudocode, skill, kịch bản video | [`agent_skill/`](../agent_skill/README.md), `.claude/skills/api-test-generator/` |
| 2026-11-26 17:33 | Chạy Agent Skill trên API 1 | [`skill_runs/API1_Login/run_log.md`](../skill_runs/API1_Login/run_log.md) |

## Kết quả audit test case do AI sinh

Số liệu lấy từ sheet TestCases của file Excel.
- Nhãn do auditor độc lập đề xuất ở bước G5 / G5R2. Sinh viên duyệt lại trong Human review.
- Case **INVALID** không được đưa vào collection.
- Case **EX** do sinh viên tự thêm (Extend) để bắt các bug AI bỏ sót.

| API | VALID | INCOMPLETE | INVALID | EX / Extend | Tổng |
|---|---:|---:|---:|---:|---:|
| API 1 – POST /api/login | 61 | 2 | 3 | 5 | 71 |
| API 2 – PUT /api/orders/:id/cancel | 40 | 10 | 9 | 5 | 64 |
| API 3 – Product CRUD | 117 | 2 | 8 | 6 | 133 |
| **Tổng** | **218** | **14** | **20** | **16** | **268** |

**Lần chạy Agent Skill trên API 1** (bước audit thay người duyệt):

| Vòng | Case audit | VALID | INCOMPLETE | INVALID |
|---|---:|---:|---:|---:|
| 1 | 50 | 40 | 8 | 2 |
| 2 (sinh lại) | 8 | 6 | 2 | 0 |
| 3 (sinh lại) | 2 | 1 | 1 → INVALID | 0 |

Kết quả cuối: 47 VALID, 3 INVALID. Newman cho PASS 33, SPEC_AMBIGUOUS 1, BUG_CANDIDATE 12, SETUP_ERROR 1.

## AI Critique

Xem [AI_CRITIQUE.md](AI_CRITIQUE.md) (sinh viên tự viết, 200–300 chữ).
