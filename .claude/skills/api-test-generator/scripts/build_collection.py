#!/usr/bin/env python3
"""cases.json -> Postman collection v2.1 + environment.
Dùng: build_collection.py OUT/cases.json OUT/collection.json [--base-url URL] [--student-id ID]
Case label INVALID bị bỏ qua. Mỗi case là một folder "[ID] purpose" trong folder nhóm (G1..G6, EX)."""
import json, sys, argparse, pathlib

# path "a.b", "0.x" hoặc lọc mảng "[id={{uid}}].x"
GET = ("const g=(o,p)=>pm.variables.replaceIn(p).split('.').reduce((a,k)=>{if(a==null)return undefined;"
       "const m=k.match(/^\\[(\\w+)=(.*)\\]$/);return m?(Array.isArray(a)?a.find(x=>x&&String(x[m[1]])===m[2]):undefined):a[k];},o);")
PRE = [
    "pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.environment.get('studentId') });",
    "console.log('X-Student-Id: ' + pm.environment.get('studentId') + ' -> ' + pm.request.method + ' ' + pm.variables.replaceIn(pm.request.url.toString()));",
]


def js(s):
    return json.dumps(s, ensure_ascii=False)


def status_test(cid, label, status, assumed):
    codes = status if isinstance(status, list) else [status]
    name = f"[{cid}] {label}status {'/'.join(map(str, codes))}" + (" (GIẢ ĐỊNH)" if assumed else "")
    return f"pm.test({js(name)}, () => pm.expect(pm.response.code).to.be.oneOf({js(codes)}));"


def check_tests(cid, checks, prefix="core"):
    out = []
    for c in checks or []:
        if "max_ms" in c:
            out.append(f"pm.test({js(f'[{cid}] {prefix}: phản hồi < ' + str(c['max_ms']) + ' ms')}, () => "
                       f"pm.expect(pm.response.responseTime).to.be.below({int(c['max_ms'])}));")
            continue
        if "header" in c:
            out.append(f"pm.test({js(f'[{cid}] {prefix}: header ' + c['header'] + ' chứa ' + c['includes'])}, () => "
                       f"pm.expect(pm.response.headers.get({js(c['header'])}) || '').to.include({js(c['includes'])}));")
            continue
        if "no_text" in c:
            out.append(f"pm.test({js(f'[{cid}] {prefix}: body không chứa ' + c['no_text'])}, () => "
                       f"pm.expect(pm.response.text()).to.not.include({js(c['no_text'])}));")
            continue
        p = c["path"]
        body = f"{GET} let j; try {{ j = pm.response.json(); }} catch (e) {{ j = undefined; }} const v = g(j, {js(p)});"
        if c.get("absent"):
            name, cond = f"[{cid}] {prefix}: không có {p}", "pm.expect(v).to.be.undefined;"
        elif c.get("exists"):
            name, cond = f"[{cid}] {prefix}: có {p}", "pm.expect(v).to.not.be.undefined;"
        elif "equals" in c:
            # "{{var}}" nguyên chuỗi → lấy giá trị biến giữ kiểu (vd id là number)
            name, cond = f"[{cid}] {prefix}: {p} = {c['equals']}", (
                f"const E = {js(c['equals'])}; const m = typeof E === 'string' && E.match(/^\\{{\\{{(\\w+)\\}}\\}}$/); "
                f"pm.expect(v).to.eql(m ? pm.variables.get(m[1]) : typeof E === 'string' ? pm.variables.replaceIn(E) : E);")
        else:
            t = c["type"]
            cond = "pm.expect(Array.isArray(v)).to.be.true;" if t == "array" else f"pm.expect(v).to.be.a({js(t)});"
            name = f"[{cid}] {prefix}: {p} là {t}"
        out.append(f"pm.test({js(name)}, () => {{ {body} {cond} }});")
    return out


def captures(cap):
    if not cap:
        return []
    lines = [GET, "let j; try { j = pm.response.json(); } catch (e) { j = {}; }"]
    for var, path in cap.items():
        lines.append(f"pm.collectionVariables.set({js(var)}, g(j, {js(path)}));")
    return lines


def request(step, cid, name, tests, pre=None):
    headers = [{"key": k, "value": v} for k, v in (step.get("headers") or {}).items()]
    req = {"method": step["method"], "header": headers,
           "url": {"raw": "{{baseUrl}}" + step["path"], "host": ["{{baseUrl}}"],
                   "path": step["path"].lstrip("/").split("?")[0].split("/")}}
    if "body" in step or "raw" in step:
        raw = step["raw"] if "raw" in step else json.dumps(step["body"], ensure_ascii=False)
        headers.append({"key": "Content-Type", "value": step.get("content_type", "application/json")})
        req["body"] = {"mode": "raw", "raw": raw}
    ev = [{"listen": "test", "script": {"type": "text/javascript", "exec": tests}}]
    if pre:
        ev.append({"listen": "prerequest", "script": {"type": "text/javascript", "exec": pre}})
    return {"name": f"[{cid}] {name}", "request": req, "event": ev}


def wait(step):
    # Newman giữ request tới khi timer trong pre-request chạy xong
    return [f"setTimeout(() => {{}}, {int(step['wait_ms'])});"] if step.get("wait_ms") else []


def case_folder(c):
    cid = c["id"]
    pre = [f"pm.collectionVariables.set({js(k)}, pm.variables.replaceIn({js(v)}));" for k, v in (c.get("vars") or {}).items()]
    items = []
    for s in c.get("setup", []):
        t = [status_test(cid, "setup: " + s["name"] + " ", s.get("expect_status", 200), False)] + captures(s.get("capture"))
        items.append(request(s, cid, "setup: " + s["name"], t, (pre if not items else []) + wait(s) or None))
    r, e = c["request"], c["expect"]
    t = [status_test(cid, "", e["status"], e.get("assumed", False))] + check_tests(cid, e.get("checks")) + captures(r.get("capture"))
    items.append(request(r, cid, f"{r['method']} {r['path']}", t, (pre if not items else []) + wait(r) or None))
    for a in c.get("after", []):
        t = [status_test(cid, "oracle: " + a["name"] + " ", a.get("expect_status", 200), False)] + check_tests(cid, a.get("checks"), "oracle") + captures(a.get("capture"))
        items.append(request(a, cid, "oracle: " + a["name"], t, wait(a) or None))
    return {"name": f"[{cid}] {c['purpose']}", "item": items}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cases"); ap.add_argument("out")
    ap.add_argument("--base-url", default="http://localhost:3000")
    ap.add_argument("--student-id", default="23120190")
    a = ap.parse_args()
    data = json.loads(pathlib.Path(a.cases).read_text())
    groups = {}
    for c in data["cases"]:
        if c.get("label") == "INVALID":
            continue
        groups.setdefault(c["group"], []).append(case_folder(c))
    order = ["G1", "G2", "G3", "G4", "G6", "EX"]
    col = {
        "info": {"name": f"{a.student_id}_{data['api']} (generated)",
                 "description": f"Sinh bởi skill api-test-generator cho {data['endpoint']}. "
                                f"Bỏ INVALID: {', '.join(c['id'] for c in data['cases'] if c.get('label') == 'INVALID') or 'không có'}",
                 "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "event": [{"listen": "prerequest", "script": {"type": "text/javascript", "exec": PRE}}],
        "item": [{"name": g, "item": groups[g]} for g in sorted(groups, key=lambda x: order.index(x) if x in order else 99)],
    }
    out = pathlib.Path(a.out)
    out.write_text(json.dumps(col, ensure_ascii=False, indent=2))
    env = {"name": "generated local", "values": [
        {"key": "baseUrl", "value": a.base_url, "enabled": True},
        {"key": "studentId", "value": a.student_id, "enabled": True}]}
    (out.parent / "env.json").write_text(json.dumps(env, ensure_ascii=False, indent=2))
    print(f"{out}: {sum(len(v) for v in groups.values())} case folder")


if __name__ == "__main__":
    main()
