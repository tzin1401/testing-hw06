#!/usr/bin/env python3
"""Kiểm tra tĩnh collection trước khi chạy. Dùng: static_check.py OUT/collection.json OUT/cases.json
Exit 1 kèm danh sách lỗi nếu sai."""
import json, sys, re

col = json.load(open(sys.argv[1]))
cases = json.load(open(sys.argv[2]))["cases"]
errors = []

pre = " ".join(" ".join(e["script"]["exec"]) for e in col.get("event", []) if e["listen"] == "prerequest")
if "X-Student-Id" not in pre or "console.log" not in pre:
    errors.append("pre-request cấp collection thiếu X-Student-Id hoặc console.log")

folders = {}
for g in col["item"]:
    for f in g["item"]:
        m = re.match(r"\[([A-Z]{2}-(?:G\d|EX)-\d{2})\]", f["name"])
        if not m:
            errors.append(f"folder sai tên: {f['name']}")
            continue
        if m.group(1) in folders:
            errors.append(f"trùng folder {m.group(1)}")
        folders[m.group(1)] = f

for c in cases:
    cid, label = c["id"], c.get("label")
    if label not in ("VALID", "INVALID", "INCOMPLETE"):
        errors.append(f"{cid}: chưa audit (label={label})")
    if label == "INVALID" and cid in folders:
        errors.append(f"{cid}: INVALID nhưng có folder")
    if label != "INVALID" and cid not in folders:
        errors.append(f"{cid}: thiếu folder")
    if not c.get("source"):
        errors.append(f"{cid}: thiếu source cho expected")

raw = json.dumps(col)
if re.search(r"eyJ[A-Za-z0-9_-]{10,}\.", raw):
    errors.append("có JWT hardcode trong collection")
for cid, f in folders.items():
    for it in f["item"]:
        url = it["request"]["url"]["raw"]
        if not url.startswith("{{baseUrl}}"):
            errors.append(f"{cid}: URL không dùng {{{{baseUrl}}}}: {url}")
        tests = [e for e in it.get("event", []) if e["listen"] == "test"]
        if not tests or "pm.test(" not in " ".join(tests[0]["script"]["exec"]):
            errors.append(f"{cid}: request '{it['name']}' không có assertion")

if errors:
    print("STATIC_CHECK FAIL\n- " + "\n- ".join(errors))
    sys.exit(1)
print(f"STATIC_CHECK OK: {len(folders)} case, {sum(len(f['item']) for f in folders.values())} request")
