#!/usr/bin/env python3
"""Sinh report/23120190_HW06_TestCases.xlsx từ:
- report/testcases/*_generated.md  (nội dung test case, gồm cả EX do người thêm)
- report/execute/*_mapping.md      (nhãn audit + folder trong collection)
- results/newman/*_20261125.json   (kết quả chạy Newman thật)
- scripts/gen_bug_reports.py       (bug ↔ case)
Chạy: python3 scripts/gen_testcases_xlsx.py   (cần file Newman JSON local, file API3 bị gitignore)
"""
import json, re, pathlib, collections
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/tzin1401/testing-hw06"
APIS = [("API1_Login", "API1 – POST /api/login", "API1_login"),
        ("API2_CancelOrder", "API2 – PUT /api/orders/:id/cancel", "API2_cancel"),
        ("API3_ProductCRUD", "API3 – Product CRUD", "API3_product")]
CID = re.compile(r"\[?([A-Z]{2}-(?:G\d|EX)-\d{2})\]?")


def md_rows(path, ncol):
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == ncol and re.fullmatch(r"[A-Z]{2}-(G\d|EX)-\d{2}", cells[0]):
            yield cells


def plain(s):
    return s.replace("`", "").replace("<br>", "\n")


def load_bugs():
    src = (ROOT / "scripts/gen_bug_reports.py").read_text().split('if __name__')[0]
    ns = {"__file__": str(ROOT / "scripts/gen_bug_reports.py")}
    exec(src, ns)
    return ns["BUGS"]


def case_matches(spec, cid):
    for part in [p.strip() for p in spec.split(",")]:
        if part.endswith("*") and cid.startswith(part[:-1]):
            return True
        if ".." in part:
            a, b = part.split("..")
            if a[:-2] == b[:-2] == cid[:-2] and int(a[-2:]) <= int(cid[-2:]) <= int(b[-2:]):
                return True
        if part == cid:
            return True
    return False


def newman_results(api):
    ran, total, failed = set(), collections.Counter(), collections.Counter()
    for f in sorted((ROOT / "results/newman").glob(f"23120190_{api}_*2026*.json")):
        for e in json.loads(f.read_text())["run"]["executions"]:
            m = CID.match(e["item"]["name"])
            if not m:
                continue
            k = m.group(1)
            ran.add(k)
            asserts = e.get("assertions") or []
            total[k] += len(asserts)
            failed[k] += sum(1 for a in asserts if a.get("error")) + (1 if e.get("requestError") else 0)
    return ran, total, failed


def main():
    bugs = load_bugs()
    rows = []
    for api, api_label, stem in APIS:
        gen = {c[0]: c for c in md_rows(ROOT / f"report/testcases/{stem}_generated.md", 9)}
        mapping = ROOT / f"report/execute/{stem}_mapping.md"
        audit = {c[0]: c for c in md_rows(mapping, 6)}
        # API3 liệt kê INVALID dạng "- PR-G1-04 – INVALID theo audit: ..." thay vì trong bảng
        for m in re.finditer(r"^- ([A-Z]{2}-G\d-\d{2}) – INVALID", mapping.read_text(), re.M):
            audit.setdefault(m.group(1), [m.group(1), "INVALID"])
        ran, total, failed = newman_results(api)
        for cid in sorted(set(gen) | set(audit), key=lambda x: (x.split("-")[1] == "EX", x)):
            g = gen.get(cid, [cid] + [""] * 8)
            label = audit.get(cid, [cid, ""])[1]
            if cid in ran:
                result = "PASS" if failed[cid] == 0 else "FAIL"
            else:
                result = "NOT RUN"
            bug_ids = [f"BUG-{b[0]}" for b in bugs if case_matches(b[4], cid)] if result == "FAIL" else []
            rows.append({
                "ID": cid, "API": api_label, "Nhóm": cid.split("-")[1],
                "Kỹ thuật": g[1], "Requirement": g[2], "Mục đích": plain(g[3]),
                "Precondition / setup": plain(g[4]), "Request": plain(g[5]),
                "Expected status": plain(g[6]), "Expected body / kiểm tra": plain(g[7]),
                "Nguồn expected": plain(g[8]),
                "Nguồn case": "Human – Extend" if "-EX-" in cid else "AI – Generate",
                "Nhãn audit": label,
                "Assertion": total[cid] if cid in ran else None,
                "Assertion fail": failed[cid] if cid in ran else None,
                "Kết quả": result,
                "Bug": ", ".join(bug_ids),
            })

    wb = Workbook()
    font = Font(name="Arial", size=10)
    bold = Font(name="Arial", size=10, bold=True)
    head_fill = PatternFill("solid", start_color="1F3864")
    head_font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    thin = Side(style="thin", color="BFBFBF")

    # --- TestCases ---
    ws = wb.active
    ws.title = "TestCases"
    cols = list(rows[0].keys())
    widths = {"ID": 12, "API": 24, "Nhóm": 7, "Kỹ thuật": 12, "Requirement": 14, "Mục đích": 32,
              "Precondition / setup": 36, "Request": 48, "Expected status": 14,
              "Expected body / kiểm tra": 40, "Nguồn expected": 30, "Nguồn case": 15,
              "Nhãn audit": 12, "Assertion": 10, "Assertion fail": 10, "Kết quả": 10, "Bug": 16}
    ws.append(cols)
    for r in rows:
        ws.append([r[c] for c in cols])
    for i, c in enumerate(cols, 1):
        ws.column_dimensions[get_column_letter(i)].width = widths[c]
    for row in ws.iter_rows():
        for cell in row:
            cell.font = font
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(top=thin, bottom=thin, left=thin, right=thin)
    for cell in ws[1]:
        cell.font, cell.fill = head_font, head_fill
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    res_col = cols.index("Kết quả") + 1
    fills = {"PASS": "E2EFDA", "FAIL": "FCE4D6", "NOT RUN": "EDEDED"}
    for r in range(2, ws.max_row + 1):
        c = ws.cell(r, res_col)
        c.fill = PatternFill("solid", start_color=fills[c.value])
        c.font = bold
    ws.freeze_panes = "B2"
    last = f"{get_column_letter(len(cols))}{ws.max_row}"
    t = Table(displayName="TestCases", ref=f"A1:{last}")
    t.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=False)
    ws.add_table(t)
    n = ws.max_row
    L = {c: get_column_letter(cols.index(c) + 1) for c in cols}

    # --- Bugs ---
    wb_b = wb.create_sheet("Bugs")
    bcols = ["Bug", "Module", "Tiêu đề", "Severity (đề xuất của AI)", "Priority (đề xuất của AI)",
             "Phát hiện bởi", "Test case", "GitHub issue"]
    wb_b.append(bcols)
    for b in bugs:
        bid, module, title, _api, cases, found, sev, pri = b[:8]
        wb_b.append([f"BUG-{bid}", module, title, sev, pri, found, cases, f"{REPO}/issues/{int(bid)}"])
    for i, w in enumerate([9, 12, 60, 14, 14, 26, 40, 46], 1):
        wb_b.column_dimensions[get_column_letter(i)].width = w
    for row in wb_b.iter_rows():
        for cell in row:
            cell.font = font
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    for r in range(2, wb_b.max_row + 1):
        c = wb_b.cell(r, 8)
        c.hyperlink = c.value
        c.font = Font(name="Arial", size=10, color="0563C1", underline="single")
    for cell in wb_b[1]:
        cell.font, cell.fill = head_font, head_fill
    wb_b.freeze_panes = "A2"
    nb = wb_b.max_row

    # --- Summary (công thức đếm từ TestCases / Bugs) ---
    sm = wb.create_sheet("Summary", 0)
    sm["A1"] = "HW06 – API Testing – Test summary (MSSV 23120190)"
    sm["A1"].font = Font(name="Arial", size=14, bold=True)
    sm["A2"] = ("Số liệu tính bằng công thức từ sheet TestCases (kết quả Newman chạy localhost ngày 2026-11-25) "
                "và sheet Bugs. NOT RUN = case bị gắn nhãn INVALID khi audit nên không đưa vào collection.")
    sm["A2"].font = Font(name="Arial", size=9, italic=True)
    hdr = ["API", "AI generate", "Human extend", "Tổng case", "INVALID (không chạy)", "Đã chạy",
           "PASS", "FAIL", "Tỉ lệ pass", "Assertion", "Assertion fail"]
    sm.append([])
    sm.append(hdr)
    rng = lambda c: f"TestCases!${L[c]}$2:${L[c]}${n}"
    for i, (_a, label, _s) in enumerate(APIS):
        r = 5 + i
        sm.append([label,
                   f'=COUNTIFS({rng("API")},$A{r},{rng("Nguồn case")},"AI – Generate")',
                   f'=COUNTIFS({rng("API")},$A{r},{rng("Nguồn case")},"Human – Extend")',
                   f"=B{r}+C{r}",
                   f'=COUNTIFS({rng("API")},$A{r},{rng("Kết quả")},"NOT RUN")',
                   f"=G{r}+H{r}",
                   f'=COUNTIFS({rng("API")},$A{r},{rng("Kết quả")},"PASS")',
                   f'=COUNTIFS({rng("API")},$A{r},{rng("Kết quả")},"FAIL")',
                   f"=IF(F{r}=0,0,G{r}/F{r})",
                   f'=SUMIFS({rng("Assertion")},{rng("API")},$A{r})',
                   f'=SUMIFS({rng("Assertion fail")},{rng("API")},$A{r})'])
    sm.append(["Tổng"] + [f"=SUM({get_column_letter(c)}5:{get_column_letter(c)}7)" for c in range(2, 9)]
              + ["=IF(F8=0,0,G8/F8)", "=SUM(J5:J7)", "=SUM(K5:K7)"])
    sm["A10"] = "Số API"
    sm["B10"] = len(APIS)
    sm["A11"] = "Số bug (GitHub Issues)"
    sm["B11"] = f"=COUNTA(Bugs!A2:A{nb})"
    sm["A12"] = "Bug do người phát hiện (AI bỏ sót)"
    sm["B12"] = f'=COUNTIF(Bugs!F2:F{nb},"*AI bỏ sót*")'
    for row in sm.iter_rows(min_row=4, max_row=12):
        for cell in row:
            cell.font = font
            cell.border = Border(top=thin, bottom=thin, left=thin, right=thin) if cell.row <= 8 else Border()
    for cell in sm[4]:
        cell.font, cell.fill = head_font, head_fill
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    for cell in sm[8]:
        cell.font = bold
    for r in range(5, 9):
        sm[f"I{r}"].number_format = "0.0%"
    sm.column_dimensions["A"].width = 36
    for c in "BCDEFGHIJK":
        sm.column_dimensions[c].width = 13
    sm.row_dimensions[4].height = 30
    for a in ("A10", "A11", "A12"):
        sm[a].font = bold

    out = ROOT / "report/23120190_HW06_TestCases.xlsx"
    wb.save(out)
    print(out, len(rows), "cases")


if __name__ == "__main__":
    main()
