# Agent Skill – AI-driven API test generator

| Thành phần | Vị trí |
|---|---|
| Sơ đồ thiết kế (sinh viên tự vẽ) | `agent_skill/diagram.png` |
| Pseudocode | [`pseudocode.md`](pseudocode.md) |
| Skill (Claude Code, dùng lại được) | [`.claude/skills/api-test-generator/`](../.claude/skills/api-test-generator/SKILL.md) |
| Kết quả mỗi lần chạy | `skill_runs/<API>/` |

## Cấu trúc skill

```
.claude/skills/api-test-generator/
├── SKILL.md                    # 8 bước, chạy tự động, không human-in-the-loop
├── references/
│   ├── techniques.md           # template G1 / G2 / G3 / G4 / G6
│   ├── bug_patterns.md         # mẫu bug AI hay bỏ sót → nhóm EX (tự mở rộng)
│   ├── audit_checklist.md      # checklist cho subagent auditor độc lập
│   └── cases_schema.md         # định dạng cases.json
└── scripts/
    ├── build_collection.py     # cases.json → Postman collection (+ X-Student-Id, assertion, oracle)
    ├── static_check.py         # kiểm tra tĩnh trước khi chạy
    ├── run.sh                  # reset SUT, chạy riêng case làm sập server, Newman thật trên localhost
    └── triage.py               # PASS / SPEC_AMBIGUOUS / BUG_CANDIDATE / SETUP_ERROR, bằng chứng từ Newman JSON
```

## Chạy

Trong Claude Code tại thư mục repo:

```
/api-test-generator POST /api/login --api API1_Login --prefix LG
```

Các script tất định đã được tự kiểm thử với Newman thật: case pass, case lệch GIẢ ĐỊNH, case INVALID bị loại, case lộ password (BUG-03) và case làm sập server (BUG-14, chạy riêng). Phân loại cho ra đúng kết quả mong đợi.
