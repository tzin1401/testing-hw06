#!/usr/bin/env python3
"""Phân loại kết quả Newman thật theo case. Dùng: triage.py OUT
PASS | SPEC_AMBIGUOUS (chỉ fail assertion GIẢ ĐỊNH) | SETUP_ERROR | BUG_CANDIDATE | NOT_RUN.
Bằng chứng lấy nguyên từ Newman JSON (JWT được che)."""
import json, sys, re, pathlib, collections

OUT = pathlib.Path(sys.argv[1])
cases = json.loads((OUT / "cases.json").read_text())["cases"]
mask = lambda s: re.sub(r"eyJ[\w-]+\.[\w-]+\.[\w-]+", "eyJ***", s)

ex = collections.defaultdict(list)
for f in sorted((OUT / "newman").glob("*.json")):
    for e in json.loads(f.read_text())["run"]["executions"]:
        m = re.match(r"\[([A-Z]{2}-(?:G\d|EX)-\d{2})\]", e["item"]["name"])
        if m:
            ex[m.group(1)].append(e)


def body_of(e):
    r = e.get("response") or {}
    data = (r.get("stream") or {}).get("data")
    return bytes(data).decode("utf-8", "replace") if data else ""


rows, bugs = [], []
for c in cases:
    cid = c["id"]
    if c.get("label") == "INVALID" or cid not in ex:
        rows.append((cid, "NOT_RUN", c.get("label_reason", "")))
        continue
    fails = [(e, a) for e in ex[cid] for a in (e.get("assertions") or []) if a.get("error")]
    fails += [(e, {"assertion": "request error: " + (e["requestError"].get("message") or e["requestError"].get("code") or "kết nối lỗi")}) for e in ex[cid] if e.get("requestError")]
    names = [a["assertion"] for _, a in fails]
    if not fails:
        verdict = "PASS"
    elif any("setup:" in n for n in names):
        verdict = "SETUP_ERROR"
    elif all("(GIẢ ĐỊNH)" in n for n in names):
        verdict = "SPEC_AMBIGUOUS"
    else:
        verdict = "BUG_CANDIDATE"
        e = fails[0][0]
        req = e["request"]
        url = req["url"] if isinstance(req["url"], str) else "/" + "/".join(req["url"].get("path", []))
        bugs.append({"id": cid, "group": c["group"], "purpose": c["purpose"], "failed": names,
                     "request": f"{req['method']} {url}",
                     "request_body": mask((req.get("body") or {}).get("raw", "")),
                     "status": (e.get("response") or {}).get("code"),
                     "response": mask(body_of(e))[:600]})
    rows.append((cid, verdict, "; ".join(names)[:200]))

count = collections.Counter(v for _, v, _ in rows)
md = [f"# Triage – {OUT.name}", "", "| Kết quả | Số case |", "|---|---:|"]
md += [f"| {k} | {count[k]} |" for k in ("PASS", "SPEC_AMBIGUOUS", "BUG_CANDIDATE", "SETUP_ERROR", "NOT_RUN")]
md += ["", "## Từng case", "", "| ID | Kết quả | Assertion fail |", "|---|---|---|"]
md += [f"| {i} | {v} | {n.replace('|', '/')} |" for i, v, n in rows]
md += ["", "## Ứng viên bug (bằng chứng từ Newman JSON)", ""]
for b in bugs:
    md += [f"### {b['id']} – {b['purpose']}", f"- Assertion fail: {'; '.join(b['failed'])}",
           f"- Request: `{b['request']}` body `{b['request_body']}`",
           f"- Response thật: HTTP {b['status']} `{b['response']}`",
           "- Severity: _(đề xuất của AI, agent điền)_", ""]
only_ex = [b["id"] for b in bugs if b["group"] == "EX"]
md += ["## Đề xuất mẫu mới cho bug_patterns.md", "",
       ("Bug chỉ case EX bắt được: " + ", ".join(only_ex)) if only_ex else "Không có."]
(OUT / "triage.md").write_text("\n".join(md) + "\n")
(OUT / "triage.json").write_text(json.dumps({"count": count, "rows": rows, "bugs": bugs}, ensure_ascii=False, indent=1))
print(dict(count), "->", OUT / "triage.md")
